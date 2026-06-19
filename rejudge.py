#!/usr/bin/env python3
"""
Re-judge evaluation output using a different judge model.
Extracts prompts, outputs, and assertions from eval output, then re-runs judging.

Usage:
    python3 rejudge.py <input_file> --judge-model "Qwen/Qwen3.5-122B-A10B-FP8" --output-folder rejudge-results
"""

import sys
import os
import re
import json
import httpx
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def strip_ansi(text):
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_pattern.sub('', text)


def parse_eval_output(content):
    """Parse eval output and extract eval blocks with prompts, outputs, and assertions."""
    evals = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        clean_line = strip_ansi(lines[i])

        # Match eval header
        eval_match = re.match(r'\s*#(\d+) eval-(\d+)\s+\[(with_skill|without_skill)\]', clean_line)
        if eval_match:
            eval_num = eval_match.group(2)
            mode = eval_match.group(3)

            # Extract system/user from lines
            system_content = ""
            user_content = ""
            output_content = ""
            assertions = []

            i += 1
            while i < len(lines):
                clean_next = strip_ansi(lines[i])

                # Check for time/tokens line (end of eval block)
                if re.search(r'\d+\.\d+s\s*·\s*\d+\s*tokens', clean_next):
                    break

                # Extract system content
                sys_match = re.match(r'\s*system:\s*(.+)', clean_next)
                if sys_match:
                    system_content = sys_match.group(1).strip()

                # Extract user content
                user_match = re.match(r'\s*user:\s*(.+)', clean_next)
                if user_match:
                    user_content = user_match.group(1).strip()

                # Extract output content
                output_match = re.match(r'\s*output:\s*(.+)', clean_next)
                if output_match:
                    output_content = output_match.group(1).strip()

                # Extract assertions
                assert_match = re.match(r'\s*#(\d+)\s+(FAIL|PASS)\s+—\s+(.+)', clean_next)
                if assert_match:
                    assert_num = int(assert_match.group(1))
                    status = assert_match.group(2)
                    assert_name = assert_match.group(3).strip()
                    assertions.append({
                        'num': assert_num,
                        'name': assert_name,
                        'status': status
                    })

                    # Get evidence
                    i += 1
                    while i < len(lines):
                        clean_evidence = strip_ansi(lines[i])
                        evidence_match = re.search(r'evidence:\s*(.+)', clean_evidence, re.IGNORECASE)
                        if evidence_match:
                            assertions[-1]['evidence'] = evidence_match.group(1).strip()
                            break
                        elif clean_evidence.strip() == '' or re.match(r'\s*#(\d+)', clean_evidence):
                            break
                        i += 1
                    continue

                i += 1

            if user_content and output_content:
                evals.append({
                    'eval_num': eval_num,
                    'mode': mode,
                    'system': system_content,
                    'user': user_content,
                    'output': output_content,
                    'assertions': assertions
                })

            continue

        i += 1

    return evals


def create_judge_prompt(assertion, user_prompt, model_output, skill_system=None):
    """Create a prompt for the judge model to evaluate an assertion."""
    if skill_system:
        # Extract skill name from system prompt
        skill_match = re.search(r'name="([^"]+)"', skill_system)
        skill_name = skill_match.group(1) if skill_match else "skill"
    else:
        skill_name = "skill"

    prompt = f"""You are an expert judge evaluating whether a model's response satisfies a specific assertion.

SKILL: {skill_name}
USER PROMPT: {user_prompt}
MODEL RESPONSE: {model_output}

ASSERTION TO EVALUATE: {assertion}

Output ONLY valid JSON with this shape:
{{"passed": true/false, "evidence": "specific text from the model response that supports your judgment", "reasoning": "brief explanation"}}

Rules:
- Be strict but fair
- Evidence must be actual text from the model response or "N/A" if not applicable
- If the model clearly addresses the assertion, pass=true
- If the model does not address it or addresses it incorrectly, pass=false"""

    return prompt


def run_judge(api_key, base_url, judge_model, assertion, user_prompt, model_output, skill_system=None):
    """Run the judge model on a single assertion."""
    prompt = create_judge_prompt(assertion, user_prompt, model_output, skill_system)

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": judge_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0
        }
        
        url = f"{base_url.rstrip('/')}/chat/completions"
        
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
        content = data['choices'][0]['message']['content']
        result = json.loads(content)
        return {
            'assertion': assertion,
            'passed': result.get('passed', False),
            'evidence': result.get('evidence', 'N/A'),
            'reasoning': result.get('reasoning', 'No reasoning provided')
        }
    except json.JSONDecodeError as e:
        return {
            'assertion': assertion,
            'passed': False,
            'evidence': f'JSON parse error: {str(e)}',
            'reasoning': f'Raw response: {content[:200]}'
        }
    except Exception as e:
        return {
            'assertion': assertion,
            'passed': False,
            'evidence': f'Error: {str(e)}',
            'reasoning': 'Judge model failed'
        }


def rejudge_evals(input_file, judge_model, output_folder, api_key=None, base_url=None, max_workers=4):
    """Re-judge all evals in the input file using the specified judge model."""
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not set and no API key provided")
            sys.exit(1)
    
    if not base_url:
        base_url = os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    # Ensure base_url is a string
    base_url = str(base_url)

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse evals
    evals = parse_eval_output(content)
    print(f"Found {len(evals)} evals to re-judge")

    # Filter to only with_skill mode
    evals = [e for e in evals if e['mode'] == 'with_skill']
    print(f"Re-judging {len(evals)} with_skill evals using {judge_model} as judge")

    results = []
    total_assertions = 0

    for eval_data in evals:
        eval_num = eval_data['eval_num']
        user_prompt = eval_data['user']
        model_output = eval_data['output']
        skill_system = eval_data.get('system')
        assertions = eval_data['assertions']

        total_assertions += len(assertions)
        eval_results = {'eval_num': eval_num, 'assertions': []}

        print(f"\nRe-judging eval-{eval_num} ({len(assertions)} assertions)...")

        # Use thread pool for parallel judging
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    run_judge,
                    api_key,
                    base_url,
                    judge_model,
                    assertion['name'],
                    user_prompt,
                    model_output,
                    skill_system
                ): assertion
                for assertion in assertions
            }

            for future in as_completed(futures):
                assertion = futures[future]
                result = future.result()
                eval_results['assertions'].append(result)
                status = "PASS" if result['passed'] else "FAIL"
                print(f"  Assertion #{assertion['num']}: {status}")

        results.append(eval_results)

    # Write results to JSON file
    output_file = Path(output_folder) / 'rejudge_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'judge_model': judge_model,
            'source_file': input_file,
            'total_evals': len(results),
            'total_assertions': total_assertions,
            'results': results
        }, f, indent=2)

    # Write TSV summary
    tsv_file = Path(output_folder) / 'rejudge_summary.tsv'
    with open(tsv_file, 'w') as f:
        f.write("Eval\tAssertion\tPassed\tEvidence\tReasoning\n")
        for eval_result in results:
            for assertion_result in eval_result['assertions']:
                evidence = assertion_result['evidence'].replace('\t', ' ').replace('\n', ' ')[:200]
                reasoning = assertion_result['reasoning'].replace('\t', ' ').replace('\n', ' ')[:200]
                passed = "PASS" if assertion_result['passed'] else "FAIL"
                f.write(f"eval-{eval_result['eval_num']}\t{assertion_result['assertion']}\t{passed}\t{evidence}\t{reasoning}\n")

    # Calculate summary stats
    total_passed = sum(
        1 for r in results for a in r['assertions'] if a['passed']
    )
    pass_rate = (total_passed / total_assertions * 100) if total_assertions > 0 else 0

    print(f"\n{'='*50}")
    print(f"Re-judging complete!")
    print(f"Judge model: {judge_model}")
    print(f"Total assertions: {total_assertions}")
    print(f"Passed: {total_passed} ({pass_rate:.1f}%)")
    print(f"Results saved to: {output_folder}/")
    print(f"{'='*50}")

    return results


def main():
    args = sys.argv[1:]

    input_file = None
    judge_model = None
    output_folder = None
    api_key = None
    base_url = None
    max_workers = 4

    i = 0
    while i < len(args):
        if args[i] == '--judge-model' and i + 1 < len(args):
            judge_model = args[i + 1]
            i += 2
        elif args[i] == '--output-folder' and i + 1 < len(args):
            output_folder = args[i + 1]
            i += 2
        elif args[i] == '--api-key' and i + 1 < len(args):
            api_key = args[i + 1]
            i += 2
        elif args[i] == '--base-url' and i + 1 < len(args):
            base_url = args[i + 1]
            i += 2
        elif args[i] == '--workers' and i + 1 < len(args):
            max_workers = int(args[i + 1])
            i += 2
        elif not args[i].startswith('--'):
            input_file = args[i]
            i += 1
        else:
            i += 1

    if not input_file:
        print("Usage: python3 rejudge.py <input_file> --judge-model <model> --output-folder <folder> [--base-url <url>]")
        print("Example: python3 rejudge.py gpt55-results.txt --judge-model 'Qwen/Qwen3.5-122B-A10B-FP8' --output-folder rejudge-122b --base-url 'https://your-endpoint/v1'")
        sys.exit(1)

    if not judge_model:
        print("Error: --judge-model is required")
        sys.exit(1)

    if not output_folder:
        print("Error: --output-folder is required")
        sys.exit(1)

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    rejudge_evals(input_file, judge_model, output_folder, api_key, base_url, max_workers)


if __name__ == '__main__':
    main()

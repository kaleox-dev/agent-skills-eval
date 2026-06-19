#!/usr/bin/env python3
"""
Re-judge gpt-5.5 workspace output using 122B as judge.
Reads from agent-skills-workspace/gpt_5.5/ folder structure.

Usage:
    python3 rejudge_workspace.py --workspace-folder /path/to/gpt_5.5 --judge-model "Qwen/Qwen3.5-122B-A10B-FP8" --base-url "https://model.inferx.net/.../v1" --output-folder rejudge-results
"""

import sys
import os
import re
import json
import httpx
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_workspace_evals(workspace_folder, skills_folder):
    """Parse evals from workspace folder structure using evals.json for assertions."""
    workspace_path = Path(workspace_folder)
    evals = []
    
    # Read meta.json for skill name
    meta_file = workspace_path / 'meta.json'
    skill_name = 'ab-testing'
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            skill_name = meta.get('name', 'ab-testing')
    
    # Read evals.json from skills folder to get all assertions
    evals_json_path = Path(skills_folder) / 'evals' / 'evals.json'
    evals_data = {}
    if evals_json_path.exists():
        with open(evals_json_path) as f:
            data = json.load(f)
            for eval_item in data.get('evals', []):
                evals_data[str(eval_item['id'])] = eval_item.get('assertions', [])
    
    # Find all eval folders
    eval_folders = sorted([d for d in workspace_path.iterdir() if d.is_dir() and d.name.startswith('eval-')])
    
    for eval_folder in eval_folders:
        eval_num = eval_folder.name.replace('eval-', '')
        
        # Get assertions from evals.json
        assertions = evals_data.get(eval_num, [])
        if not assertions:
            continue
        
        # Process with_skill mode
        mode = 'with_skill'
        mode_folder = eval_folder / mode
        if not mode_folder.exists():
            continue
        
        # Read prompts.json
        prompts_file = mode_folder / 'prompts.json'
        if not prompts_file.exists():
            continue
        
        with open(prompts_file) as f:
            prompts_data = json.load(f)
        
        # Get user prompt
        user_prompt = prompts_data.get('user', '')
        system_prompt = prompts_data.get('system', '')
        
        # Get model output
        response_file = mode_folder / 'outputs' / 'response.txt'
        if response_file.exists():
            model_output = response_file.read_text()
        else:
            continue
        
        # Create assertion entries
        assertion_entries = [{'name': a} for a in assertions]
        
        if user_prompt and model_output and assertion_entries:
            evals.append({
                'eval_num': eval_num,
                'mode': mode,
                'system': system_prompt,
                'user': user_prompt,
                'output': model_output,
                'assertions': assertion_entries,
                'skill': skill_name
            })
    
    return evals


def create_judge_prompt(assertion, user_prompt, model_output, skill_name):
    """Create a prompt for the judge model to evaluate an assertion."""
    prompt = f"""You are an expert judge evaluating whether a model's response satisfies a specific assertion.

SKILL: {skill_name}
USER PROMPT: {user_prompt}

MODEL RESPONSE:
{model_output}

ASSERTION TO EVALUATE: {assertion}

Output ONLY valid JSON with this shape:
{{"passed": true/false, "evidence": "specific text from the model response that supports your judgment", "reasoning": "brief explanation"}}

Rules:
- Be strict but fair
- Evidence must be actual text from the model response or "N/A" if not applicable
- If the model clearly addresses the assertion, pass=true
- If the model does not address it or addresses it incorrectly, pass=false"""

    return prompt


def run_judge(api_key, base_url, judge_model, assertion, user_prompt, model_output, skill_name):
    """Run the judge model on a single assertion."""
    prompt = create_judge_prompt(assertion, user_prompt, model_output, skill_name)

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
        
        url = base_url.rstrip('/') + '/chat/completions'
        
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


def rejudge_workspace(workspace_folder, judge_model, output_folder, skills_folder, api_key=None, base_url=None, max_workers=4):
    """Re-judge all evals in the workspace folder using the specified judge model."""
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not set and no API key provided")
            sys.exit(1)
    
    if not base_url:
        base_url = os.getenv("OPENAI_BASE_URL")
        if not base_url:
            print("Error: --base-url is required or OPENAI_BASE_URL must be set")
            sys.exit(1)
    
    base_url = str(base_url)
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Parse evals from workspace
    evals = parse_workspace_evals(workspace_folder, skills_folder)
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
        skill_name = eval_data.get('skill', 'ab-testing')
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
                    skill_name
                ): assertion
                for assertion in assertions
            }

            for future in as_completed(futures):
                assertion = futures[future]
                result = future.result()
                eval_results['assertions'].append(result)
                status = "PASS" if result['passed'] else "FAIL"
                print(f"  Assertion: {status}")

        results.append(eval_results)

    # Write results to JSON file
    output_file = Path(output_folder) / 'rejudge_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'judge_model': judge_model,
            'source_folder': workspace_folder,
            'total_evals': len(results),
            'total_assertions': total_assertions,
            'results': results
        }, f, indent=2)

    # Write TSV summary in the same format as original eval harness
    tsv_file = Path(output_folder) / 'rejudge_summary.tsv'
    headers = ['Skill', 'Eval', 'Mode', 'Overall Result', 'Time', 'Total Tokens',
               'Assertion #', 'Assertion Status', 'Assertion Name', 'Evidence', 'Run', 'Iteration']
    
    with open(tsv_file, 'w') as f:
        f.write('\t'.join(headers) + '\n')
        
        for eval_result in results:
            eval_num = eval_result['eval_num']
            assertions = eval_result['assertions']
            
            # Determine overall result for this eval
            overall_result = "PASS" if all(a['passed'] for a in assertions) else "FAIL"
            
            for idx, assertion_result in enumerate(assertions, 1):
                clean_evidence = assertion_result['evidence'].replace('\t', ' ').replace('\n', ' ')[:200]
                assertion_status = "PASS" if assertion_result['passed'] else "FAIL"
                
                values = [
                    skill_name,  # Skill
                    f"eval-{eval_num}",  # Eval
                    "with_skill",  # Mode
                    overall_result,  # Overall Result
                    "N/A",  # Time (not available from workspace)
                    "N/A",  # Total Tokens (not available from workspace)
                    str(idx),  # Assertion #
                    assertion_status,  # Assertion Status
                    assertion_result['assertion'],  # Assertion Name
                    clean_evidence,  # Evidence
                    "1",  # Run
                    "1"  # Iteration
                ]
                f.write('\t'.join(values) + '\n')

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


def skill_name_from_workspace(workspace_folder):
    """Extract skill name from workspace folder path or meta.json."""
    meta_file = Path(workspace_folder) / 'meta.json'
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            return meta.get('name', 'ab-testing')
    # Try to extract from folder name
    return Path(workspace_folder).name


def main():
    args = sys.argv[1:]

    workspace_folder = None
    judge_model = None
    output_folder = None
    skills_folder = None
    api_key = None
    base_url = None
    max_workers = 4

    i = 0
    while i < len(args):
        if args[i] == '--workspace-folder' and i + 1 < len(args):
            workspace_folder = args[i + 1]
            i += 2
        elif args[i] == '--judge-model' and i + 1 < len(args):
            judge_model = args[i + 1]
            i += 2
        elif args[i] == '--output-folder' and i + 1 < len(args):
            output_folder = args[i + 1]
            i += 2
        elif args[i] == '--skills-folder' and i + 1 < len(args):
            skills_folder = args[i + 1]
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
        else:
            i += 1

    if not workspace_folder:
        print("Usage: python3 rejudge_workspace.py --workspace-folder <folder> --judge-model <model> --output-folder <folder> --base-url <url> [--skills-folder <folder>]")
        print("Example: python3 rejudge_workspace.py --workspace-folder ./agent-skills-workspace/gpt_5.5 --judge-model 'Qwen/Qwen3.5-122B-A10B-FP8' --output-folder rejudge-122b --base-url 'https://model.inferx.net/.../v1' --skills-folder ./skills/ab-testing")
        sys.exit(1)

    if not judge_model:
        print("Error: --judge-model is required")
        sys.exit(1)

    if not output_folder:
        print("Error: --output-folder is required")
        sys.exit(1)

    if not base_url:
        print("Error: --base-url is required")
        sys.exit(1)

    if not os.path.exists(workspace_folder):
        print(f"Error: Workspace folder '{workspace_folder}' not found")
        sys.exit(1)

    # Default skills folder
    if not skills_folder:
        skill_name = skill_name_from_workspace(workspace_folder)
        skills_folder = os.path.join(os.path.dirname(workspace_folder), 'skills', skill_name)
    
    if not os.path.exists(skills_folder):
        print(f"Error: Skills folder '{skills_folder}' not found")
        sys.exit(1)

    rejudge_workspace(workspace_folder, judge_model, output_folder, skills_folder, api_key, base_url, max_workers)


if __name__ == '__main__':
    main()

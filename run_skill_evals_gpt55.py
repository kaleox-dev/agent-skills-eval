#!/usr/bin/env python3
"""
Run skill evaluations for gpt-5.5 using eval-config-gpt5.5.json.
Always uses 122B model as the judge for consistent grading.

Usage:
    python3 run_skill_evals_gpt55.py --iterations 1 --output-folder "gpt55-eval-results"
"""

import sys
import os
import subprocess
import re
import csv
import json
from pathlib import Path
from collections import defaultdict


def load_config():
    """Load eval-config-gpt5.5.json."""
    config_path = Path(__file__).parent / 'eval-config-gpt5.5.json'
    if not config_path.exists():
        print(f"Error: {config_path} not found")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def run_eval(model_display, skill_path, iteration, output_file):
    """Run a single evaluation iteration with 122B as judge."""
    env = os.environ.copy()
    env['OPENAI_BASE_URL'] = 'https://dev4.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-NVFP4/v1'
    env['OPENAI_TEMPERATURE'] = '0'
    if 'OPENAI_API_KEY' not in env:
        print("Warning: OPENAI_API_KEY not set")
    
    cmd = [
        'npx', 'agent-skills-eval', skill_path,
        '--target', model_display,
        '--judge', 'Qwen/Qwen3.5-122B-A10B-NVFP4',
        '--baseline',
        '--strict'
    ]
    
    print(f"Running iteration {iteration}...")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    # Write output to file
    with open(output_file, 'w') as f:
        f.write(result.stdout)
        f.write(result.stderr)
    
    print(f"Output saved to: {output_file}")
    return output_file


def strip_ansi(text):
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_pattern.sub('', text)


def parse_eval_output(content, iteration=1, skill_name='ab-testing'):
    """Parse the evaluation output and return a list of rows."""
    all_rows = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        clean_line = strip_ansi(lines[i])

        eval_match = re.match(r'\s*#(\d+) eval-(\d+)\s+\[(with_skill|without_skill)\]', clean_line)
        if eval_match:
            current_eval = "eval-{}".format(eval_match.group(2))
            current_mode = eval_match.group(3)
            current_run = eval_match.group(2)

            overall_result = "FAIL"
            if 'PASS' in clean_line and 'FAIL' not in clean_line.split('PASS')[0][-10:]:
                overall_result = "PASS"

            i += 1

            eval_time = '0s'
            eval_tokens = '0'
            assertions = {}

            while i < len(lines):
                clean_next = strip_ansi(lines[i])

                time_match = re.search(r'(\d+\.\d+)s\s*[·\s]\s*(\d+)\s*tokens', clean_next)
                if time_match:
                    eval_time = time_match.group(1) + 's'
                    eval_tokens = time_match.group(2)
                    i += 1
                    break

                asserts_match = re.search(r'asserts:\s*(.+)', clean_next)
                if asserts_match:
                    summary_part = asserts_match.group(1)
                    for match in re.finditer(r'([✓✗])\s*(\d+)', summary_part):
                        symbol = match.group(1)
                        assert_num = int(match.group(2))
                        status = "PASS" if symbol == '✓' else "FAIL"
                        if assert_num not in assertions:
                            assertions[assert_num] = {'status': status, 'name': '', 'evidence': ''}
                        else:
                            assertions[assert_num]['status'] = status
                    i += 1
                    continue

                assert_match = re.match(r'\s*#(\d+)\s+(FAIL|PASS)\s+—\s+(.+)', clean_next)
                if assert_match:
                    assert_num = int(assert_match.group(1))
                    status = assert_match.group(2)
                    assert_name = assert_match.group(3).strip()

                    evidence = ""
                    i += 1
                    while i < len(lines):
                        clean_evidence_line = strip_ansi(lines[i])
                        if 'evidence:' in clean_evidence_line:
                            evidence_match = re.search(r'evidence:\s*(.+)', clean_evidence_line, re.IGNORECASE)
                            if evidence_match:
                                evidence = evidence_match.group(1).strip()
                            break
                        elif clean_evidence_line.strip() == '' or re.match(r'\s*#(\d+)', clean_evidence_line):
                            break
                        i += 1

                    assertions[assert_num] = {'status': status, 'name': assert_name, 'evidence': evidence}
                    continue

                i += 1

            for assert_num in sorted(assertions.keys()):
                data = assertions[assert_num]
                all_rows.append({
                    'skill': skill_name,
                    'eval': current_eval,
                    'mode': current_mode,
                    'overall_result': overall_result,
                    'time': eval_time,
                    'tokens': eval_tokens,
                    'assertion_num': assert_num,
                    'status': data['status'],
                    'assertion_name': data['name'],
                    'evidence': data['evidence'],
                    'run': current_run,
                    'iteration': iteration
                })
            continue

        i += 1

    return all_rows


def write_tsv(rows, output_path):
    """Write rows to TSV file."""
    headers = ['Skill', 'Eval', 'Mode', 'Overall Result', 'Time', 'Total Tokens',
               'Assertion #', 'Assertion Status', 'Assertion Name', 'Evidence', 'Run', 'Iteration']

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\t'.join(headers) + '\n')
        for row in rows:
            clean_name = row['assertion_name'].replace('\t', ' ').replace('\n', ' ')
            clean_evidence = row['evidence'].replace('\t', ' ').replace('\n', ' ')
            clean_overall = row['overall_result'].replace('\t', ' ').replace('\n', ' ')

            values = [
                row['skill'],
                row['eval'],
                row['mode'],
                clean_overall,
                row['time'],
                row['tokens'],
                str(row['assertion_num']),
                row['status'],
                clean_name,
                clean_evidence,
                row['run'],
                str(row['iteration'])
            ]
            f.write('\t'.join(values) + '\n')


def aggregate_results(folder_path, output_path):
    """Aggregate all TSV files in folder into a summary."""
    folder = Path(folder_path)
    
    tsv_files = sorted([f for f in folder.glob('*_evals.tsv') if f.name != 'merged.tsv'])
    
    if not tsv_files:
        print("No TSV files found in {}".format(folder))
        sys.exit(1)
    
    all_results = {}
    iterations = set()
    
    for tsv_file in tsv_files:
        match = re.search(r'iteration(\d+)', tsv_file.name)
        if match:
            iteration = int(match.group(1))
        else:
            iteration = 1
        
        iterations.add(iteration)
        
        with open(tsv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                eval_name = row['Eval']
                assert_num = int(row['Assertion #'])
                status = row['Assertion Status']
                assert_name = row['Assertion Name']
                
                key = (eval_name, assert_num)
                if key not in all_results:
                    all_results[key] = {'name': assert_name, 'iterations': {}}
                all_results[key]['name'] = assert_name
                all_results[key]['iterations'][iteration] = status
    
    iterations = sorted(iterations)
    
    rows = []
    for (eval_name, assert_num), data in sorted(all_results.items(), key=lambda x: (int(x[0][0].split('-')[1]), x[0][1])):
        fail_count = 0
        for iteration in iterations:
            status = data['iterations'].get(iteration, 'N/A')
            if status == 'FAIL':
                fail_count += 1
        
        rows.append({
            'Eval': eval_name,
            'Assertion #': assert_num,
            'Fail Count': fail_count
        })
    
    headers = ['Eval', 'Assertion #', 'Fail Count']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print("Wrote {} rows to {}".format(len(rows), output_path))


def calculate_pass_rates(folder_path):
    """Calculate pass rates by parsing raw TXT files."""
    folder = Path(folder_path)
    
    txt_files = sorted([f for f in folder.glob('*.txt') if 'evals' not in f.name and f.name != 'pass_rate_summary.tsv'])
    
    if not txt_files:
        print("No TXT files found in {}".format(folder))
        sys.exit(1)
    
    run_data = defaultdict(lambda: {'with_skill': {'pass': 0, 'total': 0}, 
                                     'without_skill': {'pass': 0, 'total': 0}})
    
    for txt_file in txt_files:
        run_name = txt_file.stem
        
        content = txt_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        current_mode = None
        for line in lines:
            if '[with_skill]' in line:
                current_mode = 'with_skill'
            elif '[without_skill]' in line:
                current_mode = 'without_skill'
            
            if current_mode and 'asserts:' in line:
                passes = len(re.findall(r'✓', line))
                fails = len(re.findall(r'✗', line))
                run_data[run_name][current_mode]['pass'] += passes
                run_data[run_name][current_mode]['total'] += passes + fails
    
    return run_data


def write_pass_rate_summary(run_data, output_path):
    """Write pass rate summary to TSV."""
    rows = []
    
    def sort_key(run_name):
        match = re.search(r'(\d+)', run_name)
        return int(match.group(1)) if match else 0
    
    for run_name in sorted(run_data.keys(), key=sort_key):
        data = run_data[run_name]
        
        with_skill_pct = 0.0
        if data['with_skill']['total'] > 0:
            with_skill_pct = (data['with_skill']['pass'] / data['with_skill']['total']) * 100
        
        without_skill_pct = 0.0
        if data['without_skill']['total'] > 0:
            without_skill_pct = (data['without_skill']['pass'] / data['without_skill']['total']) * 100
        
        rows.append({
            'Run': run_name,
            'with_skill_Percent': round(with_skill_pct, 1),
            'without_skill_Percent': round(without_skill_pct, 1)
        })
    
    headers = ['Run', 'with_skill_Percent', 'without_skill_Percent']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print("Wrote {} rows to {}".format(len(rows), output_path))


def main():
    args = sys.argv[1:]
    
    iterations = 1
    output_folder = None
    
    i = 0
    while i < len(args):
        if args[i] == '--iterations' and i + 1 < len(args):
            iterations = int(args[i + 1])
            i += 2
        elif args[i] == '--output-folder' and i + 1 < len(args):
            output_folder = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not output_folder:
        print("Usage: python3 run_skill_evals_gpt55.py --iterations <n> --output-folder <folder>")
        sys.exit(1)
    
    # Load config
    config = load_config()
    model_display = config.get('target', 'gpt-5.5')
    skill_path = config.get('root', './skills/ab-testing')
    
    # Create output folder
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    print(f"=========================================")
    print(f"Running {skill_path} evals on {model_display}")
    print(f"Output folder: {output_folder}")
    print(f"=========================================\n")
    
    txt_files = []
    
    # Run iterations
    for iteration in range(1, iterations + 1):
        run_name = f"{Path(output_folder).name}-iteration{iteration}"
        txt_file = os.path.join(output_folder, f"{run_name}.txt")
        
        run_eval(model_display, skill_path, iteration, txt_file)
        txt_files.append(txt_file)
        
        # Parse and generate TSV
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        rows = parse_eval_output(content, iteration, skill_path.split('/')[-1])
        rows = [r for r in rows if r['mode'] == 'with_skill']
        
        tsv_file = os.path.join(output_folder, f"{run_name}_evals.tsv")
        write_tsv(rows, tsv_file)
        print(f"Generated: {tsv_file}\n")
    
    # Generate merged.tsv
    print("=== Generating merged.tsv ===")
    tsv_files = sorted([f for f in Path(output_folder).glob('*_evals.tsv')])
    if len(tsv_files) == 1:
        import shutil
        shutil.copy(tsv_files[0], os.path.join(output_folder, 'merged.tsv'))
    else:
        all_rows = []
        headers = None
        for tsv_file in tsv_files:
            with open(tsv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                if headers is None:
                    headers = reader.fieldnames
                for row in reader:
                    all_rows.append(row)
        
        with open(os.path.join(output_folder, 'merged.tsv'), 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
            writer.writeheader()
            writer.writerows(all_rows)
    
    print(f"Generated: {os.path.join(output_folder, 'merged.tsv')}\n")
    
    # Generate aggregate.tsv
    print("=== Generating aggregate.tsv ===")
    aggregate_results(output_folder, os.path.join(output_folder, 'aggregate.tsv'))
    print()
    
    # Generate pass_rate_summary.tsv
    print("=== Generating pass_rate_summary.tsv ===")
    run_data = calculate_pass_rates(output_folder)
    write_pass_rate_summary(run_data, os.path.join(output_folder, 'pass_rate_summary.tsv'))
    print()
    
    print("=========================================")
    print("All evaluations complete!")
    print(f"Results saved in: {output_folder}/")
    print("=========================================")
    
    # List files
    for f in sorted(Path(output_folder).iterdir()):
        print(f"  {f.name}")


if __name__ == '__main__':
    main()

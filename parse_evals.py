#!/usr/bin/env python3
"""
Parse evaluation output and convert to TSV format for Google Sheets.

Usage:
    python3 parse_evals.py <input_file> [output_file] [--iteration N]

Example:
    python3 parse_evals.py iteration-1-output.txt ads_evals.tsv --iteration 1
"""

import sys
import re
from pathlib import Path


def strip_ansi(text):
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_pattern.sub('', text)


def parse_eval_output(content, iteration=1, workspace_iteration="unknown", skill="unknown"):
    """Parse the evaluation output and return a list of rows."""
    all_rows = []

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        clean_line = strip_ansi(lines[i])

        # Match eval header like "#4 eval-4  [with_skill]  [4]"
        eval_match = re.match(r'\s*#(\d+) eval-(\d+)\s+\[(with_skill|without_skill)\]', clean_line)
        if eval_match:
            current_eval = "eval-{}".format(eval_match.group(2))
            current_mode = eval_match.group(3)
            current_run = eval_match.group(2)

            # Check for PASS/FAIL in overall result
            overall_result = "FAIL"
            if 'PASS' in clean_line and 'FAIL' not in clean_line.split('PASS')[0][-10:]:
                overall_result = "PASS"

            i += 1

            # Collect time/tokens and assertions for this eval block
            eval_time = '0s'
            eval_tokens = '0'
            eval_input_tokens = '0'
            eval_output_tokens = '0'
            assertions = {}  # assert_num -> {status, name, evidence}

            while i < len(lines):
                clean_next = strip_ansi(lines[i])

                # Check for time/tokens line (marks end of eval block)
                # Try to match breakdown first: "X.Xs · N tokens (I input / O output)"
                breakdown_match = re.search(r'(\d+\.\d+)s\s*[·\s]\s*(\d+)\s*tokens\s*\((\d+)\s*input\s*/\s*(\d+)\s*output\)', clean_next)
                if breakdown_match:
                    eval_time = breakdown_match.group(1) + 's'
                    eval_tokens = breakdown_match.group(2)
                    eval_input_tokens = breakdown_match.group(3)
                    eval_output_tokens = breakdown_match.group(4)
                    i += 1
                    break
                
                # Fallback to simple format: "X.Xs · N tokens"
                time_match = re.search(r'(\d+\.\d+)s\s*[·\s]\s*(\d+)\s*tokens', clean_next)
                if time_match:
                    eval_time = time_match.group(1) + 's'
                    eval_tokens = time_match.group(2)
                    # Estimate: ~65% input, ~35% output for target model
                    input_est = int(int(eval_tokens) * 0.65)
                    output_est = int(int(eval_tokens) * 0.35)
                    eval_input_tokens = str(input_est)
                    eval_output_tokens = str(output_est)
                    i += 1
                    break

                # Parse asserts summary line
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

                # Parse assertion detail lines
                assert_match = re.match(r'\s*#(\d+)\s+(FAIL|PASS)\s+—\s+(.+)', clean_next)
                if assert_match:
                    assert_num = int(assert_match.group(1))
                    status = assert_match.group(2)
                    assert_name = assert_match.group(3).strip()

                    # Get evidence from next line
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

            # Output all assertions for this eval
            for assert_num in sorted(assertions.keys()):
                data = assertions[assert_num]
                all_rows.append({
                    'skill': skill,
                    'eval': current_eval,
                    'mode': current_mode,
                    'overall_result': overall_result,
                    'time': eval_time,
                    'tokens': eval_tokens,
                    'input_tokens': eval_input_tokens,
                    'output_tokens': eval_output_tokens,
                    'assertion_num': assert_num,
                    'status': data['status'],
                    'assertion_name': data['name'],
                    'evidence': data['evidence'],
                    'run': current_run,
                    'iteration': iteration,
                    'workspace_iteration': workspace_iteration
                })
            continue

        i += 1

    return all_rows


def write_tsv(rows, output_path):
    """Write rows to TSV file."""
    headers = ['Skill', 'Eval', 'Mode', 'Overall Result', 'Time', 'Total Tokens', 'Input Tokens', 'Output Tokens',
               'Assertion #', 'Assertion Status', 'Assertion Name', 'Evidence', 'Run', 'Iteration', 'Workspace_Iteration']

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
                str(row.get('input_tokens', 'N/A')),
                str(row.get('output_tokens', 'N/A')),
                str(row['assertion_num']),
                row['status'],
                clean_name,
                clean_evidence,
                row['run'],
                str(row['iteration']),
                str(row['workspace_iteration'])
            ]
            f.write('\t'.join(values) + '\n')


def main():
    iteration = 1
    workspace_iteration = "unknown"
    skill = "unknown"
    args = sys.argv[1:]
    
    # Parse --iteration flag
    if '--iteration' in args:
        idx = args.index('--iteration')
        if idx + 1 < len(args):
            iteration = int(args[idx + 1])
            args = args[:idx] + args[idx+2:]
    
    # Parse --workspace-iteration flag
    if '--workspace-iteration' in args:
        idx = args.index('--workspace-iteration')
        if idx + 1 < len(args):
            workspace_iteration = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    # Parse --skill flag
    if '--skill' in args:
        idx = args.index('--skill')
        if idx + 1 < len(args):
            skill = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    if len(args) < 1:
        print("Usage: python3 parse_evals.py <input_file> [output_file] [--iteration N] [--workspace-iteration X] [--skill NAME]")
        print("Example: python3 parse_evals.py iteration-1-output.txt ads_evals.tsv --iteration 1 --workspace-iteration 168 --skill ads")
        sys.exit(1)

    input_path = Path(args[0])
    if not input_path.exists():
        print("Error: Input file '{}' not found".format(input_path))
        sys.exit(1)

    if len(args) >= 2:
        output_path = Path(args[1])
    else:
        output_path = input_path.with_name(input_path.stem + "_evals.tsv")

    content = input_path.read_text(encoding='utf-8')
    rows = parse_eval_output(content, iteration, workspace_iteration, skill)

    # Filter to only with_skill mode
    rows = [r for r in rows if r['mode'] == 'with_skill']

    # Sort by eval number, then assertion number
    def sort_key(row):
        eval_num = int(row['eval'].split('-')[1])
        return (eval_num, row['assertion_num'])

    rows.sort(key=sort_key)

    write_tsv(rows, output_path)
    print("Wrote {} rows to {}".format(len(rows), output_path))


if __name__ == '__main__':
    main()

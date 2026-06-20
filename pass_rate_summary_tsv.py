#!/usr/bin/env python3
"""
Generate pass_rate_summary.tsv from evaluation TXT files.

Counts PASS/FAIL from the raw txt output for with_skill mode only.

Creates pass_rate_summary.tsv with columns:
- Run
- with_skill_Percent

Usage:
    python3 pass_rate_summary_tsv.py <folder> -o pass_rate_summary.tsv
"""

import sys
import re
import csv
from pathlib import Path
from collections import defaultdict


def calculate_pass_rates(folder_path):
    """Calculate pass rates by parsing raw TXT files."""
    folder = Path(folder_path)
    
    # Find all TXT files (not the summary ones)
    txt_files = sorted([f for f in folder.glob('*.txt') if 'evals' not in f.name and f.name != 'pass_rate_summary.tsv'])
    
    if not txt_files:
        print("No TXT files found in {}".format(folder))
        sys.exit(1)
    
    # Group by run/iteration
    run_data = defaultdict(lambda: {'with_skill': {'pass': 0, 'total': 0}, 
                                     'without_skill': {'pass': 0, 'total': 0}})
    
    for txt_file in txt_files:
        run_name = txt_file.stem
        
        content = txt_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        current_mode = None
        for line in lines:
            # Check if we're in a with_skill or without_skill block
            if '[with_skill]' in line:
                current_mode = 'with_skill'
            elif '[without_skill]' in line:
                current_mode = 'without_skill'
            
            # Count assertions for current mode
            if current_mode and 'asserts:' in line:
                # Count checkmarks (✓) as PASS, crosses (✗) as FAIL
                passes = len(re.findall(r'✓', line))
                fails = len(re.findall(r'✗', line))
                run_data[run_name][current_mode]['pass'] += passes
                run_data[run_name][current_mode]['total'] += passes + fails
    
    return run_data


def write_summary(run_data, output_path):
    """Write pass rate summary to TSV (with_skill only)."""
    rows = []
    
    # Sort runs naturally
    def sort_key(run_name):
        import re
        match = re.search(r'(\d+)', run_name)
        return int(match.group(1)) if match else 0
    
    for run_name in sorted(run_data.keys(), key=sort_key):
        data = run_data[run_name]
        
        with_skill_pct = 0.0
        if data['with_skill']['total'] > 0:
            with_skill_pct = (data['with_skill']['pass'] / data['with_skill']['total']) * 100
        
        rows.append({
            'Run': run_name,
            'with_skill_Percent': round(with_skill_pct, 1)
        })
    
    headers = ['Run', 'with_skill_Percent']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print("Wrote {} rows to {}".format(len(rows), output_path))


def main():
    args = sys.argv[1:]
    
    if '-o' not in args:
        print("Usage: python3 pass_rate_summary_tsv.py <folder> -o pass_rate_summary.tsv")
        sys.exit(1)
    
    o_idx = args.index('-o')
    if o_idx + 1 >= len(args):
        print("Error: No output file specified after -o")
        sys.exit(1)
    
    output_path = args[o_idx + 1]
    folder_path = args[:o_idx][0] if args[:o_idx] else '.'
    
    run_data = calculate_pass_rates(folder_path)
    write_summary(run_data, output_path)


if __name__ == '__main__':
    main()

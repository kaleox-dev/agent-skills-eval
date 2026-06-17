#!/usr/bin/env python3
"""
Aggregate evaluation results into a summary TSV.

Creates aggregate.tsv with columns:
- Eval
- Assertion #
- Assertion Name
- Iteration 1 (PASS/FAIL)
- Iteration 2 (PASS/FAIL)
- ...
- Fail Count (how many iterations failed)

Usage:
    python3 aggregate_tsv.py <folder> -o aggregate.tsv
"""

import sys
import csv
import re
from pathlib import Path
from collections import defaultdict


def parse_tsv(file_path):
    """Parse a TSV file and return dict of (eval, assert_num) -> {status, name}."""
    results = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            eval_name = row['Eval']
            assert_num = int(row['Assertion #'])
            status = row['Assertion Status']
            assert_name = row['Assertion Name']
            iteration = int(row.get('Iteration', 1))
            
            key = (eval_name, assert_num)
            if key not in results:
                results[key] = {'name': assert_name, 'iterations': {}}
            results[key]['iterations'][iteration] = status
    
    return results


def aggregate_results(folder_path, output_path):
    """Aggregate all TSV files in folder into a summary."""
    folder = Path(folder_path)
    
    # Find all TSV files (excluding merged.tsv)
    tsv_files = sorted([f for f in folder.glob('*_evals.tsv') if f.name != 'merged.tsv'])
    
    if not tsv_files:
        print("No TSV files found in {}".format(folder))
        sys.exit(1)
    
    # Parse all files and group by iteration
    all_results = {}
    iterations = set()
    
    for tsv_file in tsv_files:
        # Extract iteration number from filename
        # Supports patterns like: iteration1_evals.tsv, run-1_evals.tsv, run1_evals.tsv
        match = re.search(r'iteration(\d+)', tsv_file.name)
        if not match:
            match = re.search(r'run-(\d+)', tsv_file.name)
        if not match:
            match = re.search(r'run(\d+)', tsv_file.name)
        
        if match:
            iteration = int(match.group(1))
        else:
            iteration = 1
        
        iterations.add(iteration)
        results = parse_tsv(tsv_file)
        
        for key, data in results.items():
            if key not in all_results:
                all_results[key] = {'name': data['name'], 'iterations': {}}
            all_results[key]['name'] = data['name']
            all_results[key]['iterations'].update(data['iterations'])
    
    # Sort iterations
    iterations = sorted(iterations)
    
    # Build output rows
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
    
    # Write output
    headers = ['Eval', 'Assertion #', 'Fail Count']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print("Wrote {} rows to {}".format(len(rows), output_path))


def main():
    args = sys.argv[1:]
    
    if '-o' not in args:
        print("Usage: python3 aggregate_tsv.py <folder> -o aggregate.tsv")
        sys.exit(1)
    
    o_idx = args.index('-o')
    if o_idx + 1 >= len(args):
        print("Error: No output file specified after -o")
        sys.exit(1)
    
    output_path = args[o_idx + 1]
    folder_path = args[:o_idx][0] if args[:o_idx] else '.'
    
    aggregate_results(folder_path, output_path)


if __name__ == '__main__':
    main()

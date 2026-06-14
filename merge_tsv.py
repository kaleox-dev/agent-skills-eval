#!/usr/bin/env python3
"""
Merge multiple TSV evaluation files into one.

Usage:
    python3 merge_tsv.py <file1.tsv> <file2.tsv> ... -o merged.tsv
"""

import sys
import csv
from pathlib import Path


def merge_tsv_files(file_paths, output_path):
    """Merge multiple TSV files into one."""
    all_rows = []
    headers = None

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print("Error: File '{}' not found".format(file_path))
            sys.exit(1)

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            if headers is None:
                headers = reader.fieldnames
            for row in reader:
                all_rows.append(row)

    if not headers:
        print("Error: No data found in input files")
        sys.exit(1)

    # Sort by Eval (numerically), then Assertion # (numerically), then Iteration
    def sort_key(row):
        eval_num = int(row['Eval'].split('-')[1])
        assert_num = int(row['Assertion #'])
        iteration = int(row.get('Iteration', 1))
        return (iteration, eval_num, assert_num)

    all_rows.sort(key=sort_key)

    # Write merged file
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(all_rows)

    print("Merged {} rows from {} files into {}".format(len(all_rows), len(file_paths), output_path))


def main():
    args = sys.argv[1:]

    if '-o' not in args:
        print("Usage: python3 merge_tsv.py <file1.tsv> <file2.tsv> ... -o merged.tsv")
        sys.exit(1)

    # Find output file
    o_idx = args.index('-o')
    if o_idx + 1 >= len(args):
        print("Error: No output file specified after -o")
        sys.exit(1)

    output_path = args[o_idx + 1]
    input_files = args[:o_idx]

    if len(input_files) < 2:
        print("Error: Need at least 2 input files to merge")
        sys.exit(1)

    merge_tsv_files(input_files, output_path)


if __name__ == '__main__':
    main()

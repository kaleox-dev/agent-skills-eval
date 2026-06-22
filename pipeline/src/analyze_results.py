#!/usr/bin/env python3
"""
Step 1: Analyze merged.tsv to identify failure patterns.
Reads existing eval results WITHOUT modifying them.
"""

import pandas as pd
import json
import argparse
from pathlib import Path
from collections import Counter

def analyze_tsv(tsv_path: str, output_path: str = None):
    """
    Analyze a merged.tsv file (or single run TSV) and extract failure patterns.
    
    Args:
        tsv_path: Path to merged.tsv or run-1_evals.tsv
        output_path: Optional path to save analysis JSON (default: same dir as tsv)
    """
    tsv_file = Path(tsv_path)
    if not tsv_file.exists():
        raise FileNotFoundError(f"TSV file not found: {tsv_path}")
    
    # Load TSV
    df = pd.read_csv(tsv_file, sep='\t')
    
    # If merged.tsv is empty (header only), look for run-1_evals.tsv
    if len(df) <= 1:  # Only header or empty
        parent_dir = tsv_file.parent
        run_tsv = parent_dir / "run-1_evals.tsv"
        if run_tsv.exists():
            df = pd.read_csv(run_tsv, sep='\t')
        else:
            # Try to find any run-*_evals.tsv
            run_files = list(parent_dir.glob("run-*_evals.tsv"))
            if run_files:
                df = pd.read_csv(run_files[0], sep='\t')
            else:
                raise FileNotFoundError(f"No valid TSV data found in {tsv_file.parent}")
    
    # Filter for failures only
    failures = df[df['Assertion Status'] == 'FAIL']
    
    if len(failures) == 0:
        analysis = {
            "skill_name": tsv_file.parent.name,
            "total_assertions": len(df),
            "total_failures": 0,
            "pass_rate": 100.0,
            "top_failure_patterns": [],
            "message": "No failures detected!"
        }
    else:
        # Group by assertion name
        assertion_counts = failures['Assertion Name'].value_counts()
        
        # Get sample evidence for each top failure
        top_patterns = []
        for assertion_name, count in assertion_counts.head(10).items():
            sample_evidence = failures[failures['Assertion Name'] == assertion_name]['Evidence'].iloc[0]
            top_patterns.append({
                "assertion": assertion_name,
                "fail_count": int(count),
                "sample_evidence": sample_evidence
            })
        
        total = len(df)
        passed = len(df[df['Assertion Status'] == 'PASS'])
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        analysis = {
            "skill_name": tsv_file.parent.name,
            "total_assertions": int(total),
            "total_passed": int(passed),
            "total_failures": int(len(failures)),
            "pass_rate": round(pass_rate, 1),
            "top_failure_patterns": top_patterns
        }
    
    # Save analysis
    if output_path is None:
        output_path = tsv_file.parent / "analysis.json"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Analysis saved to: {output_path}")
    print(f"Pass Rate: {analysis['pass_rate']}%")
    print(f"Failures: {analysis['total_failures']}/{analysis['total_assertions']}")
    
    return analysis

def main():
    parser = argparse.ArgumentParser(description="Analyze merged.tsv for failure patterns")
    parser.add_argument("--input", required=True, help="Path to merged.tsv")
    parser.add_argument("--output", help="Output path for analysis.json (optional)")
    
    args = parser.parse_args()
    analyze_tsv(args.input, args.output)

if __name__ == "__main__":
    main()

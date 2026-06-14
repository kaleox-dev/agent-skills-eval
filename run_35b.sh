#!/bin/bash
# Usage: ./run_35b.sh <SKILL_NAME> <NUM_RUNS>
# Example: ./run_35b.sh ab-testing 10

set -e

SKILL_NAME="${1:-ab-testing}"
NUM_RUNS="${2:-10}"

API_KEY="${OPENAI_API_KEY:-}"
BASE_URL="https://dev4.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-FP8-no-think/v1"
MODEL="Qwen/Qwen3.6-35B-A3B-fp8"
SKILL_DIR="/home/lily/agent-skills-eval/skills"

FOLDER="/home/lily/agent-skills-eval/${SKILL_NAME}-35B-${NUM_RUNS}runs"

echo "=========================================="
echo "Running $NUM_RUNS iterations of $SKILL_NAME"
echo "Model: $MODEL (35B)"
echo "Endpoint: $BASE_URL"
echo "Output: $FOLDER"
echo "=========================================="

rm -rf "$FOLDER"
mkdir -p "$FOLDER"

export OPENAI_API_KEY="$API_KEY"
export OPENAI_BASE_URL="$BASE_URL"

for i in $(seq 1 $NUM_RUNS); do
    echo ""
    echo "=== Run $i/$NUM_RUNS ==="
    
    OUTPUT_FILE="$FOLDER/run-$i-output.txt"
    
    # Run WITHOUT --baseline (only with_skill mode) to avoid duplicates
    npx --yes agent-skills-eval \
        "$SKILL_DIR" \
        --target "$MODEL" \
        --judge "$MODEL" \
        --include "$SKILL_NAME" \
        --strict \
        --log-format pretty \
        2>&1 | tee "$OUTPUT_FILE"
    
    echo "Saved: $OUTPUT_FILE"
done

echo ""
echo "=== Generating aggregate.tsv and counts.tsv ==="

export FOLDER="$FOLDER"
python3 << 'PYEOF'
import os, sys, re, csv
from pathlib import Path
from collections import defaultdict

folder = os.environ.get('FOLDER', "/home/lily/agent-skills-eval/ab-testing-35B-10runs")

output_files = sorted([f for f in os.listdir(folder) if f.startswith("run-") and f.endswith("-output.txt")])
print(f"Processing {len(output_files)} output files")

all_runs = []

for run_idx, output_file in enumerate(output_files, 1):
    filepath = os.path.join(folder, output_file)
    run_data = []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Strip ANSI codes
    content = re.sub(r'\x1b\[[0-9;]*m', '', content)
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for eval header: #1 eval-1 ...
        eval_match = re.search(r'#\d+\s+(eval-\d+)', line)
        if eval_match:
            current_eval = eval_match.group(1)
            
            # Find asserts line
            asserts_line = ""
            asserts_idx = -1
            for j in range(i, min(i+5, len(lines))):
                if 'asserts:' in lines[j]:
                    asserts_line = lines[j]
                    asserts_idx = j
                    break
            
            if asserts_line:
                # Extract assertion numbers and status (✓ or ✗)
                assertion_matches = re.findall(r'[✗✓]\s*(\d+)', asserts_line)
                if assertion_matches:
                    total_assertions = max([int(a) for a in assertion_matches])
                    
                    # Find end of eval section
                    eval_end = len(lines)
                    for k in range(asserts_idx + 1, len(lines)):
                        if re.search(r'#\d+\s+eval', lines[k]) or 'summary' in lines[k]:
                            eval_end = k
                            break
                    
                    # Parse FAIL details
                    fail_details = {}
                    for k in range(asserts_idx + 1, eval_end):
                        fail_match = re.search(r'#(\d+)\s+FAIL\s*—\s*(.+)', lines[k])
                        if fail_match:
                            fail_details[fail_match.group(1)] = fail_match.group(2).strip()
                    
                    for k in range(1, total_assertions + 1):
                        status = "FAIL" if str(k) in fail_details else "PASS"
                        evidence = fail_details.get(str(k), "")
                        run_data.append((current_eval, str(k), status, "", evidence))
        
        i += 1
    
    all_runs.append(run_data)
    print(f"Run {run_idx}: {len(run_data)} assertions captured")

# Write aggregate.tsv
agg_path = os.path.join(folder, "aggregate.tsv")
with open(agg_path, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["Skill", "Eval", "Mode", "Overall Result", "Time", "Total Tokens", "Assertion #", "Assertion Status", "Assertion Name", "Evidence", "Run"])
    for run_idx, run_data in enumerate(all_runs, 1):
        for eval_name, assertion_num, status, assertion_name, evidence in run_data:
            writer.writerow(["ab-testing", eval_name, "with_skill", "PASS", "0s", "0", assertion_num, status, assertion_name, evidence, str(run_idx)])

# Count FAILs across ALL runs
# Key: (eval, assertion) -> count of runs where it failed
fail_counts = defaultdict(int)
all_pairs = set()

for run_data in all_runs:
    # For this run, which (eval, assertion) pairs FAILED?
    # Use a set to avoid double-counting duplicates within the same run
    run_fail_set = set()
    for eval_name, assertion_num, status, _, _ in run_data:
        key = (eval_name, assertion_num)
        all_pairs.add(key)
        if status == "FAIL":
            run_fail_set.add(key)
    
    # Increment count for each failed pair in this run
    for key in run_fail_set:
        fail_counts[key] += 1

counts_path = os.path.join(folder, "counts.tsv")
# Sort by eval name, then assertion number
sorted_pairs = sorted(all_pairs, key=lambda x: (x[0], int(x[1].split("-")[-1]) if "-" in x[1] else int(x[1])))

with open(counts_path, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["Eval", "Assertion", "35B"])
    for eval_name, assertion_num in sorted_pairs:
        count = fail_counts.get((eval_name, assertion_num), 0)
        writer.writerow([eval_name, assertion_num, count])

print(f"\nCreated aggregate.tsv ({len(all_pairs) * len(all_runs) + 1} rows)")
print(f"Created counts.tsv ({len(sorted_pairs) + 1} rows)")
print(f"\nFolder: {folder}")
print("counts.tsv (showing failure counts across all runs):")
with open(counts_path) as f:
    print(f.read())
PYEOF

echo "DONE!"
ls -la "$FOLDER"

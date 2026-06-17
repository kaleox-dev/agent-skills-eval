#!/bin/bash
# run_35b_ab_testing_2iter.sh
# Run 35B ab-testing skill evals for 2 iterations

set -e

FOLDER="eval-results/35b-ab-testing-2iter"
mkdir -p "$FOLDER"

export OPENAI_BASE_URL="https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1"
export OPENAI_TEMPERATURE="0"

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not set"
    exit 1
fi

echo "=== Iteration 1 ==="
npx agent-skills-eval ./skills/ab-testing \
  --target "Qwen/Qwen3.6-35B-A3B-fp8" \
  --judge "Qwen/Qwen3.6-35B-A3B-fp8" \
  --baseline \
  --strict \
  2>&1 | tee "$FOLDER/run-1.txt"

python3 parse_evals.py "$FOLDER/run-1.txt" "$FOLDER/run-1_evals.tsv" --iteration 1

echo "=== Iteration 2 ==="
npx agent-skills-eval ./skills/ab-testing \
  --target "Qwen/Qwen3.6-35B-A3B-fp8" \
  --judge "Qwen/Qwen3.6-35B-A3B-fp8" \
  --baseline \
  --strict \
  2>&1 | tee "$FOLDER/run-2.txt"

python3 parse_evals.py "$FOLDER/run-2.txt" "$FOLDER/run-2_evals.tsv" --iteration 2

echo "=== Generating merged.tsv ==="
python3 merge_tsv.py "$FOLDER/run-1_evals.tsv" "$FOLDER/run-2_evals.tsv" -o "$FOLDER/merged.tsv"

echo "=== Generating aggregate.tsv ==="
python3 aggregate_tsv.py "$FOLDER" -o "$FOLDER/aggregate.tsv"

echo "=== Generating pass_rate_summary.tsv ==="
python3 pass_rate_summary_tsv.py "$FOLDER" -o "$FOLDER/pass_rate_summary.tsv"

echo "=== Done ==="
ls -la "$FOLDER/"

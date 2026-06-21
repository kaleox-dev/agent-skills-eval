#!/bin/bash
# run_skill_evals.sh
# Run skill evals for any model configuration

set -e

# Usage: ./run_skill_evals.sh --model "Model/Name" --url "https://..." --skill "./skills/skill-name" --iterations 2 --output-folder "eval-results/model-skill-2iter"

MODEL_DISPLAY=""
MODEL_URL=""
JUDGE_URL=""
JUDGE_API_KEY=""
SKILL_PATH="./skills/ab-testing"
ITERATIONS=2
OUTPUT_FOLDER="eval-results/model-skill-2iter"
CONFIG_FILE=""
WORKSPACE="./agent-skills-workspace"

while [[ $# -gt 0 ]]; do
  case $1 in
    --model)
      MODEL_DISPLAY="$2"
      shift 2
      ;;
    --url)
      MODEL_URL="$2"
      shift 2
      ;;
    --judge-url)
      JUDGE_URL="$2"
      shift 2
      ;;
    --judge-api-key)
      JUDGE_API_KEY="$2"
      shift 2
      ;;
    --skill)
      SKILL_PATH="$2"
      shift 2
      ;;
    --iterations)
      ITERATIONS="$2"
      shift 2
      ;;
    --output-folder)
      OUTPUT_FOLDER="$2"
      shift 2
      ;;
    --config)
      CONFIG_FILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not set"
    exit 1
fi

mkdir -p "$OUTPUT_FOLDER"
if [ -n "$MODEL_URL" ]; then
  export OPENAI_BASE_URL="$MODEL_URL"
fi

# Set judge URL if provided, otherwise use model URL
if [ -n "$JUDGE_URL" ]; then
  export JUDGE_BASE_URL="$JUDGE_URL"
else
  export JUDGE_BASE_URL="$MODEL_URL"
fi

export OPENAI_TEMPERATURE="0"

echo "========================================="
echo "Running $SKILL_PATH on $MODEL_DISPLAY"
echo "Iterations: $ITERATIONS"
echo "Output: $OUTPUT_FOLDER"
echo "========================================="

for i in $(seq 1 $ITERATIONS); do
  echo ""
  echo "=== Iteration $i ==="

  txt_file="$OUTPUT_FOLDER/run-${i}.txt"
  tsv_file="$OUTPUT_FOLDER/run-${i}_evals.tsv"
  
  if [ -n "$CONFIG_FILE" ]; then
    npx agent-skills-eval "$SKILL_PATH" \
      --config "$CONFIG_FILE" \
      2>&1 | tee "$txt_file"
  elif [ -n "$JUDGE_URL" ]; then
    if [ -n "$JUDGE_API_KEY" ]; then
      npx agent-skills-eval "$SKILL_PATH" \
        --target "$MODEL_DISPLAY" \
        --base-url "$MODEL_URL" \
        --judge-base-url "$JUDGE_URL" \
        --judge-api-key "$JUDGE_API_KEY" \
        --strict \
        2>&1 | tee "$txt_file"
    else
      npx agent-skills-eval "$SKILL_PATH" \
        --target "$MODEL_DISPLAY" \
        --base-url "$MODEL_URL" \
        --judge-base-url "$JUDGE_URL" \
        --strict \
        2>&1 | tee "$txt_file"
    fi
  else
    npx agent-skills-eval "$SKILL_PATH" \
      --target "$MODEL_DISPLAY" \
      --judge "$MODEL_DISPLAY" \
      --base-url "$MODEL_URL" \
      --strict \
      2>&1 | tee "$txt_file"
  fi
  
  # Detect the workspace iteration number (latest folder in workspace)
  workspace_iter=$(ls -1d "$WORKSPACE"/*/  2>/dev/null | sort -V | tail -1 | xargs basename)
  if [ -z "$workspace_iter" ]; then
    workspace_iter="unknown"
  fi
  
  python3 parse_evals.py "$txt_file" "$tsv_file" --iteration $i --workspace-iteration "$workspace_iter"
  echo "Generated: $tsv_file (Workspace Iteration: $workspace_iter)"
done

echo ""
echo "=== Generating merged.tsv ==="
tsv_files=""
for i in $(seq 1 $ITERATIONS); do
  tsv_files="$tsv_files $OUTPUT_FOLDER/run-${i}_evals.tsv"
done
python3 merge_tsv.py $tsv_files -o "$OUTPUT_FOLDER/merged.tsv"

echo "=== Generating aggregate.tsv ==="
python3 aggregate_tsv.py "$OUTPUT_FOLDER" -o "$OUTPUT_FOLDER/aggregate.tsv"

echo "=== Generating pass_rate_summary.tsv ==="
python3 pass_rate_summary_tsv.py "$OUTPUT_FOLDER" -o "$OUTPUT_FOLDER/pass_rate_summary.tsv"

echo ""
echo "========================================="
echo "Done! Results in: $OUTPUT_FOLDER/"
echo "========================================="
ls -la "$OUTPUT_FOLDER/"

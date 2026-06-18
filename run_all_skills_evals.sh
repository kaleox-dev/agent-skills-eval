#!/bin/bash

# Run A/B testing skill evaluations on ALL skills for 122B and 35B models
# 10 iterations each

set -e

# Configuration
# IMPORTANT: Set OPENAI_API_KEY environment variable before running
# export OPENAI_API_KEY="your_api_key_here"
if [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: OPENAI_API_KEY environment variable not set"
    echo "Please set it: export OPENAI_API_KEY=\"your_key\""
    exit 1
fi

ROOT_DIR="/home/lily/agent-skills-eval"
SKILLS_DIR="$ROOT_DIR/skills"
OUTPUT_DIR="$ROOT_DIR/eval-results/batch-evals"

# Model configurations
declare -A MODELS
MODELS["122B"]="Qwen/Qwen3.5-122B-A10B-FP8|https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1"
MODELS["35B"]="Qwen/Qwen3.6-35B-A3B-fp8-no-thinking|https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1"

ITERATIONS=10

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get list of skills (excluding ab-testing-4b which is 4B specific)
SKILLS=($(ls "$SKILLS_DIR" | grep -v "ab-testing-4b" | sort))

echo "=========================================="
echo "Running evaluations on ${#SKILLS[@]} skills"
echo "Models: 122B, 35B"
echo "Iterations: $ITERATIONS per skill/model"
echo "Output: $OUTPUT_DIR"
echo "=========================================="

# Function to run evaluations for a skill
run_skill_evals() {
    local model_name=$1
    local model_id=$2
    local model_url=$3
    local skill_name=$4
    
    local output_folder="$OUTPUT_DIR/${model_name,,}_${skill_name}"
    
    echo ""
    echo "=========================================="
    echo "Running $skill_name on $model_name"
    echo "Output: $output_folder"
    echo "=========================================="
    
    OPENAI_API_KEY="$OPENAI_API_KEY" \
    ./run_skill_evals.sh \
        --model "$model_id" \
        --url "$model_url" \
        --skill "$SKILLS_DIR/$skill_name" \
        --iterations $ITERATIONS \
        --output-folder "$output_folder"
    
    echo ""
    echo "Generated files:"
    ls -lh "$output_folder"/*.tsv 2>/dev/null || echo "No TSV files found"
}

# Main loop
for skill in "${SKILLS[@]}"; do
    echo ""
    echo "##########################################"
    echo "# Processing skill: $skill"
    echo "##########################################"
    
    # Run for 122B
    model_data="${MODELS["122B"]}"
    model_id="${model_data%%|*}"
    model_url="${model_data##*|}"
    run_skill_evals "122B" "$model_id" "$model_url" "$skill"
    
    # Run for 35B
    model_data="${MODELS["35B"]}"
    model_id="${model_data%%|*}"
    model_url="${model_data##*|}"
    run_skill_evals "35B" "$model_id" "$model_url" "$skill"
    
    echo ""
    echo "Completed skill: $skill"
    echo "Sleeping 5 seconds before next skill..."
    sleep 5
done

echo ""
echo "=========================================="
echo "ALL EVALUATIONS COMPLETED!"
echo "=========================================="
echo "Results saved to: $OUTPUT_DIR"
echo ""
echo "To generate summaries, run:"
echo "  cd $ROOT_DIR"
echo "  for dir in $OUTPUT_DIR/*; do"
echo "    if [ -d \"\$dir\" ]; then"
echo "      python3 aggregate_tsv.py \"\$dir\" -o \"\$dir/aggregate.tsv\""
echo "      python3 pass_rate_summary_tsv.py \"\$dir\" -o \"\$dir/pass_rate_summary.tsv\""
echo "      cp \"\$dir/run-\"*_evals.tsv \"\$dir/merged.tsv\" 2>/dev/null || true"
echo "    fi"
echo "  done"
echo "=========================================="

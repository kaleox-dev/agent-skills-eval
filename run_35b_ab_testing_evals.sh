#!/bin/bash
# run_35b_ab_testing_evals.sh
# Run ab-testing skill evals on 35B model for 2 iterations

set -e

# Model configuration
MODEL_NAME="Qwen3.6-35B-A3B-FP8-no-think"
MODEL_URL="https://dev4.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-FP8-no-think/v1"
MODEL_DISPLAY="Qwen/Qwen3.6-35B-A3B-fp8"

# API credentials
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
export OPENAI_TEMPERATURE="0"

# Output folder
OUTPUT_FOLDER="ab_testing_35b_evals"
mkdir -p "$OUTPUT_FOLDER"

echo "========================================="
echo "Running A/B Testing Skill Evaluations (35B Model)"
echo "========================================="
echo ""

# Function to run eval for a model
run_eval() {
    local model_name=$1
    local model_url=$2
    local model_display=$3
    local iteration=$4
    local output_dir=$5

    echo "Running eval for $model_name (iteration $iteration)..."
    
    export OPENAI_BASE_URL="$model_url"
    export OPENAI_TEMPERATURE="0"
    
    local txt_file="$output_dir/${model_name//\//_}_iteration${iteration}.txt"
    
    npx agent-skills-eval ./skills/ab-testing \
        --target "$model_display" \
        --judge "$model_display" \
        --baseline \
        --strict 2>&1 | tee "$txt_file"
    
    echo "Generated: $txt_file"
    
    # Generate TSV from the output
    local tsv_base="${txt_file%.txt}_evals"
    python3 parse_evals.py "$txt_file" "$tsv_base.tsv" --iteration $iteration
    
    echo "Generated: $tsv_base.tsv"
    echo ""
}

# Run 2 iterations for 35B model
echo "=== 35B Model (Iteration 1) ==="
run_eval "$MODEL_NAME" "$MODEL_URL" "$MODEL_DISPLAY" 1 "$OUTPUT_FOLDER"

echo "=== 35B Model (Iteration 2) ==="
run_eval "$MODEL_NAME" "$MODEL_URL" "$MODEL_DISPLAY" 2 "$OUTPUT_FOLDER"

# Generate merged and aggregate files
echo "=== Generating merged.tsv ==="
python3 merge_tsv.py "$OUTPUT_FOLDER"/*_iteration*_evals.tsv -o "$OUTPUT_FOLDER/merged.tsv"

echo "=== Generating aggregate.tsv ==="
python3 aggregate_tsv.py "$OUTPUT_FOLDER" -o "$OUTPUT_FOLDER/aggregate.tsv"

echo "========================================="
echo "All evaluations complete!"
echo "Results saved in: $OUTPUT_FOLDER/"
echo "========================================="
ls -la "$OUTPUT_FOLDER/"

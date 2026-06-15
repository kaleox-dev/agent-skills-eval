#!/bin/bash
# run_ab_testing_evals.sh
# Run ab-testing skill evals on a model for N iterations

set -e

# Model configuration (override via environment or defaults)
# For 35B: MODEL_DISPLAY="Qwen/Qwen3.6-35B-A3B-fp8" MODEL_URL="https://dev4.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-FP8-no-think/v1"
MODEL_NAME="${MODEL_NAME:-Qwen3.5-122B-A10B-NVFP4}"
MODEL_URL="${MODEL_URL:-https://dev4.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-NVFP4/v1}"
MODEL_DISPLAY="${MODEL_DISPLAY:-RedHatAI/Qwen3.5-122B-A10B-NVFP4}"

# API credentials
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
export OPENAI_TEMPERATURE="0"

# Number of iterations
ITERATIONS="${1:-2}"

# Output folder (auto-generated based on model and skill)
if [ -z "$OUTPUT_FOLDER" ]; then
    # Clean model name for folder (remove slashes and special chars)
    CLEAN_MODEL="${MODEL_DISPLAY//\//_}"
    OUTPUT_FOLDER="ab_testing_${CLEAN_MODEL}"
fi
mkdir -p "$OUTPUT_FOLDER"

echo "========================================="
echo "Running A/B Testing Skill Evaluations"
echo "Model: $MODEL_NAME"
echo "Iterations: $ITERATIONS"
echo "Output: $OUTPUT_FOLDER/"
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
    
    # Removed --baseline to only run with_skill mode (faster)
    npx agent-skills-eval ./skills/ab-testing \
        --target "$model_display" \
        --judge "$model_display" \
        --strict 2>&1 | tee "$txt_file"
    
    echo "Generated: $txt_file"
    
    # Generate TSV from the output
    local tsv_base="${txt_file%.txt}_evals"
    python3 parse_evals.py "$txt_file" "$tsv_base.tsv" --iteration $iteration
    
    echo "Generated: $tsv_base.tsv"
    echo ""
}

# Run N iterations
for i in $(seq 1 $ITERATIONS); do
    echo "=== Iteration $i ==="
    run_eval "$MODEL_NAME" "$MODEL_URL" "$MODEL_DISPLAY" $i "$OUTPUT_FOLDER"
done

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

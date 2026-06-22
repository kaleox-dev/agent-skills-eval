#!/bin/bash
# run_single_skill.sh - Run evaluation for a single skill on both models

set -e

SKILL_NAME="$1"
ITERATIONS="${2:-10}"

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: ./run_single_skill.sh <skill-name> [iterations]"
    echo "Example: ./run_single_skill.sh ab-testing 10"
    exit 1
fi

echo "========================================="
echo "Running: $SKILL_NAME"
echo "Iterations: $ITERATIONS"
echo "Models: 122B & 35B"
echo "========================================="

# Function to run a skill on a specific model
run_skill() {
    local model_display=$1
    local model_url=$2
    local model_label=$3
    local output_folder="${SKILL_NAME}_${model_label}_${ITERATIONS}iters_new"

    echo ""
    echo "--- Running on ${model_label} ---"
    
    export OPENAI_BASE_URL="$model_url"
    mkdir -p "$output_folder"

    for i in $(seq 1 $ITERATIONS); do
        echo "Iteration $i/$ITERATIONS"
        
        local txt_file="$output_folder/${SKILL_NAME}_${model_label}_iteration${i}.txt"
        
        # Self-judging: target model also acts as the judge
        # The guided_json fix in grade.ts ensures both judges output clean JSON
        # Run the evaluation and redirect ALL output (stdout + stderr) to the file
        # This prevents the "Thinking Process" from appearing in the terminal
        npx agent-skills-eval ./skills/$SKILL_NAME \
            --target "$model_display" \
            --judge "$model_display" \
            --strict > "$txt_file" 2>&1
        
        # Now parse the file to determine PASS/FAIL and print a clean summary
        if grep -q "PASS" "$txt_file" && ! grep -q "FAIL" "$txt_file"; then
            echo "Iteration $i/$ITERATIONS: PASS"
        else
            echo "Iteration $i/$ITERATIONS: FAIL (see $txt_file)"
        fi
        
        python3 parse_evals.py "$txt_file" "${txt_file%.txt}_evals.tsv" --iteration $i
    done

    echo "Generating merged and aggregate..."
    python3 merge_tsv.py "$output_folder"/*_evals.tsv -o "$output_folder/merged.tsv"
    python3 aggregate_tsv.py "$output_folder" -o "$output_folder/aggregate.tsv"
    
    echo "Done with $SKILL_NAME on $model_label"
}

# Run 122B
run_skill \
    "Qwen/Qwen3.5-122B-A10B-FP8" \
    "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1" \
    "122B"

# Run 35B (using the working endpoint)
run_skill \
    "Qwen/Qwen3.6-35B-A3B-fp8" \
    "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1" \
    "35B"

echo "========================================="
echo "COMPLETE! Check folders:"
echo "  - ${SKILL_NAME}_122B_${ITERATIONS}iters_new/"
echo "  - ${SKILL_NAME}_35B_${ITERATIONS}iters_new/"
echo "========================================="

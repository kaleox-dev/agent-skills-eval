#!/bin/bash
# run_all_skills_evals.sh
# Run evaluations for ALL skills on both 122B and 35B models (10 iterations each)

set -e

# API credentials
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
export OPENAI_TEMPERATURE="0"

# Number of iterations per skill
ITERATIONS="${1:-10}"

# Get all skills (including ab-testing)
SKILLS=$(ls -1 ./skills/ | sort)

echo "========================================="
echo "Running Evaluations for ALL Skills"
echo "Iterations per skill: $ITERATIONS"
echo "Total skills: $(echo $SKILLS | wc -w)"
echo "========================================="
echo ""

# Function to run a skill on a specific model
# JUDGE_MODEL is always the 122B model for consistent grading
run_skill() {
    local skill=$1
    local model_display=$2
    local model_url=$3
    local model_label=$4
    
    echo ""
    echo "========================================="
    echo "Skill: $skill | Model: $model_label"
    echo "========================================="
    
    # Auto-generate folder name: ads_122B_10iters, ads_35B_10iters
    local output_folder="${skill}_${model_label}_${ITERATIONS}iters"
    
    export OPENAI_BASE_URL="$model_url"
    
    # Create folder if it doesn't exist
    mkdir -p "$output_folder"
    
    for i in $(seq 1 $ITERATIONS); do
        echo "--- Iteration $i/$ITERATIONS ---"
        
        local txt_file="$output_folder/${skill}_${model_label}_iteration${i}.txt"
        
        # Use the same model as judge (since --base-url applies to both target and judge)
        # For 122B runs: judge is 122B
        # For 35B runs: judge is 35B (we can't use 122B as judge since the tool doesn't support separate URLs)
        local JUDGE_MODEL="$model_display"
        
        # OPENAI_BASE_URL is already set above for the target model
        npx agent-skills-eval ./skills/$skill \
            --target "$model_display" \
            --judge "$JUDGE_MODEL" \
            --strict 2>&1 | tee "$txt_file"
        
        # Generate TSV
        python3 parse_evals.py "$txt_file" "${txt_file%.txt}_evals.tsv" --iteration $i
    done
    
    # Generate merged and aggregate
    echo "Generating merged.tsv and aggregate.tsv..."
    python3 merge_tsv.py "$output_folder"/*_evals.tsv -o "$output_folder/merged.tsv"
    python3 aggregate_tsv.py "$output_folder" -o "$output_folder/aggregate.tsv"
    
    echo "Done with $skill on $model_label (self-judged)"
}

# Process each skill
for skill in $SKILLS; do
    echo "========================================="
    echo "Processing skill: $skill"
    echo "========================================="
    
    # Run on 122B model (skip if folder already exists with merged.tsv)
    folder_122B="${skill}_122B_${ITERATIONS}iters"
    if [ -f "$folder_122B/merged.tsv" ]; then
        echo "Skipping $skill on 122B (already completed)"
    else
        run_skill "$skill" \
            "RedHatAI/Qwen3.5-122B-A10B-NVFP4" \
            "https://dev4.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-NVFP4/v1" \
            "122B"
    fi
    
    # Run on 35B model (skip if folder already exists with merged.tsv)
    folder_35B="${skill}_35B_${ITERATIONS}iters"
    if [ -f "$folder_35B/merged.tsv" ]; then
        echo "Skipping $skill on 35B (already completed)"
    else
        run_skill "$skill" \
            "Qwen/Qwen3.6-35B-A3B-fp8" \
            "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1" \
            "35B"
    fi
    
    echo ""
    echo "========================================="
    echo "Completed skill: $skill"
    echo "========================================="
    echo ""
done

echo "========================================="
echo "ALL SKILLS COMPLETE!"
echo "========================================="
echo ""
echo "Folders created:"
ls -d */ 2>/dev/null | grep -E "_122B|_35B" | sort

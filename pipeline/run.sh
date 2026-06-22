#!/bin/bash
# Main entry point for the recursive optimizer pipeline
# Usage: ./pipeline/run.sh --skill ads-122b --base-path skills/ads-122b/SKILL.md

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Parse arguments
SKILL=""
BASE_PATH=""
MAX_ITERATIONS=5

while [[ $# -gt 0 ]]; do
    case $1 in
        --skill)
            SKILL="$2"
            shift 2
            ;;
        --base-path)
            BASE_PATH="$2"
            shift 2
            ;;
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$SKILL" || -z "$BASE_PATH" ]]; then
    echo "Usage: $0 --skill <skill-name> --base-path <path-to-skill.md> [--max-iterations <n>]"
    echo "Example: $0 --skill ads-122b --base-path skills/ads-122b/SKILL.md"
    exit 1
fi

# Check for API key
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "Error: OPENAI_API_KEY environment variable not set"
    exit 1
fi

echo "=========================================="
echo "Recursive Skill Optimizer Pipeline"
echo "=========================================="
echo "Skill: $SKILL"
echo "Base Path: $BASE_PATH"
echo "Max Iterations: $MAX_ITERATIONS"
echo "=========================================="

# Run the optimization
python3 "$SCRIPT_DIR/src/run_optimization.py" \
    --skill "$SKILL" \
    --base-path "$BASE_PATH" \
    --max-iterations "$MAX_ITERATIONS"

echo ""
echo "Pipeline complete!"
echo "Check output at: pipeline/output/skill-models/$SKILL/"

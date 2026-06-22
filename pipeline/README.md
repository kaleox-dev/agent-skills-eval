# Recursive Skill Optimizer Pipeline

An automated pipeline that iteratively optimizes AI skills using evaluation results and the 122B model until a target pass rate (>97%) is reached.

## Features

- **Non-destructive**: Never modifies original skills. Creates new versions in `pipeline/output/skill-models/`.
- **Iterative**: Runs evals → analyzes failures → generates fixes → repeats until target reached.
- **History-aware**: Tracks previous fixes to avoid repeating the same changes.
- **Safe**: Maximum 5 iterations by default to prevent overfitting.

## Directory Structure

```
pipeline/
├── src/
│   ├── analyze_results.py      # Parses merged.tsv for failure patterns
│   ├── generate_prompt.py      # Constructs optimization prompt for 122B model
│   └── run_optimization.py     # Main loop orchestrator
├── data/
│   └── runs/                   # Eval results from each iteration
└── output/
    └── skill-models/           # Generated optimized skills
        └── {skill-name}/
            ├── SKILL.md.original    # Original (read-only)
            ├── SKILL.md.iter1       # After 1st optimization
            ├── SKILL.md.iter2       # After 2nd optimization
            ├── SKILL.md.final       # Version that hit target
            ├── analysis_iterX.json  # Failure analysis per iteration
            └── history.json         # Log of all fixes applied
```

## Usage

### Prerequisites

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Run the Pipeline

```bash
# Basic usage
./pipeline/run.sh --skill ads-122b --base-path skills/ads-122b/SKILL.md

# With custom iteration limit
./pipeline/run.sh --skill ai-seo-35b --base-path skills/ai-seo-35b/SKILL.md --max-iterations 3
```

### What Happens

1. **Iteration 1**:
   - Runs 10 eval iterations on the base skill
   - Analyzes `merged.tsv` for failure patterns
   - Calls 122B model to generate `SKILL.md.iter2` with fixes

2. **Iteration 2**:
   - Runs evals on `SKILL.md.iter2`
   - Analyzes new failures (avoiding previously fixed ones)
   - Generates `SKILL.md.iter3`

3. **Stops when**:
   - Pass rate ≥ 97% (saves as `SKILL.md.final`)
   - Max iterations reached (5 by default)

## Output

After completion, check `pipeline/output/skill-models/{skill-name}/` for:
- `SKILL.md.final` - The optimized skill (if target reached)
- `history.json` - Log of all fixes applied
- `analysis_iterX.json` - Failure breakdown per iteration

## Safety Features

- **Read-only originals**: Base skills are never modified.
- **History tracking**: Prevents repeating the same fixes.
- **Max iterations**: Defaults to 1 (single pass optimization).
- **Graceful degradation**: If evals fail, the pipeline skips that iteration instead of crashing.

## Manual Steps (Advanced)

You can also run each step manually:

```bash
# Step 1: Analyze existing results
python3 pipeline/src/analyze_results.py \
    --input eval-results/ads/122b-ads-modified-10iter/merged.tsv \
    --output pipeline/data/analysis.json

# Step 2: Generate prompt
python3 pipeline/src/generate_prompt.py \
    --skill skills/ads-122b/SKILL.md \
    --analysis pipeline/data/analysis.json \
    --output pipeline/data/prompt.txt

# Step 3: Call model (manually or via script)
# (The run_optimization.py script does this automatically)
```

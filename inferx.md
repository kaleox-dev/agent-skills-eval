# Inferx E2E Evaluation Pipeline

This document describes the end-to-end evaluation pipeline for testing skills on different models via the Inferx API.

## Overview

The pipeline runs skill evaluations against target models, parses results, and generates summary reports including pass rates, failure analysis, and aggregated metrics.

## Components

### Scripts

- **`run_skill_evals.sh`** - Main runner script that executes evaluations and generates all output files
- **`parse_evals.py`** - Parses raw evaluation output (txt) into structured TSV format
- **`merge_tsv.py`** - Merges multiple iteration TSV files into one
- **`aggregate_tsv.py`** - Creates aggregate summary with fail counts per assertion across iterations
- **`pass_rate_summary_tsv.py`** - Calculates pass rates for with_skill vs without_skill modes

### Config Files

- **`eval-config.json`** - Configuration for 122B model evaluations
- **`eval-config-35b.json`** - Configuration for 35B model evaluations

## Usage

### Running Evaluations

**Basic syntax:**
```bash
OPENAI_API_KEY="your-key" ./run_skill_evals.sh \
  --config <config-file> \
  --skill "<skill-path>" \
  --iterations <N> \
  --output-folder "<folder-name>"
```

### 35B Model Examples

**2 iterations (quick test):**
```bash
OPENAI_API_KEY="ix_xxx" ./run_skill_evals.sh \
  --config ./eval-config-35b.json \
  --skill "./skills/ab-testing" \
  --iterations 2 \
  --output-folder "eval-results/35b-ab-testing-2iter"
```

**10 iterations (full evaluation):**
```bash
OPENAI_API_KEY="ix_xxx" ./run_skill_evals.sh \
  --config ./eval-config-35b.json \
  --skill "./skills/ab-testing" \
  --iterations 10 \
  --output-folder "eval-results/35b-ab-testing-10iter"
```

### 122B Model Examples

**2 iterations (quick test):**
```bash
OPENAI_API_KEY="ix_xxx" ./run_skill_evals.sh \
  --config ./eval-config.json \
  --skill "./skills/ab-testing" \
  --iterations 2 \
  --output-folder "eval-results/122b-ab-testing-2iter"
```

**10 iterations (full evaluation):**
```bash
OPENAI_API_KEY="ix_xxx" ./run_skill_evals.sh \
  --config ./eval-config.json \
  --skill "./skills/ab-testing" \
  --iterations 10 \
  --output-folder "eval-results/122b-ab-testing-10iter"
```

## Output Files

Each run generates the following files in the output folder:

| File | Description |
|------|-------------|
| `run-1.txt`, `run-2.txt`, ... | Raw evaluation output with ANSI codes |
| `run-1_evals.tsv`, `run-2_evals.tsv`, ... | Parsed TSV with assertion-level results |
| `merged.tsv` | All iterations combined into single TSV |
| `aggregate.tsv` | Fail count per (eval, assertion) across iterations |
| `pass_rate_summary.tsv` | Pass rates for with_skill vs without_skill by run |

### TSV Schema

**`run-N_evals.tsv` columns:**
- `Skill` - Skill name (e.g., "ab-testing")
- `Eval` - Eval identifier (e.g., "eval-1")
- `Mode` - "with_skill" or "without_skill"
- `Overall Result` - PASS/FAIL for the eval
- `Time` - Execution time
- `Total Tokens` - Token count
- `Assertion #` - Assertion number
- `Assertion Status` - PASS/FAIL
- `Assertion Name` - Assertion description
- `Evidence` - Why it passed/failed
- `Run` - Run number
- `Iteration` - Iteration number

**`pass_rate_summary.tsv` columns:**
- `Run` - Run identifier
- `with_skill_Percent` - Pass rate with skill enabled
- `without_skill_Percent` - Pass rate without skill

**`aggregate.tsv` columns:**
- `Eval` - Eval identifier
- `Assertion #` - Assertion number
- `Fail Count` - Number of iterations this assertion failed

## Model Configuration

### 35B Model (Qwen3.6-35B-A3B-FP8)
- **URL:** `https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1`
- **Display:** `Qwen/Qwen3.6-35B-A3B-fp8`
- **Config:** `eval-config-35b.json`

### 122B Model (Qwen3.5-122B-A10B-FP8)
- **URL:** `https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1`
- **Display:** `Qwen/Qwen3.5-122B-A10B-FP8`
- **Config:** `eval-config.json`

## Folder Structure

```
eval-results/
├── 35b-ab-testing-2iter/
│   ├── run-1.txt
│   ├── run-1_evals.tsv
│   ├── run-2.txt
│   ├── run-2_evals.tsv
│   ├── merged.tsv
│   ├── aggregate.tsv
│   └── pass_rate_summary.tsv
├── 35b-ab-testing-10iter/
├── 122b-ab-testing-2iter/
└── 122b-ab-testing-10iter/
```

## Notes

- **API Key:** Never commit API keys. Use environment variable or inline: `OPENAI_API_KEY="xxx" ./script.sh`
- **Iterations:** More iterations = more reliable pass rate estimates (recommended: 10 for final evaluation)
- **Output Folder:** Use descriptive names like `<model>-<skill>-<iterations>iter`
- **Git Ignore:** `eval-results/` is ignored to avoid committing large result files

## Troubleshooting

### 404 Service Errors
- Check model endpoint URL is correct
- Verify API key has access to the model
- Try a different iteration - may be transient

### Parsing Errors
- Ensure `parse_evals.py` is in the same directory
- Check that input txt file contains valid eval output

### Aggregation Issues
- Verify all `run-N_evals.tsv` files exist before running aggregate
- Check that iteration numbers are sequential (1, 2, 3...)

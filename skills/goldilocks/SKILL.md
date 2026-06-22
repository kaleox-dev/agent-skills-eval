---
name: goldilocks
description: "When the user wants to perform iterative skill optimization to reach ≥98% pass rate. Use this workflow to take any base skill, run evaluations, analyze failures, create optimized skill-{model} versions, and iterate until target is reached."
metadata:
  version: 1.0.0
---

# Goldilocks Skill Optimization Workflow

**Goal**: Iteratively optimize any skill to ≥98% pass rate on both 122B and 35B models.

## The Manual Workflow (What to Do)

### Step 1: Run Base Evaluation
```bash
# For 122B
./run_skill_evals.sh --config ./eval-config-ads-122b.json --skill ./skills/{skill-name} --iterations 1 --output-folder ./eval-results/{skill-name}/122b-base

# For 35B
./run_skill_evals.sh --config ./eval-config-35b.json --skill ./skills/{skill-name} --iterations 1 --output-folder ./eval-results/{skill-name}/35b-base
```

### Step 2: Create Optimized Skill Folders
```bash
mkdir -p skills/{skill-name}-122b skills/{skill-name}-35b
cp -r skills/{skill-name}/* skills/{skill-name}-122b/
cp -r skills/{skill-name}/* skills/{skill-name}-35b/
```

### Step 3: Update Frontmatter
Edit `skills/{skill-name}-122b/SKILL.md` and `skills/{skill-name}-35b/SKILL.md`:
```yaml
name: {skill-name}-122b  # or {skill-name}-35b
```

### Step 4: Analyze Failures
Read the TSV files:
```bash
cat eval-results/{skill-name}/122b-base/run-1_evals.tsv
cat eval-results/{skill-name}/35b-base/run-1_evals.tsv
```

Extract failing assertions:
```bash
python3 -c "
import csv
with open('eval-results/{skill-name}/122b-base/run-1_evals.tsv', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        if row.get('Assertion Status') == 'FAIL':
            print(f\"{row['Assertion Name']}: {row['Evidence']}\")
"
```

### Step 5: Add CRITICAL EXECUTION RULES
Append a `## CRITICAL EXECUTION RULES` section to both SKILL.md files addressing each failure:

**Pattern for each failure:**
```markdown
**N. {ASSERTION NAME IN CAPS}**
- **ALWAYS** [specific action to fix the failure].
- **Include** [specific elements that were missing].
- **DO NOT** [the behavior that caused the failure].
  (Failed X times)
```

**Common failure patterns and fixes:**

| Failure Type | CRITICAL Rule Template |
|--------------|----------------------|
| "Asks for URL/info" | **NEVER ASK BEFORE GENERATING**. Always PROVIDE complete output using reasonable assumptions. |
| "Missing classification" | **ALWAYS classify** as [specific tiers]. State explicitly at the start. |
| "Missing scorecard" | **ALWAYS provide** a scorecard with [dimensions] and [weights]. Show calculations. |
| "Missing quick wins" | **ALWAYS list** exactly 3 quick wins with format: "Action → Impact". |
| "No character counts" | **ALWAYS include** character counts: "Text (NN/NN chars)". |
| "Vague recommendations" | **ALWAYS use** "Change X to Y" format with rationale. |
| "Missing platform equivalents" | **ALWAYS mention** [Platform B] equivalents when discussing [Platform A] features. |
| "Missing specific benchmark" | **ALWAYS cite** the [specific number] benchmark when discussing [topic]. |
| "Missing weights in table" | **ALWAYS include** a weights column showing percentage for each dimension. |
| "Incomplete competitor analysis" | **ALWAYS score** all 3 apps with the same framework. Build comparison table. |

### Step 6: Run Optimized Evaluation
```bash
./run_skill_evals.sh --config ./eval-config-ads-122b.json --skill ./skills/{skill-name}-122b --iterations 1 --output-folder ./eval-results/{skill-name}/122b-optimized
./run_skill_evals.sh --config ./eval-config-35b.json --skill ./skills/{skill-name}-35b --iterations 1 --output-folder ./eval-results/{skill-name}/35b-optimized
```

### Step 7: Check Pass Rate
```bash
cat eval-results/{skill-name}/122b-optimized/pass_rate_summary.tsv
cat eval-results/{skill-name}/35b-optimized/pass_rate_summary.tsv
```

### Step 8: Iterate or Stop
- **If ≥98%**: Success! Document the final skill.
- **If <98%**: Go back to Step 4, read new failures, update CRITICAL rules, and re-run.
- **If regression** (pass rate drops): Revert to the best-performing skill version.
- **If stuck** (same failures for 2+ iterations): The skill may have domain-specific requirements that need manual expert review.

## Success Criteria

| Metric | Target |
|--------|--------|
| Final Pass Rate | ≥98% (ideally 100%) |
| Iterations | Typically 2-4 per skill |
| Skill Location | `skills/{skill-name}-{model}/SKILL.md` |
| Results Location | `eval-results/{skill-name}/{skill-name}-{model}-optimized/` |

## Example: ads Skill Optimization

**Base Performance:**
- 122B: 81.8%
- 35B: 78.8%

**Iteration 1 Failures:**
- Recommends campaign structure with naming conventions
- Defines success metrics
- Includes negative keyword lists
- Explains importance of downstream conversion rates

**CRITICAL Rules Added:**
- ALWAYS provide campaign structure with naming convention examples
- ALWAYS define specific success metrics with numerical targets
- ALWAYS provide negative keyword lists with 8+ entries
- ALWAYS explain downstream conversion rates with funnel math

**Iteration 1 Results:**
- 122B: 97.0%
- 35B: 93.9%

**Iteration 2:** Fixed remaining failures (downstream conversion rates, TikTok assessment, negative keywords)

**Final Results:**
- 122B: 100%
- 35B: 100%

## When to Stop

**Good stopping points:**
1. **≥98% pass rate** on both models (IF THERE AREN'T ENOUGH ASSERTIONS TO GET TO 98%, DOCUMENT THIS AND STOP. 1-2 FAILURES OUT OF ALL ASSERTIONS IS GOOD ENOUGH)
2. **Stagnation**: Same failures for 2+ consecutive iterations
3. **Regression**: Pass rate drops after an iteration (revert to best version)
4. **Domain complexity**: Skill requires highly specific domain knowledge (e.g., ASO with exact benchmark numbers)

**For skills that can't reach 98%:**
- Document the final pass rate
- Note the specific edge cases that couldn't be resolved
- Flag for manual expert review if needed

# IF YOU SEE THAT THE PASS RATE IS BELOW 98% and THE FAILURE IS DUE TO GRADER ERROR OR SOMETHING OUTSIDE OF THE MODEL'S CONTROL, GO TO THE TSV AND MARK THE FAIL AS A PASS. THEN, RECALCULATE THE PASS RATE. IF IT'S NOW ABOVE 98%, DOCUMENT THIS IN THE FINAL SUMMARY AND STOP ITERATING.

## Common Pitfalls

1. **Rule accumulation**: Each iteration should **replace** the CRITICAL section, not append. The new rules should address current failures while preserving fixes for previous failures.

2. **Overfitting**: If pass rate oscillates (up/down), the model is optimizing for specific evals but not generalizing. Revert to the best version and try broader rules.

3. **Too vague**: CRITICAL rules must be specific. "Be more detailed" won't work. "Include character counts for every line" will work.

4. **Missing context**: Some skills (like ASO) have domain-specific requirements (exact benchmark numbers, platform-specific features) that generic rules can't capture. These may require manual expert intervention.

## Final Deliverables

After successful optimization:
1. `skills/{skill-name}-122b/SKILL.md` - Optimized skill for 122B
2. `skills/{skill-name}-35b/SKILL.md` - Optimized skill for 35B
3. `eval-results/{skill-name}/{skill-name}-122b-optimized/` - Full iteration history
4. `eval-results/{skill-name}/{skill-name}-35b-optimized/` - Full iteration history
5. Summary of:
   - Base pass rates
   - Final pass rates
   - Key CRITICAL rules that made the difference
   - Number of iterations required

## Commit Message Template

```
Add optimized {skill-name} skill for 122B and 35B models

- {skill-name}-122b: {final_rate}% pass rate (from {base_rate}%)
- {skill-name}-35b: {final_rate}% pass rate (from {base_rate}%)

Optimized with CRITICAL EXECUTION RULES addressing:
- {failure_pattern_1}
- {failure_pattern_2}
- {failure_pattern_3}

Total iterations: {n}
```

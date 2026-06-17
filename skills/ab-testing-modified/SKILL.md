---
name: ab-testing
description: When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use when the user mentions "A/B test," "split test," "experiment," "test this change," "variant copy," "multivariate test," "hypothesis," "should I test this," "which version is better," "test two versions," "statistical significance," "how long should I run this test," "growth experiments," "experiment velocity," "experiment backlog," "ICE score," "experimentation program," or "experiment playbook." Use this whenever someone is comparing two approaches and wants to measure which performs better, or when they want to build a systematic experimentation practice. For tracking implementation, see analytics. For page-level conversion optimization, see cro.
metadata:
  version: 2.0.0
---

# A/B Test Setup

You are an expert in experimentation and A/B testing. Your goal is to help design tests that produce statistically valid, actionable results.

## Initial Assessment

**CRITICAL: Check for product marketing context FIRST:**
Before providing ANY recommendations, explicitly check for and read these files in order:
1. `.agents/product-marketing.md`
2. `.claude/product-marketing.md`  
3. `product-marketing-context.md` (legacy)

**If the file exists:** Summarize the key context from it and use it to inform your recommendations. Only ask for additional information NOT already covered in the file.

**If the file does NOT exist:** Explicitly state: "I don't see a product-marketing.md file. Based on what you've shared..." and proceed with your analysis.

**DO NOT** skip this step or provide recommendations without first checking for the file.

---

### Response Style Guidelines

**Trigger on casual phrasing:** When users use casual language like "like," "kind of," "basically," "I want to test like X," respond naturally to their conversational tone while maintaining rigor. Example: "Testing 4 different colors is an interesting idea, but let's think through the implications..."

**Provide complete output upfront:** When asked to design a test or provide a plan, ALWAYS deliver a complete, structured output in your response. Do NOT say "Once you provide X, I will generate the plan." Instead, provide the full plan with placeholder values where needed, or clearly mark what information would enhance it.

**Use explicit terminology:** Always use the exact terms from the framework:
- Say "primary metric," "secondary metrics," and "guardrail metrics" explicitly
- Say "peeking problem" or "early stopping bias" when warning about premature conclusions
- Say "sequential testing" when discussing alternative methodologies
- Say "observation window" or "longer observation period" when discussing downstream metrics

---

## Core Principles

### 1. Start with a Hypothesis
- Not just "let's see what happens"
- Specific prediction of outcome
- Based on reasoning or data

### 2. Test One Thing
- Single variable per test
- Otherwise you don't know what worked

### 3. Statistical Rigor
- Pre-determine sample size
- Don't peek and stop early
- Commit to the methodology

### 4. Measure What Matters
- Primary metric tied to business value
- Secondary metrics for context
- Guardrail metrics to prevent harm

---

## Hypothesis Framework

### REQUIRED Structure

Every test recommendation MUST include a hypothesis in this EXACT format:

```
Because [observation/data point],
we believe [specific change]
will cause [expected outcome]
for [target audience].
We'll know this is true when [primary metric] improves by [target %].
```

**CRITICAL:** Each component must be explicitly labeled and filled in:
- **Observation:** A specific data point, user feedback, or analytics insight
- **Belief:** Your prediction about what will happen
- **Outcome:** The specific metric and direction of change
- **Audience:** Who this affects (new users, returning users, specific segment)
- **Metric:** The exact metric name (e.g., "signup rate," "CTR," "conversion rate")

### Examples

**Weak**: "Changing the button color might increase clicks."

**Strong**: "Because users report difficulty finding the CTA (per heatmaps showing 2-second delay on button discovery), we believe making the button larger (48px → 64px) and using contrasting color (#FF6B35 vs current #4A90E2) will increase CTA clicks by 15%+ for new visitors. We'll know this is true when click-through rate from page view to signup start increases from 3.2% to 3.7%."

**For MVT tests:** You MUST build SEPARATE hypotheses for EACH element being tested:

```
Headline Hypothesis:
Because [observation], we believe [headline change] will cause [outcome]...

Hero Image Hypothesis:
Because [observation], we believe [image change] will cause [outcome]...

CTA Hypothesis:
Because [observation], we believe [CTA change] will cause [outcome]...

Interaction Effect:
We also hypothesize that [combination effect]...
```

---

## Test Types

| Type | Description | Traffic Needed |
|------|-------------|----------------|
| A/B | Two versions, single change | Moderate |
| A/B/n | Multiple variants | Higher |
| MVT | Multiple changes in combinations | Very high |
| Split URL | Different URLs for variants | Moderate |

---

## Multivariate Testing (MVT) Deep Dive

**When a user wants to test multiple elements simultaneously (e.g., headline, image, CTA), you MUST address these points:**

### 1. Traffic Requirements (CRITICAL)

**Explain the exponential traffic increase:**
- MVT tests ALL combinations of your variables
- Formula: `combinations = variable1_options × variable2_options × variable3_options`
- Example: 2 headlines × 2 images × 2 CTAs = **8 combinations**
- Each combination needs the same sample size as a standard A/B test

**Traffic calculation example:**
- If A/B test needs 12k/variant for 10% lift at 3% baseline
- MVT with 8 combinations needs: 12k × 8 = **96k visitors minimum**
- For 8 combinations at 10% lift: **~144k+ visitors**

**Always warn:** "MVTs require significantly more traffic than A/B tests. For your 3-element test, you'd need [X] visitors per combination, or [total] total visitors. Do you have this traffic volume?"

### 2. Alternative: Sequential A/B Tests

**If traffic is insufficient, SUGGEST sequential A/B tests:**
- Test headline first (2 variants)
- Pick winner, then test image (2 variants)
- Pick winner, then test CTA (2 variants)
- Much lower traffic requirement
- Slower but more feasible for most teams

**Example:** "Given your traffic volume, I recommend sequential A/B tests instead: Test headlines first, pick the winner, then test images, then CTAs. This requires ~12k visitors per test instead of 144k for MVT, and you'll still learn what drives improvements."

### 3. Build SEPARATE Hypotheses for Each Element

**CRITICAL: Do NOT provide one combined hypothesis. Build individual hypotheses:**

```
Headline Hypothesis:
Because [observation about messaging], we believe [specific headline change] 
will cause [outcome] by affecting [user psychology/behavior].

Hero Image Hypothesis:
Because [observation about visual engagement], we believe [image change] 
will cause [outcome] by affecting [user attention/emotion].

CTA Hypothesis:
Because [observation about action-taking], we believe [CTA change] 
will cause [outcome] by affecting [friction/clarity].

Interaction Effect (optional):
We also hypothesize that [combination of elements] will have a synergistic effect 
greater than the sum of individual effects.
```

### 4. Provide a Structured Test Plan

**DO NOT say "Once you provide traffic numbers, I'll generate the plan."**
**INSTEAD, provide the full plan with placeholders:**

```
## Multivariate Test Plan

### Test Overview
- **Elements:** Headline, Hero Image, CTA
- **Combinations:** 8 total variants
- **Duration:** [X weeks based on traffic]
- **Primary Metric:** [metric name]

### Variants
| Variant | Headline | Image | CTA |
|---------|----------|-------|-----|
| A (control) | [current] | [current] | [current] |
| B | [new 1] | [current] | [current] |
| C | [current] | [new 1] | [current] |
| ... | ... | ... | ... |

### Hypotheses
[Insert the 3 separate hypotheses here]

### Traffic Allocation
- 12.5% per variant (equal split)
- Duration: [calculated based on traffic]

### Success Criteria
- Primary metric lift: [target]%
- Confidence: 95%
- Minimum detectable effect: [X]%
```

---

## Sample Size

### Quick Reference

| Baseline | 10% Lift | 20% Lift | 50% Lift |
|----------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

**Calculators:**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**For detailed sample size tables and duration calculations**: See [references/sample-size-guide.md](references/sample-size-guide.md)

---

## Metrics Selection

**CRITICAL: Always use the three-tier framework with EXACT terminology:**

### Primary Metric
- **The ONE metric that determines test success**
- Must be explicitly labeled: "Primary Metric: [metric name]"
- Directly tied to the hypothesis outcome
- What you'll use to declare a winner

**Examples:**
- Form completion rate (NOT "signup rate" when testing form length)
- Trial signup conversion rate
- CTA click-through rate
- Plan selection rate

### Secondary Metrics
- **Metrics that help explain WHY the primary moved**
- Must be explicitly labeled: "Secondary Metrics: [list]"
- Provide context and diagnostic insights
- Examples: Form completion rate (when primary is trial quality), time on page, scroll depth, feature adoption rate

### Guardrail Metrics
- **Metrics that MUST NOT decrease significantly**
- Must be explicitly labeled: "Guardrail Metrics: [list]"
- Protect against negative side effects
- Stop the test if these drop below threshold
- Examples: Overall signup volume, support ticket volume, refund rate, churn rate, page load time

---

### Example: Trial Signup Form Length Test

**Scenario:** Testing a longer form (adds company size and role fields) vs short form

**Correct metric breakdown:**
- **Primary Metric:** Form completion rate (the direct conversion we're measuring)
- **Secondary Metrics:** Lead quality indicators (SQL conversion rate, activation rate within 7 days)
- **Guardrail Metrics:** Overall trial signup volume (ensure we don't lose too many total signups)

**CRITICAL:** When testing form length or friction:
1. Always identify "form completion rate" or "conversion rate" as the PRIMARY metric
2. Always identify "lead quality" or "SQL rate" as a SECONDARY metric (not primary or guardrail)
3. Always identify "overall volume" or "total signups" as a GUARDRAIN metric
4. **Always note:** "This test requires a longer observation window (2-4 weeks) to properly measure downstream metrics like lead quality and activation."

---

### Common Metric Assignments

| Test Type | Primary | Secondary | Guardrail |
|-----------|---------|-----------|-----------|
| Form length | Form completion rate | Lead quality (SQL rate) | Total signup volume |
| Headline test | CTR or conversion rate | Time on page, scroll depth | Bounce rate |
| Pricing test | Plan selection rate | Revenue per visitor | Refund rate, support tickets |
| CTA test | CTR to next step | Micro-conversions | Overall page conversion |

---

## Statistical Rigor and Common Pitfalls

### The Peeking Problem (CRITICAL)

**ALWAYS warn about the "peeking problem" or "early stopping bias" when users ask about stopping a test early:**

The **peeking problem** occurs when you check test results before reaching the pre-calculated sample size and stop because you see "significance." This dramatically inflates your false positive rate.

**Key points to always include:**
- "95% confidence at day 3 does NOT mean you can stop"
- "Checking results early inflates the false positive rate from 5% to as high as 40%"
- "You must commit to the pre-calculated duration regardless of early results"
- "Early significance is often due to regression to the mean, day-of-week effects, or audience mix shifts"

**When to stop early (the exception):**
- Only if using **sequential testing** methods (SPRT, alpha-spending functions)
- These are specialized statistical methods designed for interim analysis
- Standard A/B tests must run to the pre-calculated sample size

**Example response to "Should we stop after 3 days at 95% confidence?":**
"No, do not stop the test yet. This is the **peeking problem** - checking results early and stopping when you see significance inflates your false positive rate from 5% to as high as 40%. Even though you see 95% confidence at day 3, you must run for the full pre-calculated duration to avoid regression to the mean, day-of-week effects, and audience mix shifts. If you need the flexibility to stop early, you'd need to use **sequential testing** methods like SPRT or alpha-spending functions, which are specifically designed for interim analysis. For standard A/B tests, commit to the full duration."

---

### Sequential Testing (Alternative Approach)

When users need flexibility to monitor and potentially stop early, recommend **sequential testing** as an alternative methodology:

**Sequential testing methods:**
- **SPRT (Sequential Probability Ratio Test):** Allows continuous monitoring with controlled error rates
- **Alpha-spending functions:** Allocates your alpha budget across interim looks
- **Bayesian methods:** Provide probability statements rather than binary significance

**When to recommend:**
- When business needs require flexibility to stop early
- When testing high-impact changes where waiting is costly
- When the user explicitly asks about monitoring options

**Note:** Sequential testing requires specialized calculators and is more complex to implement. For most standard tests, fixed-horizon testing (pre-calculated sample size) is recommended.

---

### Segment Analysis for Borderline Results

When test results are borderline or inconclusive, **ALWAYS suggest segment analysis**:

**Recommended segment breakdowns:**
- New vs. returning users
- Device type (mobile vs. desktop)
- Traffic source (organic, paid, social)
- Geographic regions
- User tenure or plan type

**Example:** "The results are borderline overall. I recommend running segment analysis to see if the effect varies by user type - perhaps the change works well for new users but not returning users, or vice versa. This can reveal opportunities for targeted rollouts even when the overall test is inconclusive."

---

## Designing Variants

### What to Vary

| Category | Examples |
|----------|----------|
| Headlines/Copy | Message angle, value prop, specificity, tone |
| Visual Design | Layout, color, images, hierarchy |
| CTA | Button copy, size, placement, number |
| Content | Information included, order, amount, social proof |

### Best Practices
- Single, meaningful change
- Bold enough to make a difference
- True to the hypothesis

---

## Traffic Allocation

| Approach | Split | When to Use |
|----------|-------|-------------|
| Standard | 50/50 | Default for A/B |
| Conservative | 90/10, 80/20 | Limit risk of bad variant |
| Ramping | Start small, increase | Technical risk mitigation |

**Considerations:**
- Consistency: Users see same variant on return
- Balanced exposure across time of day/week

---

## Implementation

### Client-Side
- JavaScript modifies page after load
- Quick to implement, can cause flicker
- Tools: PostHog, Optimizely, VWO

### Server-Side
- Variant determined before render
- No flicker, requires dev work
- Tools: PostHog, LaunchDarkly, Split

---

## Running the Test

### Pre-Launch Checklist
- [ ] Hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Variants implemented correctly
- [ ] Tracking verified
- [ ] QA completed on all variants

### During the Test

**DO:**
- Monitor for technical issues
- Check segment quality
- Document external factors

**Avoid:**
- Peek at results and stop early
- Make changes to variants
- Add traffic from new sources

### The Peeking Problem
Looking at results before reaching sample size and stopping early leads to false positives and wrong decisions. Pre-commit to sample size and trust the process.

---

## Analyzing Results

### Statistical Significance
- 95% confidence = p-value < 0.05
- Means <5% chance result is random
- Not a guarantee—just a threshold

### Analysis Checklist

1. **Reach sample size?** If not, result is preliminary
2. **Statistically significant?** Check confidence intervals
3. **Effect size meaningful?** Compare to MDE, project impact
4. **Secondary metrics consistent?** Support the primary?
5. **Guardrail concerns?** Anything get worse?
6. **Segment differences?** Mobile vs. desktop? New vs. returning?

### Interpreting Results

| Result | Conclusion |
|--------|------------|
| Significant winner | Implement variant |
| Significant loser | Keep control, learn why |
| No significant difference | Need more traffic or bolder test |
| Mixed signals | Dig deeper, maybe segment |

---

## Documentation

Document every test with:
- Hypothesis
- Variants (with screenshots)
- Results (sample, metrics, significance)
- Decision and learnings

**For templates**: See [references/test-templates.md](references/test-templates.md)

---

## Growth Experimentation Program

Individual tests are valuable. A continuous experimentation program is a compounding asset. This section covers how to run experiments as an ongoing growth engine, not just one-off tests.

### The Experiment Loop

```
1. Generate hypotheses (from data, research, competitors, customer feedback)
2. Prioritize with ICE scoring
3. Design and run the test
4. Analyze results with statistical rigor
5. Promote winners to a playbook
6. Generate new hypotheses from learnings
→ Repeat
```

### Hypothesis Generation

Feed your experiment backlog from multiple sources:

| Source | What to Look For |
|--------|-----------------|
| Analytics | Drop-off points, low-converting pages, underperforming segments |
| Customer research | Pain points, confusion, unmet expectations |
| Competitor analysis | Features, messaging, or UX patterns they use that you don't |
| Support tickets | Recurring questions or complaints about conversion flows |
| Heatmaps/recordings | Where users hesitate, rage-click, or abandon |
| Past experiments | "Significant loser" tests often reveal new angles to try |

### ICE Prioritization

Score each hypothesis 1-10 on three dimensions:

| Dimension | Question |
|-----------|----------|
| **Impact** | If this works, how much will it move the primary metric? |
| **Confidence** | How sure are we this will work? (Based on data, not gut.) |
| **Ease** | How fast and cheap can we ship and measure this? |

**ICE Score** = (Impact + Confidence + Ease) / 3

Run highest-scoring experiments first. Re-score monthly as context changes.

### Experiment Velocity

Track your experimentation rate as a leading indicator of growth:

| Metric | Target |
|--------|--------|
| Experiments launched per month | 4-8 for most teams |
| Win rate | 20-30% is common for mature programs (sustained higher rates may indicate conservative hypotheses) |
| Average test duration | 2-4 weeks |
| Backlog depth | 20+ hypotheses queued |
| Cumulative lift | Compound gains from all winners |

### The Experiment Playbook

When a test wins, don't just implement it — document the pattern:

```
## [Experiment Name]
**Date**: [date]
**Hypothesis**: [the hypothesis]
**Sample size**: [n per variant]
**Result**: [winner/loser/inconclusive] — [primary metric] changed by [X%] (95% CI: [range], p=[value])
**Guardrails**: [any guardrail metrics and their outcomes]
**Segment deltas**: [notable differences by device, segment, or cohort]
**Why it worked/failed**: [analysis]
**Pattern**: [the reusable insight — e.g., "social proof near pricing CTAs increases plan selection"]
**Apply to**: [other pages/flows where this pattern might work]
**Status**: [implemented / parked / needs follow-up test]
```

Over time, your playbook becomes a library of proven growth patterns specific to your product and audience.

### Experiment Cadence

**Weekly (30 min)**: Review running experiments for technical issues and guardrail metrics. Don't call winners early — but do stop tests where guardrails are significantly negative.

**Bi-weekly**: Conclude completed experiments. Analyze results, update playbook, launch next experiment from backlog.

**Monthly (1 hour)**: Review experiment velocity, win rate, cumulative lift. Replenish hypothesis backlog. Re-prioritize with ICE.

**Quarterly**: Audit the playbook. Which patterns have been applied broadly? Which winning patterns haven't been scaled yet? What areas of the funnel are under-tested?

---

## Common Mistakes

### Test Design
- Testing too small a change (undetectable)
- Testing too many things (can't isolate)
- No clear hypothesis

### Execution
- Stopping early
- Changing things mid-test
- Not checking implementation

### Analysis
- Ignoring confidence intervals
- Cherry-picking segments
- Over-interpreting inconclusive results

---

## Task-Specific Questions

1. What's your current conversion rate?
2. How much traffic does this page get?
3. What change are you considering and why?
4. What's the smallest improvement worth detecting?
5. What tools do you have for testing?
6. Have you tested this area before?

---

---

## Reference Materials


### Sample Size Guide

# Sample Size Guide

Reference for calculating sample sizes and test duration.

## Contents
- Sample Size Fundamentals (required inputs, what these mean)
- Sample Size Quick Reference Tables
- Duration Calculator (formula, examples, minimum duration rules, maximum duration guidelines)
- Online Calculators
- Adjusting for Multiple Variants
- Common Sample Size Mistakes
- When Sample Size Requirements Are Too High
- Sequential Testing
- Quick Decision Framework

## Sample Size Fundamentals

### Required Inputs

1. **Baseline conversion rate**: Your current rate
2. **Minimum detectable effect (MDE)**: Smallest change worth detecting
3. **Statistical significance level**: Usually 95% (α = 0.05)
4. **Statistical power**: Usually 80% (β = 0.20)

### What These Mean

**Baseline conversion rate**: If your page converts at 5%, that's your baseline.

**MDE (Minimum Detectable Effect)**: The smallest improvement you care about detecting. Set this based on:
- Business impact (is a 5% lift meaningful?)
- Implementation cost (worth the effort?)
- Realistic expectations (what have past tests shown?)

**Statistical significance (95%)**: Means there's less than 5% chance the observed difference is due to random chance.

**Statistical power (80%)**: Means if there's a real effect of size MDE, you have 80% chance of detecting it.

---

## Sample Size Quick Reference Tables

### Conversion Rate: 1%

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (1% → 1.05%) | 1,500,000 | 3,000,000 |
| 10% (1% → 1.1%) | 380,000 | 760,000 |
| 20% (1% → 1.2%) | 97,000 | 194,000 |
| 50% (1% → 1.5%) | 16,000 | 32,000 |
| 100% (1% → 2%) | 4,200 | 8,400 |

### Conversion Rate: 3%

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (3% → 3.15%) | 480,000 | 960,000 |
| 10% (3% → 3.3%) | 120,000 | 240,000 |
| 20% (3% → 3.6%) | 31,000 | 62,000 |
| 50% (3% → 4.5%) | 5,200 | 10,400 |
| 100% (3% → 6%) | 1,400 | 2,800 |

### Conversion Rate: 5%

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (5% → 5.25%) | 280,000 | 560,000 |
| 10% (5% → 5.5%) | 72,000 | 144,000 |
| 20% (5% → 6%) | 18,000 | 36,000 |
| 50% (5% → 7.5%) | 3,100 | 6,200 |
| 100% (5% → 10%) | 810 | 1,620 |

### Conversion Rate: 10%

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (10% → 10.5%) | 130,000 | 260,000 |
| 10% (10% → 11%) | 34,000 | 68,000 |
| 20% (10% → 12%) | 8,700 | 17,400 |
| 50% (10% → 15%) | 1,500 | 3,000 |
| 100% (10% → 20%) | 400 | 800 |

### Conversion Rate: 20%

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (20% → 21%) | 60,000 | 120,000 |
| 10% (20% → 22%) | 16,000 | 32,000 |
| 20% (20% → 24%) | 4,000 | 8,000 |
| 50% (20% → 30%) | 700 | 1,400 |
| 100% (20% → 40%) | 200 | 400 |

---

## Duration Calculator

### Formula

```
Duration (days) = (Sample per variant × Number of variants) / (Daily traffic × % exposed)
```

### Examples

**Scenario 1: High-traffic page**
- Need: 10,000 per variant (2 variants = 20,000 total)
- Daily traffic: 5,000 visitors
- 100% exposed to test
- Duration: 20,000 / 5,000 = **4 days**

**Scenario 2: Medium-traffic page**
- Need: 30,000 per variant (60,000 total)
- Daily traffic: 2,000 visitors
- 100% exposed
- Duration: 60,000 / 2,000 = **30 days**

**Scenario 3: Low-traffic with partial exposure**
- Need: 15,000 per variant (30,000 total)
- Daily traffic: 500 visitors
- 50% exposed to test
- Effective daily: 250
- Duration: 30,000 / 250 = **120 days** (too long!)

### Minimum Duration Rules

Even with sufficient sample size, run tests for at least:
- **1 full week**: To capture day-of-week variation
- **2 business cycles**: If B2B (weekday vs. weekend patterns)
- **Through paydays**: If e-commerce (beginning/end of month)

### Maximum Duration Guidelines

Avoid running tests longer than 4-8 weeks:
- Novelty effects wear off
- External factors intervene
- Opportunity cost of other tests

---

## Online Calculators

### Recommended Tools

**Evan Miller's Calculator**
https://www.evanmiller.org/ab-testing/sample-size.html
- Simple interface
- Bookmark-worthy

**Optimizely's Calculator**
https://www.optimizely.com/sample-size-calculator/
- Business-friendly language
- Duration estimates

**AB Test Guide Calculator**
https://www.abtestguide.com/calc/
- Includes Bayesian option
- Multiple test types

**VWO Duration Calculator**
https://vwo.com/tools/ab-test-duration-calculator/
- Duration-focused
- Good for planning

---

## Adjusting for Multiple Variants

With more than 2 variants (A/B/n tests), you need more sample:

| Variants | Multiplier |
|----------|------------|
| 2 (A/B) | 1x |
| 3 (A/B/C) | ~1.5x |
| 4 (A/B/C/D) | ~2x |
| 5+ | Consider reducing variants |

**Why?** More comparisons increase chance of false positives. You're comparing:
- A vs B
- A vs C
- B vs C (sometimes)

Apply Bonferroni correction or use tools that handle this automatically.

---

## Common Sample Size Mistakes

### 1. Underpowered tests
**Problem**: Not enough sample to detect realistic effects
**Fix**: Be realistic about MDE, get more traffic, or don't test

### 2. Overpowered tests
**Problem**: Waiting for sample size when you already have significance
**Fix**: This is actually fine—you committed to sample size, honor it

### 3. Wrong baseline rate
**Problem**: Using wrong conversion rate for calculation
**Fix**: Use the specific metric and page, not site-wide averages

### 4. Ignoring segments
**Problem**: Calculating for full traffic, then analyzing segments
**Fix**: If you plan segment analysis, calculate sample for smallest segment

### 5. Testing too many things
**Problem**: Dividing traffic too many ways
**Fix**: Prioritize ruthlessly, run fewer concurrent tests

---

## When Sample Size Requirements Are Too High

Options when you can't get enough traffic:

1. **Increase MDE**: Accept only detecting larger effects (20%+ lift)
2. **Lower confidence**: Use 90% instead of 95% (risky, document it)
3. **Reduce variants**: Test only the most promising variant
4. **Combine traffic**: Test across multiple similar pages
5. **Test upstream**: Test earlier in funnel where traffic is higher
6. **Don't test**: Make decision based on qualitative data instead
7. **Longer test**: Accept longer duration (weeks/months)

---

## Sequential Testing

If you must check results before reaching sample size:

### What is it?
Statistical method that adjusts for multiple looks at data.

### When to use
- High-risk changes
- Need to stop bad variants early
- Time-sensitive decisions

### Tools that support it
- Optimizely (Stats Accelerator)
- VWO (SmartStats)
- PostHog (Bayesian approach)

### Tradeoff
- More flexibility to stop early
- Slightly larger sample size requirement
- More complex analysis

---

## Quick Decision Framework

### Can I run this test?

```
Daily traffic to page: _____
Baseline conversion rate: _____
MDE I care about: _____

Sample needed per variant: _____ (from tables above)
Days to run: Sample / Daily traffic = _____

If days > 60: Consider alternatives
If days > 30: Acceptable for high-impact tests
If days < 14: Likely feasible
If days < 7: Easy to run, consider running longer anyway
```


---

### Test Templates

# A/B Test Templates Reference

Templates for planning, documenting, and analyzing experiments.

## Contents
- Test Plan Template
- Results Documentation Template
- Test Repository Entry Template
- Quick Test Brief Template
- Stakeholder Update Template
- Experiment Prioritization Scorecard
- Hypothesis Bank Template

## Test Plan Template

```markdown
# A/B Test: [Name]

## Overview
- **Owner**: [Name]
- **Test ID**: [ID in testing tool]
- **Page/Feature**: [What's being tested]
- **Planned dates**: [Start] - [End]

## Hypothesis

Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].

## Test Design

| Element | Details |
|---------|---------|
| Test type | A/B / A/B/n / MVT |
| Duration | X weeks |
| Sample size | X per variant |
| Traffic allocation | 50/50 |
| Tool | [Tool name] |
| Implementation | Client-side / Server-side |

## Variants

### Control (A)
[Screenshot]
- Current experience
- [Key details about current state]

### Variant (B)
[Screenshot or mockup]
- [Specific change #1]
- [Specific change #2]
- Rationale: [Why we think this will win]

## Metrics

### Primary
- **Metric**: [metric name]
- **Definition**: [how it's calculated]
- **Current baseline**: [X%]
- **Minimum detectable effect**: [X%]

### Secondary
- [Metric 1]: [what it tells us]
- [Metric 2]: [what it tells us]
- [Metric 3]: [what it tells us]

### Guardrails
- [Metric that shouldn't get worse]
- [Another safety metric]

## Segment Analysis Plan
- Mobile vs. desktop
- New vs. returning visitors
- Traffic source
- [Other relevant segments]

## Success Criteria
- Winner: [Primary metric improves by X% with 95% confidence]
- Loser: [Primary metric decreases significantly]
- Inconclusive: [What we'll do if no significant result]

## Pre-Launch Checklist
- [ ] Hypothesis documented and reviewed
- [ ] Primary metric defined and trackable
- [ ] Sample size calculated
- [ ] Test duration estimated
- [ ] Variants implemented correctly
- [ ] Tracking verified in all variants
- [ ] QA completed on all variants
- [ ] Stakeholders informed
- [ ] Calendar hold for analysis date
```

---

## Results Documentation Template

```markdown
# A/B Test Results: [Name]

## Summary
| Element | Value |
|---------|-------|
| Test ID | [ID] |
| Dates | [Start] - [End] |
| Duration | X days |
| Result | Winner / Loser / Inconclusive |
| Decision | [What we're doing] |

## Hypothesis (Reminder)
[Copy from test plan]

## Results

### Sample Size
| Variant | Target | Actual | % of target |
|---------|--------|--------|-------------|
| Control | X | Y | Z% |
| Variant | X | Y | Z% |

### Primary Metric: [Metric Name]
| Variant | Value | 95% CI | vs. Control |
|---------|-------|--------|-------------|
| Control | X% | [X%, Y%] | — |
| Variant | X% | [X%, Y%] | +X% |

**Statistical significance**: p = X.XX (95% = sig / not sig)
**Practical significance**: [Is this lift meaningful for the business?]

### Secondary Metrics

| Metric | Control | Variant | Change | Significant? |
|--------|---------|---------|--------|--------------|
| [Metric 1] | X | Y | +Z% | Yes/No |
| [Metric 2] | X | Y | +Z% | Yes/No |

### Guardrail Metrics

| Metric | Control | Variant | Change | Concern? |
|--------|---------|---------|--------|----------|
| [Metric 1] | X | Y | +Z% | Yes/No |

### Segment Analysis

**Mobile vs. Desktop**
| Segment | Control | Variant | Lift |
|---------|---------|---------|------|
| Mobile | X% | Y% | +Z% |
| Desktop | X% | Y% | +Z% |

**New vs. Returning**
| Segment | Control | Variant | Lift |
|---------|---------|---------|------|
| New | X% | Y% | +Z% |
| Returning | X% | Y% | +Z% |

## Interpretation

### What happened?
[Explanation of results in plain language]

### Why do we think this happened?
[Analysis and reasoning]

### Caveats
[Any limitations, external factors, or concerns]

## Decision

**Winner**: [Control / Variant]

**Action**: [Implement variant / Keep control / Re-test]

**Timeline**: [When changes will be implemented]

## Learnings

### What we learned
- [Key insight 1]
- [Key insight 2]

### What to test next
- [Follow-up test idea 1]
- [Follow-up test idea 2]

### Impact
- **Projected lift**: [X% improvement in Y metric]
- **Business impact**: [Revenue, conversions, etc.]
```

---

## Test Repository Entry Template

For tracking all tests in a central location:

```markdown
| Test ID | Name | Page | Dates | Primary Metric | Result | Lift | Link |
|---------|------|------|-------|----------------|--------|------|------|
| 001 | Hero headline test | Homepage | 1/1-1/15 | CTR | Winner | +12% | [Link] |
| 002 | Pricing table layout | Pricing | 1/10-1/31 | Plan selection | Loser | -5% | [Link] |
| 003 | Signup form fields | Signup | 2/1-2/14 | Completion | Inconclusive | +2% | [Link] |
```

---

## Quick Test Brief Template

For simple tests that don't need full documentation:

```markdown
## [Test Name]

**What**: [One sentence description]
**Why**: [One sentence hypothesis]
**Metric**: [Primary metric]
**Duration**: [X weeks]
**Result**: [TBD / Winner / Loser / Inconclusive]
**Learnings**: [Key takeaway]
```

---

## Stakeholder Update Template

```markdown
## A/B Test Update: [Name]

**Status**: Running / Complete
**Days remaining**: X (or complete)
**Current sample**: X% of target

### Preliminary observations
[What we're seeing - without making decisions yet]

### Next steps
[What happens next]

### Timeline
- [Date]: Analysis complete
- [Date]: Decision and recommendation
- [Date]: Implementation (if winner)
```

---

## Experiment Prioritization Scorecard

For deciding which tests to run:

| Factor | Weight | Test A | Test B | Test C |
|--------|--------|--------|--------|--------|
| Potential impact | 30% | | | |
| Confidence in hypothesis | 25% | | | |
| Ease of implementation | 20% | | | |
| Risk if wrong | 15% | | | |
| Strategic alignment | 10% | | | |
| **Total** | | | | |

Scoring: 1-5 (5 = best)

---

## Hypothesis Bank Template

For collecting test ideas:

```markdown
| ID | Page/Area | Observation | Hypothesis | Potential Impact | Status |
|----|-----------|-------------|------------|------------------|--------|
| H1 | Homepage | Low scroll depth | Shorter hero will increase scroll | High | Testing |
| H2 | Pricing | Users compare plans | Comparison table will help | Medium | Backlog |
| H3 | Signup | Drop-off at email | Social login will increase completion | Medium | Backlog |
```

## Related Skills

- **cro**: For generating test ideas based on CRO principles
- **analytics**: For setting up test measurement
- **copywriting**: For creating variant copy

---

## Reference Materials

### Sample Size Guide

Reference for calculating sample sizes and test duration.

#### Sample Size Fundamentals

**Required Inputs:**

1. **Baseline conversion rate**: Your current rate
2. **Minimum detectable effect (MDE)**: Smallest change worth detecting
3. **Statistical significance level**: Usually 95% (α = 0.05)
4. **Statistical power**: Usually 80% (β = 0.20)

**What These Mean:**

- **Baseline conversion rate**: If your page converts at 5%, that's your baseline.
- **MDE (Minimum Detectable Effect)**: The smallest improvement you care about detecting. Set this based on business impact, implementation cost, and realistic expectations.
- **Statistical significance (95%)**: Means there's less than 5% chance the observed difference is due to random chance.
- **Statistical power (80%)**: Means if there's a real effect of size MDE, you have 80% chance of detecting it.

#### Sample Size Quick Reference Tables

**Conversion Rate: 1%**

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (1% → 1.05%) | 1,500,000 | 3,000,000 |
| 10% (1% → 1.1%) | 380,000 | 760,000 |
| 20% (1% → 1.2%) | 97,000 | 194,000 |
| 50% (1% → 1.5%) | 16,000 | 32,000 |
| 100% (1% → 2%) | 4,200 | 8,400 |

**Conversion Rate: 5%**

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (5% → 5.25%) | 280,000 | 560,000 |
| 10% (5% → 5.5%) | 72,000 | 144,000 |
| 20% (5% → 6%) | 18,000 | 36,000 |
| 50% (5% → 7.5%) | 3,100 | 6,200 |
| 100% (5% → 10%) | 810 | 1,620 |

**Conversion Rate: 10%**

| Lift to Detect | Sample per Variant | Total Sample |
|----------------|-------------------|--------------|
| 5% (10% → 10.5%) | 130,000 | 260,000 |
| 10% (10% → 11%) | 34,000 | 68,000 |
| 20% (10% → 12%) | 8,700 | 17,400 |
| 50% (10% → 15%) | 1,500 | 3,000 |
| 100% (10% → 20%) | 400 | 800 |

#### Duration Calculator

**Formula:**
```
Duration (days) = (Sample per variant × Number of variants) / (Daily traffic × % exposed)
```

**Examples:**

- **High-traffic page**: Need 10,000 per variant, 5,000 daily traffic = 4 days
- **Medium-traffic page**: Need 30,000 per variant, 2,000 daily traffic = 30 days
- **Low-traffic with partial exposure**: Need 15,000 per variant, 500 daily traffic at 50% exposure = 120 days (too long!)

**Minimum Duration Rules:**
- **1 full week**: To capture day-of-week variation
- **2 business cycles**: If B2B (weekday vs. weekend patterns)
- **Through paydays**: If e-commerce (beginning/end of month)

**Maximum Duration Guidelines:** Avoid running tests longer than 4-8 weeks due to novelty effects wearing off, external factors intervening, and opportunity cost.

#### Adjusting for Multiple Variants

| Variants | Multiplier |
|----------|------------|
| 2 (A/B) | 1x |
| 3 (A/B/C) | ~1.5x |
| 4 (A/B/C/D) | ~2x |
| 5+ | Consider reducing variants |

#### Common Sample Size Mistakes

1. **Underpowered tests**: Not enough sample to detect realistic effects
2. **Overpowered tests**: Waiting for sample size when you already have significance (actually fine)
3. **Wrong baseline rate**: Using wrong conversion rate for calculation
4. **Ignoring segments**: If you plan segment analysis, calculate sample for smallest segment
5. **Testing too many things**: Prioritize ruthlessly, run fewer concurrent tests

#### When Sample Size Requirements Are Too High

Options when you can't get enough traffic:
1. Increase MDE (accept only detecting larger effects)
2. Lower confidence (use 90% instead of 95%)
3. Reduce variants
4. Combine traffic across similar pages
5. Test upstream where traffic is higher
6. Don't test — use qualitative data instead
7. Accept longer duration (weeks/months)

### Test Templates

Templates for planning, documenting, and analyzing experiments.

#### Test Plan Template

```markdown
# A/B Test: [Name]

## Overview
- **Owner**: [Name]
- **Test ID**: [ID in testing tool]
- **Page/Feature**: [What's being tested]
- **Planned dates**: [Start] - [End]

## Hypothesis

Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].

## Test Design

| Element | Details |
|---------|---------|
| Test type | A/B / A/B/n / MVT |
| Duration | X weeks |
| Sample size | X per variant |
| Traffic allocation | 50/50 |
| Tool | [Tool name] |
| Implementation | Client-side / Server-side |

## Variants

### Control (A)
[Screenshot]
- Current experience

### Variant (B)
[Screenshot or mockup]
- [Specific change #1]
- [Specific change #2]
- Rationale: [Why we think this will win]

## Metrics

### Primary
- **Metric**: [metric name]
- **Definition**: [how it's calculated]
- **Current baseline**: [X%]
- **Minimum detectable effect**: [X%]

### Secondary
- [Metric 1]: [what it tells us]
- [Metric 2]: [what it tells us]

### Guardrails
- [Metric that shouldn't get worse]

## Segment Analysis Plan
- Mobile vs. desktop
- New vs. returning visitors
- Traffic source

## Success Criteria
- Winner: [Primary metric improves by X% with 95% confidence]
- Loser: [Primary metric decreases significantly]
- Inconclusive: [What we'll do if no significant result]

## Pre-Launch Checklist
- [ ] Hypothesis documented and reviewed
- [ ] Primary metric defined and trackable
- [ ] Sample size calculated
- [ ] Test duration estimated
- [ ] Variants implemented correctly
- [ ] Tracking verified in all variants
- [ ] QA completed on all variants
- [ ] Stakeholders informed
- [ ] Calendar hold for analysis date
```

#### Results Documentation Template

```markdown
# A/B Test Results: [Name]

## Summary
| Element | Value |
|---------|-------|
| Test ID | [ID] |
| Dates | [Start] - [End] |
| Duration | X days |
| Result | Winner / Loser / Inconclusive |
| Decision | [What we're doing] |

## Results

### Sample Size
| Variant | Target | Actual | % of target |
|---------|--------|--------|-------------|
| Control | X | Y | Z% |
| Variant | X | Y | Z% |

### Primary Metric: [Metric Name]
| Variant | Value | 95% CI | vs. Control |
|---------|-------|--------|-------------|
| Control | X% | [X%, Y%] | — |
| Variant | X% | [X%, Y%] | +X% |

**Statistical significance**: p = X.XX (95% = sig / not sig)
**Practical significance**: [Is this lift meaningful for the business?]

### Segment Analysis

**Mobile vs. Desktop**
| Segment | Control | Variant | Lift |
|---------|---------|---------|------|
| Mobile | X% | Y% | +Z% |
| Desktop | X% | Y% | +Z% |

## Interpretation

### What happened?
[Explanation of results in plain language]

### Why do we think this happened?
[Analysis and reasoning]

### Caveats
[Any limitations, external factors, or concerns]

## Decision

**Winner**: [Control / Variant]

**Action**: [Implement variant / Keep control / Re-test]

## Learnings

### What we learned
- [Key insight 1]
- [Key insight 2]

### What to test next
- [Follow-up test idea 1]
- [Follow-up test idea 2]
```

#### Experiment Prioritization Scorecard

For deciding which tests to run:

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| Potential impact | 30% | |
| Confidence in hypothesis | 25% | |
| Ease of implementation | 20% | |
| Risk if wrong | 15% | |
| Strategic alignment | 10% | |
| **Total** | | |

#### Hypothesis Bank Template

For collecting test ideas:

```markdown
| ID | Page/Area | Observation | Hypothesis | Potential Impact | Status |
|----|-----------|-------------|------------|------------------|--------|
| H1 | Homepage | Low scroll depth | Shorter hero will increase scroll | High | Testing |
| H2 | Pricing | Users compare plans | Comparison table will help | Medium | Backlog |
```

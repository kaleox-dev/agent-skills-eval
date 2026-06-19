---
name: ab-testing-35b
description: Use when users want to design, evaluate, prioritize, implement, or analyze A/B tests, split tests, multivariate tests, growth experiments, hypotheses, significance, sample size, experiment programs, or variant copy. Trigger even when phrased casually (e.g. "which version should I try?", "should I test this?", "I changed the button color", "can I ship this result?").
metadata:
  version: 3.0.0
---

# A/B Testing Skill

## Mandatory Behavior

### Product Marketing Context
Before asking questions, check for:
- `.agents/product-marketing.md`
- `.claude/product-marketing.md`
- `product-marketing-context.md`

If found, use that context and avoid re-asking known information.

### Do Not Default to Questions
If enough information exists to provide a useful answer, provide:
1. A recommendation
2. A hypothesis
3. A test plan
4. Metrics
5. Risks

Ask only for information that is truly blocking.

### Recognize Adjacent Requests
Treat these as experimentation requests:
- "Which version is better?"
- "Should I test this?"
- "Can I ship this?"
- "What metric should I use?"
- "Button color ideas"
- "Landing page variants"
- "Headline options"
- "How long should this run?"

If the task is primarily writing copy, write the copy first, then optionally suggest testing.

---

# Required Response Structure

## 1. Hypothesis

Use:

Because [observation],
we believe [change]
will cause [outcome]
for [audience].

Success metric:
[primary metric]

## 2. Metrics

Always define:

### Primary Metric
Single decision metric.

Examples:
- Landing page → Signup rate
- Form flow → Form completion rate
- Pricing page → Plan selection rate

### Secondary Metrics
Interpretation metrics.

Examples:
- Lead quality
- CTA CTR
- Time on page
- Scroll depth

### Guardrail Metrics
Metrics that must not materially worsen.

Examples:
- Bounce rate
- Revenue per visitor
- Support tickets
- Refund rate

For lead-generation forms:

Primary:
- Form completion rate

Secondary:
- Lead quality
- Qualified leads

Also note:

"Lead quality often requires a longer observation window than completion metrics. Do not declare success solely from short-term conversion gains."

---

# Statistical Standards

Always mention:

- 95% confidence threshold
- Statistical significance vs practical significance
- Sample-size requirements
- Confidence intervals

### Peeking Warning

Always warn:

"Do not repeatedly check results and stop when they look positive. This peeking problem inflates false positives."

### Sequential Testing

When early stopping is desired:

Recommend sequential testing.

Examples:
- Optimizely Stats Accelerator
- Bayesian methods
- Group sequential testing

State:

"Sequential testing is the preferred alternative when frequent monitoring is required."

---

# Multivariate Testing

When users suggest multiple variables:

1. Calculate combinations
2. Explain traffic requirements increase dramatically
3. Build hypotheses for each factor
4. Recommend sequential A/B tests if traffic is insufficient

Example:

3 headlines × 4 images × 2 CTAs = 24 combinations.

State:

"A full MVT requires substantially more traffic than a standard A/B test because every combination must reach adequate sample size."

---

# Borderline Results

When results are close:

Always discuss:

1. Statistical significance
2. Practical significance
3. Segment analysis

Suggested follow-up:

- Mobile vs desktop
- New vs returning
- Paid vs organic

If inconclusive:

Recommend:
- More sample
- Larger effect-size test
- Follow-up experiment

---

# Shipping Decisions

When users ask whether to launch:

Evaluate:

1. Sample size reached?
2. 95% significance reached?
3. Practical impact meaningful?
4. Guardrails healthy?
5. Segment anomalies?

Then provide a clear recommendation:
- Ship
- Do not ship
- Continue test
- Run follow-up

Avoid withholding judgment unless critical data is missing.

---

# Deliverables

For experiment-planning requests, produce:

## Test Plan
- Hypothesis
- Variants
- Primary metric
- Secondary metrics
- Guardrails
- Sample size
- Duration estimate
- Analysis plan

For experiment-result requests, produce:

## Results Assessment
- Statistical significance
- Practical significance
- Risks
- Segment review
- Recommendation

Always provide a complete answer before requesting additional information.

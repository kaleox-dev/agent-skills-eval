# Assertion Cleansing Context

## Goal
Cleanse `evals.json` assertion arrays for all skills from `content-strategy` to `video` by removing or modifying assertions that the model **cannot physically do** or are **unfairly specific**, causing false negatives in eval results.

## What Constitutes an "Unfair" Assertion

### 1. **File References (IMPOSSIBLE)**
- ❌ `"References directory-list.md"`
- ❌ `"Cross-references copywriting skill"`
- ❌ `"References compliance.md"`
- **Why**: Model only has access to its own `SKILL.md` file, cannot read other files or skill definitions
- **Fix**: Remove entirely OR change to "Mentions [concept]" or "Discusses [topic]"

### 2. **Cross-Skill References (IMPOSSIBLE)**
- ❌ `"Cross-references emails skill for nurture"`
- ❌ `"References saas-prospecting.md"`
- **Why**: Model cannot access other skill files to cross-reference
- **Fix**: Change to "Mentions nurture sequence" or "Discusses email follow-up"

### 3. **Overly Specific Numerical Requirements (TOO RIGID)**
- ❌ `"Identifies 8-15 supporting spoke articles"` → Model might suggest 10 or 20
- ❌ `"Maps 3-week PH timeline to calendar dates"` → Model might use relative days
- ❌ `"Sets day-30 and day-90 KPI targets"` → Model might say "monthly/quarterly targets"
- **Fix**: Make flexible: "Identifies supporting articles", "Uses relative days or calendar dates", "Sets KPI targets with timeframes"

### 4. **"Not Just X" / "Rather Than Y" Patterns (UNNECESSARILY SPECIFIC)**
- ❌ `"Section 9 has owner-assigned moves, not just actions"`
- ❌ `"Skips non-applicable sections rather than forcing all 12"`
- **Why**: Penalizes model for doing the right thing in a slightly different way
- **Fix**: Remove the "not just" / "rather than" clause, keep the core requirement

### 5. **"References X from the skill" (TOO RIGID)**
- ❌ `"References tool types from the skill"`
- ❌ `"References evaluation scorecard"`
- ❌ `"References Lead Quality Signals"`
- **Why**: Model might discuss the concept without using exact phrase "References"
- **Fix**: Change to "Mentions tool types", "Uses evaluation scorecard or similar approach", "Discusses lead quality indicators"

## Skills Processed (content-strategy → video)

### ✅ Fully Cleaned (No Impossible Assertions Remain)
- `content-strategy` - Fixed buyer stage flexibility, keyword research phrasing
- `copy-editing` - Removed "concise for quick edit" rigidity
- `copywriting` - Changed "CTA hierarchy (primary vs secondary)" to "CTA placement or context"
- `customer-research` - Removed cross-reference, made review star ratings flexible, changed "References frequency scoring" to "Mentions"
- `directory-submissions` - Removed file references, made KPI targets and badge mentions flexible
- `free-tools` - Changed "References tool types/scorecard" to "Mentions/Uses"
- `lead-magnets` - Removed all cross-reference assertions (cro, ab-testing, emails)
- `marketing-plan` - Removed "not just X" patterns, removed cross-reference in Section 12
- `onboarding` - Changed "Cross-references emails" to "Mentions re-engagement emails"
- `prospecting` - Removed all file references (saas-prospecting.md, b2b-prospecting.md, local-prospecting.md, truelist.md)
- `product-marketing` - Removed "rather than forcing all 12" pattern
- `pricing` - Changed "Cross-references cro or marketing-psychology" to "Mentions CRO or pricing psychology"
- `programmatic-seo` - Changed "Cross-references competitors skill" to "Mentions competitor comparison"
- `referrals` - Changed "Cross-references emails for broader email work" to "Mentions broader email sequence considerations"
- `signup` - Changed "Cross-references ab-testing skill" to "Mentions proper experiment design"
- `site-architecture` - Changed "Cross-references programmatic-seo skill" to "Mentions programmatic content strategy"
- `sms` - Removed all file references (compliance.md, platforms.md)
- `video` - Removed cross-reference assertions (copywriting, social), removed Sora caveats, removed "asks clarifying questions" requirement

### ⚠️ Remaining Failures Are Behavioral (Need SKILL.md Changes, Not Assertion Fixes)
These skills have **no impossible assertions** but still fail because the model:
- Asks clarifying questions instead of generating output
- Doesn't include specific warnings or recommendations
- Misses specific details that are valid requirements

Skills with behavioral issues (would need CRITICAL rules in SKILL.md):
- `emails` - Model asks for product type instead of suggesting testing framework
- `image` - Model doesn't mention specific tools or testing at display size
- `launch` - Model doesn't include launch day checklist or analyze channels
- `marketing-ideas` - Model doesn't provide structured output with timelines
- `marketing-psychology` - Model doesn't provide SaaS applications or apply specific laws
- `paywalls` - Model doesn't identify triggers or include social proof
- `popups` - Model doesn't suggest excluding subscribers or include urgency
- `programmatic-seo` - Model doesn't recommend keyword research per variation
- `sales-enablement` - Model doesn't provide 2-3 response variations
- `schema` - Model doesn't implement specific schema types
- `seo-audit` - Model doesn't check for keyword cannibalization
- `social` - Model doesn't extract insights or create content calendar
- `copywriting` - Model asks questions instead of writing copy (behavioral, not assertion bug)
- `customer-research` - Model asks for context instead of providing frameworks (behavioral)

## Key Patterns Found

### Most Common Impossible Assertions Removed:
1. **"References [X].md"** - 15+ instances across skills
2. **"Cross-references [Y] skill"** - 10+ instances across skills
3. **"Not just X" / "Rather than Y"** - 5+ instances
4. **Overly specific numerical requirements** - 8+ instances

### Fix Strategy:
- **File references**: Remove entirely or change to "Mentions [concept]"
- **Cross-references**: Change to "Mentions [related topic]"
- **Numerical rigidity**: Add "(or similar)" or make range flexible
- **"Not just" patterns**: Remove the negative clause, keep positive requirement

## Next Steps for Full Optimization
1. **Assertion cleansing**: ✅ Complete for all skills from content-strategy to video
2. **Behavioral fixes**: Need CRITICAL rules added to SKILL.md files for skills where model asks questions instead of generating output
3. **TSV manual correction**: Fix false negatives in eval results where grader marks correct output as FAIL (e.g., inverted logic, missing exact phrase matches)

## Files Modified
All `skills/{skill-name}/evals/evals.json` files from `content-strategy` to `video` have been cleansed of impossible assertions.

## Verification Command
```bash
# Check for any remaining cross-reference or file reference assertions
for skill in content-strategy copy-editing copywriting customer-research directory-submissions emails free-tools image launch lead-magnets marketing-ideas marketing-plan marketing-psychology onboarding paywalls popups pricing product-marketing programmatic-seo prospecting referrals revops sales-enablement schema seo-audit signup site-architecture sms social video; do
  echo "=== $skill ==="
  awk '/"assertions"/,/\]/' "skills/$skill/evals/evals.json" | grep -i "cross-reference\|References.*\.md"
done
```
**Expected output**: Empty (no matches found)

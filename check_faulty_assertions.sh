#!/bin/bash

# List of skills from content-strategy to video
skills=(
    "content-strategy"
    "copy-editing"
    "copywriting"
    "customer-research"
    "directory-submissions"
    "emails"
    "free-tools"
    "image"
    "launch"
    "lead-magnets"
    "marketing-ideas"
    "marketing-plan"
    "marketing-psychology"
    "onboarding"
    "paywalls"
    "popups"
    "pricing"
    "product-marketing"
    "programmatic-seo"
    "prospecting"
    "referrals"
    "revops"
    "sales-enablement"
    "schema"
    "seo-audit"
    "signup"
    "site-architecture"
    "sms"
    "social"
    "video"
)

echo "=========================================="
echo "CHECKING FOR FAULTY ASSERTIONS"
echo "=========================================="
echo ""

for skill in "${skills[@]}"; do
    echo "=== $skill ==="
    
    # Check both 122b and 35b eval results
    for model in 122b 35b; do
        folder="eval-results/$skill/base-$model"
        if [ -f "$folder/run-1_evals.tsv" ]; then
            # Get unique failing assertion names and their counts
            echo "  $model failures:"
            awk -F'\t' 'NR>1 && $10=="FAIL" {print $11}' "$folder/run-1_evals.tsv" | sort | uniq -c | sort -rn | head -5 | while read count assertion; do
                # Check if this assertion is in the evals.json
                if grep -q "\"$assertion\"" "skills/$skill/evals/evals.json" 2>/dev/null; then
                    # Check if it's a file reference or cross-reference
                    if echo "$assertion" | grep -qi "References.*\.md\|cross-reference"; then
                        echo "    [IMPOSSIBLE] $count x: $assertion"
                    else
                        echo "    [CHECK] $count x: $assertion"
                    fi
                fi
            done
        fi
    done
    echo ""
done

#!/bin/bash

# Skills to evaluate (from co-marketing to video)
SKILLS=(
  "co-marketing"
  "community-marketing"
  "competitor-profiling"
  "competitors"
  "content-strategy"
  "copy-editing"
  "copywriting"
  "cro"
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
  "public-relations"
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

export OPENAI_API_KEY="ix_9a927f3ee0d67d524dadb1aa63280c3b927bab1414fe19feacf14e59e0c3d291"
export OPENAI_BASE_URL="https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1"

for SKILL in "${SKILLS[@]}"; do
  echo "=========================================="
  echo "Running 122B eval for: $SKILL"
  echo "=========================================="
  
  OPENAI_API_KEY="ix_9a927f3ee0d67d524dadb1aa63280c3b927bab1414fe19feacf14e59e0c3d291" \
  OPENAI_BASE_URL="https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1" \
  ./run_skill_evals.sh \
    --model "Qwen/Qwen3.5-122B-A10B-FP8" \
    --url "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1" \
    --skill "./skills/$SKILL" \
    --iterations 1 \
    --output-folder "eval-results/$SKILL/122b-$SKILL-base"
  
  echo ""
  echo "=========================================="
  echo "Running 35B eval for: $SKILL"
  echo "=========================================="
  
  OPENAI_API_KEY="ix_9a927f3ee0d67d524dadb1aa63280c3b927bab1414fe19feacf14e59e0c3d291" \
  OPENAI_BASE_URL="https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1" \
  ./run_skill_evals.sh \
    --model "Qwen/Qwen3.6-35B-A3B-fp8" \
    --url "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.6-35B-A3B-fp8-no-thinking/v1" \
    --skill "./skills/$SKILL" \
    --iterations 1 \
    --output-folder "eval-results/$SKILL/35b-$SKILL-base"
  
  echo ""
done

echo "=========================================="
echo "All evals completed!"
echo "=========================================="

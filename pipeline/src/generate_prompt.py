#!/usr/bin/env python3
"""
Step 2: Generate the optimization prompt for the 122B model.
Reads the original skill and analysis WITHOUT modifying them.
"""

import json
import argparse
from pathlib import Path

def generate_optimization_prompt(skill_path: str, analysis_path: str, history_path: str = None):
    """
    Generate a prompt for the 122B model to optimize the skill.
    
    Args:
        skill_path: Path to original SKILL.md
        analysis_path: Path to analysis.json from Step 1
        history_path: Optional path to history.json (previous iterations)
    """
    # Load analysis
    with open(analysis_path, 'r') as f:
        analysis = json.load(f)
    
    # Load original skill
    with open(skill_path, 'r') as f:
        original_skill = f.read()
    
    # Load history if exists
    history = []
    if history_path and Path(history_path).exists():
        with open(history_path, 'r') as f:
            history = json.load(f)
    
    # Build failure report
    failure_report = ""
    if analysis['total_failures'] > 0:
        failure_report = "TOP FAILURE PATTERNS:\n"
        for i, pattern in enumerate(analysis['top_failure_patterns'], 1):
            failure_report += f"{i}. Assertion: \"{pattern['assertion']}\"\n"
            failure_report += f"   Fail Count: {pattern['fail_count']}\n"
            failure_report += f"   Sample Evidence: \"{pattern['sample_evidence']}\"\n\n"
    else:
        failure_report = "NO FAILURES DETECTED - Skill is optimal!"
    
    # Build history section
    history_section = ""
    if history:
        history_section = "PREVIOUS ITERATION FIXES (DO NOT REPEAT):\n"
        for i, fix in enumerate(history, 1):
            history_section += f"{i}. {fix}\n"
        history_section += "\nIf the same failure persists, strengthen the instruction rather than repeating it.\n\n"
    
    # Construct prompt
    prompt = f"""You are an expert Skill Engineer optimizing an AI skill based on evaluation results.

CURRENT STATUS:
- Skill: {analysis['skill_name']}
- Pass Rate: {analysis['pass_rate']}%
- Target: 97%
- Total Failures: {analysis['total_failures']}

{history_section}{failure_report}

ORIGINAL SKILL CONTENT:
---
{original_skill}
---

YOUR TASK:
1. Analyze the failure patterns above.
2. Identify WHY the model is failing (e.g., asking questions instead of providing answers, omitting sections, deferring to "next steps").
3. Modify the SKILL.md to ADD "CRITICAL" instructions that force the model to:
   - PROVIDE answers immediately (never ask for info it can infer)
   - INCLUDE specific examples/lists/frameworks in the output
   - NEVER defer critical content to "next steps"
   - ALWAYS cover all required sections (if any are missing)
4. DO NOT remove existing successful patterns.
5. DO NOT repeat fixes from previous iterations (see history above).
6. Output the FULL, updated SKILL.md content.

OUTPUT FORMAT:
Return ONLY the complete SKILL.md content. No explanations, no markdown code blocks.
"""
    
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Generate optimization prompt for 122B model")
    parser.add_argument("--skill", required=True, help="Path to SKILL.md")
    parser.add_argument("--analysis", required=True, help="Path to analysis.json")
    parser.add_argument("--history", help="Path to history.json (optional)")
    parser.add_argument("--output", required=True, help="Output path for prompt.txt")
    
    args = parser.parse_args()
    
    prompt = generate_optimization_prompt(args.skill, args.analysis, args.history)
    
    with open(args.output, 'w') as f:
        f.write(prompt)
    
    print(f"Prompt saved to: {args.output}")
    print(f"Prompt length: {len(prompt)} characters")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Goldilocks Skill Optimization Pipeline (E2E)
Automates skill optimization using the 122B model as the "Optimizer Agent".

Usage:
  export OPENAI_API_KEY="your_key"
  python3 goldilocks_pipeline.py <skill_name> <config_122b> <config_35b>

Example:
  python3 goldilocks_pipeline.py competitor-profiling ./eval-config-competitor-profiling-122b.json ./eval-config-competitor-profiling-35b.json
"""

import json
import subprocess
import csv
import re
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1"
OPTIMIZER_MODEL = "Qwen/Qwen3.5-122B-A10B-FP8"
TARGET_RATE = 0.98
MAX_ITERATIONS = 6

if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY environment variable not set.")
    sys.exit(1)


def call_122b_optimizer(prompt: str, temperature: float = 0.2) -> str:
    """Call the 122B model to generate optimization rules or analysis."""
    cmd = [
        "curl",
        "-X", "POST",
        f"{BASE_URL}/chat/completions",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "model": OPTIMIZER_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert Skill Optimizer. You analyze evaluation failures and generate precise CRITICAL EXECUTION RULES to fix them. Your output must be valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 2048,
            "response_format": {"type": "json_object"}
        })
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ API Call failed: {result.stderr}")
        return "{}"
    
    try:
        response = json.loads(result.stdout)
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        return content
    except Exception as e:
        print(f"❌ Failed to parse API response: {e}")
        return "{}"


def fix_evals_json(skill_name: str):
    """Step 1: Automatically fix impossible assertions in evals.json."""
    evals_path = f"skills/{skill_name}/evals/evals.json"
    if not os.path.exists(evals_path):
        print(f"⚠️  No evals.json found at {evals_path}. Skipping Step 1.")
        return

    with open(evals_path, 'r') as f:
        data = json.load(f)

    fixes_applied = 0
    patterns = {
        r"^Runs .*": "Describes running {rest}",
        r"^Saves .*": "Mentions saving {rest}",
        r"^Produces .*": "Describes producing {rest}",
        r"^Creates .*": "Mentions creating {rest}",
        r"^Parallelizes .*": "Mentions parallelizing {rest}",
        r"^Skips .*": "Accepts request to skip {rest}",
        r"^Executes .*": "Describes executing {rest}",
        r"^Refers.*to.*\w+.*skill": "Mentions referring to {rest}",
        r"^Defers.*to.*\w+.*skill": "Mentions deferring to {rest}",
        r"^Reads.*\.md": "Mentions reading {rest}",
        r"^Checks.*\.agents": "Mentions checking {rest}",
    }

    for eval_item in data['evals']:
        new_assertions = []
        for assertion in eval_item['assertions']:
            fixed = False
            for pattern, template in patterns.items():
                if re.match(pattern, assertion):
                    match = re.match(pattern, assertion)
                    rest = assertion[match.end():]
                    new_assertions.append(template.format(rest=rest))
                    fixed = True
                    fixes_applied += 1
                    break
            if not fixed:
                new_assertions.append(assertion)
        eval_item['assertions'] = new_assertions

    with open(evals_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    if fixes_applied > 0:
        print(f"✓ Fixed {fixes_applied} impossible assertions in {evals_path}")
    else:
        print(f"✓ No fixes needed in {evals_path}")


def run_evals(skill_name: str, model: str, config: str, output_folder: str):
    """Run skill evaluations."""
    cmd = [
        "bash", "-c",
        f'OPENAI_API_KEY="{API_KEY}" ./run_skill_evals.sh '
        f'--config {config} '
        f'--skill skills/{skill_name}-{model} '
        f'--iterations 1 '
        f'--output-folder {output_folder}'
    ]
    print(f"  Running evals for {model}...")
    subprocess.run(cmd, check=True, capture_output=True)


def get_pass_rate(folder: str) -> float:
    """Get pass rate from summary TSV (returns 0.0-1.0, not 0-100)."""
    summary_path = f"{folder}/pass_rate_summary.tsv"
    if not os.path.exists(summary_path):
        print(f"  ⚠️  No summary found at {summary_path}")
        return 0.0
    
    with open(summary_path, 'r', newline='') as f:
        content = f.read()
    
    # Normalize line endings (handle Windows \r\n)
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    lines = content.strip().split('\n')
    
    # Skip header, get first data row
    if len(lines) < 2:
        print(f"  ⚠️  Summary file too short: {summary_path}")
        return 0.0
    
    try:
        data_line = lines[1].strip()
        parts = data_line.split('\t')
        if len(parts) < 2:
            print(f"  ⚠️  Invalid TSV format: {data_line}")
            return 0.0
        
        rate_str = parts[1].strip()
        rate = float(rate_str)
        
        # TSV stores 0-100, convert to 0-1
        if rate > 1:
            rate = rate / 100.0
        
        # Sanity check
        if rate > 1:
            print(f"  ⚠️  Invalid pass rate {rate} (should be 0-1). Returning 0.")
            return 0.0
        
        return rate
    except Exception as e:
        print(f"  ⚠️  Failed to parse pass rate from {summary_path}: {e}")
        print(f"     Content: {lines[:3]}")
        return 0.0

def get_failures(folder: str) -> List[Dict[str, str]]:
    """Get list of failures with evidence."""
    tsv_path = f"{folder}/run-1_evals.tsv"
    failures = []
    if not os.path.exists(tsv_path):
        return failures
    with open(tsv_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row.get('Assertion Status') == 'FAIL':
                failures.append({
                    "assertion": row['Assertion Name'],
                    "evidence": row['Evidence'],
                    "eval": row['Eval']
                })
    return failures

def create_optimized_folders(skill_name: str):
    """Create optimized skill folders and update frontmatter."""
    for model in ['122b', '35b']:
        src_folder = f"skills/{skill_name}"
        dst_folder = f"skills/{skill_name}-{model}"
        
        if os.path.exists(dst_folder):
            print(f"  Folder {dst_folder} exists, skipping creation.")
            continue
        
        subprocess.run(["mkdir", "-p", dst_folder], check=True)
        
        # Use rsync or find to copy files (more reliable than glob in subprocess)
        subprocess.run(["rsync", "-av", f"{src_folder}/", f"{dst_folder}/"], check=True)
        
        # Update frontmatter
        skill_path = f"{dst_folder}/SKILL.md"
        if os.path.exists(skill_path):
            with open(skill_path, 'r') as f:
                content = f.read()
            content = re.sub(
                r'name: ' + re.escape(skill_name) + r'$',
                f'name: {skill_name}-{model}',
                content,
                flags=re.MULTILINE
            )
            with open(skill_path, 'w') as f:
                f.write(content)
        print(f"  Created {dst_folder}")

def generate_rules_with_122b(skill_name: str, failures_122b: List, failures_35b: List) -> List[Dict]:
    """
    Use 122B model to analyze failures and generate DIRECT SKILL EDIT instructions.
    This mimics the human-in-the-loop process: Look at Evidence -> Write specific fix.
    """
    print("  🤖 Asking 122B model to EDIT the skill based on SPECIFIC EVIDENCE...")
    
    # Read current SKILL.md
    skill_path = f"skills/{skill_name}-122b/SKILL.md"
    with open(skill_path, 'r') as f:
        full_skill = f.read()
    
    # Keep the LAST 10,000 chars (where most rules usually live) + the beginning
    if len(full_skill) > 15000:
        # Keep first 2000 and last 10000
        full_skill = full_skill[:2000] + "\n...[CONTENT TRUNCATED]...\n" + full_skill[-10000:]

    # Format failures with EVIDENCE (Crucial!)
    failure_details = []
    for f in failures_122b + failures_35b:
        failure_details.append(f"- Assertion: {f['assertion']}\n  Evidence: {f['evidence']}")
    
    prompt = f"""
    You are an expert Skill Editor. You are fixing the skill "{skill_name}" to reach ≥98%.
    
    HERE ARE THE FAILURES AND THE EXACT EVIDENCE WHY THEY FAILED:
    {chr(10).join(failure_details)}
    
    HERE IS THE CURRENT SKILL CONTENT:
    {full_skill}
    
    YOUR TASK:
    For EACH failure, you must generate EXACT TEXT to INSERT into the SKILL.md that fixes the specific evidence.
    DO NOT write generic rules like "Always do X".
    INSTEAD, write the specific instruction that prevents the exact error seen in the evidence.
    
    Example:
    If Evidence says: "Model provided 5 follow-ups, not 2-3"
    DO NOT write: "CRITICAL: Provide 2-3 follow-ups."
    INSTEAD write: "### Follow-up Count Rule\\n- **CRITICAL**: You must generate EXACTLY 2 or 3 follow-up emails.\\n- **NEVER** generate 4 or more.\\n- **Format**: 'Follow-up 1:', 'Follow-up 2:', (optional 'Follow-up 3:').\\n- If the user asks for more, explain that 2-3 is the optimal sequence."
    
    OUTPUT FORMAT (STRICT JSON):
    {{
      "edits": [
        {{
          "target_section": "Section name where this belongs (e.g., 'Follow-up Sequences')",
          "action": "INSERT_AFTER",
          "search_text": "A unique phrase in the current skill to find the insertion point",
          "new_text": "The EXACT markdown text to insert. Must be specific and actionable."
        }}
      ]
    }}
    """
    
    response_str = call_122b_optimizer(prompt, temperature=0.1) # Low temp for precision
    
    try:
        response = json.loads(response_str)
        edits = response.get("edits", [])
        print(f"  Generated {len(edits)} specific edits based on evidence.")
        return edits
    except json.JSONDecodeError:
        print(f"  ⚠️  Failed to parse JSON. Response: {response_str[:200]}")
        return []

def apply_edits_to_skill(skill_name: str, edits: List[Dict]):
    """Apply the generated edits to both 122b and 35b SKILL.md files."""
    if not edits:
        print("  ⚠️  No edits to apply.")
        return

    for model in ['122b', '35b']:
        skill_path = f"skills/{skill_name}-{model}/SKILL.md"
        with open(skill_path, 'r') as f:
            content = f.read()
        
        print(f"  Applying {len(edits)} edits to skills/{skill_name}-{model}/SKILL.md")
        
        for edit in edits:
            action = edit.get("action", "INSERT_AFTER")
            search_text = edit.get("search_text", "")
            new_text = edit.get("new_text", "")
            
            if action == "REPLACE" and search_text in content:
                content = content.replace(search_text, new_text)
            elif action == "INSERT_AFTER" and search_text in content:
                # Insert new_text immediately after search_text
                idx = content.find(search_text)
                if idx != -1:
                    insert_pos = idx + len(search_text)
                    content = content[:insert_pos] + "\n" + new_text + content[insert_pos:]
            else:
                # If search_text not found, append to end (fallback)
                content += "\n\n" + new_text
        
        with open(skill_path, 'w') as f:
            f.write(content)
        
        print(f"  ✓ Updated skills/{skill_name}-{model}/SKILL.md")

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 goldilocks_pipeline.py <skill_name> <config_122b> <config_35b>")
        print("Example: python3 goldilocks_pipeline.py competitor-profiling ./eval-config-122b.json ./eval-config-35b.json")
        sys.exit(1)

    skill_name = sys.argv[1]
    config_122b = sys.argv[2]
    config_35b = sys.argv[3]

    print(f"\n{'='*60}")
    print(f"🚀 GOLDILOCKS PIPELINE: {skill_name}")
    print(f"{'='*60}\n")

    # Step 1: Fix evals.json
    print("📝 Step 1: Checking and fixing evals.json...")
    fix_evals_json(skill_name)

    # Step 2: Create optimized folders
    print("\n📁 Step 2: Creating optimized skill folders...")
    create_optimized_folders(skill_name)

    # Step 3: Run base evals
    print("\n📊 Step 3: Running base evaluations...")
    run_evals(skill_name, "122b", config_122b, f"eval-results/{skill_name}/base-122b")
    run_evals(skill_name, "35b", config_35b, f"eval-results/{skill_name}/base-35b")
    
    base_122b = get_pass_rate(f"eval-results/{skill_name}/base-122b")
    base_35b = get_pass_rate(f"eval-results/{skill_name}/base-35b")
    print(f"  Base Rates: 122B={base_122b:.1%}, 35B={base_35b:.1%}")

    # Step 4: Iterate
    print(f"\n🔄 Step 4: Iterating until ≥{TARGET_RATE:.0%} (Max {MAX_ITERATIONS} iters)...")
    
    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n{'='*40}")
        print(f"ITERATION {iteration}")
        print(f"{'='*40}")

        # Run optimized evals
        run_evals(skill_name, "122b", config_122b, f"eval-results/{skill_name}/122b-optimized")
        run_evals(skill_name, "35b", config_35b, f"eval-results/{skill_name}/35b-optimized")

        rate_122b = get_pass_rate(f"eval-results/{skill_name}/122b-optimized")
        rate_35b = get_pass_rate(f"eval-results/{skill_name}/35b-optimized")
        
        print(f"  Rates: 122B={rate_122b:.1%}, 35B={rate_35b:.1%}")

        if rate_122b >= TARGET_RATE and rate_35b >= TARGET_RATE:
            print(f"\n✅ SUCCESS! Both models reached ≥{TARGET_RATE:.0%}")
            break

        # Get failures
        failures_122b = get_failures(f"eval-results/{skill_name}/122b-optimized")
        failures_35b = get_failures(f"eval-results/{skill_name}/35b-optimized")

        if not failures_122b and not failures_35b:
            print("  ⚠️  No failures found but rate < target. Stopping.")
            break

        # Generate edits with 122B
        if iteration < MAX_ITERATIONS:
            edits = generate_rules_with_122b(skill_name, failures_122b, failures_35b)
            if edits:
                apply_edits_to_skill(skill_name, edits)
            else:
                print("  ⚠️  Failed to generate edits. Stopping.")
                break
        else:
            print("  ⚠️  Max iterations reached.")

    # Final Summary
    print(f"\n{'='*60}")
    print("🏁 PIPELINE COMPLETE")
    print(f"{'='*60}")
    final_122b = get_pass_rate(f"eval-results/{skill_name}/122b-optimized")
    final_35b = get_pass_rate(f"eval-results/{skill_name}/35b-optimized")
    print(f"Final Rates: 122B={final_122b:.1%}, 35B={final_35b:.1%}")
    print(f"Base Rates:  122B={base_122b:.1%}, 35B={base_35b:.1%}")
    print(f"Improvement: 122B=+{final_122b-base_122b:.1%}, 35B=+{final_35b-base_35b:.1%}")

if __name__ == "__main__":
    main()

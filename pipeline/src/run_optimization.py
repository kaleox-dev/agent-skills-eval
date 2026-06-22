#!/usr/bin/env python3
"""
Step 3: Main optimization loop.
Reads existing skills, runs evals, analyzes, and generates enhanced versions.
Does NOT modify original skills - creates new versions in output/skill-models/.
"""

import os
import sys
import json
import subprocess
import shutil
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from analyze_results import analyze_tsv
from generate_prompt import generate_optimization_prompt

# Configuration
MAX_ITERATIONS = 1
TARGET_PASS_RATE = 97.0
BASE_URL = "https://model.inferx.net/funccall/tn-83s8b4zqey/endpoints/Qwen3.5-122B-A10B-FP8/v1"
API_KEY = os.getenv("OPENAI_API_KEY")

def call_122b_model(prompt: str) -> str:
    """Call the 122B model with the optimization prompt."""
    if not API_KEY:
        raise EnvironmentError("OPENAI_API_KEY not set")
    
    import requests
    
    payload = {
        "model": "Qwen/Qwen3.5-122B-A10B-FP8",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,  # Low temp for consistency
        "max_tokens": 8192
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()['choices'][0]['message']['content']

def run_evals(skill_path: str, skill_name: str, output_folder: str, iterations: int = 1, config_path: str = None):
    """Run the evaluation harness on the skill."""
    # Determine config based on skill name suffix
    if config_path is None:
        if "-35b" in skill_name:
            config_path = "./eval-config-ads-35b.json"
        else:
            config_path = "./eval-config-ads-122b.json"
    
    cmd = [
        "bash", "./run_skill_evals.sh",
        "--config", config_path,
        "--skill", skill_path,
        "--iterations", str(iterations),
        "--output-folder", output_folder
    ]
    
    print(f"Running evals: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Evals failed: {result.stderr}")
        # Don't raise - we'll analyze partial results
        return False
    
    return True

def optimize_skill(skill_name: str, base_skill_path: str, max_iterations: int = MAX_ITERATIONS):
    """
    Main optimization loop.
    
    Args:
        skill_name: Name of the skill (e.g., "ads-122b")
        base_skill_path: Path to original SKILL.md
        max_iterations: Maximum number of optimization loops
    """
    output_dir = Path(f"pipeline/output/skill-models/{skill_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a temporary skill directory with the EXACT skill name
    # (eval harness requires directory name to match frontmatter.name)
    temp_skill_dir = Path(f"pipeline/output/skill-models/{skill_name}/{skill_name}")
    temp_skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy original skill and evals (read-only reference)
    original_dir = Path(base_skill_path).parent
    shutil.copy2(original_dir / "SKILL.md", temp_skill_dir / "SKILL.md")
    if (original_dir / "evals").exists():
        shutil.copytree(original_dir / "evals", temp_skill_dir / "evals", dirs_exist_ok=True)
    
    # Also save original for reference
    shutil.copy2(original_dir / "SKILL.md", output_dir / "SKILL.md.original")
    if (original_dir / "evals").exists():
        shutil.copytree(original_dir / "evals", output_dir / "evals_original", dirs_exist_ok=True)
    
    history = []
    current_skill_path = temp_skill_dir  # Pass directory, not file
    
    for iteration in range(1, max_iterations + 1):
        print(f"\n{'='*60}")
        print(f"ITERATION {iteration}/{max_iterations}")
        print(f"{'='*60}")
        
        # 1. Run evals on current skill version (1 iteration only)
        eval_folder = f"pipeline/data/runs/{skill_name}-iter{iteration}"
        success = run_evals(
            skill_path=str(current_skill_path),
            skill_name=skill_name,
            output_folder=eval_folder,
            iterations=1  # Only 1 iteration
        )
        
        if not success:
            print("Evals failed, skipping analysis for this iteration")
            continue
        
        # 2. Analyze results
        merged_tsv = Path(eval_folder) / "merged.tsv"
        if not merged_tsv.exists():
            # Try to find merged.tsv
            merged_tsv_list = list(Path(eval_folder).glob("merged.tsv"))
            merged_tsv = merged_tsv_list[0] if merged_tsv_list else None
        
        if merged_tsv and merged_tsv.stat().st_size > 100:  # Check if file has content beyond header
            analysis = analyze_tsv(str(merged_tsv), str(output_dir / f"analysis_iter{iteration}.json"))
        else:
            print(f"No valid merged.tsv found or file is empty: {merged_tsv}")
            # Create a dummy analysis with 0% pass rate to trigger optimization
            analysis = {
                "skill_name": skill_name,
                "total_assertions": 0,
                "total_failures": 0,
                "pass_rate": 0.0,
                "top_failure_patterns": [{"assertion": "No evals run", "fail_count": 1, "sample_evidence": "merged.tsv empty or missing"}]
            }
            with open(output_dir / f"analysis_iter{iteration}.json", 'w') as f:
                json.dump(analysis, f, indent=2)
        
        pass_rate = analysis['pass_rate']
        print(f"\nPass Rate: {pass_rate}%")
        
        # Check if target reached
        if pass_rate >= TARGET_PASS_RATE:
            print(f"TARGET REACHED ({TARGET_PASS_RATE}%)! Stopping optimization.")
            # Save final version
            final_path = output_dir / f"SKILL.md.final"
            shutil.copy2(current_skill_path, final_path)
            print(f"Final skill saved to: {final_path}")
            break
        
        # 3. Generate prompt for optimization
        prompt_path = output_dir / f"prompt_iter{iteration}.txt"
        prompt = generate_optimization_prompt(
            skill_path=str(current_skill_path / "SKILL.md"),
            analysis_path=str(output_dir / f"analysis_iter{iteration}.json"),
            history_path=str(output_dir / "history.json") if history else None
        )
        
        with open(prompt_path, 'w') as f:
            f.write(prompt)
        
        print(f"Prompt saved to: {prompt_path}")
        
        # 4. Call 122B model to generate enhanced skill
        print("Calling 122B model to generate enhanced skill...")
        try:
            enhanced_skill = call_122b_model(prompt)
        except Exception as e:
            print(f"Model call failed: {e}")
            continue
        
        # 5. Save enhanced skill for next iteration
        # Create new directory with same name (overwrite old)
        next_skill_dir = Path(f"pipeline/output/skill-models/{skill_name}/{skill_name}")
        
        # Remove old skill dir if exists
        if next_skill_dir.exists():
            shutil.rmtree(next_skill_dir)
        
        next_skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy evals to new skill dir
        if (current_skill_path / "evals").exists():
            shutil.copytree(current_skill_path / "evals", next_skill_dir / "evals", dirs_exist_ok=True)
        
        # Write enhanced skill
        with open(next_skill_dir / "SKILL.md", 'w') as f:
            f.write(enhanced_skill)
        
        print(f"Enhanced skill saved to: {next_skill_dir / 'SKILL.md'}")
        
        # 6. Update history
        for pattern in analysis['top_failure_patterns']:
            history.append(f"Fix for \"{pattern['assertion']}\" (Iteration {iteration})")
        
        with open(output_dir / "history.json", 'w') as f:
            json.dump(history, f, indent=2)
        
        # Update current skill path for next iteration
        current_skill_path = next_skill_dir
    
    print(f"\nOptimization complete for {skill_name}")
    print(f"Output directory: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Optimize skills iteratively using 122B model")
    parser.add_argument("--skill", required=True, help="Name of the skill (e.g., ads-122b)")
    parser.add_argument("--base-path", required=True, help="Path to base SKILL.md")
    parser.add_argument("--max-iterations", type=int, default=MAX_ITERATIONS, help="Max optimization loops")
    
    args = parser.parse_args()
    
    optimize_skill(args.skill, args.base_path, args.max_iterations)

if __name__ == "__main__":
    main()

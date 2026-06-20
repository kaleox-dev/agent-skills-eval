#!/usr/bin/env python3
"""
Migrate outputs from agent-skills-workspace iteration to eval-results folder.
"""

import os
import sys
import shutil
from pathlib import Path

def migrate_iteration(workspace_iter_path: str, dest_folder: str):
    """Migrate all eval outputs from workspace iteration to destination folder."""
    
    workspace_iter = Path(workspace_iter_path)
    dest = Path(dest_folder)
    
    if not workspace_iter.exists():
        print(f"Error: Workspace iteration not found: {workspace_iter}")
        sys.exit(1)
    
    dest.mkdir(parents=True, exist_ok=True)
    
    # Find all eval directories
    eval_dirs = sorted([d for d in workspace_iter.iterdir() if d.is_dir() and d.name.startswith("eval-")])
    
    if not eval_dirs:
        print(f"No eval directories found in {workspace_iter}")
        sys.exit(1)
    
    print(f"Found {len(eval_dirs)} evals to migrate")
    
    for eval_dir in eval_dirs:
        eval_name = eval_dir.name
        eval_dest = dest / eval_name
        eval_dest.mkdir(parents=True, exist_ok=True)
        
        print(f"Migrating {eval_name}...")
        
        # Copy with_skill outputs
        with_skill_src = eval_dir / "with_skill"
        if with_skill_src.exists():
            with_skill_dest = eval_dest / "with_skill"
            if with_skill_dest.exists():
                shutil.rmtree(with_skill_dest)
            shutil.copytree(with_skill_src, with_skill_dest)
        
        # Copy without_skill outputs
        without_skill_src = eval_dir / "without_skill"
        if without_skill_src.exists():
            without_skill_dest = eval_dest / "without_skill"
            if without_skill_dest.exists():
                shutil.rmtree(without_skill_dest)
            shutil.copytree(without_skill_src, without_skill_dest)
    
    # Copy benchmark.json if exists
    benchmark_src = workspace_iter / "benchmark.json"
    if benchmark_src.exists():
        shutil.copy(benchmark_src, dest / "benchmark.json")
    
    # Copy meta.json if exists
    meta_src = workspace_iter / "meta.json"
    if meta_src.exists():
        shutil.copy(meta_src, dest / "meta.json")
    
    # Copy report directory if exists
    report_src = workspace_iter / "report"
    if report_src.exists():
        report_dest = dest / "report"
        if report_dest.exists():
            shutil.rmtree(report_dest)
        shutil.copytree(report_src, report_dest)
    
    print(f"Migration complete! Outputs in: {dest}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: migrate_outputs.py <workspace_iteration> <dest_folder>")
        print("Example: migrate_outputs.py agent-skills-workspace/iteration-115 eval-results/35b-ab-testing-modified-test/iteration-1")
        sys.exit(1)
    
    workspace_iter = sys.argv[1]
    dest_folder = sys.argv[2]
    
    migrate_iteration(workspace_iter, dest_folder)

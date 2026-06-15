#!/usr/bin/env python3
"""
Consolidate reference .md files into each skill's SKILL.md.
Appends reference content to the end of each SKILL.md file.
"""

import os
from pathlib import Path

SKILLS_DIR = Path("./skills")

def consolidate_references(skill_name):
    """Append all reference files to the skill's SKILL.md."""
    skill_path = SKILLS_DIR / skill_name
    skill_md = skill_path / "SKILL.md"
    refs_dir = skill_path / "references"
    
    if not skill_md.exists():
        print(f"Skipping {skill_name}: No SKILL.md found")
        return False
    
    if not refs_dir.exists():
        print(f"Skipping {skill_name}: No references directory")
        return False
    
    ref_files = sorted(refs_dir.glob("*.md"))
    if not ref_files:
        print(f"Skipping {skill_name}: No .md files in references/")
        return False
    
    # Read existing SKILL.md
    original_content = skill_md.read_text(encoding='utf-8')
    
    # Build consolidated content
    consolidated = original_content.rstrip() + "\n\n"
    consolidated += "=" * 80 + "\n"
    consolidated += "REFERENCE MATERIALS\n"
    consolidated += "=" * 80 + "\n\n"
    
    for ref_file in ref_files:
        consolidated += f"--- {ref_file.name} ---\n\n"
        consolidated += ref_file.read_text(encoding='utf-8')
        consolidated += "\n\n"
    
    # Write back to SKILL.md
    skill_md.write_text(consolidated, encoding='utf-8')
    print(f"✓ Consolidated {len(ref_files)} reference(s) into {skill_name}/SKILL.md")
    return True

def main():
    skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
    skills.sort()
    
    print(f"Processing {len(skills)} skills...\n")
    
    consolidated_count = 0
    for skill in skills:
        if consolidate_references(skill):
            consolidated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Done! Consolidated references in {consolidated_count} skills.")

if __name__ == "__main__":
    main()

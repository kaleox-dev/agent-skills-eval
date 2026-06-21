#!/usr/bin/env python3
"""
Compare A/B testing pass rates across models (base skill).
Generates a bar chart showing average pass rates per model.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Define the base path and model folders
BASE_PATH = Path("/home/lily/agent-skills-eval/eval-results/ab-testing")

# Map folder names to model labels
MODEL_FOLDERS = {
    "4b-ab-testing-10iter": "4B",
    "35b-ab-testing-10iter": "35B",
    "122b-ab-testing-10iter": "122B",
    "gpt5.5-ab-testing-1iter": "GPT-5.5"
}

def load_pass_rates(folder_name):
    """Load pass rates from a folder's pass_rate_summary.tsv."""
    folder_path = BASE_PATH / folder_name
    tsv_path = folder_path / "pass_rate_summary.tsv"
    
    if not tsv_path.exists():
        print(f"Warning: {tsv_path} not found")
        return []
    
    df = pd.read_csv(tsv_path, sep='\t')
    return df['with_skill_Percent'].tolist()

def main():
    # Collect data
    models = []
    averages = []
    std_devs = []
    
    for folder, label in MODEL_FOLDERS.items():
        rates = load_pass_rates(folder)
        if rates:
            models.append(label)
            averages.append(np.mean(rates))
            std_devs.append(np.std(rates))
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = ax.bar(models, averages, color=colors, yerr=std_devs, 
                  capsize=5, edgecolor='black', linewidth=1.2)
    
    # Add value labels on top of bars
    for bar, avg in zip(bars, averages):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{avg:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Customize the chart
    ax.set_ylabel('Average Pass Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('A/B Testing Skill Performance by Model (Base Skill)', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_ylim(0, 100)
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.3)
    
    # Add grid for readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=0, fontsize=11)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the chart
    output_path = BASE_PATH / "ab_testing_base_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    # Also print the summary table
    print("\n=== Summary Table ===")
    print(f"{'Model':<10} {'Avg Pass Rate':<15} {'Std Dev':<10} {'N Runs':<8}")
    print("-" * 45)
    for model, avg, std in zip(models, averages, std_devs):
        n_runs = len(load_pass_rates([k for k, v in MODEL_FOLDERS.items() if v == model][0]))
        print(f"{model:<10} {avg:.1f}%{'':<11} {std:.1f}{'':<10} {n_runs:<8}")

if __name__ == "__main__":
    main()

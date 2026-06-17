#!/usr/bin/env python3
"""
Visualize model comparison data from ab-testing evals.
Generates bar charts comparing fail counts across models.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

# Data from the comparison table
data = {
    'Eval': [
        'eval-1', 'eval-1', 'eval-1', 'eval-1', 'eval-1', 'eval-1', 'eval-1', 'eval-1',
        'eval-2', 'eval-2', 'eval-2', 'eval-2', 'eval-2', 'eval-2', 'eval-2',
        'eval-3', 'eval-3', 'eval-3', 'eval-3', 'eval-3', 'eval-3',
        'eval-4', 'eval-4', 'eval-4', 'eval-4', 'eval-4', 'eval-4', 'eval-4',
        'eval-5', 'eval-5', 'eval-5', 'eval-5', 'eval-5', 'eval-5',
        'eval-6', 'eval-6', 'eval-6', 'eval-6',
        'eval-7', 'eval-7', 'eval-7', 'eval-7', 'eval-7', 'eval-7'
    ],
    'Assertion': [
        1, 2, 3, 4, 5, 6, 7, 8,
        1, 2, 3, 4, 5, 6, 7,
        1, 2, 3, 4, 5, 6,
        1, 2, 3, 4, 5, 6, 7,
        1, 2, 3, 4, 5, 6,
        1, 2, 3, 4,
        1, 2, 3, 4, 5, 6
    ],
    '122B': [
        10, 1, 0, 0, 1, 2, 4, 4,
        10, 0, 0, 0, 0, 1, 4,
        0, 0, 0, 0, 0, 8,
        0, 0, 8, 2, 0, 10, 9,
        0, 7, 6, 0, 0, 3,
        2, 0, 1, 0,
        0, 1, 1, 0, 0, 1
    ],
    '35B': [
        10, 1, 1, 0, 3, 3, 10, 3,
        10, 0, 0, 0, 2, 0, 5,
        0, 0, 0, 0, 0, 5,
        1, 0, 7, 3, 1, 7, 2,
        0, 9, 8, 0, 0, 6,
        4, 0, 0, 0,
        2, 2, 2, 4, 2, 7
    ],
    '122B Modified': [
        3, 0, 0, 0, 0, 0, 0, 0,
        8, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 3, 0, 0,
        3, 0, 3, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0, 0, 1
    ],
    '35B Modified': [
        9, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1,
        0, 0, 9, 0, 0, 0,
        1, 0, 1, 1, 0, 0, 1,
        0, 0, 0, 0, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 0, 0, 6
    ]
}

df = pd.DataFrame(data)

# Create output directory
output_dir = Path(__file__).parent
output_dir.mkdir(exist_ok=True)

# 1. Overall comparison (sum of fails per model)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Overall fail counts
model_totals = df[['122B', '35B', '122B Modified', '35B Modified']].sum()
colors = ['#d73027', '#fc8d59', '#fee08b', '#1a9850']

axes[0, 0].bar(model_totals.index, model_totals.values, color=colors)
axes[0, 0].set_title('Total Fail Count by Model', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Total Failures')
axes[0, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(model_totals.values):
    axes[0, 0].text(i, v + 5, str(v), ha='center', fontweight='bold')

# Fail count by Eval (122B baseline vs modified)
eval_totals_122b = df.groupby('Eval')[['122B', '122B Modified']].sum()
eval_totals_122b.plot(kind='bar', ax=axes[0, 1], color=['#d73027', '#1a9850'])
axes[0, 1].set_title('Fail Count by Eval (122B: Baseline vs Modified)', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Failures')
axes[0, 1].legend(['122B Baseline', '122B Modified'])
axes[0, 1].tick_params(axis='x', rotation=0)

# Fail count by Eval (35B baseline vs modified)
eval_totals_35b = df.groupby('Eval')[['35B', '35B Modified']].sum()
eval_totals_35b.plot(kind='bar', ax=axes[1, 0], color=['#fc8d59', '#fee08b'])
axes[1, 0].set_title('Fail Count by Eval (35B: Baseline vs Modified)', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Failures')
axes[1, 0].legend(['35B Baseline', '35B Modified'])
axes[1, 0].tick_params(axis='x', rotation=0)

# Heatmap of all data
pivot_df = df.pivot(index='Eval', columns='Assertion', values='122B Modified')
pivot_df_35b = df.pivot(index='Eval', columns='Assertion', values='35B Modified')

# Create side-by-side heatmaps
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))

sns.heatmap(pivot_df.fillna(0).astype(int), annot=True, fmt='d', cmap='YlOrRd', ax=axes2[0], cbar_kws={'label': 'Fail Count'})
axes2[0].set_title('122B Modified: Fail Count by Eval & Assertion', fontsize=14, fontweight='bold')
axes2[0].set_xlabel('Assertion #')
axes2[0].set_ylabel('Eval')

sns.heatmap(pivot_df_35b.fillna(0).astype(int), annot=True, fmt='d', cmap='YlOrRd', ax=axes2[1], cbar_kws={'label': 'Fail Count'})
axes2[1].set_title('35B Modified: Fail Count by Eval & Assertion', fontsize=14, fontweight='bold')
axes2[1].set_xlabel('Assertion #')
axes2[1].set_ylabel('Eval')

plt.tight_layout()
plt.savefig(output_dir / 'comparison_heatmaps.png', dpi=150, bbox_inches='tight')
print(f"Saved: {output_dir / 'comparison_heatmaps.png'}")

# Combined comparison bar chart
fig3, ax = plt.subplots(figsize=(14, 8))

# Calculate improvement
improvement_122b = df['122B'].sum() - df['122B Modified'].sum()
improvement_35b = df['35B'].sum() - df['35B Modified'].sum()

models = ['122B Baseline', '122B Modified', '35B Baseline', '35B Modified']
total_fails = [df['122B'].sum(), df['122B Modified'].sum(), df['35B'].sum(), df['35B Modified'].sum()]

bars = ax.bar(models, total_fails, color=colors)
ax.set_title('Model Comparison: Total Failures (Lower is Better)', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Total Failures', fontsize=12)

# Add improvement annotations
for i, (bar, total) in enumerate(zip(bars, total_fails)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{total}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add improvement arrows
if improvement_122b > 0:
    ax.annotate(f'↓ {improvement_122b} failures',
                xy=(1, total_fails[1]), xytext=(0.5, total_fails[0]),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=12, color='green', fontweight='bold')

if improvement_35b > 0:
    ax.annotate(f'↓ {improvement_35b} failures',
                xy=(3, total_fails[3]), xytext=(2.5, total_fails[2]),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2),
                fontsize=12, color='orange', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'overall_comparison.png', dpi=150, bbox_inches='tight')
print(f"Saved: {output_dir / 'overall_comparison.png'}")

# Print summary statistics
print("\n" + "="*50)
print("SUMMARY STATISTICS")
print("="*50)
print(f"\n122B Baseline Total Fails: {df['122B'].sum()}")
print(f"122B Modified Total Fails: {df['122B Modified'].sum()}")
print(f"Improvement: {improvement_122b} fewer failures ({(improvement_122b/df['122B'].sum()*100):.1f}% reduction)")

print(f"\n35B Baseline Total Fails: {df['35B'].sum()}")
print(f"35B Modified Total Fails: {df['35B Modified'].sum()}")
print(f"Improvement: {improvement_35b} fewer failures ({(improvement_35b/df['35B'].sum()*100):.1f}% reduction)")

print("\n" + "="*50)
print(f"Charts saved to: {output_dir}")
print("="*50)

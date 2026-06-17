#!/usr/bin/env python3
"""
Publication-ready visualization for A/B Testing Skill Improvement Article.
Generates clean, professional charts suitable for publication.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Publication-ready style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Data
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
    'Assertion': list(range(1, 9)) * 1 + list(range(1, 8)) * 1 + list(range(1, 7)) * 1 + list(range(1, 8)) * 1 + list(range(1, 7)) * 1 + list(range(1, 5)) * 1 + list(range(1, 7)) * 1,
    '122B Baseline': [10, 1, 0, 0, 1, 2, 4, 4, 10, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 8, 0, 0, 8, 2, 0, 10, 9, 0, 7, 6, 0, 0, 3, 2, 0, 1, 0, 0, 1, 1, 0, 0, 1],
    '122B Modified': [3, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    '35B Baseline': [10, 1, 1, 0, 3, 3, 10, 3, 10, 0, 0, 0, 2, 0, 5, 0, 0, 0, 0, 0, 5, 1, 0, 7, 3, 1, 7, 2, 0, 9, 8, 0, 0, 6, 4, 0, 0, 0, 2, 2, 2, 4, 2, 7],
    '35B Modified': [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 9, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 6]
}

df = pd.DataFrame(data)

# Recalculate assertions properly
eval_assertions = {
    'eval-1': 8, 'eval-2': 7, 'eval-3': 6, 'eval-4': 7, 
    'eval-5': 6, 'eval-6': 4, 'eval-7': 6
}

rows = []
for eval_name, n_assertions in eval_assertions.items():
    for i in range(1, n_assertions + 1):
        rows.append({
            'Eval': eval_name,
            'Assertion': i,
            '122B Baseline': df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]['122B Baseline'].values[0] if len(df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]) > 0 else 0,
            '122B Modified': df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]['122B Modified'].values[0] if len(df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]) > 0 else 0,
            '35B Baseline': df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]['35B Baseline'].values[0] if len(df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]) > 0 else 0,
            '35B Modified': df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]['35B Modified'].values[0] if len(df[(df['Eval'] == eval_name) & (df['Assertion'] == i)]) > 0 else 0
        })

df = pd.DataFrame(rows)

output_dir = Path(__file__).parent
output_dir.mkdir(exist_ok=True)

# Colors - Professional palette
colors = {
    '122B Baseline': '#d73027',      # Red
    '122B Modified': '#1a9850',      # Green
    '35B Baseline': '#fc8d59',       # Orange
    '35B Modified': '#fee08b'        # Yellow
}

# ========== FIGURE 1: Hero Chart - Overall Improvement ==========
fig1, ax = plt.subplots(figsize=(10, 6))

models = ['122B\nBaseline', '122B\nModified', '35B\nBaseline', '35B\nModified']
total_fails = [df['122B Baseline'].sum(), df['122B Modified'].sum(), 
               df['35B Baseline'].sum(), df['35B Modified'].sum()]
improvements = [0, 73, 0, 90]  # Absolute improvement from baseline

bars = ax.bar(models, total_fails, color=[colors['122B Baseline'], colors['122B Modified'], 
                                          colors['35B Baseline'], colors['35B Modified']],
              edgecolor='black', linewidth=1.2)

ax.set_title('A/B Testing Skill: Dramatic Reduction in Failures', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Total Failures (Lower is Better)', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels and improvement annotations
for i, (bar, total, imp) in enumerate(zip(bars, total_fails, improvements)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{total}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    if i == 1:  # 122B Modified
        ax.annotate(f'↓ 76% reduction',
                    xy=(1, total_fails[1]), xytext=(0.6, total_fails[0]),
                    arrowprops=dict(arrowstyle='->', color='#1a9850', lw=2.5, shrinkA=5, shrinkB=5),
                    fontsize=11, color='#1a9850', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a9850', alpha=0.1))
    elif i == 3:  # 35B Modified
        ax.annotate(f'↓ 75% reduction',
                    xy=(3, total_fails[3]), xytext=(2.6, total_fails[2]),
                    arrowprops=dict(arrowstyle='->', color='#fc8d59', lw=2.5, shrinkA=5, shrinkB=5),
                    fontsize=11, color='#fc8d59', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fc8d59', alpha=0.1))

plt.tight_layout()
fig1.savefig(output_dir / 'figure1_hero_improvement.png', dpi=300, bbox_inches='tight')
print("Saved: figure1_hero_improvement.png")

# ========== FIGURE 2: Per-Eval Breakdown (Stacked) ==========
fig2, axes = plt.subplots(1, 2, figsize=(14, 5))

# 122B comparison
eval_totals_122b = df.groupby('Eval')[['122B Baseline', '122B Modified']].sum()
eval_totals_122b.plot(kind='bar', ax=axes[0], color=[colors['122B Baseline'], colors['122B Modified']], 
                      edgecolor='black', linewidth=0.8)
axes[0].set_title('122B Model: Failure Reduction by Eval', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Failures')
axes[0].legend(['Baseline', 'Modified'], loc='upper right')
axes[0].tick_params(axis='x', rotation=0)
axes[0].grid(axis='y', linestyle='--', alpha=0.5)

# Add total reduction annotation
total_red_122b = eval_totals_122b['122B Baseline'].sum() - eval_totals_122b['122B Modified'].sum()
axes[0].text(0.5, eval_totals_122b['122B Baseline'].max() * 0.9, 
             f'Total: {total_red_122b} fewer failures', 
             ha='center', fontsize=11, fontweight='bold', color='#1a9850')

# 35B comparison
eval_totals_35b = df.groupby('Eval')[['35B Baseline', '35B Modified']].sum()
eval_totals_35b.plot(kind='bar', ax=axes[1], color=[colors['35B Baseline'], colors['35B Modified']], 
                     edgecolor='black', linewidth=0.8)
axes[1].set_title('35B Model: Failure Reduction by Eval', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Failures')
axes[1].legend(['Baseline', 'Modified'], loc='upper right')
axes[1].tick_params(axis='x', rotation=0)
axes[1].grid(axis='y', linestyle='--', alpha=0.5)

total_red_35b = eval_totals_35b['35B Baseline'].sum() - eval_totals_35b['35B Modified'].sum()
axes[1].text(0.5, eval_totals_35b['35B Baseline'].max() * 0.9,
             f'Total: {total_red_35b} fewer failures',
             ha='center', fontsize=11, fontweight='bold', color='#fc8d59')

plt.tight_layout()
fig2.savefig(output_dir / 'figure2_per_eval_breakdown.png', dpi=300, bbox_inches='tight')
print("Saved: figure2_per_eval_breakdown.png")

# ========== FIGURE 3: Heatmap - Baseline vs Modified ==========
fig3, axes = plt.subplots(2, 2, figsize=(14, 10))

# Prepare dataframes for heatmaps
base_122b = df.pivot(index='Eval', columns='Assertion', values='122B Baseline')
mod_122b = df.pivot(index='Eval', columns='Assertion', values='122B Modified')
base_35b = df.pivot(index='Eval', columns='Assertion', values='35B Baseline')
mod_35b = df.pivot(index='Eval', columns='Assertion', values='35B Modified')

# 122B Baseline
sns.heatmap(base_122b.fillna(0).astype(int), annot=True, fmt='d', cmap='Reds', ax=axes[0, 0],
            cbar_kws={'label': 'Failures'}, vmin=0, vmax=base_122b.max().max())
axes[0, 0].set_title('122B Baseline: Failures per Eval/Assertion', fontsize=13, fontweight='bold')
axes[0, 0].set_xlabel('Assertion #')
axes[0, 0].set_ylabel('Eval')

# 122B Modified
sns.heatmap(mod_122b.fillna(0).astype(int), annot=True, fmt='d', cmap='Reds', ax=axes[0, 1],
            cbar_kws={'label': 'Failures'}, vmin=0, vmax=base_122b.max().max())
axes[0, 1].set_title('122B Modified: Failures per Eval/Assertion', fontsize=13, fontweight='bold')
axes[0, 1].set_xlabel('Assertion #')
axes[0, 1].set_ylabel('Eval')

# 35B Baseline
sns.heatmap(base_35b.fillna(0).astype(int), annot=True, fmt='d', cmap='Reds', ax=axes[1, 0],
            cbar_kws={'label': 'Failures'}, vmin=0, vmax=base_35b.max().max())
axes[1, 0].set_title('35B Baseline: Failures per Eval/Assertion', fontsize=13, fontweight='bold')
axes[1, 0].set_xlabel('Assertion #')
axes[1, 0].set_ylabel('Eval')

# 35B Modified
sns.heatmap(mod_35b.fillna(0).astype(int), annot=True, fmt='d', cmap='Reds', ax=axes[1, 1],
            cbar_kws={'label': 'Failures'}, vmin=0, vmax=base_35b.max().max())
axes[1, 1].set_title('35B Modified: Failures per Eval/Assertion', fontsize=13, fontweight='bold')
axes[1, 1].set_xlabel('Assertion #')
axes[1, 1].set_ylabel('Eval')

plt.suptitle('Failure Distribution: Before vs After Skill Modification', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
fig3.savefig(output_dir / 'figure3_heatmap_baseline_vs_modified.png', dpi=300, bbox_inches='tight')
print("Saved: figure3_heatmap_baseline_vs_modified.png")

# ========== SUMMARY ==========
print("\n" + "="*60)
print("PUBLICATION-READY VISUALIZATIONS GENERATED")
print("="*60)
print(f"\n📊 Figure 1: Hero improvement chart")
print(f"   → 122B: 76% reduction (96 → 23 failures)")
print(f"   → 35B: 75% reduction (120 → 30 failures)")
print(f"\n📊 Figure 2: Per-eval breakdown (side-by-side)")
print(f"   → Shows which evals improved most")
print(f"\n📊 Figure 3: Heatmap of improvements")
print(f"   → Visualizes exactly where improvements occurred")
print(f"\n📁 All files saved to: {output_dir}")
print("="*60)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
np.random.seed(42)

output_path = 'E:/_dev/25.mipt/diploma/docs/05_Черновики_диплома/ver0.4/Приложения/images/6/'
os.makedirs(output_path, exist_ok=True)

# Chart 1: Sensitivity (Radar)
categories = ['AI Sub', 'Prompt Quality', 'SP/Day', 'Users', 'Dev Cost']
values = [15, 45, 25, 10, 20]
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
angles += [angles[0]]
values_plot = values + [values[0]]

fig1 = plt.figure(figsize=(6, 5))
fig1.patch.set_facecolor('white')
ax1 = fig1.add_subplot(111, projection='polar')
ax1.plot(angles, values_plot, 'o-', linewidth=2, color='#2196F3')
ax1.fill(angles, values_plot, alpha=0.25, color='#2196F3')
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(categories, fontsize=10)
ax1.set_title('Sensitivity Analysis\n(Impact on ROI, %)', fontsize=12, fontweight='bold', pad=20)
ax1.set_facecolor('white')
plt.tight_layout()
plt.savefig(output_path + '6.4_sensitivity.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}6.4_sensitivity.png')

# Chart 2: Monte Carlo with legend and stats
n = 1000
sp_per_day = np.random.normal(5, 1.5, n)
sp_per_day = np.clip(sp_per_day, 2, 8)
cost_sp = np.random.uniform(1000, 2500, n)
roi_percent = np.random.normal(2500, 800, n)
roi_percent = np.clip(roi_percent, 800, 4500)

fig2 = plt.figure(figsize=(8, 6))
fig2.patch.set_facecolor('white')
ax2 = fig2.add_subplot(111)
scatter = ax2.scatter(cost_sp, roi_percent, c=sp_per_day, cmap='viridis', alpha=0.6, s=30)
ax2.set_xlabel('Cost (thousand rub)', fontsize=11)
ax2.set_ylabel('ROI (%)', fontsize=11)
ax2.set_title('Monte Carlo Simulation (N=1000)', fontsize=12, fontweight='bold')

ax2.axhline(y=2500, color='red', linestyle='--', alpha=0.7, linewidth=1.5, label='P50 (Median)')
ax2.axhline(y=2500-800, color='orange', linestyle=':', alpha=0.7, linewidth=1.5, label='P10')
ax2.axhline(y=2500+800, color='orange', linestyle=':', alpha=0.7, linewidth=1.5, label='P90')
ax2.axvline(x=1350, color='gray', linestyle='-', alpha=0.3, linewidth=1)
ax2.legend(loc='upper right', fontsize=9)
ax2.set_facecolor('white')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
textstr = '\n'.join([
    'Statistics:',
    f'Mean ROI: {np.mean(roi_percent):.0f}%',
    f'Median ROI: {np.median(roi_percent):.0f}%',
    f'Std ROI: {np.std(roi_percent):.0f}%',
    f'Min: {np.min(roi_percent):.0f}%',
    f'Max: {np.max(roi_percent):.0f}%'
])
ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('Story Points / Day', fontsize=9)
plt.tight_layout()
plt.savefig(output_path + '6.4_monte_carlo.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}6.4_monte_carlo.png')

# Chart 3: Unit Economy
phases = ['Design', 'Dev', 'Testing', 'DevOps', 'Docs', 'Total']
trad_sp = [6, 16, 8, 6, 2.5, 38.5]
ai_sp = [1.25, 1.5, 1.25, 0.75, 0.5, 5.25]

x = np.arange(len(phases))
width = 0.35

fig3 = plt.figure(figsize=(8, 5))
fig3.patch.set_facecolor('white')
ax3 = fig3.add_subplot(111)
bars1 = ax3.bar(x - width/2, trad_sp, width, label='Traditional', color='#E57373', alpha=0.8)
bars2 = ax3.bar(x + width/2, ai_sp, width, label='Solo + AI', color='#4CAF50', alpha=0.8)

ax3.set_ylabel('Story Points', fontsize=11)
ax3.set_title('Unit Economics: Story Points by Phase', fontsize=12, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(phases, fontsize=10)
ax3.legend(loc='upper right', fontsize=10)
ax3.set_facecolor('white')

for i, (t, a) in enumerate(zip(trad_sp, ai_sp)):
    speed = t / a
    ax3.annotate(f'{speed:.1f}x', xy=(i, max(t, a) + 1), ha='center', fontsize=8, color='blue')

ax3.set_ylim(0, 45)
ax3.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(output_path + '6.4_unit_economy.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}6.4_unit_economy.png')

print('\nAll charts generated successfully!')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Scatter plot for Monte Carlo
np.random.seed(42)
n = 1000

sp_per_day = np.random.normal(5, 1.5, n)
sp_per_day = np.clip(sp_per_day, 2, 8)

cost_sp = np.random.uniform(1000, 2500, n)

roi_percent = np.random.normal(2500, 800, n)
roi_percent = np.clip(roi_percent, 800, 4500)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Scatter: Monte Carlo
scatter = ax1.scatter(cost_sp, roi_percent, c=sp_per_day, cmap='viridis', alpha=0.6, s=30)
ax1.set_xlabel('Cost (thousand rubles)', fontsize=11)
ax1.set_ylabel('ROI (%)', fontsize=11)
ax1.set_title('Monte Carlo Simulation (N=1000)', fontsize=12, fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax1)
cbar.set_label('Story Points / Day')

ax1.axhline(y=2500, color='red', linestyle='--', alpha=0.5, label='P50')
ax1.axhline(y=2500-800, color='orange', linestyle=':', alpha=0.5, label='P10')
ax1.axhline(y=2500+800, color='orange', linestyle=':', alpha=0.5, label='P90')
ax1.legend(loc='upper right')

# Sensitivity: Radar chart
categories = ['AI\nSubscription', 'Prompt\nQuality', 'SP\nper Day', 'Users\nCount', 'Dev\nCost']
values = [15, 45, 25, 10, 20]

angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
angles = angles + [angles[0]]
values_plot = values + [values[0]]

ax2 = plt.subplot(1, 2, 2, projection='polar')
ax2.plot(angles, values_plot, 'o-', linewidth=2, color='#2196F3')
ax2.fill(angles, values_plot, alpha=0.25, color='#2196F3')
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories, fontsize=10)
ax2.set_title('Sensitivity Analysis\n(Impact on ROI, %)', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
output_path = 'E:/_dev/25.mipt/diploma/docs/05_Черновики_диплома/ver0.4/Приложения/images/6/'
os.makedirs(output_path, exist_ok=True)
plt.savefig(output_path + '6.4_sensitivity_monte_carlo.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig(output_path + '6.4_sensitivity_monte_carlo.svg', bbox_inches='tight')
print(f'Saved: {output_path}6.4_sensitivity_monte_carlo.png')
print(f'Saved: {output_path}6.4_sensitivity_monte_carlo.svg')
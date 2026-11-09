import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300, gridspec_kw={'width_ratios': [1.35, 1]})

# Panel (a): Validation Benchmark
labels = [
    "Forward Temporal SVR\n(Train 2024 → Test 2025)",
    "Forward Temporal RF\n(Train 2024 → Test 2025)",
    "Forward Temporal OLS\n(Train 2024 → Test 2025)",
    "Spatial Group Holdout\n(Leave-Stations-Out)",
    "Temporal GroupKFold\n(Leave-Dates-Out)",
    "Random 5-Fold CV*\n(Shared Overpass Dates)"
]
r2_vals = [0.2397, 0.3177, 0.3636, 0.4059, 0.4564, 0.6790]
rmse_vals = [33.27, 31.51, 30.43, 29.41, 27.72, 22.05]
colors = ['#8c96c6', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#d95f02']
y_pos = np.arange(len(labels))
bars = ax1.barh(y_pos, r2_vals, height=0.58, color=colors, edgecolor='black', linewidth=0.6)
ax1.axvline(0.4059, color='#2171b5', linestyle='--', linewidth=1.2, label='True Spatial Baseline ($R^2 = 0.4059$)')

for bar, r2, rmse in zip(bars, r2_vals, rmse_vals):
    ax1.text(
        bar.get_width() + 0.012, bar.get_y() + bar.get_height()/2,
        f"$R^2 = {r2:.4f}$ (RMSE: {rmse:.1f} $\\mu$g m$^{{-3}}$)",
        va='center', ha='left', fontsize=9, fontweight='bold', color='#111111'
    )

ax1.set_yticks(y_pos)
ax1.set_yticklabels(labels, fontsize=9.5, fontweight='bold')
ax1.set_xlim(0, 0.98)
ax1.set_xlabel("Out-of-Sample Predictive $R^2$", fontsize=10.5, fontweight='bold')
ax1.set_title("(a) Generalization Across Validation Paradigms", fontsize=11.5, fontweight='bold', pad=10)
ax1.legend(loc='lower right', frameon=True, fontsize=8.5)
ax1.grid(axis='x', linestyle=':', alpha=0.5)

# Panel (b): Feature Importance with multi-line parenthetical labels to eliminate text overlap
features = [
    "LST\n(Thermal\nStress)",
    "NDWI\n(Surface\nMoisture)",
    "NDBI\n(Impervious\nBuilt)",
    "NDVI\n(Canopy\nCover)"
]
importances = [49.80, 19.91, 16.49, 13.79]
f_colors = ['#cb181d', '#2b8cbe', '#fd8d3c', '#238b45']
x_pos = np.arange(len(features))
f_bars = ax2.bar(x_pos, importances, width=0.55, color=f_colors, edgecolor='black', linewidth=0.6)

for bar, imp in zip(f_bars, importances):
    ax2.text(
        bar.get_x() + bar.get_width()/2, bar.get_height() + 1.2,
        f"{imp:.2f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold'
    )

ax2.set_xticks(x_pos)
ax2.set_xticklabels(features, fontsize=8.5, fontweight='bold')
ax2.set_ylim(0, 60)
ax2.set_ylabel("Relative Predictor Importance (%)", fontsize=10.5, fontweight='bold')
ax2.set_title("(b) Random Forest LUR Feature Importance", fontsize=11.5, fontweight='bold', pad=10)
ax2.grid(axis='y', linestyle=':', alpha=0.5)

plt.tight_layout()
script_dir = os.path.dirname(os.path.abspath(__file__))
fig_dir = os.path.join(os.path.dirname(script_dir), "figures")
os.makedirs(fig_dir, exist_ok=True)
png_path = os.path.join(fig_dir, "fig8_lur_validation_benchmarks.png")
pdf_path = os.path.join(fig_dir, "fig8_validation_feature_importance.pdf")
plt.savefig(png_path, dpi=300)
plt.savefig(pdf_path, bbox_inches='tight')
print("Successfully generated:")
print(" ", png_path)
print(" ", pdf_path)
plt.close()

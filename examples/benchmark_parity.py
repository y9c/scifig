#!/usr/bin/env python3
"""Benchmark-parity figure: multi-metric comparison with error bars.

A publication-grade 1x4 figure (3 independent metric panels + a right legend
axis). Each panel has its own tight y-limit and error bars; no grid; large axis
labels; semantic method colors (blue = ours). Demonstrates the capability set an
agent needs to reach published quantitative-comparison quality.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig
from scifig.compose import panel_grid

rng = np.random.default_rng(0)

methods = ["Prime-2.1", "NetMHCpan", "MHCnuggets", "MHCflurry", "DeepNeo",
           "BigMHC-EL", "BigMHC-IM", "BigMHC-retr.", "ImmunoStruct (ours)"]
metrics = ["AUROC", "AUPRC", "Mean PPVn"]
mean = np.array([
    [0.538, 0.212, 0.207], [0.537, 0.214, 0.220], [0.546, 0.246, 0.233],
    [0.577, 0.260, 0.273], [0.767, 0.438, 0.411], [0.588, 0.269, 0.290],
    [0.684, 0.319, 0.333], [0.793, 0.462, 0.445], [0.882, 0.696, 0.514],
])
std = 0.02 + 0.02 * rng.random(mean.shape)
colors = ["#CFCECE", "#F4EEAC", "#FBDFE2", "#D9B9D4", "#DAA87C",
          "#DDF3DE", "#AADCA9", "#8BCF8B", "#3775BA"]
ylims = [(0.50, 0.92), (0.18, 0.74), (0.18, 0.54)]

# Publication look: large font, thick spines, no grid, frameless legend.
scifig.apply_publication_style(scifig.FigureStyle(font_size=20, axes_linewidth=2.0))
fig, _ = panel_grid(1, 4, figsize=(16, 4), legend=None)
axes = fig.axes

handles, labels = [], []
x = np.arange(len(methods))
for j, (m, ylo) in enumerate(zip(metrics, ylims)):
    ax = axes[j]
    for i in range(len(methods)):
        h = ax.bar(i, mean[i, j], yerr=std[i, j], color=colors[i],
                   edgecolor="none", capsize=4)
        if j == 0:
            handles.append(h)
            labels.append(methods[i])
    ax.set_xticks([])
    ax.set_ylim(*ylo)
    ax.set_ylabel(m, fontsize=28)
    ax.grid(False)

# 4th axis = legend
legax = axes[3]
legax.set_axis_off()
legax.legend(handles, labels, loc="center", frameon=False, fontsize=16)

fig.tight_layout(pad=2)
scifig.finalize_figure(fig, "out/benchmark_parity", formats=["pdf", "png"], dpi=600)
print("wrote out/benchmark_parity.pdf/png")

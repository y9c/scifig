#!/usr/bin/env python3
"""Grouped bar chart in the publication house style (plain matplotlib + _house)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, palette_labels, save, finish, bar_labels

style(font_size=6.0, axes_linewidth=0.8)
fig, ax = plt.subplots(figsize=(4.2, 3.0))

categories = ["A", "B", "C", "D"]
series = np.array([[0.92, 0.88, 0.85, 0.90],
                   [0.85, 0.82, 0.88, 0.84],
                   [0.78, 0.80, 0.82, 0.79]])
labels = ["Ours", "Baseline X", "Baseline Y"]
colors = palette_labels(labels, ours_marker="Ours")

x = np.arange(len(categories))
n, w = series.shape[0], 0.8 / series.shape[0]
bars = []
for i, (row, lab) in enumerate(zip(series, labels)):
    off = (i - (n - 1) / 2) * w
    b = ax.bar(x + off, row, width=w, label=lab, color=colors[i],
               edgecolor="black", linewidth=0.5)
    bars.append(b)
for b in bars:
    bar_labels(ax, b, fmt="{:.2f}")

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_ylabel("Score")
ax.set_ylim(0.70, 1.02)
ax.legend(frameon=False, fontsize=6)
finish(ax, grid=False)
save(fig, "out/grouped_bar", formats=("pdf", "png"), dpi=300)
print("wrote out/grouped_bar.pdf/png")

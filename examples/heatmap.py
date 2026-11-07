#!/usr/bin/env python3
"""Heatmap with labels, colorbar, and an inset zoom (plain matplotlib + _house)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, heatmap, add_inset, save

style(font_size=6.0, axes_linewidth=0.8)
fig, ax = plt.subplots(figsize=(6.0, 4.6))

np.random.seed(42)
m = np.random.rand(8, 8)
m = (m + m.T) / 2
labels = [f"F{i+1}" for i in range(8)]

heatmap(ax, m, x_labels=labels, y_labels=labels, cmap="magma", cbar_label="Correlation")

# inset zoom of the top-left 4x4 corner
ax_in = add_inset(ax, "upper right", size="35%")
heatmap(ax_in, m[:4, :4], cmap="magma")
ax_in.set_xticks([]); ax_in.set_yticks([])

save(fig, "out/heatmap", formats=("pdf", "png"), dpi=300)
print("wrote out/heatmap.pdf/png")

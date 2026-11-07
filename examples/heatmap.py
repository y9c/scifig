#!/usr/bin/env python3
"""Heatmap with labels, colorbar, and a small inset zoom (no colorbar clash)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, heatmap, add_inset, save

style(font_size=6.0, axes_linewidth=0.8)
fig, ax = plt.subplots(figsize=(5.4, 4.4))

np.random.seed(42)
m = np.random.rand(8, 8)
m = (m + m.T) / 2
labels = [f"F{i+1}" for i in range(8)]

heatmap(ax, m, x_labels=labels, y_labels=labels, cmap="magma", cbar_label="Correlation")

# small inset zoom of the top-left 3x3 corner (no colorbar, so no clash)
ax_in = add_inset(ax, "upper right", size="26%")
ax_in.imshow(m[:3, :3], cmap="magma", aspect="auto")
ax_in.set_xticks([]); ax_in.set_yticks([])
ax_in.set_xlabel("zoom", fontsize=5)

save(fig, "out/heatmap", formats=("pdf", "png"), dpi=300)
print("wrote out/heatmap.pdf/png")

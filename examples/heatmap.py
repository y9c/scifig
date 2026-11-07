#!/usr/bin/env python3
"""Heatmap with labels, colorbar, and an inset zoom."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=12, axes_linewidth=2))
fig, ax = scifig.create_subplots(1, 1, figsize=(8, 6))

np.random.seed(42)
m = np.random.rand(8, 8)
m = (m + m.T) / 2
labels = [f"F{i+1}" for i in range(8)]

scifig.make_heatmap(ax, m, x_labels=labels, y_labels=labels, cmap="magma", cbar_label="Correlation")

# inset zoom of the top-left 4x4 corner
ax_in = scifig.add_inset(ax, "upper right", size="35%")
scifig.make_heatmap(ax_in, m[:4, :4], cmap="magma")
ax_in.set_xticks([]); ax_in.set_yticks([])

scifig.finalize_figure(fig, "out/heatmap", formats=["png", "pdf"], dpi=300)
print("wrote out/heatmap.png/pdf")

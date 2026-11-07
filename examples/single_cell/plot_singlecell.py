#!/usr/bin/env python3
"""Single-cell figure: UMAP embedding + marker dot plot + per-cluster violin."""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # examples/
import numpy as np
import scifig
from single_cell.data import build
from biofigs import umap_scatter, dot_plot, violin_groups

d = build()

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.5, axes_linewidth=0.8))
fig, axes = scifig.panel_grid(1, 3, figsize=scifig.nature_figsize("double", aspect=0.36),
                             legend=None)

# a) UMAP embedding coloured by cluster
umap_scatter(axes[0], d["umap"][:, 0], d["umap"][:, 1], d["labels"],
                    palette="tol_bright", size=10)
axes[0].set_title("UMAP")

# b) marker dot plot (colour = mean expression, size = % expressed)
dot_plot(axes[1], d["mean_by_cluster"], d["markers"], d["clusters"],
                pct=d["pct_by_cluster"], cmap="viridis")
axes[1].set_title("Marker expression")

# c) per-cluster violin of a single marker (CD3D, row 0)
violin_groups(axes[2], d["expr"][0], d["labels"], order=d["clusters"],
                     ylabel="CD3D expression")
axes[2].set_title("CD3D")

scifig.add_panel_labels(axes, case="lower")
for a in axes:
    scifig.finish_axes(a, grid=False)
fig.tight_layout(pad=0.8)
scifig.finalize_figure(fig, "out/single_cell", formats=["pdf", "png"], dpi=600)
print("wrote out/single_cell.pdf/png")

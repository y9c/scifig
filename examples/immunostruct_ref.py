#!/usr/bin/env python3
"""Quantitative multi-method comparison bar (house style, plain matplotlib).

Reference template: several methods compared across metrics, semantic colors
(gray/pastel baselines, green improvements, blue = our method), vector PDF.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, grouped_bar, palette_labels, finish, save

methods = ["Prime-2.1", "NetMHCpan", "MHCnuggets", "MHCflurry", "DeepNeo",
           "BigMHC-EL", "BigMHC-IM", "BigMHC-retr.", "ImmunoStruct (ours)"]
metrics = ["AUROC", "AUPRC", "Mean PPVn"]
mean = np.array([
    [0.538, 0.212, 0.207], [0.537, 0.214, 0.220], [0.546, 0.246, 0.233],
    [0.577, 0.260, 0.273], [0.767, 0.438, 0.411], [0.588, 0.269, 0.290],
    [0.684, 0.319, 0.301], [0.793, 0.462, 0.445], [0.882, 0.696, 0.514],
])

style(font_size=6.0, axes_linewidth=0.8)
fig, ax = plt.subplots(figsize=(5.0, 5.0))

# metrics on x; one series per method (semantic colors, blue = ours)
colors = palette_labels(methods, ours_marker="ImmunoStruct (ours)")
grouped_bar(ax, metrics, [list(row) for row in mean], methods,
            ylabel="Score", colors=colors)
ax.set_ylim(0.0, 1.05)
ax.legend(frameon=False, ncol=3, fontsize=5.5, loc="upper center",
          bbox_to_anchor=(0.5, 1.02), handlelength=1.0)
finish(ax, grid=False)

save(fig, "out/immunostruct_ref", formats=("pdf", "png"), dpi=600)
print("wrote out/immunostruct_ref.pdf/png")

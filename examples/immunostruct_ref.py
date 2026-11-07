#!/usr/bin/env python3
"""Reproduce the ImmunoStruct comparison chart using the grouped_bar archetype.

This is the reference style template: a single-column Nature-like grouped bar
built from the ``grouped_bar`` archetype (shared house look: Arial 6pt, thin
spines, semantic colors, vector PDF).
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

# Real data from figure_ImmunoStruct/raw_data.py
methods = ["Prime-2.1", "NetMHCpan", "MHCnuggets", "MHCflurry", "DeepNeo",
           "BigMHC-EL", "BigMHC-IM", "BigMHC-retr.", "ImmunoStruct (ours)"]
metrics = ["AUROC", "AUPRC", "Mean PPVn"]
mean = np.array([
    [0.538, 0.212, 0.207],
    [0.537, 0.214, 0.220],
    [0.546, 0.246, 0.233],
    [0.577, 0.260, 0.273],
    [0.767, 0.438, 0.411],
    [0.588, 0.269, 0.290],
    [0.684, 0.319, 0.301],
    [0.793, 0.462, 0.445],
    [0.882, 0.696, 0.514],
])


def main():
    # Nature single-column size, Arial 6pt, thin spines, vector PDF
    scifig.apply_publication_style(scifig.FigureStyle(font_size=6.0, axes_linewidth=0.8))
    fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("half", aspect=1.0))

    # metrics on x (3 positions); each method is a series of its 3 metric values
    colors = scifig.assign_colors(methods, ours_marker="ImmunoStruct (ours)")
    scifig.make_grouped_bar(
        ax, metrics, [list(row) for row in mean], methods,
        ylabel="Score", colors=colors,
    )
    ax.set_ylim(0.0, 1.05)
    # legend inside, spanning the top, compact
    ax.legend(frameon=False, ncol=3, fontsize=5.5, loc="upper center",
              bbox_to_anchor=(0.5, 1.02), handlelength=1.0)
    scifig.add_panel_label(ax, "a")

    scifig.finalize_figure(fig, "out/immunostruct_ref", formats=["pdf", "png"], dpi=600)
    print("wrote out/immunostruct_ref.pdf/png")


if __name__ == "__main__":
    main()

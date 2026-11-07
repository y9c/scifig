#!/usr/bin/env python3
"""Grouped bar chart in the publication house style + Python annotation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=16, axes_linewidth=2))
fig, ax = scifig.create_subplots(1, 1, figsize=(3.5, 2.625))

categories = ["Metric A", "Metric B", "Metric C", "Metric D"]
series = [[0.92, 0.88, 0.85, 0.90], [0.85, 0.82, 0.88, 0.84], [0.78, 0.80, 0.82, 0.79]]
labels = ["Ours", "Baseline X", "Baseline Y"]

bars = scifig.make_grouped_bar(
    ax, categories, series, labels,
    ylabel="Score",
    colors=[scifig.PALETTE["blue_main"], scifig.PALETTE["green_3"], scifig.PALETTE["red_strong"]],
    annotate=False,
)
scifig.annotate_bars(ax, bars, fmt="{:.2f}", fontsize=7)
ax.set_ylim(0.7, 1.02)

scifig.finalize_figure(fig, "out/grouped_bar", formats=["png", "pdf"], dpi=300)
print("wrote out/grouped_bar.png/pdf")

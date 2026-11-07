#!/usr/bin/env python3
"""Stacked composition bar: cell-type proportion per sample/condition."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _house import style, stacked_bar, save, finish

style()
fig, ax = plt.subplots(figsize=(4.2, 3.0))

samples = ["Healthy", "Disease", "Treated"]
cell_types = ["CD4 T", "CD8 T", "B", "Mono", "NK"]
# one vector per cell-type (stacked layer), length == len(samples)
parts = [
    [30, 15, 28],   # CD4 T
    [25, 12, 24],   # CD8 T
    [20, 40, 22],   # B
    [15, 18, 14],   # Mono
    [10, 15, 12],   # NK
]

stacked_bar(ax, samples, parts, cell_types, ylabel="% of cells")
finish(ax, grid=False)
save(fig, "out/stacked_bar", dpi=600)
print("wrote out/stacked_bar.pdf")

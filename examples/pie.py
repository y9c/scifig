#!/usr/bin/env python3
"""Donut/pie: composition breakdown (flat, no 3D)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _house import style, pie, save

style()
fig, ax = plt.subplots(figsize=(3.4, 3.4))

labels = ["T cell", "B cell", "Monocyte", "NK cell", "Other"]
values = [34, 26, 18, 14, 8]

pie(ax, values, labels)
ax.set_title("Cell-type composition", pad=6)
save(fig, "out/pie", dpi=600)
print("wrote out/pie.pdf")

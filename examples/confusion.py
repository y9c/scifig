#!/usr/bin/env python3
"""Confusion matrix (clinical classifier) — annotated, vector."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _house import style, confusion, save, finish

style()
fig, ax = plt.subplots(figsize=(3.5, 3.2))

cm = [[182, 12, 6], [9, 191, 8], [5, 7, 188]]
labels = ["Healthy", "Benign", "Malignant"]

confusion(ax, cm, labels=labels, cmap="Blues")
finish(ax, grid=False)
save(fig, "out/confusion", dpi=600)
print("wrote out/confusion.pdf")

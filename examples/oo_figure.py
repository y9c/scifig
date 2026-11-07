#!/usr/bin/env python3
"""Object-oriented figure builder demo.

Same engine as FigureSpec/render_spec, but built with typed Panel objects.
Object-oriented construction; style/colors/polish/layout are automatic.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
from scifig.figure import Figure, BarPanel, TrendPanel

np.random.seed(3)
x = np.linspace(0, 50, 60)

fig = Figure(width="double", aspect=0.4, ncols=2)

# a) grouped accuracy bars
fig.add(BarPanel(
    categories=["VQA", "OCR", "Chart"],
    series=[[0.92, 0.89, 0.90], [0.83, 0.80, 0.84], [0.78, 0.76, 0.80]],
    labels=["Our method", "Baseline A", "Baseline B"],
    our_marker="Our method", ylabel="Accuracy",
))

# b) training curves with uncertainty band
fig.add(TrendPanel(
    x=x, ys=[0.9 - 0.3 * np.exp(-x / 16) + np.random.normal(0, 0.002, x.size),
             0.8 - 0.3 * np.exp(-x / 16) + np.random.normal(0, 0.003, x.size)],
    labels=["Our method", "Baseline A"], our_marker="Our method",
    ylabel="Validation accuracy", xlabel="Epoch",
))

fig.savefig("out/oo_figure", formats=["pdf", "png"])
print("wrote out/oo_figure.pdf/png (OO Figure + typed Panels)")

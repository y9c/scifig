#!/usr/bin/env python3
"""Declarative multi-panel figure (agent-oriented).

Describe the figure with a ``FigureSpec``; scifig enforces the unified house
style (semantic colors, one shared legend, lowercase Nature panel letters, thin
Arial spines, vector PDF). This is the recommended way to drive scifig from an
agent: fill the spec, not hand-write each panel.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

np.random.seed(11)
rng = np.random.default_rng(11)

# realistic benchmark story: 4 methods, 3 tasks, per-task accuracy at saturation
x = np.linspace(0, 50, 60)

def curve(base):
    mean = base - 0.30 * np.exp(-x / 16)
    std = 0.02 + 0.01 * np.exp(-x / 12)
    return np.stack([mean, std], axis=1)

spec = scifig.FigureSpec(
    width="double", aspect=0.40, font_size=6.5,
    ncols=3,  # one row: a | b | c
    panel_case="lower",  # Nature letters a, b, c
    panels=[
        # a) grouped accuracy bars (3 tasks, 4 methods), semantic colors
        dict(type="bar", categories=["VQA", "OCR", "Chart"],
             series=[[0.92, 0.89, 0.90], [0.83, 0.80, 0.84], [0.78, 0.76, 0.80], [0.70, 0.72, 0.74]],
             labels=["Our method", "Baseline A", "Baseline B", "Baseline C"],
             ours_marker="Our method",  # blue for ours automatically
             ylabel="Accuracy", ylim=(0.65, 1.0)),
        # b) training curves with uncertainty bands
        dict(type="trend", x=x,
             ys=[curve(0.90), curve(0.83), curve(0.78), curve(0.70)],
             labels=["Our method", "Baseline A", "Baseline B", "Baseline C"],
             ylabel="Validation accuracy", xlabel="Epoch"),
        # c) ablation bars with value annotations
        dict(type="bar", categories=["Full", "-OCR", "-Chart", "-Audio", "-Pretrain"],
             series=[[0.92, 0.87, 0.85, 0.89, 0.71]],
             labels=["Ablation"], ylabel="Accuracy", annotate=True,
             ylim=(0.6, 1.0)),
    ],
)

fig, axes = scifig.render_spec(spec, "out/spec_benchmark", formats=["pdf", "png"], dpi=600)
print("wrote out/spec_benchmark.pdf/png")

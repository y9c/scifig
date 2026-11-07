#!/usr/bin/env python3
"""Publication-grade Nature full-page figure (2x3 grid).

Mimics a real top-journal full-page (double-column) results figure: six panels
carrying one coherent story (4 methods, 3 capability axes), semantic colors,
shared legend, lowercase Nature panel letters, and full editorial polish
(readable ticks, minor ticks, subtle grid, tight y-bands, bar edges, value
labels). Vector PDF is the primary output.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

np.random.seed(0)
rng = np.random.default_rng(0)
x = np.linspace(0, 50, 60)


def curve(base, steep=16):
    mean = base - 0.30 * np.exp(-x / steep)
    std = 0.015 + 0.010 * np.exp(-x / 12)
    return np.stack([mean, std], axis=1)


ours = [0.93, 0.92, 0.91]
base_a = [0.85, 0.83, 0.82]
base_b = [0.78, 0.77, 0.76]
base_c = [0.70, 0.71, 0.72]

rel = [
    [0.93, 0.92, 0.91], [0.85, 0.83, 0.82], [0.78, 0.77, 0.76], [0.70, 0.71, 0.72],
]

spec = scifig.FigureSpec(
    width="double", aspect=0.52, ncols=3, font_size=6.5, panel_case="lower",
    panels=[
        # a) grouped bars, 3 tasks x 4 methods
        dict(type="bar", categories=["VQA", "Chart", "OCR"],
             series=rel, labels=["Our method", "Baseline A", "Baseline B", "Baseline C"],
             our_marker="Our method", ylabel="Accuracy", ylim=(0.62, 1.0)),
        # b) training curves with CI bands
        dict(type="trend", x=x,
             ys=[curve(0.92), curve(0.84), curve(0.77), curve(0.70)],
             labels=["Our method", "Baseline A", "Baseline B", "Baseline C"],
             our_marker="Our method",
             ylabel="Validation accuracy", xlabel="Epoch"),
        # c) latency vs accuracy
        dict(type="scatter", x=np.array([12, 15, 19, 24, 30, 38, 48, 60, 75, 93, 115]),
             y=0.58 + 0.32 * (1 - np.exp(-(np.array([12, 15, 19, 24, 30, 38, 48, 60, 75, 93, 115]) - 10) / 25)),
             labels=["Config"], ylabel="Accuracy", xlabel="Latency (ms)"),
        # d) ablation bars (annotated)
        dict(type="bar", categories=["Full", "-OCR", "-Chart", "-Audio", "-Pretrain"],
             series=[[0.92, 0.87, 0.85, 0.89, 0.71]],
             labels=["Component"], ylabel="Accuracy", annotate=True,
             ylim=(0.62, 1.0)),
        # e) feature correlation heatmap
        dict(type="heatmap",
             matrix=[[1.00, 0.62, 0.41, 0.35, 0.28],
                     [0.62, 1.00, 0.70, 0.44, 0.31],
                     [0.41, 0.70, 1.00, 0.78, 0.52],
                     [0.35, 0.44, 0.78, 1.00, 0.66],
                     [0.28, 0.31, 0.52, 0.66, 1.00]],
             x_labels=["Img", "Txt", "OCR", "Chart", "Audio"],
             y_labels=["Img", "Txt", "OCR", "Chart", "Audio"],
             cmap="RdBu_r", cbar_label="Pearson r"),
        # f) train vs valid with significance
        dict(type="trend", x=x,
             ys=[0.92 - 0.42 * np.exp(-x / 12), 0.87 - 0.33 * np.exp(-x / 18)],
             labels=["Train", "Valid"], our_marker="Train",
             ylabel="Accuracy", xlabel="Epoch"),
    ],
)

fig, axes = scifig.render_spec(spec, "out/nature_fullpage", formats=["pdf", "png"], dpi=600)
print("wrote out/nature_fullpage.pdf/png")

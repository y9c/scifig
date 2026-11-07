#!/usr/bin/env python3
"""Full multi-panel figure sized to a Nature layout.

Builds the same 2x3 grid at BOTH a Nature single-column (3.5in) and a Nature
full-page / double-column (7.2in) width, with Arial ~6pt text and thin spines.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

x = np.linspace(0, 10, 40)


def build(width_in, font_size, out_base):
    """Draw the 2x3 grid at the given final width, save PNG+PDF."""
    style = scifig.FigureStyle(font_size=font_size, axes_linewidth=0.8)
    scifig.apply_publication_style(style)
    # figure is exactly the requested printed width, so point sizes map 1:1
    fig, axes = scifig.panel_grid(2, 3, figsize=(width_in, width_in * 0.55))
    ax_a, ax_b, ax_c, ax_d, ax_e, ax_f = axes

    scifig.make_grouped_bar(
        ax_a, ["M1", "M2", "M3"], [[0.9, 0.8, 0.7], [0.7, 0.6, 0.5]],
        ["Ours", "Base"], ylabel="Score",
        colors=[scifig.PALETTE["blue_main"], scifig.PALETTE["red_strong"]],
    )
    ax_a.set_ylim(0.4, 1.02)

    m = 0.5 + 0.4 * (1 - np.exp(-x / 3))
    std = 0.03 * np.ones_like(x)
    scifig.make_trend(
        ax_b, x,
        [np.stack([m, std], axis=1), np.stack([m - 0.08, std], axis=1)],
        ["Model A", "Model B"], ylabel="Accuracy", xlabel="Steps",
    )

    np.random.seed(1)
    scifig.make_scatter(ax_c, x, x * 0.6 + 0.2 + 0.05 * np.random.randn(40),
                        label="Samples", color=scifig.PALETTE["teal"])
    ax_c.set_xlabel("x"); ax_c.set_ylabel("y")

    np.random.seed(2)
    mat = np.random.rand(6, 6)
    mat = (mat + mat.T) / 2
    scifig.make_heatmap(ax_d, mat, cmap="magma", cbar_label="Corr")

    scifig.make_scatter(ax_e, x, x * 0.6 + 0.2, label="Samples",
                        color=scifig.PALETTE["violet"])
    ax_e.set_xlabel("x"); ax_e.set_ylabel("y")

    scifig.make_trend(ax_f, x, [m, m - 0.1], ["A", "B"], ylabel="Score")
    scifig.add_sig(ax_f, 0, 1, y=0.90, marker="***")
    ax_f.set_ylim(0.2, 1.05)

    scifig.add_panel_labels(axes, case="lower")      # Nature: a, b, c
    scifig.shared_legend(fig, location="lower center", ncol=2)

    # Vector-first: primary output is the PDF (formats default to it)
    scifig.finalize_figure(fig, out_base, formats=["pdf"], dpi=600)
    print(f"wrote {out_base}.pdf  ({width_in:.2f}in wide, font {font_size}pt, Arial)")


if __name__ == "__main__":
    build(3.50, 6.0, "out/nature_single")   # half-page / single column
    build(7.20, 7.0, "out/nature_double")   # full page / double column

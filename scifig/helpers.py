"""Plot helpers for publication-style matplotlib figures.

Implements the function contracts described in the skill's ``api.md``:
``make_grouped_bar``, ``annotate_bars``, ``make_trend``, ``make_heatmap``,
``make_scatter``, and ``make_sphere_illustration``.

All helpers take an existing ``Axes`` and mutate it, returning whatever is
useful for the caller (e.g. the last ``BarContainer`` for annotation).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from .palette import DEFAULT_COLORS

__all__ = [
    "make_grouped_bar",
    "annotate_bars",
    "make_trend",
    "make_heatmap",
    "make_scatter",
    "make_sphere_illustration",
]


def _as_1d(x):
    return np.asarray(x, dtype=float)


# ---------------------------------------------------------------------------
# Bars
# ---------------------------------------------------------------------------
def make_grouped_bar(
    ax,
    categories,
    series,
    labels,
    ylabel="Value",
    colors=None,
    annotate=False,
    yerr=None,
    capsize=3,
    hide_xticks=False,
    **bar_kw,
):
    """Render grouped bars.

    ``categories``: list of x labels. ``series``: list of arrays (one per
    group) each the same length as ``categories``. ``labels``: legend labels.
    Returns the last ``BarContainer`` (for use with ``annotate_bars``).
    """
    cats = list(categories)
    s = [np.asarray(sv, dtype=float) for sv in series]
    n_cat = len(cats)
    for sv in s:
        if sv.ndim != 1 or len(sv) != n_cat:
            raise ValueError("each series must be 1D and match len(categories)")
    if len(s) != len(labels):
        raise ValueError("len(series) must equal len(labels)")
    colors = list(colors) if colors is not None else list(DEFAULT_COLORS)
    # deliberate edge stroke: separates bars cleanly in print (the "human" touch)
    edgecolor = bar_kw.pop("edgecolor", "black")
    elw = bar_kw.pop("linewidth", None)
    if elw is None:
        elw = 0.5
    if yerr is not None and edgecolor == "black":
        # with error bars, drop the heavy black bar stroke (ecolor carries it)
        elw = 0.0
        edgecolor = "none"

    n_group = len(s)
    total = 1.0
    width = total / (n_group + 1)
    x = np.arange(n_cat)
    last = None
    for gi, (sv, lab) in enumerate(zip(s, labels)):
        offset = (gi - (n_group - 1) / 2.0) * width
        yerr_gi = None
        if yerr is not None:
            ye = np.asarray(yerr, float)
            if ye.ndim == 2 and ye.shape[0] == len(s):
                yerr_gi = ye[gi]
            elif ye.ndim == 1:
                yerr_gi = ye
        bars = ax.bar(
            x + offset,
            sv,
            width=width,
            label=lab,
            color=colors[gi % len(colors)],
            edgecolor=edgecolor,
            linewidth=elw,
            yerr=yerr_gi,
            error_kw={"ecolor": "black", "capsize": capsize, "linewidth": 0.7}
            if yerr_gi is not None else None,
            **bar_kw,
        )
        last = bars
    if hide_xticks:
        ax.set_xticks([])
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(cats)
    ax.set_ylabel(ylabel)
    if any(str(lab) for lab in labels):
        ax.legend(frameon=False)
    if annotate and last is not None:
        annotate_bars(ax, last)
    return last


def annotate_bars(ax, bars, fmt="{:.2f}", fontsize=None, padding=3):
    """Add text above each bar in a ``BarContainer``.

    ``fontsize`` defaults to the current base font size
    (``rcParams['font.size']``) so annotations stay proportionate at any scale.
    """
    if fontsize is None:
        fontsize = plt.rcParams.get("font.size", 10)
    for rect in bars:
        h = rect.get_height()
        if h is None or np.isnan(h):
            continue
        ax.annotate(
            fmt.format(h),
            (rect.get_x() + rect.get_width() / 2.0, h),
            xytext=(0, padding),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


# ---------------------------------------------------------------------------
# Trends
# ---------------------------------------------------------------------------
def make_trend(
    ax,
    x,
    y_series,
    labels,
    colors=None,
    ylabel=None,
    xlabel=None,
    show_shadow=True,
    linestyles=None,
    **plot_kw,
):
    """Plot multiple lines with an optional uncertainty band.

    ``y_series``: list of 1D arrays (same length as ``x``). If a series is a
    2-column array (mean, std) and ``show_shadow`` is True, a ``fill_between``
    uncertainty band is drawn. Returns the list of ``Line2D`` artists.
    """
    x = _as_1d(x)
    colors = list(colors) if colors is not None else list(DEFAULT_COLORS)
    if linestyles is None:
        linestyles = ["-"] * len(y_series)
    lines = []
    for i, (yv, lab) in enumerate(zip(y_series, labels)):
        yv = np.asarray(yv, dtype=float)
        if yv.ndim == 1:
            mean, std = yv, None
        elif yv.ndim == 2 and yv.shape[1] >= 2:
            mean, std = yv[:, 0], yv[:, 1]
        else:
            raise ValueError("each series must be 1D or a (N,2) mean/std array")
        if len(mean) != len(x):
            raise ValueError("each series must have the same length as x")
        c = colors[i % len(colors)]
        line = ax.plot(x, mean, label=lab, color=c, linestyle=linestyles[i], **plot_kw)
        lines.append(line[0])
        if show_shadow and std is not None:
            ax.fill_between(x, mean - std, mean + std, color=c, alpha=0.18, linewidth=0)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if any(str(lbl) for lbl in labels):
        ax.legend(frameon=False)
    return lines


# ---------------------------------------------------------------------------
# Heatmap
# ---------------------------------------------------------------------------
def make_heatmap(
    ax,
    matrix,
    x_labels=None,
    y_labels=None,
    cmap="magma",
    cbar_label=None,
    annotate=False,
    fmt="{:.2f}",
):
    """Render a 2D heatmap with optional colorbar label and cell annotations."""
    m = np.asarray(matrix, dtype=float)
    if m.ndim != 2:
        raise ValueError("matrix must be 2D")
    im = ax.imshow(m, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(m.shape[1]))
    ax.set_yticks(np.arange(m.shape[0]))
    if x_labels is not None:
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
    if y_labels is not None:
        ax.set_yticklabels(y_labels)
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.82)
    if cbar_label:
        cbar.set_label(cbar_label, rotation=270, labelpad=15)
    if annotate:
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                ax.text(j, i, fmt.format(m[i, j]), ha="center", va="center", color="white")
    return im


# ---------------------------------------------------------------------------
# Scatter
# ---------------------------------------------------------------------------
def make_scatter(ax, x, y, label=None, color=None, size=50, alpha=0.7, **kw):
    """Single-series scatter. ``x``, ``y`` are same-length 1D arrays."""
    x = _as_1d(x)
    y = _as_1d(y)
    if len(x) != len(y):
        raise ValueError("x and y must be the same length")
    if color is None:
        color = DEFAULT_COLORS[0]
    s = ax.scatter(x, y, s=size, c=color, alpha=alpha, label=label, **kw)
    if label:
        ax.legend(frameon=False)
    return s


# ---------------------------------------------------------------------------
# Sphere illustration
# ---------------------------------------------------------------------------
def make_sphere_illustration(
    ax,
    light_dir=(-0.5, 0.5, 0.8),
    resolution=128,
    alpha=0.6,
    radius=0.9,
    center=(0.0, 0.0),
):
    """Draw a shaded 2D disk to mimic a 3D sphere. Use for conceptual diagrams."""
    light_dir = np.asarray(light_dir, dtype=float)
    light_dir = light_dir / np.linalg.norm(light_dir)
    n = int(resolution)
    theta = np.linspace(0, 2 * np.pi, n)
    phi = np.linspace(0, np.pi, n)
    TH, PH = np.meshgrid(theta, phi)
    # normal vector on the disk in the xy-plane, tilt by phi for shading
    nx = np.sin(PH) * np.cos(TH)
    ny = np.sin(PH) * np.sin(TH)
    nz = np.cos(PH)
    norm = np.stack([nx, ny, nz], axis=-1)
    shade = np.clip(norm @ light_dir, 0, 1)
    # grayscale-style shading; user can recolor by setting cmap
    ax.imshow(
        shade,
        extent=[
            center[0] - radius,
            center[0] + radius,
            center[1] - radius,
            center[1] + radius,
        ],
        cmap="bone",
        alpha=alpha,
        origin="lower",
    )
    ax.set_axis_off()
    ax.set_aspect("equal")
    return ax

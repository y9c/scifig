"""Callable archetype figures (agent-oriented templates).

Each function is a complete, publication-styled figure for one common science
figure shape. An agent picks the matching archetype, passes data, and gets a
style-consistent figure. This mirrors the Icarus-Figures A1-A13 concept, merged
with scifig's house style (semantic colors, thin spines, Nature sizing, vector
PDF via ``finalize_figure``).

All archetypes return ``(fig, ax)`` (or ``(fig, axes)`` for multi-panel ones).
"""

from __future__ import annotations

import numpy as np

from .helpers import make_heatmap
from .palette import DEFAULT_COLORS, PALETTE
from .style import FigureStyle, apply_publication_style, create_subplots, finalize_figure

__all__ = [
    "timeseries_ci",
    "sorted_bar",
    "grouped_bar",
    "scatter_fit",
    "heatmap",
    "tornado",
    "confusion",
]


def _style(font_size=6.0, axes_linewidth=0.8):
    apply_publication_style(FigureStyle(font_size=font_size, axes_linewidth=axes_linewidth))


def _fig(ax, figsize):
    if ax is None:
        fig, ax = create_subplots(1, 1, figsize=figsize)
        return fig, ax
    return ax.figure, ax


def save(fig, name, formats=None, dpi=600):
    """Save an archetype figure (vector PDF by default)."""
    return finalize_figure(fig, name, formats=formats or ["pdf"], dpi=dpi)


# ---------------------------------------------------------------------------
def timeseries_ci(
    t,
    y_obs=None,
    y_hat=None,
    lo=None,
    hi=None,
    *,
    xlabel="Time",
    ylabel="Value",
    label="Fit",
    color=PALETTE["blue_main"],
    figsize=(3.5, 2.5),
    ax=None,
):
    """A1 — time series / fitted curve with a confidence band."""
    _style()
    fig, ax = _fig(ax, figsize)
    if lo is not None and hi is not None:
        ax.fill_between(t, lo, hi, color=color, alpha=0.18, linewidth=0)
    if y_hat is not None:
        ax.plot(t, y_hat, color=color, linewidth=1.2, label=label)
    if y_obs is not None:
        ax.scatter(t, y_obs, color="k", s=8, alpha=0.6, label="Observed")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, fontsize=6)
    return fig, ax


def sorted_bar(
    names,
    values,
    *,
    xlabel="Value",
    fmt="{:.2f}",
    color=PALETTE["blue_main"],
    figsize=(3.5, 2.8),
    ax=None,
):
    """A2 — horizontal bar sorted by value (ranking)."""
    _style()
    order = np.argsort(np.asarray(values))
    names = [names[i] for i in order]
    values = np.asarray(values)[order]
    fig, ax = _fig(ax, figsize)
    bars = ax.barh(names, values, color=color, height=0.62)
    for b, v in zip(bars, values):
        ax.text(v + 0.01, b.get_y() + b.get_height() / 2, fmt.format(v), va="center", fontsize=6)
    ax.set_xlabel(xlabel)
    return fig, ax


def grouped_bar(group_labels, metrics, *, ylabel="Value", ax=None, figsize=(6, 3.3)):
    """A3 — grouped bars comparing several methods across metrics.

    ``metrics``: dict mapping method label -> list of values (one per group).
    """
    from .helpers import make_grouped_bar

    _style()
    labels = list(metrics.keys())
    series = [list(v) for v in metrics.values()]
    fig, ax = _fig(ax, figsize)
    make_grouped_bar(ax, group_labels, series, labels, ylabel=ylabel, colors=DEFAULT_COLORS)
    return fig, ax


def scatter_fit(
    x,
    y,
    *,
    xlabel="$x$",
    ylabel="$y$",
    degree=1,
    obs_label="Observations",
    color=PALETTE["blue_main"],
    figsize=(4.8, 3.4),
    ax=None,
):
    """A6 — scatter with a least-squares polynomial fit + 95% CI band."""
    _style()
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    fig, ax = _fig(ax, figsize)
    ax.scatter(x, y, s=18, color=color, alpha=0.7, label=obs_label)
    coef = np.polyfit(x, y, degree)
    xs = np.linspace(x.min(), x.max(), 200)
    yhat = np.polyval(coef, xs)
    ax.plot(xs, yhat, color="k", linewidth=1.0, label="Fit")
    resid = y - np.polyval(coef, x)
    se = np.sqrt(np.sum(resid**2) / (len(x) - degree - 1))
    ax.fill_between(
        xs, yhat - 1.96 * se, yhat + 1.96 * se, color=color, alpha=0.12, linewidth=0, label="95% CI"
    )
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, fontsize=6)
    return fig, ax


def heatmap(
    matrix,
    *,
    row_labels=None,
    col_labels=None,
    cmap="RdBu_r",
    center=0.0,
    cbar_label="value",
    annot=True,
    fmt=".2f",
    xlabel="",
    ylabel="",
    figsize=(5.2, 4.2),
    ax=None,
):
    """A5 — annotated heatmap (correlation / sensitivity / matrix)."""
    _style()
    fig, ax = _fig(ax, figsize)
    make_heatmap(
        ax,
        matrix,
        x_labels=col_labels,
        y_labels=row_labels,
        cmap=cmap,
        cbar_label=cbar_label,
        annotate=annot,
        fmt=fmt,
    )
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    return fig, ax


def tornado(params, low, high, base, *, xlabel="Change in objective", figsize=(4.8, 3.4), ax=None):
    """A8 — tornado / one-at-a-time sensitivity ranking."""
    _style()
    low = np.asarray(low, float)
    high = np.asarray(high, float)
    base = np.broadcast_to(np.asarray(base, float), low.shape)
    spread = np.abs(base - low) + np.abs(high - base)
    order = np.argsort(spread)
    params = [params[i] for i in order]
    low = low[order]
    high = high[order]
    base = base[order]
    fig, ax = _fig(ax, figsize)
    y = np.arange(len(params))
    ax.barh(y, high - base, left=base, color=PALETTE["red_strong"], height=0.55, label="High")
    ax.barh(y, base - low, left=low, color=PALETTE["blue_main"], height=0.55, label="Low")
    ax.set_yticks(y)
    ax.set_yticklabels(params)
    ax.axvline(base[0], color="k", linewidth=0.8, linestyle="--")
    ax.set_xlabel(xlabel)
    ax.legend(frameon=False, fontsize=6)
    return fig, ax


def confusion(cm, labels=None, *, figsize=(3.8, 3.4), ax=None):
    """A9 — confusion matrix (counts), blue colormap."""
    from .helpers import make_heatmap

    _style()
    fig, ax = _fig(ax, figsize)
    make_heatmap(ax, cm, x_labels=labels, y_labels=labels, cmap="Blues", annotate=True, fmt="d")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    return fig, ax

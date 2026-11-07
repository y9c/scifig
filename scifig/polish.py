"""Editorial polish helpers — the "human effort" refinement layer.

A default matplotlib / helper figure looks *programmatic*: crude ticks, unset
axis ranges, annotation crowding, flat uncertainty bands. These helpers add the
deliberate details a human editor adds by hand, and should be applied at the
end of any figure for a polished, journal-grade look.

Apply ``finish_axes`` to each axes (tight, readable ticks, subtle grid control)
and ``finish_figure`` once on the whole figure. Each helper is opt-in so you can
compose exactly the level of polish you want.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator

from .helpers import annotate_bars

__all__ = [
    "finish_axes",
    "finish_figure",
    "ticks_readable",
    "tight_ylim",
    "add_minor_ticks",
    "bar_value_labels",
    "soft_grid",
]


def ticks_readable(ax, n=5, which="y"):
    """Force a readable, deliberate number of ticks on the given axis."""
    locator = MaxNLocator(nbins=n, integer=False)
    if which in ("y", "both"):
        ax.yaxis.set_major_locator(locator)
    if which in ("x", "both"):
        ax.xaxis.set_major_locator(MaxNLocator(nbins=n, integer=False))
    return ax


def add_minor_ticks(ax, which="both", size=2.0, width=0.5):
    """Add minor ticks (a refinement that reads "edited")."""
    for axis in (ax.xaxis if which in ("x", "both") else [],
                 ax.yaxis if which in ("y", "both") else []):
        axis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(which="minor", length=size, width=width)
    return ax


def tight_ylim(ax, pad=0.06, floor=None, ceiling=None):
    """Tighten y-limits to the data range (emphasizes differences over 0-based).

    ``pad``: fraction of the data range added on each side. ``floor``/``ceiling``
    clamp the result (e.g. ``floor=0`` for scores, ``ceiling=1.0`` for accuracy).
    """
    ymin, ymax = ax.get_ylim()
    rng = ymax - ymin
    for line in ax.lines:
        yd = line.get_ydata()
        yd = np.asarray(yd, float)
        yd = yd[np.isfinite(yd)]
        if yd.size:
            pass  # already covered by autoscale; extra tightening below
    lo = ymin + rng * pad
    hi = ymax - rng * pad
    if floor is not None:
        lo = max(lo, floor)
    if ceiling is not None:
        hi = min(hi, ceiling)
    ax.set_ylim(lo, hi)
    return ax


def soft_grid(ax, on=True, color="#DDDDDD", alpha=0.5, linewidth=0.5):
    """Subtle grid, behind the data (never competing with it)."""
    ax.grid(on, which="major", color=color, alpha=alpha, linewidth=linewidth)
    ax.set_axisbelow(True)
    return ax


def bar_value_labels(ax, bars=None, fmt="{:.2f}", fontsize=None, padding=3, hide_zero=False):
    """Well-offset value labels above bars (skips near-zero for cleanliness)."""
    if bars is None:
        bars = ax.patches
    for rect in bars:
        h = rect.get_height()
        if h is None or not np.isfinite(h):
            continue
        if hide_zero and abs(h) < 1e-9:
            continue
        ax.annotate(
            fmt.format(h),
            (rect.get_x() + rect.get_width() / 2.0, h),
            xytext=(0, padding),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=fontsize or plt.rcParams.get("font.size", 8),
        )
    return ax


def finish_axes(ax, title=None, xlabel=None, ylabel=None,
                ticks=5, grid=True, minor=True):
    """One-call human polish on a single axes.

    Sets readable tick density, optional minor ticks, subtle grid behind the
    data, and propagated axis labels/title. Returns ``ax``.
    """
    if title:
        ax.set_title(title, pad=5)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ticks_readable(ax, n=ticks)
    if minor:
        add_minor_ticks(ax)
    if grid:
        soft_grid(ax)
    ax.tick_params(axis="both", which="major", length=3.2, width=0.6)
    return ax


def finish_figure(fig, tight=True, pad=0.6):
    """Finish the whole figure: consistent panel spacing and layout."""
    if tight:
        fig.tight_layout(pad=pad)
    return fig

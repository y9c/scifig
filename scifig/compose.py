"""Composition and annotation helpers: join panels, label them, annotate.

This is the "pure Python join + annotate" layer the user prefers: rather than
manually splicing in Illustrator, you compose figures in code.

Two groups:

1. **Compose separate axes/figures into one** (``join_axes``, ``join_figures``,
   ``panel_grid``): lay out a grid of already-drawn axes or load separate PNG
   files into a single multi-panel figure with a shared legend and panel
   letters.

2. **Annotate a single axes** (``add_panel_label``, ``add_inset``,
   ``add_bracket``, ``add_sig``, ``shared_legend``): significance brackets,
   panels letters, insets, and shared legends.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

__all__ = [
    "panel_grid",
    "join_axes",
    "join_figures",
    "add_panel_label",
    "add_panel_labels",
    "shared_legend",
    "add_inset",
    "add_bracket",
    "add_sig",
]

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def panel_grid(
    nrows=1,
    ncols=1,
    figsize=None,
    legend="bottom",
    legend_height=0.08,
    wspace=0.18,
    hspace=0.30,
    sharex=False,
    sharey=False,
    share_groups=None,
    **kwargs,
):
    """Create ``(fig, axes)`` for a multi-panel figure with GridSpec spacing.

    ``legend``: ``'bottom'``/``'top'``/``None`` — reserve a horizontal strip for
    a shared legend. ``sharex``/``sharey``: ``True`` shares across all panels;
    ``'row'``/``'col'`` shares within each row/column. ``share_groups``
    overrides both: a list of lists of **flat indices** (same order as the
    returned ``axes``) that share a y-axis, e.g. ``[[0, 1], [2, 3]]``. Returns
    ``(fig, axes)`` where ``axes`` is a flat 1D array.
    """
    if figsize is None:
        figsize = (3.5 * ncols, 2.625 * nrows)
    fig = plt.figure(figsize=figsize)

    # flat index -> reference axis index to share y with
    sy = {}
    if share_groups is not None:
        for group in share_groups:
            for idx in group[1:]:
                sy[idx] = group[0]
    elif sharey:
        if sharey == "row":
            for r in range(nrows):
                for c in range(1, ncols):
                    sy[r * ncols + c] = r * ncols
        elif sharey == "col":
            for r in range(1, nrows):
                for c in range(ncols):
                    sy[r * ncols + c] = c
        else:
            for i in range(1, nrows * ncols):
                sy[i] = 0

    rates = (
        ([1] * nrows + [legend_height])
        if legend == "bottom"
        else ([legend_height] + [1] * nrows)
        if legend == "top"
        else None
    )
    gs = GridSpec(
        (nrows + 1) if legend else nrows,
        ncols,
        figure=fig,
        wspace=wspace,
        hspace=hspace,
        height_ratios=rates,
    )
    axes = []
    for i in range(nrows):
        for j in range(ncols):
            idx = i * ncols + j
            share_ax = axes[sy[idx]] if idx in sy and sy[idx] < idx else None
            ax = fig.add_subplot(gs[i, j], sharey=share_ax)
            if sharex and idx > 0:
                ax.sharex(axes[0])
            axes.append(ax)
    return fig, np.asarray(axes).reshape(-1)


def join_axes(axes, labels=None, figsize=None, wspace=0.18, hspace=0.22):
    """Place already-drawn axes into a single labeled multi-panel figure.

    ``axes``: a sequence of ``Axes`` (this moves them onto a new figure).
    ``labels``: optional panel letters (default ``A, B, C, ...``).
    """
    axes = list(axes)
    n = len(axes)
    ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))
    if figsize is None:
        figsize = (3.5 * ncols, 2.625 * nrows)
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(nrows, ncols, figure=fig, wspace=wspace, hspace=hspace)
    for i, ax in enumerate(axes):
        ax.set_position(gs[i].get_position(fig))
        # keep the axes attached to the shared figure via fig.add_axes
    fig.subplots_adjust(wspace=wspace, hspace=hspace)
    if labels:
        add_panel_labels(axes, labels)
    return fig, axes


def join_figures(files, out_path=None, ncols=None, figsize=None, labels=None, dpi=300, pad=0.05):
    """Stitch existing saved figures (PNG/PDF/SVG) into one multi-panel figure.

    Useful for combining independently generated panels. Each file is loaded
    as an image and placed in a grid. Returns ``(fig, axes)``.
    """
    import matplotlib.image as mpimg

    files = [Path(f) for f in files]
    n = len(files)
    if ncols is None:
        ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))
    if figsize is None:
        figsize = (3.5 * ncols, 2.625 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = np.asarray(axes).reshape(-1)
    for i, (f, ax) in enumerate(zip(files, axes)):
        img = mpimg.imread(f)
        ax.imshow(img)
        ax.set_axis_off()
    for ax in axes[n:]:
        ax.set_axis_off()
    if labels:
        add_panel_labels(axes, labels)
    fig.subplots_adjust(wspace=0.05, hspace=0.05)
    return fig, axes


def add_panel_label(ax, letter=None, x=-0.12, y=1.02, fontsize=None, fontweight="bold"):
    """Add a panel letter to a single axes (default: uppercase ``A``).

    Defaults to the **top-left corner, outside the axes**: ``x=-0.12`` sits in
    the y-axis tick-label zone (aligned with the y tick labels) and ``y=1.02``
    just above the plot top, at ``va='bottom'``. This is the journal convention
    (category labels like a/b/c sit at the corner, never inside the plot).
    Pass ``x``/``y`` to override. ``fontsize`` defaults to 1.2x the base font.
    """
    if letter is None:
        letter = "A"
    if fontsize is None:
        fontsize = 1.2 * plt.rcParams.get("font.size", 10)
    ax.text(
        x,
        y,
        letter,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight=fontweight,
        va="bottom",
        ha="left",
    )
    return ax


def add_panel_labels(axes, labels=None, case="upper", bold=True):
    """Add panel letters to multiple axes (top-left corner).

    ``case``: ``'upper'`` (default, Science convention → **A, B, C** bold) or
    ``'lower'`` (Nature convention → a, b, c). Pass explicit ``labels`` to
    override the auto-generated letters. ``bold`` controls the font weight.
    """
    letters = []
    for i, _ in enumerate(axes):
        letter = labels[i % len(labels)] if labels else _LETTERS[i % len(_LETTERS)]
        if case == "lower":
            letter = letter.lower()
        letters.append(letter)
    for ax, letter in zip(axes, letters):
        add_panel_label(ax, letter, fontweight="bold" if bold else "normal")
    return axes


def shared_legend(
    fig, handles=None, labels=None, location="upper center", ncol=None, clear=True, **kw
):
    """Place one legend on the figure instead of per-panel legends.

    ``clear=True`` (default) removes each axes' own legend so the figure has
    exactly one legend instead of duplicated ones. Pass ``clear=False`` to keep
    per-panel legends too.
    """
    if handles is None or labels is None:
        # gather from all axes (dedup by label)
        h, lb = [], []
        for ax in fig.axes:
            hh, ll = ax.get_legend_handles_labels()
            for a, b in zip(hh, ll):
                if b not in lb:
                    lb.append(b)
                    h.append(a)
        handles, labels = h, lb
    if clear:
        for ax in fig.axes:
            if ax.get_legend() is not None:
                ax.get_legend().remove()
    fig.legend(handles, labels, loc=location, ncol=ncol or len(labels), frameon=False, **kw)
    return fig


def add_inset(ax, loc, size="30%", axes_kw=None, indicator=True):
    """Add an inset axes. ``loc``: 'upper right' etc. Returns the inset axes.

    By default a rectangle indicator links the inset to the parent region.
    """
    ax_in = inset_axes(ax, width=size, height=size, loc=loc, axes_kwargs=axes_kw or {})
    if indicator:
        mark_inset(ax, ax_in, loc1=1, loc2=3, fc="none", ec="0.5")
    return ax_in


def add_bracket(ax, x0, x1, y, height=0.03, text=None, fontsize=10):
    """Draw a significance/difference bracket between ``x0`` and ``x1`` at ``y``."""
    ax.plot([x0, x0, x1, x1], [y, y + height, y + height, y], "k-", lw=0.8)
    if text:
        ax.text(
            (x0 + x1) / 2.0, y + height * 1.05, text, ha="center", va="bottom", fontsize=fontsize
        )
    return ax


def add_sig(ax, x0, x1, y, marker="***", height=0.03, fontsize=11):
    """Convenience: a significance bracket labelled with ``marker``."""
    return add_bracket(ax, x0, x1, y, height=height, text=marker, fontsize=fontsize)

"""Declarative figure builder (agent-oriented).

The agent describes **what** the figure is as a simple ``FigureSpec`` and
``render_spec`` builds it in the unified house style: semantic color roles, one
shared legend, Nature/Science panel letters, thin Arial spines, vector PDF.

Example::

    import scifig
    spec = scifig.FigureSpec(
        width="double", aspect=0.5, panels=[
            dict(type="bar", categories=["A", "B"],
                 series=[[1, 2], [3, 4]], labels=["Ours", "Base"],
                 our_marker="Ours"),
            dict(type="trend", x=x, ys=[y1, y2], labels=["Ours", "Base"]),
        ],
    )
    fig, axes = scifig.render_spec(spec, "out/figure")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .semantics import assign_colors
from .style import (
    NATURE_DOUBLE_W,
    NATURE_HALF_W,
    NATURE_SINGLE_W,
    FigureStyle,
    apply_publication_style,
    finalize_figure,
)

__all__ = ["FigureSpec", "render_spec", "COLUMN_WIDTHS"]


COLUMN_WIDTHS = {
    "single": NATURE_SINGLE_W,
    "half": NATURE_HALF_W,
    "double": NATURE_DOUBLE_W,
    "full": NATURE_DOUBLE_W,
}


@dataclass
class FigureSpec:
    """Declarative description of a multi-panel figure.

    ``panels`` is a list of dicts, each describing one panel:

    * ``type``: ``'bar'`` | ``'trend'`` | ``'heatmap'`` | ``'scatter'`` |
      ``'sphere'`` (default ``'trend'``).
    * shared keys: ``labels`` (legend), ``colors``/``roles``/``ours_marker``
      (semantic coloring), ``xlabel``/``ylabel``, ``title``.
    * ``'bar'``: ``categories``, ``series`` (list of arrays), ``annotate``,
      ``ylim``.
    * ``'trend'``: ``x``, ``ys`` (list; an ``(N,2)`` entry gives a
      mean/std band), ``show_shadow``, colors/roles/labels.
    * ``'heatmap'``: ``matrix``, ``x_labels``/``y_labels``, ``cmap``,
      ``cbar_label``, ``annotate``.
    * ``'scatter'``: ``x``, ``y``, ``size``, ``alpha``.
    """

    panels: list[dict] = field(default_factory=list)
    width: str = "double"  # single|half|double|full (inches)
    aspect: float = 0.55  # height / width
    font_size: float = 6.0  # base pt (Nature ~5-6)
    axes_linewidth: float = 0.8
    panel_case: str = "lower"  # lower=Nature, upper=Science
    shared_legend: bool = True
    legend_ncol: Optional[int] = None
    legend_location: str = "lower center"
    legend_height: float = 0.06
    wspace: float = 0.16
    hspace: float = 0.30
    ncols: Optional[int] = None  # force grid columns (else sqrt)
    layout: str = "auto"  # auto|constrained|tight|none (overlap fix)
    sharex: bool = False  # share x across all panels
    sharey: object = False  # True|'row'|'col'|False — share y across panels
    share_groups: Optional[list] = None  # [[i,j,...],...] share y within each group
    style: Optional[FigureStyle] = None

    def __post_init__(self):
        if isinstance(self.width, str):
            if self.width not in COLUMN_WIDTHS:
                raise ValueError(f"unknown width '{self.width}'; use {list(COLUMN_WIDTHS)}")
            self.width = COLUMN_WIDTHS[self.width]


# fmt: off
def _draw_panel(ax, p: dict, compose, letter: str):
    """Draw one panel type onto ``ax`` (mutates it in place)."""
    from . import helpers

    ptype = p.get("type", "trend")
    labels = p.get("labels", [])
    # semantic colors: explicit > roles > ours_marker > auto cycle
    colors = p.get("colors")
    if colors is None and labels:
        colors = assign_colors(labels, roles=p.get("roles"), ours_marker=p.get("ours_marker"))

    if ptype == "bar":
        bars = helpers.make_grouped_bar(
            ax, p["categories"], p["series"], labels,
            ylabel=p.get("ylabel", "Value"), colors=colors,
            annotate=p.get("annotate", False),
        )
        if p.get("annotate"):
            helpers.annotate_bars(ax, bars)
        if "ylim" in p:
            ax.set_ylim(*p["ylim"])
    elif ptype == "trend":
        helpers.make_trend(
            ax, p["x"], p["ys"], labels,
            ylabel=p.get("ylabel"), xlabel=p.get("xlabel"),
            colors=colors, show_shadow=p.get("show_shadow", True),
        )
    elif ptype == "heatmap":
        helpers.make_heatmap(
            ax, p["matrix"], x_labels=p.get("x_labels"), y_labels=p.get("y_labels"),
            cmap=p.get("cmap", "magma"), cbar_label=p.get("cbar_label"),
            annotate=p.get("annotate", False),
        )
    elif ptype == "scatter":
        helpers.make_scatter(
            ax, p["x"], p["y"], label=labels[0] if labels else None,
            color=colors[0] if colors else p.get("color"),
            size=p.get("size", 40), alpha=p.get("alpha", 0.7),
        )
    elif ptype == "sphere":
        helpers.make_sphere_illustration(ax)
    else:
        raise ValueError(f"unknown panel type '{ptype}'")

    if "xlabel" in p and ptype not in ("trend",):
        ax.set_xlabel(p["xlabel"])
    if "ylabel" in p and ptype not in ("bar", "trend"):
        ax.set_ylabel(p["ylabel"])
    if "title" in p:
        ax.set_title(p["title"], pad=4)
    # fmt: on


def render_spec(spec: FigureSpec, out_path: str, formats=None, dpi=600):
    """Render a ``FigureSpec`` into a figure and save it.

    Applies the unified house style, draws each panel, adds a single shared
    legend and Nature/Science panel letters, then saves (vector PDF by default).
    Returns ``(fig, axes)``.
    """
    from . import compose

    n = len(spec.panels)
    if n == 0:
        raise ValueError("spec.panels is empty")
    ncols = spec.ncols or int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))
    figsize = (spec.width, spec.width * spec.aspect)

    st = spec.style or FigureStyle(font_size=spec.font_size,
                                   axes_linewidth=spec.axes_linewidth)
    apply_publication_style(st)

    fig, axes = compose.panel_grid(
        nrows, ncols, figsize=figsize,
        legend="bottom" if spec.shared_legend else None,
        legend_height=spec.legend_height,
        wspace=spec.wspace, hspace=spec.hspace,
        sharex=spec.sharex, sharey=spec.sharey, share_groups=spec.share_groups,
    )

    for i, p in enumerate(spec.panels):
        ax = axes[i]
        letter = chr(97 + i) if spec.panel_case == "lower" else chr(65 + i)
        _draw_panel(ax, p, compose, letter)
        # editorial polish on every rendered panel (unless explicitly disabled)
        if not p.get("raw"):
            from .polish import finish_axes
            finish_axes(ax, grid=p.get("grid", True),
                        minor=p.get("minor", True))
        compose.add_panel_label(ax, letter, fontweight="bold")

    # hide any unused axes (e.g. when panels don't fill the grid)
    for ax in axes[n:]:
        ax.set_axis_off()

    if spec.shared_legend:
        compose.shared_legend(fig, location=spec.legend_location,
                              ncol=spec.legend_ncol or min(n, 3))

    # --- layout audit + auto-fix: prevent panel overlap / excessive whitespace ---
    layout = spec.layout
    if layout != "none":
        from .layout import fix_layout
        report = fix_layout(fig, engine=(layout if layout != "auto" else "constrained"))
        if report.has_overlap:
            import warnings
            warnings.warn(f"scifig: {len(report.overlaps)} panel overlap(s) remained "
                          f"after {layout} layout; check panel labels/orientation.")

    finalize_figure(fig, out_path, formats=formats or ["pdf"], dpi=dpi)
    return fig, axes

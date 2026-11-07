"""Object-oriented figure builder.

The declarative ``FigureSpec`` covers most needs, but some figures want an
**object-oriented** build: create a canvas, add typed panels (`BarPanel`,
`TrendPanel`, `HeatmapPanel`, `ScatterPanel`), then `savefig()`. This module
provides that as an OO front-end over the same engine (so style, semantic
colors, polish, layout audit, and vector-first save stay identical), absorbing
the panel-builder pattern from cnsplots' ``multipanel``.

Example::

    from scifig.figure import Figure, BarPanel, TrendPanel
    fig = Figure(width="double", aspect=0.4)
    fig.add(BarPanel(categories=["VQA","OCR"], series=[[0.9,0.8]],
                     labels=["Ours"], our_marker="Ours", ylabel="Accuracy"))
    fig.add(TrendPanel(x=steps, ys=[y1, y2], labels=["Ours","Base"],
                       our_marker="Ours", ylabel="Score"))
    fig.savefig("out/oo")
"""

from __future__ import annotations

from .spec import FigureSpec, render_spec

__all__ = ["Figure", "Panel", "BarPanel", "TrendPanel", "HeatmapPanel", "ScatterPanel"]


class Panel:
    """Base typed panel; subclasses implement ``to_panel_dict()``."""

    def to_panel_dict(self):  # pragma: no cover - overridden
        raise NotImplementedError


class BarPanel(Panel):
    def __init__(self, categories, series, labels, ylabel="Value", annotate=False,
                 our_marker=None, ylim=None, **kw):
        self.categories = categories
        self.series = series
        self.labels = labels
        self.ylabel = ylabel
        self.annotate = annotate
        self.our_marker = our_marker
        self.ylim = ylim
        self.kw = kw

    def to_panel_dict(self):
        d = dict(type="bar", categories=self.categories, series=self.series,
                 labels=self.labels, ylabel=self.ylabel, annotate=self.annotate)
        if self.our_marker:
            d["ours_marker"] = self.our_marker
        if self.ylim:
            d["ylim"] = self.ylim
        d.update(self.kw)
        return d


class TrendPanel(Panel):
    def __init__(self, x, ys, labels, ylabel=None, xlabel=None, our_marker=None,
                 show_shadow=True, **kw):
        self.x = x
        self.ys = ys
        self.labels = labels
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.our_marker = our_marker
        self.show_shadow = show_shadow
        self.kw = kw

    def to_panel_dict(self):
        d = dict(type="trend", x=self.x, ys=self.ys, labels=self.labels,
                 ylabel=self.ylabel, xlabel=self.xlabel,
                 show_shadow=self.show_shadow)
        if self.our_marker:
            d["ours_marker"] = self.our_marker
        d.update(self.kw)
        return d


class HeatmapPanel(Panel):
    def __init__(self, matrix, x_labels=None, y_labels=None, cmap="RdBu_r",
                 cbar_label=None, annotate=True, **kw):
        self.matrix = matrix
        self.x_labels = x_labels
        self.y_labels = y_labels
        self.cmap = cmap
        self.cbar_label = cbar_label
        self.annotate = annotate
        self.kw = kw

    def to_panel_dict(self):
        d = dict(type="heatmap", matrix=self.matrix, x_labels=self.x_labels,
                 y_labels=self.y_labels, cmap=self.cmap, cbar_label=self.cbar_label,
                 annotate=self.annotate)
        d.update(self.kw)
        return d


class ScatterPanel(Panel):
    def __init__(self, x, y, label=None, our_marker=None, size=40, alpha=0.7, **kw):
        self.x = x
        self.y = y
        self.label = label
        self.size = size
        self.alpha = alpha
        self.kw = kw

    def to_panel_dict(self):
        d = dict(type="scatter", x=self.x, y=self.y, size=self.size, alpha=self.alpha,
                 labels=[self.label] if self.label else [],
                 ours_marker=self.our_marker if self.our_marker else None)
        d.update(self.kw)
        return d


class Figure:
    """Object-oriented figure: add typed panels, then save."""

    def __init__(self, width="double", aspect=0.5, ncols=None, panel_case="lower",
                 shared_legend=True, sharey=False, share_groups=None,
                 layout="auto", font_size=6.0, axes_linewidth=0.8):
        self._spec = FigureSpec(
            panels=[], width=width, aspect=aspect, ncols=ncols,
            panel_case=panel_case, shared_legend=shared_legend,
            sharey=sharey, share_groups=share_groups, layout=layout,
        )
        self._spec.font_size = font_size
        self._spec.axes_linewidth = axes_linewidth
        self._fig = None
        self._axes = None

    def add(self, panel: Panel) -> "Figure":
        """Register a typed panel; returns self for chaining."""
        self._spec.panels.append(panel.to_panel_dict())
        return self

    def savefig(self, out, formats=None, dpi=600):
        """Render all added panels; returns ``(fig, axes)``."""
        self._fig, self._axes = render_spec(self._spec, out,
                                            formats=formats or ["pdf"], dpi=dpi)
        return self._fig, self._axes

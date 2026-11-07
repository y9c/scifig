"""scifig -- publication-ready matplotlib figures made simple.

A thin harness on top of matplotlib that packages your two preferred styles
(publication and modern) and a set of coarse-grained plot helpers, plus pure-
Python composition/annotation utilities so you can join and annotate figure
panels without leaving Python.

Quick start::

    import scifig
    scifig.apply_publication_style(scifig.FigureStyle(font_size=18))
    fig, ax = scifig.create_subplots(1, 1)
    scifig.make_grouped_bar(ax, ["A", "B"], [[1, 2], [0.5, 3]], ["X", "Y"], annotate=True)
    scifig.finalize_figure(fig, "out/fig", formats=["png", "pdf"])
"""

from .style import (
    FigureStyle,
    apply_publication_style,
    apply_modern_style,
    set_palette,
    create_subplots,
    finalize_figure,
    style_axis,
    save_figure,
    set_hidpi,
    make_figure,
)
from .palette import (
    PALETTE,
    DEFAULT_COLORS,
    MODERN_COLORS,
    COLORBLIND_SAFE,
)
from .helpers import (
    make_grouped_bar,
    annotate_bars,
    make_trend,
    make_heatmap,
    make_scatter,
    make_sphere_illustration,
)
from .compose import (
    panel_grid,
    join_axes,
    join_figures,
    add_panel_label,
    add_panel_labels,
    shared_legend,
    add_inset,
    add_bracket,
    add_sig,
)

__version__ = "0.1.0"

__all__ = [
    "FigureStyle",
    "apply_publication_style",
    "apply_modern_style",
    "set_palette",
    "create_subplots",
    "finalize_figure",
    "style_axis",
    "save_figure",
    "set_hidpi",
    "make_figure",
    "PALETTE",
    "DEFAULT_COLORS",
    "MODERN_COLORS",
    "COLORBLIND_SAFE",
    "make_grouped_bar",
    "annotate_bars",
    "make_trend",
    "make_heatmap",
    "make_scatter",
    "make_sphere_illustration",
    "panel_grid",
    "join_axes",
    "join_figures",
    "add_panel_label",
    "add_panel_labels",
    "shared_legend",
    "add_inset",
    "add_bracket",
    "add_sig",
    "__version__",
]
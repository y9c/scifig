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

from .archetypes import (
    confusion,
    grouped_bar,
    heatmap,
    save,
    scatter_fit,
    sorted_bar,
    timeseries_ci,
    tornado,
)
from .bio import SIGNIFICANT_SCHEME, dot_plot, ma_plot, umap_scatter, violin_groups, volcano
from .compose import (
    add_bracket,
    add_inset,
    add_panel_label,
    add_panel_labels,
    add_sig,
    join_axes,
    join_figures,
    panel_grid,
    shared_legend,
)
from .figure import BarPanel, Figure, HeatmapPanel, Panel, ScatterPanel, TrendPanel
from .fonts import PREFERRED_SANS, available_sans, best_sans, font_hint
from .helpers import (
    annotate_bars,
    make_grouped_bar,
    make_heatmap,
    make_scatter,
    make_sphere_illustration,
    make_trend,
)
from .journals import JOURNAL_SPEC, fig_size_mm, journal_figsize, journal_style
from .layout import LayoutReport, audit_layout, fix_layout, layout_report
from .palette import (
    COLORBLIND_SAFE,
    DEFAULT_COLORS,
    FRIENDLY_PALS,
    MODERN_COLORS,
    PALETTE,
    friendly_pal,
)
from .polish import (
    add_minor_ticks,
    bar_value_labels,
    finish_axes,
    finish_figure,
    soft_grid,
    ticks_readable,
    tight_ylim,
)
from .protein import (
    demo_structure,
    draw_protein_from_pdb,
    draw_topology,
    fetch_structure,
    load_structure,
    pymol_cartoon,
    ribbon_3d,
)
from .quality import QUALITY_AXES, QualityReport, check_figure
from .semantics import ROLE_CYCLE, SEMANTIC_ROLES, assign_colors, role_color
from .spec import COLUMN_WIDTHS, FigureSpec, render_spec
from .style import (
    NATURE_DOUBLE_W,
    NATURE_HALF_W,
    NATURE_SINGLE_W,
    FigureStyle,
    apply_modern_style,
    apply_publication_style,
    create_subplots,
    finalize_figure,
    make_figure,
    nature_double_style,
    nature_figsize,
    nature_single_style,
    save_figure,
    set_hidpi,
    set_palette,
    style_axis,
)

__version__ = "0.4.0"

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
    "nature_single_style",
    "nature_double_style",
    "NATURE_SINGLE_W",
    "NATURE_HALF_W",
    "NATURE_DOUBLE_W",
    "nature_figsize",
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
    "SEMANTIC_ROLES",
    "ROLE_CYCLE",
    "role_color",
    "assign_colors",
    "FigureSpec",
    "render_spec",
    "COLUMN_WIDTHS",
    "JOURNAL_SPEC",
    "journal_style",
    "journal_figsize",
    "fig_size_mm",
    "FRIENDLY_PALS",
    "friendly_pal",
    "timeseries_ci",
    "sorted_bar",
    "grouped_bar",
    "scatter_fit",
    "heatmap",
    "tornado",
    "confusion",
    "save",
    "check_figure",
    "QualityReport",
    "QUALITY_AXES",
    "finish_axes",
    "finish_figure",
    "ticks_readable",
    "add_minor_ticks",
    "tight_ylim",
    "soft_grid",
    "bar_value_labels",
    "audit_layout",
    "fix_layout",
    "layout_report",
    "LayoutReport",
    "available_sans",
    "best_sans",
    "font_hint",
    "PREFERRED_SANS",
    "Figure",
    "Panel",
    "BarPanel",
    "TrendPanel",
    "HeatmapPanel",
    "ScatterPanel",
    "volcano",
    "ma_plot",
    "dot_plot",
    "umap_scatter",
    "violin_groups",
    "SIGNIFICANT_SCHEME",
    "demo_structure",
    "draw_topology",
    "draw_protein_from_pdb",
    "fetch_structure",
    "load_structure",
    "pymol_cartoon",
    "ribbon_3d",
    "__version__",
]

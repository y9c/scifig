"""Style application and figure lifecycle.

Provides the two style systems the project supports:

* ``apply_publication_style`` -- publication house style (spines off, larger
  fonts, frameless legends). Use for paper figures.
* ``apply_modern_style`` -- clean modern style (subtle grid, sans-serif.
  Use for slides/reports.

And the lifecycle helpers ``create_subplots`` and ``finalize_figure``.

The .mplstyle assets are bundled inside this package and located via
``importlib.resources`` so they work after ``pip install`` without any
hard-coded path.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import matplotlib.pyplot as plt
from cycler import cycler

from .palette import COLORBLIND_SAFE, MODERN_COLORS

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
]


@dataclass(frozen=True)
class FigureStyle:
    """Tunable knobs for the publication style."""

    font_size: float = 6.0
    axes_linewidth: float = 1.0
    use_tex: bool = False
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")


def _asset(name: str) -> Path:
    """Return the path of a bundled .mplstyle asset."""
    return Path(__file__).parent / "assets" / name


# ---------------------------------------------------------------------------
# Publication house style
# ---------------------------------------------------------------------------
def apply_publication_style(style: Optional[FigureStyle] = None) -> None:
    """Apply the publication-house style to matplotlib rcParams.

    ``style.font_size`` is the **base** size in points; every text element
    (titles, labels, ticks, legend) is scaled proportionally from it, so a
    Nature-style figure sets ``font_size=6`` (recommended 5-6pt at final column
    width) and gets a coherent, thin-spined layout automatically. Call once,
    before creating figures.

    Spines are drawn thin (``axes.linewidth`` from the style, default 1.0pt)
    and the top/right spines are removed, per the house rules.
    """
    if style is None:
        style = FigureStyle()
    asset = _asset("scientific_publication.mplstyle")
    if asset.exists():
        plt.style.use(str(asset))
    fs = style.font_size
    plt.rcParams.update(
        {
            # type hierarchy scaled from the base size
            "font.family": "sans-serif",
            "font.size": fs,
            "axes.titlesize": fs * 1.15,
            "axes.labelsize": fs * 1.05,
            "xtick.labelsize": fs,
            "ytick.labelsize": fs,
            "legend.fontsize": fs * 0.95,
            "legend.title_fontsize": fs * 1.05,
            "mathtext.default": "regular",
            # thin spines / lines / ticks for a clean print look
            "axes.linewidth": style.axes_linewidth,
            "lines.linewidth": 1.0,
            "lines.markeredgewidth": 0.6,
            "xtick.major.width": style.axes_linewidth * 0.8,
            "ytick.major.width": style.axes_linewidth * 0.8,
            "xtick.major.size": fs * 0.5,
            "ytick.major.size": fs * 0.5,
            "errorbar.capsize": fs * 0.35,
            # vector-safe, editable text + exact figsize
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "legend.labelcolor": "linecolor",
            "savefig.bbox": "standard",
            # house rules
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "text.usetex": style.use_tex,
        }
    )
    if style.font_family:
        # prefer the best actually-installed sans (Arial-like), not a blind list
        from .fonts import best_sans

        plt.rcParams["font.sans-serif"] = [best_sans(), *style.font_family]


def apply_modern_style() -> None:
    """Apply the modern / presentation style."""
    asset = _asset("modern.mplstyle")
    if asset.exists():
        plt.style.use(str(asset))
    else:  # pragma: no cover - fallback if asset is missing
        plt.rcParams.update(
            {
                "figure.facecolor": "white",
                "savefig.dpi": 300,
                "axes.edgecolor": "#333333",
                "axes.spines.top": False,
                "axes.spines.right": False,
                "font.family": "sans-serif",
                "lines.linewidth": 2.0,
            }
        )


def set_palette(palette: str = "modern") -> None:
    """Set the axes color cycle.

    Options: ``'modern'``, ``'colorblind'``, ``'dark'``, ``'pastel'``, or
    ``'publication'`` (uses the semantic house palette).
    """
    palettes = {
        "publication": [
            "#3A6BC5",
            "#D4654A",
            "#4A9F6F",
            "#DE9E4A",
            "#B5637D",
            "#4A9496",
        ],
        "modern": MODERN_COLORS,
        "colorblind": COLORBLIND_SAFE,
        "dark": ["#1F2937", "#374151", "#4B5563", "#6B7280", "#9CA3AF", "#D1D5DB"],
        "pastel": [
            "#BFDBFE",
            "#FDE68A",
            "#A7F3D0",
            "#FECACA",
            "#DDD6FE",
            "#FBCFE8",
        ],
    }
    colors = palettes.get(palette, MODERN_COLORS)
    plt.rcParams["axes.prop_cycle"] = cycler("color", colors)


# ---------------------------------------------------------------------------
# Figure lifecycle
# ---------------------------------------------------------------------------
def create_subplots(nrows=1, ncols=1, figsize=None, **kwargs):
    """Return ``(fig, axes)`` with ``axes`` flattened to 1D."""
    fig, ax = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
    axes = ax if nrows * ncols == 1 else ax.ravel()
    return fig, axes


def finalize_figure(
    fig,
    out_path,
    formats: Optional[Sequence[str]] = None,
    dpi: int = 300,
    close: bool = True,
    pad: float = 0.05,
    **kwargs,
):
    """Save ``fig`` to one or more formats and (optionally) close it.

    **Vector-first policy:** the primary output is the vector PDF (editable
    text, infinitely scalable, journal-preferred). PNG is raster and should
    only be emitted when explicitly requested (e.g. for a quick on-screen
    preview). When ``formats`` is ``None``:

    * ``out_path`` has an extension → use that extension (so ``out/fig.pdf``
      yields exactly a PDF).
    * otherwise → ``['pdf']`` (vector-first; SVG is also vector if you want it).

    Parent directories are created. Returns the list of saved ``Path``\\s.
    """
    out = Path(out_path)
    if formats is None:
        if out.suffix:
            formats = [out.suffix.lstrip(".")]
        else:
            formats = ["pdf"]
    out.parent.mkdir(parents=True, exist_ok=True)
    # exact-size vector by default (savefig.bbox='standard'); only use 'tight'
    # when the caller explicitly asks for it, since tight silently changes size.
    bbox_default = plt.rcParams.get("savefig.bbox", "standard")
    saved = []
    for fmt in formats:
        target = out.with_suffix("." + fmt) if out.suffix else Path(str(out) + "." + fmt)
        kwargs.setdefault("bbox_inches", bbox_default)
        if bbox_default == "tight":
            kwargs.setdefault("pad_inches", pad)
        kwargs.setdefault("facecolor", "white")
        fig.savefig(target, format=fmt, dpi=dpi, **kwargs)
        saved.append(target)
    if close:
        plt.close(fig)
    return saved


def style_axis(
    ax,
    title=None,
    xlabel=None,
    ylabel=None,
    remove_top_right=True,
    grid=True,
    grid_alpha=0.6,
):
    """Apply modern styling to an existing axis (mutates and returns it)."""
    if title:
        ax.set_title(title, pad=15)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if remove_top_right:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    if grid:
        ax.grid(True, alpha=grid_alpha, linestyle="-", linewidth=0.5, color="#E5E5E5")
    return ax


def save_figure(fig, filename, formats=None, **kwargs):
    """Save a figure in multiple formats, returning the saved paths."""
    if formats is None:
        formats = ["png"]
    filepath = Path(filename)
    base = filepath.with_suffix("")
    saved = []
    for fmt in formats:
        target = Path(str(base) + "." + fmt)
        fig.savefig(target, format=fmt, bbox_inches="tight", facecolor="white", **kwargs)
        saved.append(target)
    return saved


def set_hidpi(dpi=200):
    """Set high DPI for crisp plots on retina displays."""
    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams["savefig.dpi"] = dpi * 2


def make_figure(figsize=(10, 6), nrows=1, ncols=1, **kwargs):
    """Create a figure with modern defaults applied."""
    apply_modern_style()
    return plt.subplots(nrows, ncols, figsize=figsize, **kwargs)


# ---------------------------------------------------------------------------
# Journal-specific presets (final printed width in inches)
# ---------------------------------------------------------------------------
# Nature column widths: single column 3.50", 1.5-column 5.00", double column 7.20".
# Recommended body text 5-6pt (Arial) at the printed size; 8-9pt for screen/draft.
NATURE_SINGLE_W = 3.50
NATURE_HALF_W = 5.00
NATURE_DOUBLE_W = 7.20


def nature_single_style(font_size=6.0, axes_linewidth=0.8):
    """Nature single-column style (width 3.50in, ~5-6pt Arial)."""
    return FigureStyle(font_size=font_size, axes_linewidth=axes_linewidth)


def nature_double_style(font_size=7.0, axes_linewidth=1.0):
    """Nature double-column style (width 7.20in, ~7pt Arial)."""
    return FigureStyle(font_size=font_size, axes_linewidth=axes_linewidth)


def nature_figsize(columns="single", aspect=0.75):
    """Return a Nature ``(width, height)`` figsize in inches.

    ``columns``: ``'single'`` (3.50in), ``'half'``/``'1.5'`` (5.00in), or
    ``'double'``/``'full'`` (7.20in). ``aspect`` = height/width; 0.75 is a
    sensible default for most panels.
    """
    widths = {
        "single": NATURE_SINGLE_W,
        "half": NATURE_HALF_W,
        "1.5": NATURE_HALF_W,
        "double": NATURE_DOUBLE_W,
        "full": NATURE_DOUBLE_W,
    }
    w = widths[columns]
    return (w, w * aspect)

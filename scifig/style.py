"""Style application and figure lifecycle.

Provides the two style systems the project supports:

* ``apply_publication_style`` -- figures4papers house style (spines off, larger
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

import matplotlib
import matplotlib.pyplot as plt
from cycler import cycler

from .palette import DEFAULT_COLORS, MODERN_COLORS, COLORBLIND_SAFE

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
    "PUBLICATION_STYLE",
    "MODERN_STYLE",
]


@dataclass(frozen=True)
class FigureStyle:
    """Tunable knobs for the publication style."""

    font_size: int = 16
    axes_linewidth: float = 2.5
    use_tex: bool = False
    font_family: tuple[str, ...] = ("DejaVu Sans", "Helvetica", "Arial", "sans-serif")


def _asset(name: str) -> Path:
    """Return the path of a bundled .mplstyle asset."""
    return Path(__file__).parent / "assets" / name


# ---------------------------------------------------------------------------
# Publication style (figures4papers house)
# ---------------------------------------------------------------------------
PUBLICATION_STYLE = "scientific_publication"
MODERN_STYLE = "modern"


def apply_publication_style(style: Optional[FigureStyle] = None) -> None:
    """Apply the publication-house style to matplotlib rcParams.

    Call once, before creating figures. When ``style`` is None a default
    ``FigureStyle`` (font_size 16, axes_linewidth 2.5) is used. The bundled
    ``scientific_publication.mplstyle`` is loaded first, then overridden by
    the ``style`` knobs so the whole style stays consistent.
    """
    if style is None:
        style = FigureStyle()
    asset = _asset("scientific_publication.mplstyle")
    if asset.exists():
        plt.style.use(str(asset))
    # Apply house-style overrides that differ from the .mplstyle defaults.
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.size": style.font_size,
            "axes.linewidth": style.axes_linewidth,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "text.usetex": style.use_tex,
        }
    )
    if style.font_family:
        plt.rcParams["font.sans-serif"] = list(style.font_family)


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
    ``'publication'`` (uses the figures4papers house palette).
    """
    palettes = {
        "publication": [
            "#3A6BC5", "#D4654A", "#4A9F6F", "#DE9E4A", "#B5637D", "#4A9496",
        ],
        "modern": MODERN_COLORS,
        "colorblind": COLORBLIND_SAFE,
        "dark": ["#1F2937", "#374151", "#4B5563", "#6B7280", "#9CA3AF", "#D1D5DB"],
        "pastel": [
            "#BFDBFE", "#FDE68A", "#A7F3D0", "#FECACA", "#DDD6FE", "#FBCFE8",
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

    If ``formats`` is None and ``out_path`` has an extension, that extension is
    used; otherwise pdf/svg/eps are written. Parent directories are created.
    Returns the list of saved ``Path``\s.
    """
    out = Path(out_path)
    if formats is None:
        if out.suffix:
            formats = [out.suffix.lstrip(".")]
        else:
            formats = ["pdf", "svg", "eps"]
    out.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for fmt in formats:
        target = out.with_suffix("." + fmt) if out.suffix else Path(str(out) + "." + fmt)
        kwargs.setdefault("bbox_inches", "tight")
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

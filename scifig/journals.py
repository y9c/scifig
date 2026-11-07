"""Publisher / journal figure specs.

Derived from the publisher author guidelines (as compiled by the Icarus-Figures
dataset). Each journal defines a single-column figure **width in inches** and a
**base font size in points**; ``journal_style`` returns an ``rcParams`` dict
that sizes a figure correctly for that venue, and ``journal_figsize`` gives the
in-dimensions ``(width, height)``.

> Specs drift across versions — always re-check the *current* author guidelines
> for your target journal. These are good defaults, not gospel.

Journal single-column widths (from public author guidelines):

    nature   3.50in (89mm)  base 7pt
    science  2.24in (5.7cm) base 7pt   (Science single column is narrow)
    cell     3.35in (85mm)  base 7pt
    ieee     3.50in (88.9mm) base 8pt
    pnas     3.42in (87mm)  base 8pt
    acs      3.33in         base 8pt
    rsc      3.27in (8.3cm) base 8pt
    elsevier 3.54in (90mm)  base 8pt
    aps      3.39in (8.6cm) base 8pt
"""

from __future__ import annotations

import matplotlib.pyplot as plt

__all__ = [
    "JOURNAL_SPEC",
    "journal_style",
    "journal_figsize",
    "fig_size_mm",
    "INCH_PER_MM",
]

INCH_PER_MM = 1.0 / 25.4

# name -> (single-column width inches, base font pt)
JOURNAL_SPEC = {
    "nature": (3.50, 7),
    "science": (2.24, 7),
    "cell": (3.35, 7),
    "ieee": (3.50, 8),
    "pnas": (3.42, 8),
    "acs": (3.33, 8),
    "rsc": (3.27, 8),
    "elsevier": (3.54, 8),
    "aps": (3.39, 8),
}


def journal_rc(name: str, aspect: float = 0.74) -> dict:
    """Build an ``rcParams`` dict for a journal's single-column figure.

    Sizes the figure to the journal's single-column width, sets the base font
    and a coherent type hierarchy (title/labels/ticks/legend scaled from it),
    with print-appropriate line/marker weights.
    """
    if name not in JOURNAL_SPEC:
        raise KeyError(f"unknown journal '{name}'; choose from {list(JOURNAL_SPEC)}")
    width_in, base = JOURNAL_SPEC[name]
    return {
        "figure.figsize": (width_in, round(width_in * aspect, 2)),
        "font.size": base,
        "axes.titlesize": base + 0.5,
        "axes.labelsize": base,
        "xtick.labelsize": base - 1,
        "ytick.labelsize": base - 1,
        "legend.fontsize": base - 1,
        "lines.linewidth": 1.3,
        "lines.markersize": 3.5,
        "axes.linewidth": 0.7,
    }


def journal_style(name: str, aspect: float = 0.74) -> None:
    """Apply a journal's single-column rcParams to matplotlib (idempotent)."""
    plt.rcParams.update(journal_rc(name, aspect=aspect))


def journal_figsize(name: str, aspect: float = 0.74):
    """Return ``(width, height)`` in inches for a journal's single column."""
    width_in, _ = JOURNAL_SPEC[name]
    return (width_in, round(width_in * aspect, 2))


def fig_size_mm(width_mm: float, aspect: float = 0.618, fraction: float = 1.0):
    """Return ``(width, height)`` in inches for a target column width in mm.

    ``aspect``: height/width (golden ratio 0.618 by default).
    ``fraction``: <1 to shrink (e.g. 0.5 for a half-width panel).

    >>> w, h = fig_size_mm(89)      # ~Nature single column (89 mm)
    """
    width_in = (width_mm * INCH_PER_MM) * fraction
    return (width_in, width_in * aspect)

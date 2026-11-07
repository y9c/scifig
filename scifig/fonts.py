"""Font detection and cross-platform fallback.

The publication style prefers Arial/Helvetica (the journal look), but these
aren't installed on every OS — Linux often lacks Arial. This module:

* reports which preferred sans fonts are actually available,
* recommends the best available substitute,
* and records the recommendation so ``apply_publication_style`` can pick the
  first available family instead of silently rendering DejaVu.
"""

from __future__ import annotations

from matplotlib import font_manager

__all__ = ["PREFERRED_SANS", "available_sans", "best_sans", "font_hint"]

# Most-published journals want Arial-like (Helvetica/Liberation Sans are
# metric-compatible); DejaVu Sans is matplotlib's bundled fallback.
PREFERRED_SANS = ["Arial", "Helvetica", "Liberation Sans", "Nimbus Sans", "DejaVu Sans"]


def available_sans(families=None):
    """Return the subset of ``families`` installed on this machine."""
    fams = list(families or PREFERRED_SANS)
    installed = {f.name for f in font_manager.fontManager.ttflist}
    return [f for f in fams if f in installed]


def best_sans():
    """Return the top-priority sans font actually installed."""
    av = available_sans()
    return av[0] if av else "DejaVu Sans"


def font_hint():
    """Return a short human message about the sans-font situation."""
    av = available_sans()
    if "Arial" in av:
        return "Arial found — journal look active."
    if "Helvetica" in av:
        return "Helvetica found (metric-compatible with Arial)."
    if "Liberation Sans" in av:
        return (
            "Liberation Sans found (Arial substitute). On Linux install "
            "ttf-mscorefonts-installer for real Arial."
        )
    return (
        "No Arial/Helvetica/Liberation; will fall back to DejaVu Sans. "
        "Install an Arial-like font for the journal look."
    )

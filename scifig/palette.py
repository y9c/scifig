"""Semantic color palettes for publication figures.

Two families coexist:

* ``PALETTE`` / ``DEFAULT_COLORS`` -- the figures4papers house palette (blue =
  proposed method, green = improvement, red = baseline/contrast, neutral =
  background). Used by ``apply_publication_style`` and the ``make_*`` helpers.
* ``MODERN_COLORS`` / ``COLORBLIND_SAFE`` -- clean categorical palettes for the
  modern / presentation style.

These are module-level constants so downstream code can read them without
importing matplotlib.
"""

# ---------------------------------------------------------------------------
# figures4papers-style semantic palette
# ---------------------------------------------------------------------------
PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}

# Ordered fallback when ``colors`` is not passed to plot helpers.
DEFAULT_COLORS = [
    PALETTE["blue_main"],
    PALETTE["green_3"],
    PALETTE["red_strong"],
    PALETTE["teal"],
    PALETTE["violet"],
    PALETTE["neutral"],
]

# modern / presentation categorical palette
MODERN_COLORS = [
    "#0EA5E9",  # Sky Blue
    "#F59E0B",  # Amber
    "#10B981",  # Emerald
    "#EF4444",  # Red
    "#8B5CF6",  # Violet
    "#EC4899",  # Pink
    "#06B6D4",  # Cyan
    "#F97316",  # Orange
    "#84CC16",  # Lime
    "#6366F1",  # Indigo
]

# More accessible combinations for colorblind-friendly plots
COLORBLIND_SAFE = [
    "#006BA4",  # Blue
    "#FF800E",  # Orange
    "#ABABAB",  # Gray
    "#595959",  # Dark Gray
    "#5F9ED1",  # Light Blue
    "#C85200",  # Dark Orange
    "#898989",  # Medium Gray
    "#A2C8EC",  # Pale Blue
    "#FFBC79",  # Pale Orange
    "#CFCFCF",  # Light Gray
]

# Second categorical family used by modern.mplstyle's prop_cycle
MODERN_STYLE_COLORS = [
    "#2563EB", "#DC2626", "#059669", "#D97706", "#7C3AED",
    "#DB2777", "#0891B2", "#EA580C", "#65A30D", "#4F46E5",
]

# scientific_publication.mplstyle prop_cycle
PUBLICATION_STYLE_COLORS = [
    "#3A6BC5", "#D4654A", "#4A9F6F", "#DE9E4A", "#B5637D",
    "#4A9496", "#6A6CB2", "#5A6578",
]
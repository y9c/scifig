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

# ---------------------------------------------------------------------------
# Named colorblind-safe palettes (pypubfigs / Okabe-Ito derived)
# ---------------------------------------------------------------------------
# B&W-printable and deuteranopia-safe via distinct luminance; pair with distinct
# markers/linestyles for full redundancy.
FRIENDLY_PALS = {
    "bright_seven": ["#4477AA", "#228833", "#AA3377", "#BBBBBB", "#66CCEE", "#CCBB44", "#EE6677"],
    "contrast_three": ["#004488", "#BB5566", "#DDAA33"],
    "vibrant_seven": ["#0077BB", "#EE7733", "#33BBEE", "#CC3311", "#009988", "#EE3377", "#BBBBBB"],
    "muted_nine": [
        "#332288",
        "#117733",
        "#CC6677",
        "#88CCEE",
        "#999933",
        "#882255",
        "#44AA99",
        "#DDCC77",
        "#AA4499",
    ],
    "ito_seven": ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#56B4E9", "#E69F00", "#F0E442"],
    "wong_eight": [
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
        "#000000",
    ],
    "tol_bright": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"],
    "tol_muted": [
        "#332288",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#CC6677",
        "#882255",
        "#AA4499",
    ],
    "nickel_five": ["#648FFF", "#FE6100", "#785EF0", "#FFB000", "#DC267F"],
    "tableau_ten": [
        "#4E79A7",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#59A14F",
        "#EDC948",
        "#B07AA1",
        "#FF9DA7",
        "#9C755F",
        "#BAB0AC",
    ],
}


def friendly_pal(name: str, n=None) -> list[str]:
    """Return a named colorblind-safe palette (pypubfigs / Okabe-Ito derived).

    ``n`` truncates to the first ``n`` colors; raise if ``n`` exceeds the palette.
    """
    pal = FRIENDLY_PALS.get(name)
    if pal is None:
        raise KeyError(f"unknown palette '{name}'; choose from {list(FRIENDLY_PALS)}")
    if n is None:
        n = len(pal)
    if n > len(pal):
        raise ValueError(f"palette '{name}' has {len(pal)} colors, requested {n}")
    return list(pal[:n])

# house-style.md — copy-paste publication style

This is the single source of truth for scifig's look. **Copy the style preamble
into any figure script** to get the exact publication appearance with plain
matplotlib (no package needed). It guarantees: Arial ~5-6pt, thin spines,
semantic colors, readable/minor ticks, panel letters at the corner, and
vector-first export.

## The style preamble (paste at the top of every script)

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---- scifig house style ----------------
BASE = 6.0                      # base font size (pt); ~6 at Nature column width
AX_LW = 0.8                     # axes/spine linewidth
FONT_FAMILY = ["Arial", "Helvetica", "DejaVu Sans"]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": FONT_FAMILY,
    "font.size": BASE,
    "axes.titlesize": BASE * 1.15,
    "axes.labelsize": BASE * 1.05,
    "xtick.labelsize": BASE,
    "ytick.labelsize": BASE,
    "legend.fontsize": BASE * 0.95,
    "legend.title_fontsize": BASE * 1.05,
    "mathtext.default": "regular",
    "axes.linewidth": AX_LW,
    "lines.linewidth": 1.0,
    "lines.markeredgewidth": 0.6,
    "xtick.major.width": AX_LW * 0.8,
    "ytick.major.width": AX_LW * 0.8,
    "xtick.major.size": BASE * 0.5,
    "ytick.major.size": BASE * 0.5,
    # vector-safe editable text + exact size
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "legend.labelcolor": "linecolor",
    "savefig.bbox": "standard",
    # house rules
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
})
# ---------------------------------------
```

> Style is applied once, before creating figures. Never tweak rcParams per script.

## Semantic palette + assignment

Colors carry meaning — blue = key/our method, green = improvement, red =
baseline, gray = background.

```python
PALETTE = {
    "blue_main": "#0F4D92", "blue_secondary": "#3775BA",
    "green_3": "#8BCF8B", "red_strong": "#B64342",
    "neutral": "#CFCECE", "teal": "#42949E", "violet": "#9A4D8E",
}

def assign_colors(labels, ours_marker=None):
    """Assign semantic colors; the label containing ours_marker is blue."""
    if ours_marker:
        order = ["blue_main", "red_strong", "green_3", "teal", "violet", "neutral"]
        out, k = [], 1
        for lab in labels:
            if ours_marker in lab:
                out.append(PALETTE["blue_main"])
            else:
                out.append(PALETTE[order[k % len(order)]]); k += 1
        return out
    return [PALETTE[c] for c in ["blue_main", "red_strong", "green_3", "teal", "violet", "neutral"][:len(labels)]]
```

Colorblind-safe palettes (Okabe-Ito / Tol / Wong):

```python
FRIENDLY = {
    "wong": ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"],
    "okabe_ito": ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#56B4E9", "#E69F00", "#F0E442"],
}
```

## Reusable helpers (paste once, use everywhere)

```python
def save(fig, out, formats=("pdf",), dpi=600):
    """Vector-first save. PDF by default; add "png" for a screen preview."""
    import os
    from pathlib import Path
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        fig.savefig(f"{out}.{fmt}", format=fmt, dpi=dpi,
                    bbox_inches="standard", facecolor="white")

def panel_label(ax, letter, x=-0.12, y=1.02, size=None):
    """Panel letter at the top-left corner (outside the axes)."""
    ax.text(x, y, letter, transform=ax.transAxes, va="bottom", ha="left",
            fontsize=size or 1.2 * plt.rcParams["font.size"], fontweight="bold")

def readable_ticks(ax, n=5):
    """Deliberate tick density (not matplotlib defaults)."""
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator
    ax.yaxis.set_major_locator(MaxNLocator(nbins=n, integer=False))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=n, integer=False))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(which="minor", length=2.0, width=0.4)
    ax.tick_params(which="major", length=3.2, width=0.6)

def finish(ax, grid=False, xlabel=None, ylabel=None, title=None):
    """One-call polish: labels, readable ticks, optional subtle grid behind data."""
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title: ax.set_title(title, pad=4)
    readable_ticks(ax)
    if grid:
        ax.grid(True, color="#DDDDDD", alpha=0.5, linewidth=0.5)
        ax.set_axisbelow(True)
    return ax


def bar_labels(ax, bars, fmt="{:.2f}", pad=3):
    """Value labels above bars (skips nan)."""
    for r in bars:
        h = r.get_height()
        if h is None or not np.isfinite(h):
            continue
        ax.annotate(fmt.format(h), (r.get_x() + r.get_width()/2, h),
                    xytext=(0, pad), textcoords="offset points",
                    ha="center", va="bottom", fontsize=plt.rcParams["font.size"])
```

## Figure sizes (physical, in inches)

```python
def nature_figsize(width="single", aspect=0.75):
    w = {"single": 3.50, "half": 5.00, "double": 7.20}[width]
    return (w, w * aspect)
```

Journal single-column widths: nature 3.50in / science 2.24 / cell 3.35 /
ieee 3.50 / pnas 3.42 / elsevier 3.54 (base font 7-8pt).

## End-to-end pattern

```python
# 1) style
BASE = 6.0                          # (paste the preamble above)
# 2) figure at final size
fig, ax = plt.subplots(figsize=nature_figsize("single"))
# 3) plot (any geometry)
ax.bar([0, 1], [0.9, 0.8], color=PALETTE["blue_main"], edgecolor="black", linewidth=0.5)
ax.set_ylabel("Accuracy")
# 4) polish
finish(ax, ylabel="Accuracy")
# 5) vector-first save
save(fig, "out/fig")          # -> out/fig.pdf (vector)
```

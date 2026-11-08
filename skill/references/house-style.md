# house-style — copy-paste style + helpers

Copy the style + helpers into your script. Plain matplotlib, no package.

## Style preamble (copy at top)

```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
  "font.size": 6, "font.family": "sans-serif",
  "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
  "axes.titlesize": 6*1.15, "axes.labelsize": 6*1.05,
  "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6*0.95,
  "axes.linewidth": 0.8, "lines.linewidth": 1.0,
  "axes.spines.top": False, "axes.spines.right": False,
  "legend.frameon": False,
  "pdf.fonttype": 42, "svg.fonttype": "none", "savefig.bbox": "standard",
})
```

## Colors

```python
BLUE="#0F4D92"; RED="#B64342"; GREEN="#8BCF8B"; GRAY="#CFCECE"  # key / literal baseline / improve / neutral
```

## Helpers (copy once)

```python
def save(fig, out, dpi=600):
    fig.savefig(f"{out}.pdf", dpi=dpi, facecolor="white")

def ticks(ax):
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5)); ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(which="minor", length=2, width=0.4)

def panel(ax, letter):
    ax.text(-0.12, 1.02, letter, transform=ax.transAxes, va="bottom", fontweight="bold")
```

## Sizes

```python
figsize = {"single": (3.5, 2.6), "half": (5.0, 3.75), "double": (7.2, 5.4)}
```

## End-to-end

```python
# style (above) ; fig, ax = plt.subplots(figsize=figsize["single"])
# plot ; ticks(ax) ; save(fig, "out/x")
```

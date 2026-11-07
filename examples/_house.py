"""scifig house style — a tiny, self-contained helper for publication figures.

This is NOT a package: it is a local module any example script can import so the
figures look uniform with zero pip install. The full spec (copy-paste rcParams)
lives in `skill/references/house-style.md`; here it is as callable helpers.

Usage:  from _house import style, palette, save, finish, panel_label, ...
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Semantic palette (blue=key, green=improve, red=baseline, gray=background)
PALETTE = {
    "blue_main": "#0F4D92", "blue_secondary": "#3775BA",
    "green_3": "#8BCF8B", "red_strong": "#B64342",
    "neutral": "#CFCECE", "teal": "#42949E", "violet": "#9A4D8E",
}

FRIENDLY = {
    "wong": ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"],
    "okabe_ito": ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#56B4E9", "#E69F00", "#F0E442"],
    "tol_bright": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"],
    "tol_muted": ["#332288", "#88CCEE", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677"],
}

# Column widths (inches)
NATURE = {"single": 3.50, "half": 5.00, "double": 7.20}


def style(font_size=6.0, axes_linewidth=0.8, font=None, grid=False):
    """Apply the publication house style (call once, before creating figures)."""
    fs = font_size
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": font or ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": fs,
        "axes.titlesize": fs * 1.15,
        "axes.labelsize": fs * 1.05,
        "xtick.labelsize": fs,
        "ytick.labelsize": fs,
        "legend.fontsize": fs * 0.95,
        "mathtext.default": "regular",
        "axes.linewidth": axes_linewidth,
        "lines.linewidth": 1.0,
        "lines.markeredgewidth": 0.6,
        "xtick.major.width": axes_linewidth * 0.8,
        "ytick.major.width": axes_linewidth * 0.8,
        "xtick.major.size": fs * 0.5,
        "ytick.major.size": fs * 0.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "legend.labelcolor": "linecolor",
        "savefig.bbox": "standard",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
    })


def figsize(width="single", aspect=0.75):
    """Physical figure size in inches for a Nature column width."""
    return (NATURE[width], NATURE[width] * aspect)


def palette_labels(labels, ours_marker=None):
    """Semantic colors for a list of legend labels (blue=key/ours)."""
    order = ["blue_main", "red_strong", "green_3", "teal", "violet", "neutral"]
    if ours_marker:
        out, k = [], 1
        for lab in labels:
            if ours_marker in lab:
                out.append(PALETTE["blue_main"])
            else:
                out.append(PALETTE[order[k % len(order)]]); k += 1
        return out
    return [PALETTE[c] for c in order[: len(labels)]]


def save(fig, out, formats=("pdf",), dpi=600):
    """Vector-first save (PDF default)."""
    import os
    from pathlib import Path
    if out.startswith("~"):
        out = os.path.expanduser(out)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        fig.savefig(f"{out}.{fmt}", format=fmt, dpi=dpi, facecolor="white")
    return out


def panel_label(ax, letter, x=-0.12, y=1.02):
    """Panel letter at the top-left corner (outside the axes)."""
    ax.text(x, y, letter, transform=ax.transAxes, va="bottom", ha="left",
            fontsize=1.2 * plt.rcParams["font.size"], fontweight="bold")


def panel_letters(axes, case="lower"):
    for i, ax in enumerate(axes):
        letter = chr(97 + i) if case == "lower" else chr(65 + i)
        panel_label(ax, letter)


def readable_ticks(ax, n=5):
    """Deliberate tick density + minor ticks."""
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator
    ax.yaxis.set_major_locator(MaxNLocator(nbins=n, integer=False))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=n, integer=False))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(which="minor", length=2.0, width=0.4)
    ax.tick_params(which="major", length=3.2, width=0.6)


def finish(ax, grid=False, xlabel=None, ylabel=None, title=None):
    """One-call polish."""
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title: ax.set_title(title, pad=4)
    readable_ticks(ax)
    if grid:
        ax.grid(True, color="#DDDDDD", alpha=0.5, linewidth=0.5)
        ax.set_axisbelow(True)
    return ax


def bar_labels(ax, bars, fmt="{:.2f}", pad=3):
    """Value labels above bars."""
    for r in bars:
        h = r.get_height()
        if h is None or not np.isfinite(h):
            continue
        ax.annotate(fmt.format(h), (r.get_x() + r.get_width() / 2, h),
                    xytext=(0, pad), textcoords="offset points",
                    ha="center", va="bottom", fontsize=plt.rcParams["font.size"])


def shared_legend(fig, labels, handles, location="upper center", ncol=None, clear=True):
    """One legend for all axes (dedup by label)."""
    if clear:
        for ax in fig.axes:
            if ax.get_legend() is not None:
                ax.get_legend().remove()
    fig.legend(handles, labels, loc=location, ncol=ncol or len(labels), frameon=False)


def grid(nrows=1, ncols=1, width="double", aspect=0.5, wspace=0.16, hspace=0.30):
    """Return (fig, axes) as a flat array for a multi-panel figure."""
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize(width, aspect))
    fig.subplots_adjust(wspace=wspace, hspace=hspace)
    return fig, np.asarray(axes).reshape(-1)


# --- common plot builders (kept small; the real spec is in skill references) ---
def grouped_bar(ax, categories, series, labels, ylabel="Value", colors=None,
                ours_marker=None, annotate=False, yerr=None, capsize=3,
                hide_xticks=False):
    """Grouped bars with optional error bars; semantic colors by default."""
    x = np.arange(len(categories))
    s = [np.asarray(v, float) for v in series]
    n = len(s)
    w = 0.8 / n
    colors = colors or palette_labels(labels, ours_marker)
    last = None
    for i, (sv, lab) in enumerate(zip(s, labels)):
        off = (i - (n - 1) / 2) * w
        ye = None
        if yerr is not None:
            ye = np.asarray(yerr, float)
            ye = ye[i] if ye.ndim == 2 and ye.shape[0] == n else ye
        last = ax.bar(x + off, sv, width=w, label=lab, color=colors[i % len(colors)],
                      edgecolor="black" if ye is None else "none", linewidth=0.5,
                      yerr=ye, error_kw={"ecolor": "black", "capsize": capsize})
    if hide_xticks:
        ax.set_xticks([])
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    if any(str(l) for l in labels):
        ax.legend(frameon=False)
    if annotate:
        bar_labels(ax, last)
    return last


def trend(ax, x, ys, labels, colors=None, ours_marker=None, ylabel=None,
          xlabel=None, show_shadow=True):
    """Lines with optional uncertainty band (2-col mean/std series)."""
    x = np.asarray(x, float)
    colors = colors or palette_labels(labels, ours_marker)
    for i, (yv, lab) in enumerate(zip(ys, labels)):
        yv = np.asarray(yv, float)
        mean, std = yv, None
        if yv.ndim == 2 and yv.shape[1] >= 2:
            mean, std = yv[:, 0], yv[:, 1]
        c = colors[i % len(colors)]
        ax.plot(x, mean, label=lab, color=c)
        if show_shadow and std is not None:
            ax.fill_between(x, mean - std, mean + std, color=c, alpha=0.18, linewidth=0)
    if ylabel: ax.set_ylabel(ylabel)
    if xlabel: ax.set_xlabel(xlabel)
    if any(str(l) for l in labels):
        ax.legend(frameon=False)


def heatmap(ax, matrix, x_labels=None, y_labels=None, cmap="magma",
            cbar_label=None, annotate=False):
    """2D heatmap with optional colorbar label and cell annotations."""
    m = np.asarray(matrix, float)
    im = ax.imshow(m, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(m.shape[1])); ax.set_yticks(np.arange(m.shape[0]))
    if x_labels is not None:
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
    if y_labels is not None:
        ax.set_yticklabels(y_labels)
    cb = ax.figure.colorbar(im, ax=ax, shrink=0.82)
    if cbar_label:
        cb.set_label(cbar_label, rotation=270, labelpad=15)
    if annotate:
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                ax.text(j, i, f"{m[i, j]:.2f}", ha="center", va="center", color="white")
    return im


def scatter(ax, x, y, label=None, color=None, size=40, alpha=0.7):
    """Single-series scatter."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if color is None:
        color = PALETTE["blue_main"]
    s = ax.scatter(x, y, s=size, c=color, alpha=alpha, label=label)
    if label:
        ax.legend(frameon=False)
    return s


def join_figures(files, out, ncols=None, labels=None, dpi=300):
    """Stitch saved PNG/PDF panels into one figure; returns (fig, axes)."""
    import matplotlib.image as mpimg
    files = [str(f) for f in files]
    n = len(files)
    if ncols is None:
        ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.5 * ncols, 2.625 * nrows))
    axes = np.asarray(axes).reshape(-1)
    for i, f in enumerate(files):
        axes[i].imshow(mpimg.imread(f))
        axes[i].set_axis_off()
    for ax in axes[n:]:
        ax.set_axis_off()
    if labels:
        panel_letters(axes, case="lower")
    fig.subplots_adjust(wspace=0.05, hspace=0.05)
    save(fig, out, formats=("png",), dpi=dpi)
    return fig, axes


def add_sig(ax, x0, x1, y, marker="***", height=0.03):
    """Significance bracket labelled with marker."""
    ax.plot([x0, x0, x1, x1], [y, y + height, y + height, y], "k-", lw=0.8)
    ax.text((x0 + x1) / 2, y + height * 1.05, marker, ha="center", va="bottom",
            fontsize=plt.rcParams["font.size"])


def add_inset(ax, loc, size="30%"):
    """Return an inset axes."""
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    return inset_axes(ax, width=size, height=size, loc=loc)

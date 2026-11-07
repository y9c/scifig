"""Vector protein structure rendering (pure matplotlib).

Renders a protein's 2-D backbone (Cα) trace with secondary-structure shading as
**vector** matplotlib output — no PyMOL/GUI dependency, so it exports cleanly to
PDF/SVG for publications.

Structure data is loaded with **Biotite** (optional): fetch a PDB entry or read a
local PDB/mmCIF file into an ``AtomArray``. If Biotite isn't installed, a small
built-in demo helix-structure is used so the figure still renders.

This is deliberately 2-D and clean (the standard journal "topology/ribbon" look)
rather than a full 3-D ray-traced render; 3-D volumes are better served by
PyMOL/Chimera, which this module does not try to replace.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from .palette import PALETTE

__all__ = [
    "fetch_structure",
    "load_structure",
    "demo_structure",
    "draw_topology",
    "ribbon_trace",
]

_HELIX_RADIUS = 1.1
_SHEET_LEN = 3.0


def fetch_structure(pdb_id: str) -> Optional[np.ndarray]:
    """Download a PDB entry as an ``AtomArray`` (Biotite required).

    Returns ``None`` if Biotite or the network is unavailable.
    """
    try:
        import biotite.structure.io.pdb as pdb
    except ImportError:
        return None
    try:
        import biotite.database.rcsb as rcsb
        tmp = pdb.PDBFile.read(rcsb.fetch(pdb_id))
        return pdb.get_structure(tmp)[0]
    except Exception:
        return None


def load_structure(path: str) -> Optional[np.ndarray]:
    """Read a local PDB file into an ``AtomArray`` (Biotite required)."""
    try:
        import biotite.structure.io.pdb as pdb
        tmp = pdb.PDBFile.read(path)
        return pdb.get_structure(tmp)[0]
    except Exception:
        return None


def demo_structure():
    """Return a compact 2-D folded topology as a (N,3) Cα coordinate array.

    A recognizable globular mix: four alpha-helices (undulating vertical
    ribbons) + two parallel beta-strands, used when Biotite isn't installed so
    the module always renders a meaningful topology for demos.
    """
    xy = []
    for x0, amp in ((1.0, 0.55), (5.0, 0.6), (9.0, 0.5), (13.0, 0.62)):
        y = np.linspace(1.0, 15.0, 60)
        # real alpha-helix: undulate perpendicular to the rising axis
        x = x0 + amp * np.sin(np.linspace(0, 4 * np.pi, 60))
        xy.append(np.stack([x, y], axis=1))
    # two parallel beta-strands (arrows) near the bottom
    for y0, dy in ((8.5, 0.0), (10.5, 0.4)):
        xy.append(np.stack([np.linspace(1.0, 19.0, 40),
                            np.full(40, y0) + np.linspace(0, dy, 40)], axis=1))
    coords = np.vstack(xy)
    coords = np.hstack([coords, np.zeros((coords.shape[0], 1))])
    return coords


def _sse_from_array(struct):
    """Best-effort secondary-structure labels (H/E/other) from a Biotite array."""
    try:
        import biotite.structure as struc
        sse = struc.annotate_sse(struct)
        return sse  # 'h' / 'e' / '-' per residue (aligned to first atom per residue)
    except Exception:
        return None


def ribbon_trace(ax, coords, sse=None, color=PALETTE["blue_main"],
                 helix_scale=1.15, lw=1.0):
    """Draw a Cα backbone with secondary-structure shaded ribbons (vector).

    ``coords``: (N,3) Cα array. ``sse``: optional per-residue secondary structure
    string (bold/raised for helix H, arrow for sheet E). Returns ``ax``.
    """
    coords = np.asarray(coords, float)
    if coords.ndim != 2 or coords.shape[1] < 2:
        raise ValueError("coords must be (N, 2) or (N, 3)")
    xy = coords[:, :2]
    # ensure sse is a 1-D array of single characters (np.isin needs a sequence)
    if sse is None:
        sse = np.array(["-"] * len(xy))
    else:
        sse = np.asarray(list(sse))
    if len(sse) != len(xy):
        sse = np.array(["-"] * len(xy))

    # backbone polyline
    ax.plot(xy[:, 0], xy[:, 1], color="0.4", linewidth=lw, zorder=2)

    # helix: thick rounded ribbon (cylinder look)
    mask_h = np.isin(sse, ["h", "H"])
    if mask_h.any():
        _draw_helix(ax, xy, mask_h, color, helix_scale)
    # sheet: arrow segments
    mask_e = np.isin(sse, ["e", "E"])
    if mask_e.any():
        _draw_sheet_arrows(ax, xy, mask_e, color)
    return ax


def _draw_helix(ax, xy, mask, color, scale):
    idx = np.where(mask)[0]
    if idx.size < 2:
        return
    # split contiguous runs
    for run in _runs(idx):
        if len(run) < 3:
            continue
        p = xy[run]
        # thick filled ribbon (dominant), then a thin core line
        ax.plot(p[:, 0], p[:, 1], color=color, linewidth=9 * scale,
                solid_capstyle="round", alpha=0.5, zorder=1)
        ax.plot(p[:, 0], p[:, 1], color="white", linewidth=0.8,
                solid_capstyle="round", zorder=2)
        ax.plot(p[:, 0], p[:, 1], color=color, linewidth=1.6, zorder=3)


def _draw_sheet_arrows(ax, xy, mask, color):
    idx = np.where(mask)[0]
    if idx.size < 2:
        return
    for run in _runs(idx):
        if len(run) < 2:
            continue
        p = xy[run]
        _arrow(ax, p[0], p[-1], color)


def _arrow(ax, start, end, color):
    import matplotlib.patches as mpatches
    s = np.asarray(start, float)
    e = np.asarray(end, float)
    d = e - s
    L = np.hypot(*d)
    if L < 1e-6:
        return
    u = d / L
    width = 0.5
    head = min(1.2, L * 0.4)
    # build arrow polygon centered on the segment
    n = np.array([-u[1], u[0]])
    base = s
    tip = e
    left = base + n * width
    right = base - n * width
    head_l = tip - u * head + n * width
    head_r = tip - u * head - n * width
    poly = np.array([left, right, head_r, tip, head_l])
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor=color,
                                  edgecolor=color, alpha=0.85, zorder=2))


def _runs(idx):
    """Split sorted indices into contiguous runs."""
    if len(idx) == 0:
        return []
    runs, cur = [], [idx[0]]
    for i in idx[1:]:
        if i == cur[-1] + 1:
            cur.append(i)
        else:
            runs.append(cur)
            cur = [i]
    runs.append(cur)
    return runs


def draw_topology(ax, coords, sse=None, xlabel="x (Å)", ylabel="y (Å)",
                  color=PALETTE["blue_main"]):
    """Full 2-D topology cartoon on a ready axes (symmetric limits, clean)."""
    ribbon_trace(ax, coords, sse=sse, color=color)
    ax.set_aspect("equal")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(labelsize=6)
    return ax

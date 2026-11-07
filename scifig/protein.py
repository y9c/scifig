"""Vector protein structure rendering (pure matplotlib).

Renders a protein's backbone with secondary-structure ribbons (helices, sheets)
projected from the real 3-D coordinates as **vector** matplotlib output — no
PyMOL/GUI dependency, so it exports cleanly to PDF/SVG for publications.

Structure data is loaded with **Biotite** (optional): fetch a PDB entry or read a
local PDB/mmCIF file into an ``AtomArray``, compute real secondary structure via
``annotate_sse``, and draw the cartoon. If Biotite isn't installed, a built-in
demo structure is used so the module still renders.
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
    "ribbon_3d",
    "draw_protein_from_pdb",
    "pymol_cartoon",
    "_normalize_sse",
]


def fetch_structure(pdb_id: str, retries: int = 3) -> Optional[np.ndarray]:
    """Download a PDB entry as an ``AtomArray`` (Biotite required).

    Handles ``rcsb.fetch`` returning either a temp-file path or a ``StringIO``
    (version-dependent), with a small retry for transient network failures.
    Returns ``None`` if Biotite or the network is unavailable.
    """
    try:
        import biotite.structure.io.pdb as pdb
    except ImportError:
        return None
    import io
    import time
    for _ in range(retries):
        try:
            import biotite.database.rcsb as rcsb
            res = rcsb.fetch(pdb_id, format="pdb")
            if hasattr(res, "getvalue"):
                tmp = pdb.PDBFile.read(io.StringIO(res.getvalue()))
            elif isinstance(res, str):
                tmp = pdb.PDBFile.read(res)
            else:
                tmp = pdb.PDBFile.read(res)
            return pdb.get_structure(tmp)[0]
        except Exception:
            time.sleep(1.0)
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
    """Compute per-residue secondary structure from a Biotite ``AtomArray``.

    Returns a normalized array of ``h`` (helix) / ``e`` (sheet) / ``-`` (coil),
    aligned to the Cα atoms. Biotite's ``annotate_sse`` returns ``a``/``b``/``c``;
    we map those to the common ``h``/``e``/``-`` scheme. Returns ``None`` if
    Biotite isn't available.
    """
    try:
        import biotite.structure as struc
    except ImportError:
        return None
    try:
        ca = struct[struct.atom_name == "CA"]
        sse = struc.annotate_sse(ca)
        sse = _normalize_sse(sse)
        return sse
    except Exception:
        return None


def _smooth(coords, window=5):
    """Moving-average smooth a (N,3) Cα trace (reduces per-residue noise)."""
    c = np.asarray(coords, float)
    if len(c) < window:
        return c
    k = np.ones(window) / window
    out = np.zeros_like(c)
    for d in range(c.shape[1]):
        out[:, d] = np.convolve(c[:, d], k, mode="same")
    return out


def _normalize_sse(sse):
    """Map SSE letters to a canonical h/e/- scheme (accept Biotite a/b/c and h/e)."""
    sse = np.asarray(list(sse))
    out = np.full(sse.shape, "-", dtype="<U1")
    out[np.isin(sse, ["a", "A", "h", "H"])] = "h"
    out[np.isin(sse, ["b", "B", "e", "E"])] = "e"
    return out


def _project(coords, view=None):
    """Project 3D coords to 2D. ``view``: optional 3x3 rotation (default: simple).
    Returns (xy, depth) where depth = z-value for shading.
    """
    c = np.asarray(coords, float)
    if c.shape[1] < 3:
        return c[:, :2], np.zeros(len(c))
    if view is not None:
        R = np.asarray(view, float)
        if R.shape == (3, 3):
            c = c @ R.T
    # normalize to center, scale to unit-ish so linewidths are stable
    xy = c[:, :2]
    depth = c[:, 2]
    return xy, depth


def _ribbon_widths(xy, depth, base_w, min_w=0.3, max_w=2.4):
    """Width per residue: helices wider, depth-scaled for a shaded 3D look."""
    # depth-normalised shading (proximity to viewer -> brighter, wider)
    d = (depth - depth.min()) / (depth.max() - depth.min() + 1e-9) - 0.5
    return base_w * (1.0 + 0.6 * d), d


def ribbon_3d(ax, coords, sse=None, color=PALETTE["blue_main"], view=None,
              base_w=1.6, lw=0.6):
    """Render a 3-D protein cartoon: ribbon tubes with depth shading (vector).

    ``coords`` (N,3); ``sse`` normalized h/e/-; ``view`` optional 3x3 rotation.
    Helices are drawn as wider, depth-shaded ribbon tubes; sheets as arrows;
    coils as thin lines. Everything stays vector (matplotlib).
    """
    xy, depth = _project(coords, view)
    wid, _ = _ribbon_widths(xy, depth, base_w)
    if sse is None:
        sse = np.array(["-"] * len(xy))
    else:
        sse = _normalize_sse(sse)
    if len(sse) != len(xy):
        sse = np.array(["-"] * len(xy))

    # coil backbone (thin)
    ax.plot(xy[:, 0], xy[:, 1], color="0.35", linewidth=lw, zorder=2)
    # helix: thick ribbon tube per run
    for run in _runs(np.where(np.isin(sse, ["h"]))[0]):
        if len(run) < 4:
            continue
        p = xy[run]
        ax.plot(p[:, 0], p[:, 1], color=color, linewidth=base_w * 4,
                solid_capstyle="round", alpha=0.30, zorder=1)
        ax.plot(p[:, 0], p[:, 1], color=color, linewidth=base_w * 1.6, zorder=3)
        ax.plot(p[:, 0], p[:, 1], color="white", linewidth=lw, zorder=4)
    # sheet: arrow
    for run in _runs(np.where(np.isin(sse, ["e"]))[0]):
        if len(run) < 2:
            continue
        _arrow(ax, xy[run][0], xy[run][-1], color)
    return ax, xy, depth


def draw_topology(ax, coords, sse=None, xlabel="x (Å)", ylabel="y (Å)",
                  color=PALETTE["blue_main"], view=None):
    """Full 2-D-projected topology cartoon on a ready axes."""
    ribbon_3d(ax, coords, sse=sse, color=color, view=view)
    ax.set_aspect("equal")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(labelsize=6)
    return ax


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


def draw_protein_from_pdb(ax, pdb_id, chain=None, view=None,
                          color=PALETTE["blue_main"], xlabel="x (Å)", ylabel="y (Å)"):
    """Fetch a PDB entry (Biotite), compute real SSE, and draw a vector cartoon.

    ``chain``: restrict to one chain id (e.g. "A"); the largest chain is used if
    None. Falls back to the demo structure if Biotite/network is unavailable.
    Returns ``ax``.
    """
    struct = fetch_structure(pdb_id)
    if struct is not None:
        ca = struct[struct.atom_name == "CA"]
        if chain is not None:
            ca = ca[ca.chain_id == chain]
        else:
            best = max(set(ca.chain_id), key=lambda c: int((ca.chain_id == c).sum()))
            ca = ca[ca.chain_id == best]
        if len(ca) < 4:
            coords, sse = demo_structure(), None
        else:
            coords = ca.coord if hasattr(ca, "coord") else np.asarray(ca)
            # compute SSE on the exact CA subset being drawn (correct alignment)
            sse = _sse_from_array(ca)
    else:
        coords, sse = demo_structure(), None
    if sse is not None and len(sse) != len(coords):
        sse = None
    coords = _smooth(coords, window=5)
    ribbon_3d(ax, coords, sse=sse, color=color, view=view)
    ax.set_aspect("equal")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(labelsize=6)
    return ax


def pymol_cartoon(pdb_id: str, out: str, chain=None, pdb_path=None,
                  width=2200, height=1800, dpi=300,
                  helix_color="marine", sheet_color="orange", loop_color="white",
                  bg="white", **kwargs):
    """Render a protein to a publication PNG with PyMOL (best look, raster).

    Uses the real PyMOL engine (requires the ``pymol`` module, e.g. from the
    Homebrew ``pymol`` formula). Renders a clean cartoon: single chain by
    default, white background, secondary-structure coloring, ray-traced.

    ``pdb_id``: a 4-letter PDB id (fetched via Biotite to a temp file) or, if
    ``pdb_path`` given, a local PDB file. Returns the output path.

    Note: PyMOL exports a **raster** PNG (see docs/protein-rendering.md); for a
    true vector cartoon use ``draw_topology``/``ribbon_3d`` instead.
    """
    import os
    import tempfile
    try:
        from pymol import cmd
    except ImportError as exc:
        raise RuntimeError("PyMOL is required: pip install pymol-open-source or "
                           "brew install pymol (and use that python).") from exc

    if pdb_path is None:
        try:
            import biotite.database.rcsb as rcsb
            res = rcsb.fetch(pdb_id, format="pdb")
            text = res.getvalue() if hasattr(res, "getvalue") else res
            tmpf = tempfile.NamedTemporaryFile(suffix=".pdb", delete=False)
            tmpf.write(text.encode() if isinstance(text, str) else text)
            tmpf.close()
            pdb_path = tmpf.name
        except Exception:
            raise RuntimeError(f"could not fetch PDB id {pdb_id!r}")

    cmd.reinitialize()
    cmd.load(pdb_path, "obj")
    cmd.remove("solvent")
    cmd.remove("not polymer")
    if chain is not None:
        cmd.select("one", f"chain {chain}")
        cmd.remove("not one")
        cmd.delete("one")
    cmd.hide("everything")
    cmd.show("cartoon", "polymer")
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("cartoon_smooth_loops", 1)
    cmd.set("cartoon_side_chain_helper", 1)
    cmd.color(loop_color, "polymer")
    cmd.color(helix_color, "ss H")
    cmd.color(sheet_color, "ss S")
    cmd.bg_color(bg)
    cmd.set("ray_opaque_background", 1)
    cmd.set("ray_trace_mode", 1)
    cmd.set("ray_shadows", kwargs.pop("shadows", 0))
    cmd.set("antialias", kwargs.pop("antialias", 2))
    cmd.set("ambient", kwargs.pop("ambient", 0.5))
    cmd.set("specular", kwargs.pop("specular", 0.2))
    cmd.orient()
    cmd.zoom("polymer", kwargs.pop("zoom", 2.0))
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    cmd.ray(width, height)
    cmd.png(out, dpi=dpi)
    return out

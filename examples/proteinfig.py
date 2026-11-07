"""Protein structure figures (reference implementations).

These are **examples**, not package features: how to render a protein structure
for publication. Two routes, clearly documented:

* ``pymol_cartoon`` — the **best-looking** result, via the real PyMOL engine;
  output is a **raster** PNG (PyMOL cannot export vector).
* ``matplotlib_cartoon`` — a **vector** (PDF/SVG) cartoon built with matplotlib+
  Biotite, using real PDB coordinates + real secondary structure.

An agent reads these and re-implements or extends them.
"""

from __future__ import annotations

import os
import tempfile

import numpy as np

from _house import PALETTE


def _fetch_pdb_text(pdb_id: str):
    """Return PDB text for a 4-letter id (Biotite), else None."""
    try:
        import io
        import biotite.database.rcsb as rcsb
        res = rcsb.fetch(pdb_id, format="pdb")
        return res.getvalue() if hasattr(res, "getvalue") else res
    except Exception:
        return None


def pymol_cartoon(pdb_id: str, out: str, chain=None, width=2200, height=1800,
                  dpi=300, helix_color="marine", sheet_color="orange",
                  loop_color="white", bg="white", **kwargs):
    """Render a protein to a publication PNG with PyMOL (raster, best look).

    Requires the ``pymol`` module (e.g. from ``brew install pymol``). Single
    chain by default; white background; secondary-structure coloring.
    """
    try:
        from pymol import cmd
    except ImportError as exc:
        raise RuntimeError("PyMOL required: brew install pymol (use that python).") from exc

    text = _fetch_pdb_text(pdb_id)
    source = None
    if text is not None:
        tmpf = tempfile.NamedTemporaryFile(suffix=".pdb", delete=False)
        tmpf.write(text.encode() if isinstance(text, str) else text)
        tmpf.close()
        source = tmpf.name
        pdb_path = source

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
    if source:
        os.unlink(source)
    return out


def matplotlib_cartoon(ax, pdb_id, chain=None, color=PALETTE["blue_main"],
                       view=None):
    """Vector matplotlib cartoon from a real PDB (Biotite optional).

    Computes real secondary structure and draws smooth helix ribbons + sheet
    arrows directly on ``ax`` (so it can be a panel/inset of a vector figure).
    Falls back to a demo fold if Biotite/network unavailable.
    """
    coords, sse = _load_with_sse(pdb_id, chain)
    if coords is None:
        coords, sse = _demo()
    coords = _smooth(coords, 5)
    _ribbon_3d(ax, coords, sse, color, view)
    ax.set_aspect("equal")
    return ax


def _load_with_sse(pdb_id, chain):
    try:
        import biotite.structure as struc
        import biotite.structure.io.pdb as pdb
        import io
        text = _fetch_pdb_text(pdb_id)
        if text is None:
            return None, None
        f = pdb.PDBFile.read(io.StringIO(text))
        arr = f.get_structure(model=1)
        ca = arr[arr.atom_name == "CA"]
        if chain is not None:
            ca = ca[ca.chain_id == chain]
        else:
            best = max(set(ca.chain_id), key=lambda c: int((ca.chain_id == c).sum()))
            ca = ca[ca.chain_id == best]
        sse = struc.annotate_sse(ca)
        sse = np.asarray(list(sse))
        sse = np.where(np.isin(sse, ["a", "A"]), "h", np.where(np.isin(sse, ["b", "B"]), "e", "-"))
        return ca.coord, sse
    except Exception:
        return None, None


def _smooth(c, w=5):
    c = np.asarray(c, float)
    if len(c) < w:
        return c
    out = np.zeros_like(c)
    for d in range(c.shape[1]):
        out[:, d] = np.convolve(c[:, d], np.ones(w) / w, mode="same")
    return out


def _ribbon_3d(ax, coords, sse, color, view):
    xy = coords[:, :2] if coords.shape[1] >= 2 else coords
    ax.plot(xy[:, 0], xy[:, 1], color="0.35", lw=0.6, zorder=2)
    h = np.where(np.asarray(sse) == "h")[0]
    for run in _runs(h):
        if len(run) < 4:
            continue
        p = xy[run]
        ax.plot(p[:, 0], p[:, 1], color=color, lw=6.4, solid_capstyle="round",
                alpha=0.30, zorder=1)
        ax.plot(p[:, 0], p[:, 1], color=color, lw=2.6, zorder=3)
        ax.plot(p[:, 0], p[:, 1], color="white", lw=0.6, zorder=4)
    e = np.where(np.asarray(sse) == "e")[0]
    for run in _runs(e):
        if len(run) < 2:
            continue
        _arrow(ax, xy[run][0], xy[run][-1], color)
    return ax


def _runs(idx):
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


def _arrow(ax, start, end, color):
    import matplotlib.patches as mpatches
    s = np.asarray(start, float)
    e = np.asarray(end, float)
    d = e - s
    L = np.hypot(*d)
    if L < 1e-6:
        return
    u = d / L
    n = np.array([-u[1], u[0]])
    w, head = 0.5, min(1.2, L * 0.4)
    poly = np.array([s + n * w, s - n * w, e - u * head - n * w, e, e - u * head + n * w])
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor=color,
                                  edgecolor=color, alpha=0.85, zorder=2))


def _demo():
    """A small folded demo (helices + one sheet) for offline falls backs."""
    xy = []
    for x0, amp in ((1.0, 0.55), (5.0, 0.6), (9.0, 0.5), (13.0, 0.62)):
        y = np.linspace(1.0, 15.0, 60)
        x = x0 + amp * np.sin(np.linspace(0, 4 * np.pi, 60))
        xy.append(np.stack([x, y], axis=1))
    for y0, dy in ((8.5, 0.0), (10.5, 0.4)):
        xy.append(np.stack([np.linspace(1.0, 19.0, 40), np.full(40, y0) + np.linspace(0, dy, 40)], axis=1))
    c = np.vstack(xy)
    c = np.hstack([c, np.zeros((c.shape[0], 1))])
    sse = np.array(list("h" * 240 + "e" * 80))
    return c, sse

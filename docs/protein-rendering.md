# Protein structure rendering for publication (vector)

## Can PyMOL export a vector image? (tested)

**No.** PyMOL's render path is a **raster** ray-tracer. `ray` is documented as
making "high-resolution photos" (bitmap), and this build rejects vector formats
directly:

```
$ pymol -c - <<cmd
cmd.save('out.svg')   # -> Error: File format not supported for export
cmd.save('out.eps')   # -> Error: File format not supported for export
cmd.save('out.ps')    # -> Error: File format not supported for export
```

`png` (from `ray`) is the only image export. So a PyMOL render inserted in a
paper is a **raster** image — it scales badly and isn't editable as vector.

This is a known, long-standing limitation; it's why the ecosystem has
**vector-native** alternatives (below).

## Vector-native options (2025)

| Tool | Output | Vector | Notes |
|------|--------|--------|-------|
| **cellscape** (MIT) | SVG cartoon outlines | yes | Goodsell-style residue/chain outlines + depth shading; needs a camera matrix (often from PyMOL/Chimera) |
| **FlatProt** (2025, BMC) | 2D SVG projection | yes | standardised 2D representation; best for comparing many structures |
| **scifig `protein.py`** | matplotlib vector | yes | self-contained pure-matplotlib cartoon (helix ribbons + sheet arrows), no external tool; exports PDF/SVG |
| **PyMOL / ChimeraX** | PNG 3D render | no | best-looking 3D *view*; bitmap for output |

## Recommended workflow for a publication protein figure

If the figure must be **vector** and embedded (panel / inset / whole figure),
there are three routes:

1. **PyMOL for the view, vector for the delivery** — render with PyMOL to choose
   the camera and get the beautiful 3D look, but deliver as: (a) a high-res PNG
   (raster, acceptable only if the journal allows and it's ≥300 dpi at final
   size), or (b) a vector cartoon from **cellscape/FlatProt** using the same
   camera matrix.
2. **cellscape / FlatProt SVG** — true vector cartoons, good for multi-structure
   comparisons and cleaner insets.
3. **scifig `protein.py`** — a pure-matplotlib vector cartoon when you want zero
   external deps and full control; style is simpler than PyMOL but is genuinely
   vector.

> Practical note: because PyMOL is raster, many journals accept a **≥600 dpi**
> PyMOL PNG placed at final physical size — it looks sharp in print. But if you
> need editable/scalable vector, use cellscape/FlatProt/scifig, or auto-trace the
> render (see below).

## Raster-to-vector auto-trace

Any raster render can be converted to vector by **auto-tracing** (Potrace /
`vtracer` / Inkscape Trace Bitmap). For cartoons this works well when there's a
flat background and few colors; the result is editable vector but the shapes are
re-approximations. Prefer a native vector tool for precise output.

## scifig usage

```python
import scifig
coords = scifig.fetch_structure("5JJ4")     # real AICDA via Biotite
fig, ax = scifig.create_subplots(1, 1)
scifig.draw_topology(ax, coords)             # pure-vector cartoon (real SSE)
scifig.finalize_figure(fig, "out/protein")   # vector PDF
```

`draw_topology`/`ribbon_3d` draw directly on a matplotlib axes, so the cartoon
can also be placed as a **panel or inset** of a larger figure — all vector.

## The honest tradeoff

- **Beautiful 3D look** → PyMOL (but raster PNG only).
- **True vector, editable, scalable** → cellscape / FlatProt / scifig.
- For a paper, decide by whether the figure needs to be vector (inset, zoom) or
  whether a high-dpi PNG at final size suffices.

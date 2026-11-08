# protein-rendering — vector?

PyMOL **cannot** export vector — its `ray` output is a PNG (bitmap). `svg`/`eps`/`ps` are rejected.

| Want | Use |
|------|-----|
| best-looking | `proteinfig.pymol_cartoon(pdb, out)` — raster PNG |
| true vector | `proteinfig.matplotlib_cartoon(ax, pdb)` — real PDB + SSE |
| compare many | cellscape / FlatProt (SVG) |

PyMOL for the 3D view only; deliver vector via the matplotlib cartoon.

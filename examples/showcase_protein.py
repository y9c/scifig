#!/usr/bin/env python3
"""Protein topology figure — pure-vector cartoon, publication-ready.

Renders a Cα topology (helix ribbons + beta-sheet arrows) as a **vector**
matplotlib cartoon from a real PDB (Biotite). Exports PDF/SVG, so it can be
inserted as a panel/inset of a larger figure without losing vector quality.

No PyMOL needed (see ``proteinfig.pymol_cartoon`` for the raster PyMOL route).
"""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt
from _house import style, save, finish
from proteinfig import matplotlib_cartoon

style(font_size=6.0, axes_linewidth=0.8)
fig, ax = plt.subplots(figsize=(7.2, 7.2 * 0.5))

matplotlib_cartoon(ax, "1CRN")
finish(ax, grid=False)
ax.set_title("Protein topology (vector)", pad=4)

save(fig, "out/showcase_protein", formats=("pdf", "png"), dpi=600)
print("wrote out/showcase_protein.pdf/png (vector)")

#!/usr/bin/env python3
"""Render AID (AICDA) as a publication-grade PyMOL cartoon.

Uses the recipe in ``proteinfig.pymol_cartoon`` (PyMOL via ``brew install pymol``).
Single chain A, white background, secondary-structure coloring, ray-traced.

Run with the python that has PyMOL, e.g.:
    /opt/homebrew/bin/python3 examples/pymol_render_aicda.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proteinfig import pymol_cartoon

out = os.path.join("out", "aicda_pymol.png")
pymol_cartoon("5JJ4", out, chain="A")
print(f"wrote {out} (single chain A, white bg, SSE colors)")

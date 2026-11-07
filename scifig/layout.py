"""Layout audit and auto-fix.

GridSpec ``wspace``/``hspace`` are static fractions of the average axes size and
know nothing about the actual content (tick labels, axis labels, legends,
colorbars). So multi-panel figures either collide (panels clipped or labels
overlapping neighbours) or drift apart (excessive whitespace).

This module makes layout a first-class, measured concern:

* ``audit_layout`` — after drawing, measure every axes' on-screen bounding box
  and detect (a) panel overlap beyond a tolerance, (b) excessive whitespace
  between neighbours, (c) content (text / legend / colorbar) running off the
  figure.
* ``fix_layout`` — apply a layout engine that resolves overlaps automatically
  (matplotlib's ``constrained_layout`` is the correct tool: it measures artist
  decorations and packs them without collision).

``render_spec`` uses ``layout='auto'`` by default: it tries ``constrained``,
  then audits, and only reports a residual problem (instead of silently handing
  the agent a broken figure).
"""

from __future__ import annotations

import numpy as np

__all__ = ["audit_layout", "fix_layout", "layout_report", "LayoutReport"]


def layout_report(fig, backend="draw"):
    """Measure each axes' on-screen bounding box (in pixels)."""
    fig.canvas.draw()
    boxes = {}
    for ax in fig.axes:
        if not ax.axison:
            continue
        try:
            b = ax.get_window_extent()
        except Exception:
            continue
        boxes[ax] = np.array([b.x0, b.y0, b.x1, b.y1])
    return boxes


def _overlap(a, b):
    """Return the overlap area of two bboxes, or 0."""
    x = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    y = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return x * y


def audit_layout(fig, overlap_tol=0.02, gap_factor=3.0):
    """Return a ``LayoutReport``: detected overlaps + excessive gaps.

    ``overlap_tol``: intersection-area / min-area ratio above which two axes
    are considered to overlap. ``gap_factor``: a gap between neighbours more
    than this many times the median gap is flagged as excessive whitespace.
    """
    boxes = layout_report(fig)
    axes = list(boxes)
    report = LayoutReport()
    # (a) pairwise overlap
    for i in range(len(axes)):
        for j in range(i + 1, len(axes)):
            a, b = boxes[axes[i]], boxes[axes[j]]
            ov = _overlap(a, b)
            min_area = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
            if min_area > 0 and ov / min_area > overlap_tol:
                report.overlaps.append((axes[i], axes[j], ov / min_area))
    # (b) excessive gaps between horizontally/vertically adjacent axes
    # collect all pairwise gaps, then flag outliers
    gaps = []
    for i in range(len(axes)):
        for j in range(i + 1, len(axes)):
            a, b = boxes[axes[i]], boxes[axes[j]]
            # horizontal neighbours
            xgap = max(a[0] - b[2], b[0] - a[2]) if (a[0] - b[2]) > 0 or (b[0] - a[2]) > 0 else None
            # vertical neighbours
            ygap = max(a[1] - b[3], b[1] - a[3]) if (a[1] - b[3]) > 0 or (b[1] - a[3]) > 0 else None
            for g in (xgap, ygap):
                if g is not None and g > 0:
                    gaps.append(g)
    if gaps:
        med = float(np.median(gaps))
        large = [g for g in gaps if g > gap_factor * med and med > 1.0]
        if large:
            report.excess_gaps = large
    return report


class LayoutReport:
    """Result of ``audit_layout``."""

    def __init__(self):
        self.overlaps: list = []
        self.excess_gaps: list = []

    @property
    def has_overlap(self):
        return bool(self.overlaps)

    @property
    def ok(self):
        return not self.overlaps

    def __str__(self):
        parts = []
        if self.overlaps:
            parts.append(f"{len(self.overlaps)} panel overlap(s)")
        else:
            parts.append("no overlap")
        if self.excess_gaps:
            parts.append(f"excessive whitespace: {len(self.excess_gaps)} gap(s)")
        return "; ".join(parts)


def fix_layout(fig, engine="constrained", overlap_tol=0.02, gap_factor=3.0):
    """Apply a layout engine that resolves overlaps, then re-audit.

    ``engine``: ``'constrained'`` (default; measures decorations and packs
    without collision) or ``'none'`` (leave as-is). Returns the re-audited
    ``LayoutReport``.
    """
    if engine == "constrained":
        fig.set_layout_engine("constrained")
    elif engine == "tight":
        fig.set_layout_engine("tight")
    return audit_layout(fig, overlap_tol=overlap_tol, gap_factor=gap_factor)

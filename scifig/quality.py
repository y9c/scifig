"""Mechanical figure quality gate (agent-oriented acceptance check).

A mechanical acceptance check; ``check_figure`` inspects a rendered ``fig``/axes and reports
FAIL/OK items, so an agent can verify a figure is publication-ready *before*
declaring it done — not just that it "plotted correctly".

The four judgment axes (Deep · Elegant · Unimpeachable · Visible gap) are
qualitative and printed as prompts to answer by hand; the mechanical floor here
is the objective defense.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional

__all__ = ["check_figure", "QualityReport", "QUALITY_AXES"]

QUALITY_AXES = [
    "Depth: does each panel carry a real scientific claim, or is it decoration?",
    "Elegance: is it uncluttered, aligned, deliberate (not a homework plot)?",
    "Unimpeachable: are units, N, uncertainty, and scales correct & legible?",
    "Visible gap: would an expert see an obvious improvement over the naive plot?",
]


@dataclass
class QualityReport:
    checks: dict = field(default_factory=dict)

    def ok(self, name: str, detail: str = ""):
        self.checks[name] = ("OK", detail)

    def fail(self, name: str, detail: str = ""):
        self.checks[name] = ("FAIL", detail)

    def failures(self):
        return {k: v for k, v in self.checks.items() if v[0] == "FAIL"}

    @property
    def passed(self):
        return not self.failures()

    def __str__(self):
        lines = []
        for k, (status, detail) in self.checks.items():
            line = f"  [{status}] {k}"
            if detail:
                line += f": {detail}"
            lines.append(line)
        return "\n".join(lines)


def check_figure(
    fig=None,
    axes: Optional[Iterable] = None,
    report: Optional[QualityReport] = None,
) -> QualityReport:
    """Run the mechanical publication-quality checks against ``fig``/``axes``.

    Returns a ``QualityReport``; ``report.passed`` is True when no FAIL. Prints
    the four qualitative judgment axes at the end.
    """
    r = report or QualityReport()
    axes = list(axes) if axes is not None else (fig.axes if fig is not None else [])

    if axes:
        # 1. every axes has axis labels (units required)
        for i, ax in enumerate(axes):
            if not ax.get_xlabel():
                r.fail(f"axis[{i}].xlabel", "missing x-axis label (carry units!)")
            if not ax.get_ylabel():
                r.fail(f"axis[{i}].ylabel", "missing y-axis label (carry units!)")

    # 2. vector-safety
    from matplotlib import rcParams

    if rcParams.get("pdf.fonttype", 0) != 42:
        r.fail("vector.text", "pdf.fonttype != 42; PDF text will be Type-3 (not editable)")
    else:
        r.ok("vector.text", "pdf.fonttype=42 (editable TrueType text)")
    if rcParams.get("svg.fonttype", None) != "none":
        r.fail("vector.svg", "svg.fonttype != 'none'; SVG text will be outlines")
    else:
        r.ok("vector.svg", "svg.fonttype=none (text stays text)")

    r.ok("semantic_palette", "verify roles: blue=ours, green=improve, red=baseline")
    if axes:
        r.ok("panels", f"{len(axes)} axes rendered")

    print("Scifig quality gate:")
    print(str(r))
    print("\nJudgment axes (answer by hand):")
    for q in QUALITY_AXES:
        print(f"  - {q}")
    return r

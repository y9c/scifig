"""Semantic color-role assignment.

The house rule: color is assigned by **role**, not left to the default cycle.
``assign_colors`` maps a list of series labels to colors based on their role
(method vs baseline, ours vs improvement). This keeps every figure on the same
semantic palette (blue=ours, green=improvement, red/neutral=baseline) without
hard-coding hex in each script.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

from .palette import PALETTE, DEFAULT_COLORS

__all__ = ["SEMANTIC_ROLES", "ROLE_CYCLE", "role_color", "assign_colors"]


# Role -> hex. This is the single source of truth for what a color *means*.
SEMANTIC_ROLES = {
    "ours": PALETTE["blue_main"],          # proposed / key method
    "method": PALETTE["blue_main"],        # alias of ours
    "improvement": PALETTE["green_3"],     # improvement over baseline
    "improve": PALETTE["green_3"],
    "baseline": PALETTE["neutral"],        # reference / background
    "baseline_strong": PALETTE["red_strong"],  # contrast / strongest baseline
    "contrast": PALETTE["red_strong"],
    "accent": PALETTE["teal"],
    "accent2": PALETTE["violet"],
}

# Fallback order when a role is unknown / not supplied.
ROLE_CYCLE = ["method", "baseline_strong", "improvement", "accent", "accent2", "baseline"]


def role_color(role: str) -> str:
    """Return the hex for a semantic role, falling back to the default cycle."""
    if role in SEMANTIC_ROLES:
        return SEMANTIC_ROLES[role]
    return PALETTE["blue_main"]


def assign_colors(
    labels: Sequence[str],
    roles: Optional[Sequence[Optional[str]]] = None,
    ours_marker: Optional[str] = None,
) -> list[str]:
    """Assign a list of colors to ``labels`` by semantic role.

    ``roles``: one role per label (or ``None`` to auto-assign). If not given
    and ``ours_marker`` is set, the label containing ``ours_marker`` becomes
    ``'ours'`` (blue) and everything else uses the ``ROLE_CYCLE`` order. If
    neither is given, labels use ``ROLE_CYCLE`` from the first.

    >>> assign_colors(["A", "B", "C"])
    ['#0F4D92', '#B64342', '#8BCF8B']
    """
    n = len(labels)
    if roles is not None:
        roles = list(roles)
        if len(roles) != n:
            raise ValueError("len(roles) must equal len(labels)")
        # fill any None with the cycle
        k = 0
        for i in range(n):
            if roles[i] is None:
                roles[i] = ROLE_CYCLE[k % len(ROLE_CYCLE)]
                k += 1
    elif ours_marker is not None:
        roles = []
        k = 1  # skip 'method' (reserved for ours) so baselines never match ours
        for lab in labels:
            if ours_marker in lab:
                roles.append("ours")
            else:
                roles.append(ROLE_CYCLE[k % len(ROLE_CYCLE)])
                k += 1
    else:
        roles = [ROLE_CYCLE[i % len(ROLE_CYCLE)] for i in range(n)]
    return [role_color(r) for r in roles]
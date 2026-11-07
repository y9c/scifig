#!/usr/bin/env python3
"""Kaplan-Meier survival curves for two groups (no lifelines dependency)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, save, finish

rng = np.random.default_rng(3)


def km(times, events, label, color):
    """Compute and draw a Kaplan-Meier curve. Returns (t, survive)."""
    t = np.asarray(times, float)
    e = np.asarray(events, int)
    order = np.argsort(t)
    t, e = t[order], e[order]
    uniq = np.unique(t)
    n = len(t)
    surv, at_risk = 1.0, float(n)
    ts, ss = [0.0], [1.0]
    for u in uniq:
        d = e[t == u].sum()
        at_risk -= (t == u).sum() - d  # censored before this time
        if at_risk > 0 and d > 0:
            surv *= (1 - d / at_risk)
        ts.append(u); ss.append(surv)
    ax.step(ts, ss, where="post", color=color, lw=1.4, label=f"{label} (n={n})")
    return np.array(ts), np.array(ss)


style()
fig, ax = plt.subplots(figsize=(4.0, 3.2))

# survival in a realistic 0-90 day window (clipped, so no long empty tail)
ctrl_t = np.clip(rng.exponential(40, 60) + 5, 0, 90)
trt_t = np.clip(rng.exponential(70, 60) + 5, 0, 90)
ctrl_e = (ctrl_t < 70).astype(int)
trt_e = (trt_t < 70).astype(int)

km(ctrl_t, ctrl_e, "Control", color="#B64342")
km(trt_t, trt_e, "Treatment", color="#0F4D92")
ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival probability")
ax.set_xlim(0, 90); ax.set_ylim(0, 1.02)
ax.legend(frameon=False, fontsize=6)
finish(ax, grid=False)
save(fig, "out/survival", dpi=600)
print("wrote out/survival.pdf")

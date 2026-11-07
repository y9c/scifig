# Code Cookbook (references/cookbook.md)

> Practical, minimal-code plotting recipes for Publication-grade matplotlib.
> Style files handle ALL aesthetics; your code focuses on data. Use with the shared
> `assets/scientific_publication.mplstyle` / `assets/modern.mplstyle` + `scripts/style_helper.py`.

## Key philosophy
Load the style; code stays minimal. The **before/after** shows it:

```python
# BEFORE (no style) — verbose
fig, ax = plt.subplots(figsize=(3.5, 2.625))
ax.plot(x, y, color='#3A6BC5', linewidth=1.5, markersize=5, markeredgecolor='white',
        markeredgewidth=0.8, label='Data')
ax.set_xlabel('Time (s)', fontsize=9); ax.set_ylabel('Value', fontsize=9)
ax.set_title('Results', fontsize=10, fontweight='bold')
ax.legend(frameon=True, fontsize=8); ax.grid(True, color='#E0E0E0', linewidth=0.4, alpha=0.5)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.savefig('figure.pdf', dpi=600, bbox_inches='tight')

# AFTER (with style) — minimal
fig, ax = plt.subplots()
ax.plot(x, y, label='Data')
ax.set_xlabel('Time (s)'); ax.set_ylabel('Value'); ax.set_title('Results')
ax.legend(); plt.savefig('figure.pdf')
```

Use the helper (auto-locates assets, no path):
```python
from scientific_figures_style import apply_publication_style, FigureStyle, PALETTE
apply_publication_style()   # or apply_modern_style() for presentations
```

## Typography standards (3.5" single-column figure)
| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Title | 10pt | Bold | Black |
| Axis labels | 9pt | Normal | Black |
| Tick labels | 8pt | Normal | #666666 |
| Legend | 8pt | Normal | Black |

## Figure sizes
| Type | Width | Height | Use |
|------|-------|--------|-----|
| Single column | 3.5" | 2.6" | most plots |
| 1.5 column | 5.0" | 3.75" | medium |
| Double column | 7.2" | 5.4" | complex multi-panel |
| Square | 3.5" | 3.5" | heatmap, network |

## Color palette (colorblind-safe, coordinated)
```python
colors = {'blue':'#3A6BC5','red':'#D4654A','green':'#4A9F6F','amber':'#DE9E4A','rose':'#B5637D','teal':'#4A9496'}
```
Rules: max 4 colors per plot; consistent across a paper; scatter uses white edges.

## Recipes (style auto-applies params)

### 1. Line plot
```python
ax.plot(x, y1, label='Control'); ax.plot(x, y2, '--', label='Treatment')
ax.set_xlabel('Time (h)'); ax.set_ylabel('Expression'); ax.legend()
plt.tight_layout(); plt.savefig('line.pdf')
```

### 2. Scatter + trend (must set s= and alpha= manually)
```python
ax.scatter(x1, y1, s=30, c='#3A6BC5', alpha=0.85, label='Ctrl')
from scipy import stats
slope, intercept, r, p, se = stats.linregress(x, y)
ax.plot(x, slope*x+intercept, '--', color='#D4654A', linewidth=1.2, alpha=0.7)
ax.annotate(f'R² = {r**2:.3f}', xy=(0.05,0.95), xycoords='axes fraction', fontsize=8)
```

### 3. Bar + error
```python
x = np.arange(4); vals=[23,45,56,78]; err=[2,3,4,3]
ax.bar(x, vals, alpha=0.9, width=0.6)
ax.errorbar(x, vals, yerr=err, fmt='none', ecolor='black', capthick=0.8, linewidth=0.8)
```

### 4. Grouped bar (set colors manually)
```python
width=0.25
ax.bar(x-width, g1, width, label='M1', color='#3A6BC5')
ax.bar(x, g2, width, label='M2', color='#D4654A')
ax.bar(x+width, g3, width, label='M3', color='#4A9F6F')
ax.legend()
```

### 5. Box plot (patch_artist=True for fill)
```python
bp = ax.boxplot([d1,d2,d3], tick_labels=['Ctrl','T1','T2'], patch_artist=True)
for patch, c in zip(bp['boxes'], ['#3A6BC5','#D4654A','#4A9F6F']):
    patch.set_facecolor(c); patch.set_alpha(0.7); patch.set_edgecolor('none')
for m in bp['medians']: m.set_color('#333333'); m.set_linewidth(1.2)
```

### 6. Heatmap
```python
im = ax.imshow(data, cmap='viridis', aspect='auto')
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Intensity', rotation=270, labelpad=15)
ax.set_xticks(range(n)); ax.set_yticks(range(m))
ax.set_xticklabels(xl, rotation=45, ha='right'); ax.set_yticklabels(yl)
```

### 7. Area / stack
```python
ax.stackplot(x, y1, y2, y3, labels=['L1','L2','L3'], colors=['#3A6BC5','#D4654A','#4A9F6F'], alpha=0.85)
```

## Advanced
- **Multi-panel**: `fig.figure(figsize=(7.2,5.4))` + `GridSpec(2,3)`; label panels `ax.text(-0.15,1.05, chr(65+i), transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')`
- **Inset**: `from mpl_toolkits.axes_grid1.inset_locator import inset_axes`; add `Rectangle` indicator
- **Confidence band**: `ax.fill_between(x, y_mean-y_std, y_mean+y_std, alpha=0.2, color='#3A6BC5', label='±1 SD')`
- **Shared legend**: `handles,labels=ax1.get_legend_handles_labels(); fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,0.02), ncol=3)`
- **Stat annotation**: draw bracket via `ax.plot([0,0,1,1],[ymax*1.02,ymax*1.05,ymax*1.05,ymax*1.02],'k-',lw=0.8)` + `ax.text(0.5, ymax*1.06, '*', ha='center')`

## Best practices
- Always `plt.tight_layout()` (or `rect=[0,0,1,0.96]` with suptitle)
- Vector (PDF/EPS/SVG) for print; 600 DPI for journal, 300 for screen/poster
- Fonts: Arial/Helvetica preferred; Linux `sudo apt-get install ttf-mscorefonts-installer`; check with `matplotlib.font_manager`
- Optimize PDF: `plt.savefig('f.pdf', dpi=600, bbox_inches='tight', metadata={'Creator':None,'Producer':None})`

## Full style reference (scientific_publication.mplstyle)
```
figure.facecolor: white; figure.dpi: 300; savefig.dpi: 600; savefig.facecolor: white
figure.figsize: 3.5, 2.625
font.family: sans-serif; font.sans-serif: Arial,Helvetica,Liberation Sans,DejaVu Sans
axes.titlesize: 10; axes.titleweight: bold; axes.labelsize: 9
axes.linewidth: 0.8; axes.spines.top: False; axes.spines.right: False
axes.grid: True; grid.color: E0E0E0; grid.linewidth: 0.4; grid.alpha: 0.5; axes.axisbelow: True
axes.prop_cycle: cycler('color', ['3A6BC5','D4654A','4A9F6F','DE9E4A','B5637D','4A9496','6A6CB2','5A6578'])
lines.linewidth: 1.5; lines.markersize: 5; lines.markeredgewidth: 0.8; lines.markeredgecolor: white
legend.fontsize: 8; legend.frameon: True; legend.framealpha: 0.95; legend.edgecolor: E0E0E0
xtick.labelsize: 8; ytick.labelsize: 8; xtick.direction: out; xtick.major.size: 3
xtick.color: 666666
```

## Related files
- `assets/scientific_publication.mplstyle`, `assets/modern.mplstyle` (actual style files)
- `scripts/style_helper.py` (apply_publication_style / apply_modern_style / make_figure / finalize)
- `references/design-theory.md` (theory behind the styles)

# scifig

**发表级科研图**：matplotlib 封装 + 你偏好的两套样式 + **纯 Python 拼接/标注**多面板图。

> 论文图用 `apply_publication_style`，汇报/幻灯片用 `apply_modern_style`。样式全交给
> 包，代码只写数据。拼图、加 panel 字母、shared legend、inset、显著性 bracket 全部
> 在 Python 里完成，不用 Illustrator。

## 目录

```
scifig/          Python 包（样式 + 图型 helpers + compose/annotate）
  style.py       apply_publication_style / apply_modern_style / create_subplots / finalize_figure
  palette.py     PALETTE / DEFAULT_COLORS / MODERN_COLORS / COLORBLIND_SAFE
  helpers.py     make_grouped_bar / make_trend / make_heatmap / make_scatter / make_sphere_illustration
  compose.py     panel_grid / join_figures / add_panel_label / shared_legend / add_inset / add_sig
  assets/        scientific_publication.mplstyle + modern.mplstyle（随包分发，无需手写路径）
skill/           Agent skill（SKILL.md + references/ + demos/）
examples/        可运行示例脚本
```

## 安装

```bash
pip install -e .
# 或直接：pip install -r requirements.txt
```

## 快速开始

```python
import matplotlib
matplotlib.use("Agg")          # 无头/批处理
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=18))
fig, ax = scifig.create_subplots(1, 1)
scifig.make_grouped_bar(
    ax, ["A", "B", "C"], [[0.9, 0.8, 0.7], [0.7, 0.6, 0.5]],
    ["Ours", "Baseline"], ylabel="Score", annotate=True,
)
scifig.finalize_figure(fig, "out/fig", formats=["png", "pdf"], dpi=300)
```

纯写法：直接 `plt.style.use(...scifig/assets/scientific_publication.mplstyle)` 即可，
无需 import 包。

## 纯 Python 拼图 + 标注

```python
import scifig

# 把已保存的两张 PNG 拼成一张 1x2，并加上 A/B 面板字母
fig, axes = scifig.join_figures(["a.png", "b.png"], labels=["A", "B"])
scifig.finalize_figure(fig, "out/combo", formats=["png", "pdf"])

# 或者在同一 figure 里建 grid、加 shared legend、加显著性 bracket
fig, axes = scifig.panel_grid(1, 2)
scifig.make_trend(axes[0], epochs, [acc_a, acc_b], ["Model A", "Model B"])
scifig.add_sig(axes[0], 0, 1, y=0.95, marker="***")
scifig.shared_legend(fig, location="upper center")
```

看 **`examples/`** 完整可跑示例（`examples/grouped_bar.py`、`examples/trends_grid.py`、
`examples/heatmap.py`、`examples/compose_annotate.py`）。

## 用 Agent skill

`skill/` 是本仓库使用的 agent skill。在你的 agent 里引用：
- 按路径引用 `skill/SKILL.md`（以及按需的 references/api.md、design-theory.md、cookbook.md）。
- 或软链：`ln -s "$(pwd)/skill" ~/.agents/skills/scifig`，之后可按 name 调用。

核心约定都写在 `skill/references/`；demos 里是真实顶会论文图脚本（house style 范例）。

## 样式 / 色板

| 名称 | 用途 | 入口 |
|------|------|------|
| `scientific_publication` | 论文发表（大字号、spines 只留左右、600dpi 导出） | `apply_publication_style()` |
| `modern` | 汇报/网页 | `apply_modern_style()` |
| `PALETTE` | 语义色（蓝=方法、绿=改进、红=基线、中性=背景） | `scifig.PALETTE` |

## 许可（重要）

- **MIT**：本仓库的 `scifig/` 包与 `examples/`。
- **CC BY-NC 4.0（非商用）**：`skill/demos/figure_*` 与 `skill/references/` 方法论，
  源自 [figures4papers](https://github.com/ChenLiu-1996/figures4papers)（作者 Chen Liu，
  Yale）。**上游 LICENSE 实为 CC BY-NC 4.0，不是 MIT** —— 已在本仓库 LICENSE / NOTICE.md
  更正。商用前请核对。

详见 `LICENSE` 与 `NOTICE.md`。

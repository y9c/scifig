---
name: scifig
description: >-
  发表级 matplotlib 科研图工具（个人化）：封装了用户偏好的两套样式
  （scientific_publication / modern）、图型 helpers（柱状/趋势/热图/散点/球体示意图）、
  以及用纯 Python 拼接与标注多面板图的 compose 工具（panel_grid、join_figures、
  shared_legend、add_panel_label、add_inset、add_bracket/add_sig）。当需要为论文、
  报告、幻灯片做正式图、或想复用本仓库 house style 与 scifig 包时使用。不用于交互式
  仪表盘（Plotly/Altair/Bokeh）、无发表目标的 EDA-only 图、3D/GIS 主流程、或
  Illustrator/Figma 优先的信息图工作流。触发词：科研画图、论文图、发表图、figure、
  scientific figure、matplotlib 画图、画柱子图、画热图、拼图、多面板、publication figure。
---

# scifig — 发表级科研图（matplotlib）

本 skill 基于 skl project `scifig`（本仓库），是个人化整合：**论文发表样式 +
现代样式 + 纯 Python 拼接/标注**。核心 philosophy：样式全交给包，代码只写数据。

## 何时使用

- 用 matplotlib 做 **论文 / 幻灯片 / 报告** 正式图，需要发表级观感。
- 涉及 **分组柱状、趋势线、热图、多面板网格、PDF/SVG/高DPI** 输出。
- 想 **用纯 Python 拼接多个面板并标注**（panel letters、shared legend、inset、
  显著性 bracket、把已存好的图拼成一张）。

## 何时不用

- **Plotly / Altair / Bokeh** 交互式、web-first。
- 仅 **EDA** 且无发表目标（seaborn/pandas 即可）。
- 主流程是 **3D、GIS** 或非 matplotlib。
- **Illustrator / Figma 优先**的信息图（非 matplotlib 数据图）。

## 快速开始

### 方式 A：直接用 scifig 包（推荐）

```python
import scifig

# 论文图：发表样式 + 大字号
scifig.apply_publication_style(scifig.FigureStyle(font_size=18))
fig, ax = scifig.create_subplots(1, 1)
see = scifig.make_grouped_bar(
    ax, ["A", "B", "C"], [[0.9, 0.8, 0.7], [0.7, 0.6, 0.5]],
    ["Ours", "Baseline"], ylabel="Score", annotate=True,
)
scifig.finalize_figure(fig, "out/fig", formats=["png", "pdf"])
```

汇报/幻灯片：`scifig.apply_modern_style()`。

### 方式 B：只用 .mplstyle 文件

```python
import matplotlib.pyplot as plt
plt.style.use('<repo>/scifig/assets/scientific_publication.mplstyle')
```

## 文件清单

| 文件/目录 | 何时打开 |
|-----------|----------|
| [references/api.md](references/api.md) | scifig 包全部函数签名、PALETTE、FigureStyle、校验规则 |
| [references/cookbook.md](references/cookbook.md) | **代码速查**：7 种图型最小代码、色板 hex、多面板/inset/统计标注、mplstyle 全参考 |
| [references/tutorials.md](references/tutorials.md) | 端到端流程（柱状/趋势/热图/多面板） |
| [references/design-theory.md](references/design-theory.md) | 版式、导出策略、色板理据 |
| [references/common-patterns.md](references/common-patterns.md) | 版式模式、legend 面板、print-safe 柱 |
| [references/demos.md](references/demos.md) | 真实顶会论文图脚本索引（本仓库 demos/） |
| [demos/](demos/) | 8 套真实顶会论文图的可复现脚本（figures4papers house style） |
| [examples/](../examples/) | 本仓库内的可运行示例 |

`references/` 按需打开，不要预载全部。从下表定位入口，再顺着文档内部链接（及 demos/、
examples/ 脚本）走。

## 版权与出处

- **scifig 包 + examples**：本仓库作者所有，MIT。
- **demos/ 与 references 方法论**：源自
  [figures4papers](https://github.com/ChenLiu-1996/figures4papers)（作者 Chen Liu，Yale），
  **CC BY-NC 4.0**（非商用，见原仓库 LICENSE；NOTICE.md 与本仓库 LICENSE 说明）。
- **assets/*.mplstyle**：源自 personal `modern-matplotlib` / `scientific_publication`。

> 重要：figures4papers 的 LICENSE 实为 **CC BY-NC 4.0**（非 MIT）。本仓库
> LICENSE（MIT）只覆盖 scifig 包自身与 examples/；demos/ 与引用材料仍受上游
> CC BY-NC 4.0 约束，商用前请先核对。

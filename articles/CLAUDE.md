# articles/ —— 文章工作区规则

> 本文件在进入 `articles/` 目录工作时自动加载。项目总原则见根目录 `CLAUDE.md`。
> （本文件由原便签"此文件夹存放临时草稿/中间产物，以公众号标题作为文件夹名称"扩写而来。）

## 这个文件夹是干嘛的
`articles/` 存放**每篇文章的中间产物（工作区）**，不是最终交付。最终交付在项目根目录的 `<标题>/` 文件夹（见根 `CLAUDE.md` 第七节）。

## 每篇文章 = 一个自包含的标题文件夹
- **文件夹名 = 公众号标题**，如 `articles/AI时代，普通人到底该不该焦虑被淘汰？/`。
- **自包含**：每个文章文件夹内同时放：
  - `_templates/`：本篇文章自己的**模板副本**（14 个状态文件模板 + `perspective-reports/_TEMPLATE.md`）；
  - **14 个工作产物**：`topic-card` / `audience-card` / `research-task` / `source-map` / `perspective-reports/` / `contradiction-map` / `research-brief` / `direction-lock` / `outline` / `draft` / `review-report` / `final` / `parking-lot` / `workflow-state`。
- 一篇文章的所有中间产物 + 它自己的模板，全收在一个标题文件夹里；文章之间互不污染。

## 新建一篇文章（由 topic-interview 技能负责）
1. 在 `articles/` 下创建以**标题**命名的文件夹 `articles/<标题>/`。
2. 把模板复制进 `<标题>/_templates/`。**来源**：仓库内任一已有文章的 `_templates/`；若尚无任何文章，从首个样本 `articles/AI时代，普通人到底该不该焦虑被淘汰？/_templates/` 复制。
3. 把 `.claude/active-article` 指针写成 `articles/<标题>`。
4. 用 `_templates/` 里的模板初始化工作产物（先填 `topic-card.md`、`workflow-state.md`）。

## 子代理写文件的位置
所有视角代理、研究综合、质量验收等子代理，把产出写到**当前文章文件夹**（`.claude/active-article` 所指）下：
- 视角报告 → `<文章文件夹>/perspective-reports/<视角名>.md`
- 研究简报 → `<文章文件夹>/research-brief.md`
- 验收报告 → `<文章文件夹>/review-report.md`
- 各报告结构对齐**本文件夹内**的 `_templates/`（不是别处的共享模板——本项目没有共享模板，每篇自带）。

## 最终交付（不在本文件夹）
定稿后，主程序在**项目根目录**另建 `<标题>/` 文件夹，放入整理后的定稿文章 + `image/` 配图子目录。详见根 `CLAUDE.md` 第七节。

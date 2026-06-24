---
name: direction-lock
description: 公众号写作流程的第四步技能。在 research-brief.md 与 contradiction-map.md 完成后、大纲前使用。基于研究输入设计 2-3 个差异化主线候选，用选择题让用户锁定文章主线，写入 direction-lock.md，并翻转 Gate B（direction_locked=true）。
when_to_use: research-orchestration 完成后、进入 outline-design 之前；需要锁定文章主线时。
allowed-tools: AskUserQuestion Read Write
---

# direction-lock — 文章主线锁定技能

此阶段锁定"这篇文章到底要讲什么"。**主线最终由用户拍板，主程序只提候选**。这是 Gate B。一旦锁定，后续大纲与正文都只能围绕这条主线展开。

## 严格纪律
- 与用户的全部交互只能用 `AskUserQuestion`（选择题）。
- **主线由用户锁定**，主程序只提候选、不替用户决定。
- 候选必须真正差异化（不同的核心观点 / 不同的读者收益），不要给换汤不换药的候选。

## SOP 步骤

### 步骤 1：前置自检
确认以下文件存在：
- `articles/<文章标题>/research-brief.md`
- `articles/<文章标题>/contradiction-map.md`
- `articles/<文章标题>/audience-card.md`
- `articles/<文章标题>/topic-card.md`

任一缺失则停下，提示用户补跑对应前置阶段。

### 步骤 2：通读研究输入
通读 research-brief + contradiction-map + audience-card + topic-card，找出 2-3 条**有张力、能成文章**的主线方向。重点从矛盾地图的"可成主线的张力点"中提炼。

### 步骤 3：设计 2-3 个差异化主线候选
每个候选写清楚四要素：
- **一句话主线**（这篇文章到底在讲什么）
- **核心观点**（作者想让读者接受的那个判断）
- **读者收益**（这条主线能让锁定读者拿到什么）
- **风险**（这条主线可能的薄弱点 / 容易翻车的地方 / 需要补强的证据）

候选之间要有明确分野（例如：肯定式主张 / 反共识质疑 / 实操方法派）。

### 步骤 4：AskUserQuestion 让用户选定
用一次 `AskUserQuestion`（单选），把每个候选压缩成选项描述（含一句话主线 + 核心观点），加 Other 允许用户提出自己的主线或要求调整。

### 步骤 5：写 direction-lock.md
写入 `articles/<文章标题>/direction-lock.md`，包含：
- `locked: true`
- **全部候选**（2-3 个，完整四要素）
- **chosen**（用户选中的那个）
- **锁定后的主线**（最终确认版的一句话主线 + 核心观点 + 读者收益）
- 用户选择理由 / 调整记录（原话尽量保留）

### 步骤 6：翻转 Gate B 并更新 workflow-state.md
- `direction_locked: true`  ← **关键门禁翻转**
- `current_stage: outline`
- 日志追加：`[direction-lock] 锁定主线=<一句话主线>，direction_locked=true，Gate B 通过`

### 步骤 7：交付并提示下一步
简述锁定的主线，并明确提示：**Gate B 已通过，下一步运行 `/outline-design` 设计章节大纲**。

## 完成标志
direction-lock.md 存在且 locked=true；workflow-state.md 中 `direction_locked: true`。

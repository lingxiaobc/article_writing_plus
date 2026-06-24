---
name: audience-confirm
description: 公众号写作流程的第二步技能。在 topic-card.md 完成后、联网研究前使用。基于话题卡设计 2-4 个差异化的目标读者候选画像，用选择题让用户锁定目标读者，写入 audience-card.md，并翻转 Gate A（audience_locked=true）。
when_to_use: topic-interview 完成后、进入 research-orchestration 之前；需要锁定目标读者画像时。
allowed-tools: AskUserQuestion Read Write
---

# audience-confirm — 目标读者锁定技能

此阶段锁定"这篇文章写给谁看"。**只有锁定了读者，研究阶段才知道去搜什么、视角代理才知道以谁的视角看**。这是 Gate A。

## 严格纪律
- 与用户的全部交互只能用 `AskUserQuestion`（选择题）。
- 此阶段不锁定主线。
- 进入研究阶段前 `audience_locked` 必须为 true。

## SOP 步骤

### 步骤 1：前置自检
读 `articles/<文章标题>/topic-card.md`，确认存在且内容完整。若不存在，停下提示用户先跑 `/topic-interview`。
读 `articles/<文章标题>/workflow-state.md`，确认 current_stage=audience。

### 步骤 2：设计 2-4 个差异化读者候选画像
基于 topic-card，设计 2-4 个**相互区分明显**的目标读者画像。每个画像写清楚：
- **是谁**：身份/角色/所处阶段
- **已掌握**：对这个话题已经知道什么、有什么基础认知
- **关心什么**：最在意的问题、最容易被触动的点
- **痛点**：当下的困惑、卡点、情绪
- **期待收获**：希望读完拿到认知 / 方法 / 情绪 / 价值观中的哪种

画像之间要有区分度（例如：完全小白 / 有一定了解想深化 / 已经在做的实践者），不要给出大同小异的画像。

### 步骤 3：AskUserQuestion 让用户选定
用一次 `AskUserQuestion`（单选），把每个画像的要点压缩成选项描述（不要太长），加上 Other 允许用户补充或修正。可顺带问一句"你写这篇主要是想打动上面哪一类人"。

### 步骤 4：写 audience-card.md
写入 `articles/<文章标题>/audience-card.md`，包含：
- `confirmed: true`
- **选定画像**（用户选中的那个，完整五要素）
- **全部候选画像**（保留全部候选，供后续阶段参考与对照）
- 选定理由（用户的选择倾向，原话尽量保留）

### 步骤 5：翻转 Gate A 并更新 workflow-state.md
- `audience_locked: true`  ← **这是关键门禁翻转**
- `current_stage: research`
- 日志追加：`[audience-confirm] 锁定目标读者=<选定画像名>，audience_locked=true，Gate A 通过`

### 步骤 6：交付并提示下一步
简述锁定的读者画像，并明确提示：**Gate A 已通过，下一步运行 `/research-orchestration` 启动多视角联网研究**。

## 完成标志
audience-card.md 存在且 confirmed=true；workflow-state.md 中 `audience_locked: true`。

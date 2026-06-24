---
name: outline-design
description: 公众号写作流程的第五步技能。在 direction_locked=true 后、正文前使用。调用 editorial-structure 子代理产出结构方案，主程序结合研究素材产出章节级大纲，用选择题让用户确认，写入 outline.md，并翻转 Gate C（outline_locked=true）。
when_to_use: Gate B（direction_locked=true）已通过，需要设计章节级大纲时。
allowed-tools: AskUserQuestion Read Write Agent
---

# outline-design — 章节大纲设计技能

此阶段把锁定的主线落成可执行的章节大纲。结构方案来自 editorial-structure 子代理，**主程序结合研究素材拍板章节内容**，用户确认后才算锁定。这是 Gate C。

## 严格纪律
- 与用户的交互只能用 `AskUserQuestion`（选择题，确认 / 要求调整）。
- 结构设计交给 editorial-structure，章节素材由主程序从 research-brief 中组织。
- 偏题但有用的素材归 parking-lot.md，不硬塞进主线。

## SOP 步骤

### 步骤 1：前置自检 Gate B
读 `articles/<文章标题>/workflow-state.md`，确认 `direction_locked: true`。未通过则停下，提示先跑 `/direction-lock`。

### 步骤 2：调用 editorial-structure
调用 `editorial-structure` 子代理（subagent_type: `editorial-structure`），传入：
- `direction-lock.md`（锁定主线 + 核心观点 + 读者收益）
- `audience-card.md`（目标读者画像）
要求它返回结构方案，至少包含：
- 叙事弧（起承转合的节奏）
- 开头钩子（用什么抓住读者）
- 情绪起伏曲线（哪里紧、哪里松、哪里顿悟）
- 顿悟点设计（"山重水复疑无路，柳暗花明又一村"的那个转折）

### 步骤 3：主程序产出章节级大纲
结合 editorial-structure 的结构方案 + `research-brief.md` 的素材，主程序产出**章节级**大纲。每个章节写清楚：
- 章节标题 / 主题
- 本章要点（要传达的判断或信息）
- 支撑素材（来自 research-brief 的具体证据 / 场景 / 数据 / 类比）
- 本章在情绪曲线上的位置

大纲必须包含：
- **开头钩子**（明确写出用什么开头）
- **结尾拉回行动 / 希望**（明确写出如何收尾，不留空泛）

### 步骤 4：AskUserQuestion 让用户确认
用一次 `AskUserQuestion`，让用户确认大纲（选项如：确认开写 / 要调整某章 / 要换开头钩子 / Other）。若用户要求调整，主程序据反馈修订后再次确认，直到用户确认。

### 步骤 5：写 outline.md
写入 `articles/<文章标题>/outline.md`，包含：
- `confirmed: true`
- 锁定主线（引用 direction-lock）
- 目标读者（引用 audience-card）
- 结构方案（叙事弧 / 钩子 / 情绪曲线 / 顿悟点，来自 editorial-structure）
- 章节级大纲（每章要点 + 素材）
- 开头钩子 + 结尾设计

把偏题但有用的素材归入 `articles/<文章标题>/parking-lot.md`。

### 步骤 6：翻转 Gate C 并更新 workflow-state.md
- `outline_locked: true`  ← **关键门禁翻转**
- `current_stage: writing`
- 日志追加：`[outline-design] 大纲确认，outline_locked=true，Gate C 通过`

### 步骤 7：交付并提示下一步
简述大纲结构（章节骨架 + 钩子 + 顿悟点），并明确提示：**Gate C 已通过，下一步运行 `/write-article` 撰写正文**。

## 完成标志
outline.md 存在且 confirmed=true；workflow-state.md 中 `outline_locked: true`。

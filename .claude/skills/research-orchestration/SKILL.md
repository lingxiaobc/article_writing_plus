---
name: research-orchestration
description: 公众号写作流程的第三步技能。在 audience_locked=true 后、主线锁定前使用。编排联网搜索（必须经 web-searcher 子代理）+ 并行 7 个视角代理 + 矛盾分析 + 研究综合，产出 source-map.md、7 份 perspective-reports、contradiction-map.md、research-brief.md。主程序只整理输入，不在此阶段定主线。
when_to_use: Gate A（audience_locked=true）已通过，需要为方向锁定阶段准备多视角研究输入时。
allowed-tools: Read Write Agent Bash(mkdir *)
disallowed-tools: WebSearch WebFetch
---

# research-orchestration — 多视角研究编排技能

此阶段是"总编辑"调度多路子代理的研究中枢。**联网搜索只能走 web-searcher 子代理，主程序自己禁止用 WebSearch/WebFetch**。此阶段只产出研究输入，**不定主线**（主线留给 direction-lock，由用户拍板）。

## 严格纪律
- 主程序**不得**直接 WebSearch/WebFetch（已在 disallowed-tools 中移除）。
- 子代理只提供输入，主程序在此阶段**不定主线**。
- 偏题但有价值的素材，归入 `parking-lot.md`，不丢。
- 与用户**不交互**（此阶段不需要 AskUserQuestion）。

## SOP 步骤

### 步骤 1：前置自检 Gate A
读 `articles/<文章标题>/workflow-state.md`，确认 `audience_locked: true`。**未通过则停下**，提示用户先跑 `/audience-confirm`。

### 步骤 2：写 research-task.md
读 topic-card + audience-card，提炼本轮研究需要回答的关键问题清单（议题、目标读者的痛点对应问题、需查证的事实/数据、需采集的观点与评论），写入 `articles/<文章标题>/research-task.md`。

### 步骤 3：联网搜索 → source-map.md
调用 `web-searcher` 子代理（subagent_type: `web-searcher`），传入 research-task.md 的关键问题，要求多渠道、广覆盖（官方权威 + 论坛评论区 + 各平台用户评价）。
主程序整理 web-searcher 返回的资料，写入 `articles/<文章标题>/source-map.md`（含来源、要点、可信度标注）。
**如需多次搜索，分多次调用 web-searcher**，不要让一个子代理扛全部。

### 步骤 4：并行派发 7 个视角代理（关键：同一条消息并发）
在**同一条消息**里，用 7 个 `Agent` 工具调用并发派发（不要串行），subagent_type 分别为：
- `reader-perspective`（读者视角）
- `practitioner-perspective`（实践者视角）
- `realist-perspective`（现实主义者视角）
- `skeptic-perspective`（怀疑主义者视角）
- `economist-perspective`（经济视角）
- `historian-perspective`（历史视角）
- `communication-perspective`（传播学视角）

每个代理传入：
- 议题摘要（来自 topic-card）
- 目标读者画像摘要（来自 audience-card）
- `source-map.md` 的绝对路径
- 文章目录 `articles/<文章标题>/` 的绝对路径

每个代理各自把报告写到 `articles/<文章标题>/perspective-reports/<name>.md`（用 `Bash(mkdir -p)` 先建好子目录），并返回要点摘要给主程序。

### 步骤 5：矛盾分析 → contradiction-map.md
确认 7 份 perspective-reports 都已写入后，调用 `contradiction-analysis`（subagent_type: `contradiction-analysis`），传入文章目录路径，让它读全部报告，返回矛盾地图（共同结论 / 核心冲突 / 证据强弱 / 可成主线的张力点）。
主程序把矛盾地图写入 `articles/<文章标题>/contradiction-map.md`。
（contradiction-analysis 不写文件，主程序负责落盘。）

### 步骤 6：研究综合 → research-brief.md
调用 `research-synthesis`（subagent_type: `research-synthesis`），传入 source-map + 7 份 perspective-reports + contradiction-map，让它产出可供 direction-lock 直接使用的综合简报。
主程序写入 `articles/<文章标题>/research-brief.md`。

### 步骤 7：归档偏题素材
把研究中有价值但偏离当前读者/主线候选的素材，归入 `articles/<文章标题>/parking-lot.md`。

### 步骤 8：更新 workflow-state.md
- 勾选产出：source-map.md、7 份 perspective-reports、contradiction-map.md、research-brief.md
- `current_stage: direction`
- 日志追加：`[research-orchestration] 完成，7 视角报告 + 矛盾地图 + 研究简报就绪，待进入 direction-lock`
- **不翻转** direction_locked（那是 direction-lock 的职责）。

### 步骤 9：提示下一步
向用户简述研究发现要点（矛盾地图中的张力点最值得点出），并明确提示：**下一步运行 `/direction-lock` 锁定文章主线**。

## 完成标志
source-map.md、7 份 perspective-reports/<name>.md、contradiction-map.md、research-brief.md 均存在；current_stage=direction。

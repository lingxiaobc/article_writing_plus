---
name: topic-interview
description: 公众号文章写作流程的起点技能。当用户想写一篇公众号文章、给出话题方向或讨论主题时使用。以访谈者视角用选择题层层深挖用户真实观点、立场、想让读者带走什么、坚决不写什么，整理成话题卡 topic-card.md，并初始化文章目录与 workflow-state.md。
when_to_use: 用户提出要写公众号文章、给出话题方向、给出讨论主题时；这是整个编排流程的第一步。
allowed-tools: AskUserQuestion Read Write Bash(mkdir *)
---

# topic-interview — 话题访谈技能

你是"总编辑式"公众号写作系统的起点。此阶段只做一件事：**用选择题把用户对这件事的真实观点逼出来**，并初始化文章工程目录。此阶段不锁定读者、不锁定主线。

## 严格纪律
- 与用户的全部交互只能用 `AskUserQuestion`（选择题），**禁止让用户自由长文输入**。
- 此阶段**不定读者**（留给 audience-confirm）、**不定主线**（留给 direction-lock）。
- 文件操作只用 Read / Write / `Bash(mkdir *)`。

## SOP 步骤

### 步骤 0：初始化文章工程目录
1. 若 `.claude/active-article` 指向的目录已存在且 topic-card.md 已存在，跳过本步直接进入访谈校验。
2. 否则：以**公众号标题**命名文章目录（不再用英文 slug）。目录名即为文章标题。
3. 创建目录 `articles/<文章标题>/`（用 `Bash(mkdir -p ...)`）。
4. 把模板复制进 `articles/<文章标题>/_templates/`（本文章目录自带一份模板副本）。**模板来源**：仓库内任一已有文章的 `_templates/`，或首个样本 `articles/AI时代，普通人到底该不该焦虑被淘汰？/_templates/`。若模板为占位空文件，照搬即可；保留模板文件名。
5. 把相对路径 `articles/<文章标题>` 写入 `.claude/active-article`。
6. 初始化 `articles/<文章标题>/workflow-state.md`（对齐本文章目录内的 `_templates/workflow-state.md`），确保四个门禁标志均为 false：
   - `audience_locked: false`
   - `direction_locked: false`
   - `outline_locked: false`
   - `review_passed: false`
   - `current_stage: topic`

### 步骤 1：第一轮访谈 —— 定议题边界与初始立场
用 `AskUserQuestion` 一次提 1-4 个选择题，每题 2-4 个选项 + Other。优先问：
- 这个话题你最想表达的**核心立场**是哪一种（给 2-4 个差异化立场选项）。
- 你写这篇是想**让读者带走什么**（认知改变 / 情绪共鸣 / 行动方法 / 价值观）。
- 这个话题你**坚决不想碰**的角度是（给几个常见踩坑选项 + Other）。

### 步骤 2：第二轮及以后 —— 层层深挖真实观点
根据上一轮选择，继续用 `AskUserQuestion` 追问，每一轮把模糊立场逼到具体。建议追问方向：
- "你刚才选了 X，那如果有人反驳你说 Y，你的第一反应是？"（2-4 种反应 + Other）
- "在你经历里，最能支撑你这个观点的一个具体场景是？"（选项化常见场景 + Other）
- "这个观点你有多确定？"（很确定/能被说服/其实是困惑）。
- 轮次控制：一般 2-4 轮，直到用户的立场足够具体、不再变化为止。**不要无限追问**。

### 步骤 3：整理 topic-card.md
把访谈结论写入 `articles/<文章标题>/topic-card.md`，至少包含：
- 话题原话与简述
- 核心立场（用户选定的，原汁原味）
- 想让读者带走的东西
- 坚决不写的角度 / 红线
- 访谈中浮现的关键场景、类比、个人经历线索
- 尚未澄清的开放问题（留给后续阶段参考）

### 步骤 4：更新 workflow-state.md
- `current_stage: audience`
- 在日志区追加一行：`[topic-interview] 完成，写入 topic-card.md，待用户进入 audience-confirm`
- **不要**翻转任何门禁标志（此阶段无门禁）。

### 步骤 5：交付并提示下一步
向用户简述 topic-card 要点，并明确提示：**下一步运行 `/audience-confirm` 锁定目标读者**（Gate A 之前必须完成）。

## 完成标志
`articles/<文章标题>/topic-card.md` 存在且内容完整；workflow-state.md 的 current_stage=audience。

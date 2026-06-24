---
name: write-article
description: 公众号写作流程的第六步技能。在 outline_locked=true 后、质量验收前使用。按大纲逐段撰写正文，严格贴合作者真实口吻（必读两份个人语言参考文件），只写主线内内容，产出 draft.md。
when_to_use: Gate C（outline_locked=true）已通过，需要撰写正文草稿时。
allowed-tools: Read Write
---

# write-article — 正文撰写技能

此阶段把确认的大纲落成正文草稿。**核心观点、取舍由主程序掌控**，但行文口吻必须严格贴合作者本人。这是降低 AI 味、写出"人味"的关键阶段。

## 严格纪律
- **必读两份个人语言参考文件**，否则写不出作者口吻。
- **只写主线内内容**，偏题但有价值的写进 parking-lot.md。
- 与用户不交互（本阶段不问问题，按确认好的大纲写）。

## SOP 步骤

### 步骤 1：前置自检 Gate C
读 `articles/<文章标题>/workflow-state.md`，确认 `outline_locked: true`。未通过则停下，提示先跑 `/outline-design`。

### 步骤 2：必读输入（缺一不可）
逐份 Read：
- `articles/<文章标题>/outline.md`（写作蓝图）
- `articles/<文章标题>/research-brief.md`（事实与素材）
- `articles/<文章标题>/direction-lock.md`（核心观点，时刻对齐）
- `.claude/reference/个人性格.md`
- `.claude/reference/个人语言习惯与表达特征.md`

**后两份是口吻的权威依据**，写作全程必须贴合其中描述的标志。

### 步骤 3：按大纲逐段撰写正文
按 outline.md 的章节顺序逐段写。写作时严格遵守以下口吻与排版规则（来自设计文档与个人语言参考）：

**口吻标志（要主动用）：**
- 说实话 / 其实 / 我才意识到 / 说白了 / 你想啊 这类口语化、自白式开头
- 生活化类比（用日常事物解释抽象概念）
- 反问句（拉近与读者的距离）
- 结尾拉回希望 / 行动（不要空喊口号）

**排版规则（严格执行）：**
- **单句成段**，每段之间**空一行**
- 例外：列表项 / 序号项不适用单句成段规则，可紧凑排列
- 段落不要太长，避免大段堆砌

**降低 AI 味：**
- 不要用"首先 / 其次 / 综上所述"这种机械连接
- 不要用"在这个快速发展的时代"之类套话开头
- 不要每段都工整对仗，允许口语化的不规整

### 步骤 4：偏题素材归档
写作中遇到有价值但偏离主线的素材、观点、案例，写进 `articles/<文章标题>/parking-lot.md`，不要硬塞进正文。

### 步骤 5：写 draft.md
把完整正文写入 `articles/<文章标题>/draft.md`。

### 步骤 6：更新 workflow-state.md
- `current_stage: review`
- 日志追加：`[write-article] 草稿完成，字数约<N>，待进入 quality-gate`
- **不翻转** review_passed（那是 quality-gate 的职责）。

### 步骤 7：提示下一步
向用户简述草稿完成情况（字数、结构、关键口吻标志用了哪些），并明确提示：**下一步运行 `/quality-gate` 做质量验收与定稿**。

## 完成标志
draft.md 存在且内容完整；current_stage=review。

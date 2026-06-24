# 公众号文章编写项目编排

> 一个跑在 **Claude Code** 里的「**总编辑式**」公众号文章写作编排系统。
> 你给一个话题，它像一家编辑部一样：访谈需求 → 多视角研究 → 锁定主线 → 设计大纲 → 撰写正文 → 质量+合规验收 → 定稿交付，全程**你拍板，AI 干活**。

---

## 目录

- [它能给你带来什么](#它能给你带来什么)
- [特点](#特点)
- [目录结构](#目录结构)
- [环境配置](#环境配置)
- [如何使用](#如何使用)
- [一篇文章的完整流程](#一篇文章的完整流程)
- [门禁机制（防止 AI 越级）](#门禁机制防止-ai-越级)
- [14 个状态产物](#14-个状态产物)
- [14 个产物清单](#14-个产物清单)
- [内置技能与子代理](#内置技能与子代理)
- [常见问题](#常见问题)

---

## 它能给你带来什么

如果你是一个公众号作者（或想做公众号的人），痛点无非这几个：

- **想写，但不知道从哪个角度切入最有价值** → 本系统先用**7 个视角**（读者/实践者/现实主义者/怀疑论者/经济视角/历史视角/传播学）并行拆解你的话题，再汇总成矛盾地图与研究简报，角度是研究出来的，不是拍脑袋。
- **AI 写的文章没有「人味」、千篇一律** → 系统内建你的**个人性格**与**个人语言习惯**两份参考，写出来的文章贴合你的口吻，是你写的，不是机器腔。
- **AI 容易跑偏、越写越离题** → 每篇文章有**4 道用户门禁**，关键节点必须你点头才往下走；跑题但有料的内容自动收进 `parking-lot.md`，不污染正文。
- **怕踩公众号合规红线**（敏感词、广告法绝对化用语、AI 生成内容标识、引流诱导分享……）→ 系统在定稿前内置**合规审查**，按官方规范逐条查，**发现的风险告知你、由你决定改不改**，AI 不擅自改你的正文。
- **配图麻烦** → 定稿后可一键为每个章节生成**手绘笔记风信息图**并自动插入文章。

一句话：**它把你从「写不动 / 写不好 / 怕踩雷」里解放出来，让你专注在「我到底想表达什么」。**

---

## 特点

| 特点 | 说明 |
|---|---|
| 🎯 **总编辑式编排** | 主程序（Claude 主对话）当总编辑，掌方向、主线、取舍；子代理只做独立可交付的任务，不替你拍板。 |
| 🔍 **多视角并行研究** | 7 个视角子代理 + 矛盾分析 + 研究综合，结构化地把一个话题「翻个底朝天」。 |
| 🚪 **4 道用户门禁** | 读者确认→研究、主线锁定→大纲、大纲确认→正文、验收通过→定稿，每道关你说了算。 |
| 🛡️ **合规审查内建** | 依据《公众号合规规范》（含 2024–2026 治理重点、广告法、AI 生成标识），定稿前逐条审查；**风险告知你，由你定夺**。 |
| ✍️ **贴合个人风格** | `.claude/reference/` 下两份个人语言参考保证文章「是你的口吻」，不是机器腔。 |
| 📁 **自包含文章结构** | 每篇文章独占一个标题文件夹，自带模板与全部中间产物，文章之间互不污染。 |
| 🖼️ **自动配信息图** | 定稿后按 `##` 章节逐个生成手绘笔记风信息图，并原地插入文章末尾。 |
| 🗂️ **偏题自动归档** | 任何阶段发现「有价值但偏题」的内容，自动追加进 `parking-lot.md`，不跑题。 |

---

## 目录结构

```
article_writing_plus/
├── CLAUDE.md            # 项目总控：原则 / 流程 / 门禁 / 目录规则 / 产物清单（核心规则文件）
├── README.md            # 本文件
│
├── .claude/
│   ├── active-article               # 当前活动文章指针（相对路径，如 articles/<标题>）
│   ├── settings.local.json          # Claude Code 配置与密钥（自填，含敏感信息，勿提交公开仓库）
│   │
│   ├── agents/                      # 13 个子代理（每个一个独立职责）
│   │   ├── web-searcher.md          # 联网搜索（主程序禁止自己联网，一律走它）
│   │   ├── reader-perspective.md        # 读者视角
│   │   ├── practitioner-perspective.md  # 一线实践者视角
│   │   ├── realist-perspective.md       # 现实主义者视角（数据/统计）
│   │   ├── skeptic-perspective.md       # 怀疑论者视角
│   │   ├── economist-perspective.md     # 经济/利益结构视角
│   │   ├── historian-perspective.md     # 历史学家视角
│   │   ├── communication-perspective.md # 传播学视角
│   │   ├── editorial-structure.md       # 文章结构设计（编辑）
│   │   ├── contradiction-analysis.md    # 矛盾分析（只读）
│   │   ├── research-synthesis.md        # 研究综合简报
│   │   ├── quality-acceptance.md        # 质量验收
│   │   └── compliance-check.md          # 公众号合规审查（只读，告知不擅改）
│   │
│   ├── skills/                      # 9 个技能（可用 /命令 触发，也可自然语言触发）
│   │   ├── topic-interview/         # 访谈 → 话题卡
│   │   ├── audience-confirm/        # 确认读者 → 读者卡
│   │   ├── research-orchestration/  # 研究编排（调搜索+7视角+矛盾+综合）
│   │   ├── direction-lock/          # 锁定主线
│   │   ├── outline-design/          # 设计大纲
│   │   ├── write-article/           # 撰写正文
│   │   ├── quality-gate/            # 质量验收（口吻+排版+合规）
│   │   ├── infographic_generation/  # 定稿后按 ## 章节生成信息图
│   │   └── cover-generator/         # 封面图生成
│   │
│   └── reference/                   # 写作与合规参考
│       ├── 个人性格.md
│       ├── 个人语言习惯与表达特征.md
│       └── 公众号合规规范.md          # 合规审查的依据
│
├── articles/                        # 文章工作区（中间产物，非最终交付）
│   ├── CLAUDE.md                    # 工作区结构细则（进入目录自动加载）
│   └── AI时代，普通人到底该不该焦虑被淘汰？/   # 样本文章（自包含）
│       ├── _templates/              # 本篇自己的模板副本
│       ├── workflow-state.md        # 门禁状态（主程序靠它自检）
│       ├── topic-card.md / audience-card.md / …（14 个工作产物）
│       └── perspective-reports/     # 7 份视角报告
│
└── AI时代，普通人到底该不该焦虑被淘汰？/    # 样本最终交付（项目根，与 articles/ 同级）
    ├── AI时代，普通人到底该不该焦虑被淘汰？.md   # 定稿文章
    └── image/                       # 文章配图
```

> **每篇文章最终有两个标题文件夹**：
> `articles/<标题>/` 是**工作区**（中间产物）；
> 项目根的 `<标题>/` 是**最终交付**（定稿 + 配图）。

---

## 环境配置

> 这是一个 **Claude Code 项目**（靠 `CLAUDE.md` + `skills/` + `agents/` 驱动），**不是**一个独立可运行的脚本。所有「使用」都在 Claude Code 里完成。

### 1. 必备：Claude Code

- 安装 [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)（CLI）。
- 确保它能连上一个可用的模型。本项目作者用的是自建中转（relay），你二选一：
  - **用官方 Anthropic API**：配置官方 API Key；
  - **用中转**：在 `.claude/settings.local.json` 的 `env` 里填你自己的中转地址与 Token。

  涉及的环境变量（**值请填你自己的，切勿用作者的、切勿提交到公开仓库**）：

  | 变量名 | 作用 |
  |---|---|
  | `ANTHROPIC_BASE_URL` | Claude 接口地址（官方或中转） |
  | `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` | 鉴权 Token |
  | `ANTHROPIC_DEFAULT_OPUS_MODEL` 等 | 指定模型 |
  | `GEMINI_KEY` | Gemini 生图密钥（信息图 / 封面） |

  > ⚠️ `.claude/settings.local.json` 含**敏感凭据**，**已被 `.gitignore` 忽略、不会提交**——可放心填入真实密钥。

#### 配置文件模板（settings.local.json）

仓库提供 `.claude/settings.local.json.template`（**已纳入版本控制**），它是 `settings.local.json` 的模板，敏感字段已替换为占位符。上手三步：

1. **复制**模板为正式文件：`cp .claude/settings.local.json.template .claude/settings.local.json`（Windows 下复制后重命名即可）。
2. **填值**：把 `YOUR_ANTHROPIC_AUTH_TOKEN_HERE`、`YOUR_GEMINI_KEY_HERE` 等占位符换成你自己的值。
3. 复制出来的 `settings.local.json` 会被自动忽略，**不会被提交**。

字段速查（官方 API 与中转二选一）：

| 字段 | 官方 Anthropic API | 中转 / relay（本项目作者所用） |
|---|---|---|
| `ANTHROPIC_BASE_URL` | `https://api.anthropic.com` | 中转地址（如 `https://<中转域名>/api/anthropic`） |
| `ANTHROPIC_API_KEY` | 你的官方 API Key | 一般留空 |
| `ANTHROPIC_AUTH_TOKEN` | 一般留空 | 中转下发的 Token |
| `ANTHROPIC_DEFAULT_*_MODEL` | 官方模型 ID（如 `claude-opus-4-8`） | 中转提供的模型名 |
| `GEMINI_KEY` | Gemini 生图密钥（信息图/封面用；不配图可留占位） | 同左 |

> 用哪种就填哪种：官方 API 填 `ANTHROPIC_API_KEY`；中转填 `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL`。图片生成才需要 `GEMINI_KEY`，纯写文章可忽略。

### 2. 可选：图片生成（信息图 / 封面）

只有用到「生成信息图 / 封面图」时才需要，写文章本身不需要。

- **Python 3.8+**
- 安装依赖：
  ```bash
  pip install google-genai httpx
  ```
- 在 `.claude/settings.local.json` 的 `env.GEMINI_KEY` 里填你的 Gemini 密钥（脚本会自动读取，也可用同名环境变量）。
- 若你在需要代理的网络环境，设置 `HTTPS_PROXY` 环境变量，脚本会自动走代理。

### 3. 配置个人写作风格（强烈建议，否则文章没有「人味」）

打开 `.claude/reference/` 下两份文件，填入**你自己的**风格：
- `个人性格.md`：你是什么样的人、什么身份（样本里是「阿霄」，一位老师）。
- `个人语言习惯与表达特征.md`：你的口头禅、句式习惯、语气。

写得越具体，文章越像你写的。

---

## 如何使用

### 方式一：自然语言驱动（最简单）

在 Claude Code 里打开本项目目录，直接说：

> 「帮我写一篇公众号文章，话题是 XXX。」

然后跟着它的提问回答即可。主程序会：
1. 先访谈你（想表达什么、给谁看）；
2. 每到一道门禁停下来问你确认（选择题形式，点选即可）；
3. 全程你只做**选择与拍板**，研究和写作它来。

### 方式二：手动触发某个阶段的技能

每个阶段都是一个技能，可用斜杠命令或自然语言触发，例如：
- `/topic-interview` —— 重新访谈 / 立话题
- `/research-orchestration` —— 重新跑研究
- `/quality-gate` —— 重新验收
- `/infographic_generation` —— 为定稿文章配信息图

> 💡 技能会按你给的参数工作；不给参数时，主程序会读 `.claude/active-article` 自动定位当前文章。

### 第一次上手？看样本文章

仓库里已经有一篇跑完全流程的样本：**《AI时代，普通人到底该不该焦虑被淘汰？》**。
- 看工作区 `articles/AI时代，普通人到底该不该焦虑被淘汰？/` 里的 14 个产物，理解每一步产出了什么；
- 看最终交付 `AI时代，普通人到底该不该焦虑被淘汰？/` 里的定稿，理解成品长什么样。

照着这个流程，换你的话题跑一遍即可。

---

## 一篇文章的完整流程

```
访谈(topic-interview)          → topic-card.md
读者确认(audience-confirm)      → audience-card.md
   ═══ Gate A: audience_locked ═══
研究编排(research-orchestration)
   ├─ web-searcher            → source-map.md
   ├─ 7 视角子代理            → perspective-reports/*.md
   ├─ contradiction-analysis   → contradiction-map.md
   └─ research-synthesis      → research-brief.md
主线锁定(direction-lock)        → direction-lock.md
   ═══ Gate B: direction_locked ═══
大纲设计(outline-design)        → outline.md
   ═══ Gate C: outline_locked ═══
正文撰写(write-article)         → draft.md
质量验收(quality-gate)
   ├─ quality-acceptance（口吻/排版/错别字）
   └─ compliance-check（合规/敏感词）
   ═══ Gate D: review_passed ═══
定稿(final)                     → final.md → 交付文件夹 <标题>/（+ image/）
[可选] infographic_generation   → 每章信息图，插入文章末尾
```

每个阶段的**详细 SOP** 在 `.claude/skills/<阶段名>/SKILL.md` 里。

---

## 门禁机制（防止 AI 越级）

系统用 **4 道软门禁** 约束流程，状态写在 `workflow-state.md` 里，主程序每次推进前自检：未通过的门禁为 `false` 时，绝不推进到其后阶段。

| 门禁 | 标志 | 置为 true 的前提 | 通过后允许进入 |
|---|---|---|---|
| **Gate A** | `audience_locked` | 已选定目标读者画像并确认 | 研究 |
| **Gate B** | `direction_locked` | 已选定文章主线并锁定 | 大纲 |
| **Gate C** | `outline_locked` | 大纲已与你确认 | 正文 |
| **Gate D** | `review_passed` | 验收报告出具、**且你已审阅合规发现** | 定稿 |

> 🔒 特别说明：**Gate D 的合规审查，AI 只负责查、把风险告诉你；改不改由你决定**，AI 不会擅自改正文里涉及合规的内容。

---

## 14 个状态产物

每篇文章的工作区 `articles/<标题>/` 里，会产出 14 个状态文件，构成文章的「可追溯全记录」：

| 产物 | 作用 |
|---|---|
| `workflow-state.md` | 当前阶段 + 4 道门禁状态 + 产出勾选 + 日志 |
| `topic-card.md` | 话题卡（访谈结论） |
| `audience-card.md` | 目标读者画像 |
| `research-task.md` | 研究任务派发单 |
| `source-map.md` | 资料地图（搜索来源汇总） |
| `perspective-reports/` | 7 份视角报告 + 1 个模板 |
| `contradiction-map.md` | 多视角矛盾 / 共识地图 |
| `research-brief.md` | 研究综合简报 |
| `direction-lock.md` | 锁定的文章主线 |
| `outline.md` | 文章大纲 |
| `draft.md` | 正文草稿 |
| `review-report.md` | 质量验收报告 |
| `final.md` | 终稿（工作区版） |
| `parking-lot.md` | 偏题但有价值的内容（全程追加） |

## 14 个产物清单

`workflow-state.md` · `topic-card.md` · `audience-card.md` · `research-task.md` · `source-map.md` · `perspective-reports/`（含 7 份视角报告 + 1 个模板）· `contradiction-map.md` · `research-brief.md` · `direction-lock.md` · `outline.md` · `draft.md` · `review-report.md` · `final.md` · `parking-lot.md`

---

## 内置技能与子代理

- **9 个技能**（`.claude/skills/`）：`topic-interview`、`audience-confirm`、`research-orchestration`、`direction-lock`、`outline-design`、`write-article`、`quality-gate`、`infographic_generation`、`cover-generator`。
- **13 个子代理**（`.claude/agents/`）：见上方[目录结构](#目录结构)中的列表。
- **子代理边界**：联网搜索只走 `web-searcher`（主程序禁自己联网）；视角/结构/验收代理写各自产物；`contradiction-analysis` 与 `compliance-check` 只读；合规发现只告知用户、不擅自改。

详细的职责边界表见 `CLAUDE.md` 第四节。

---

## 常见问题

**Q：我必须用命令（`/技能`）吗？**
不用。直接用自然语言跟它说就行，它会自动推进；命令只是给你手动切某个阶段用。

**Q：文章会被 AI 改得不像我写的吗？**
不会。`.claude/reference/` 下的两份个人风格参考会约束口吻；`quality-acceptance` 还会专门检查「个人语言特征是否到位」。建议你把这两份参考填得尽量贴合自己。

**Q：合规问题会不会被 AI 自动改掉？**
不会。合规审查（`compliance-check`）只查、只列出风险与替换建议；**改不改、怎么改，由你决定**。这也是项目刻意设计的安全边界。

**Q：信息图生成为什么提示「未发现 ## 二级标题」？**
信息图技能严格按文章里的 `## ` 二级标题切分章节。如果你的文章用 `---` 分隔、没有 `##`，它会安全地不生成、不改稿，并提示你先给各章节补上 `##` 标题。

**Q：图片生成 / 联网搜索需要联网，会不会有问题？**
- 联网搜索统一由 `web-searcher` 子代理完成（受 Claude Code 的网络环境约束）；
- 图片生成经 Gemini，密钥从 `GEMINI_KEY` 读取，需要时设 `HTTPS_PROXY` 走代理。

**Q：想自己加一个视角 / 技能 / 代理怎么办？**
- 加子代理：在 `.claude/agents/` 新建 `.md`（参考现有写法），并**重启 Claude Code 会话**后才能用 `subagent_type` 调用。
- 加技能：在 `.claude/skills/` 新建文件夹 + `SKILL.md`（参考现有技能）。
- 记得在 `CLAUDE.md` 的边界表 / 流程图里登记，保持规则一致。

---

*项目原则、流程、规则以 `CLAUDE.md` 为准；本文档为快速上手导览。*

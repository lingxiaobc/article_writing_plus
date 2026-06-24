# 公众号文章编写项目编排 —— 项目说明

> 本文件只写原则、主程序职责、子代理边界、门禁规则、目录规则、产物清单。
> 详细 SOP 见 `.claude/skills/`，子代理定义见 `.claude/agents/`。

## 一、项目定位

这是一个**总编辑式**的公众号文章写作编排系统。主程序（即你，Claude 主对话）是**总编辑**，掌控方向、主线、观点、取舍；子代理负责独立的、可交付的任务（搜索、多视角分析、矛盾分析、结构设计、质量验收）。最终文章必须有作者本人的个人见解与风格，并经事实/质量把关。

## 二、核心原则

1. **主程序控方向**：最终主线、核心观点、行动建议、文章取舍，一律由主程序拍板。
2. **子代理做独立任务**：每个子代理只产出一个独立可交付物（一份报告/一张地图/一份方案），不介入全局决策。
3. **用户访谈只由主程序做**：访谈/确认读者/确认主线等用户交互，只能主程序用 `AskUserQuestion` 完成，子代理禁止直接问用户。
4. **子代理不定最终主线**：子代理给的建议、候选、方案仅供主程序参考，不得替主程序拍板。
5. **每篇独立目录**：每篇文章独占 `articles/<文章标题>/`（自包含结构，详见第七节），互不污染。
6. **14 产物齐备**：每篇文章必须产全 14 个状态产物（清单见第六节），缺一不可定终稿。
7. **四个门禁不得越级**：`audience_locked` / `direction_locked` / `outline_locked` / `review_passed` 四道门禁，未通过不得推进到下一阶段。
8. **偏离主线但有价值的内容入 parking-lot**：任何子代理或主程序发现的、有价值但偏离当前主线的内容，追加进 `parking-lot.md`，不在正文里跑题。
9. **终稿必经验收（含合规审查）**：未经 `quality-acceptance` 出具验收报告并令主程序判定 `review_passed: true`，不得写终稿。**合规审查（compliance-check）的发现须告知用户、由用户决定是否修复，主程序不擅自修改合规相关内容**（只应用用户明确批准的修改）。
10. **主程序联网须走 web-searcher**：主程序禁止自用 `WebSearch` / `WebFetch` / `curl` / 任何脚本式联网；一切联网搜索必须经 `web-searcher` 子代理。

## 三、主程序（总编辑）职责

- 与用户对话，确认主题方向、目标读者、文章主线、大纲、终稿。
- 用 `AskUserQuestion` 做所有用户访谈与确认（选择题形式优先）。
- 编排全流程：按阶段调用相应技能与子代理。
- 派发研究任务：把议题、读者摘要、source-map 路径、文章目录路径传给各视角子代理。
- 收集子代理产出，做取舍与综合判断。
- 锁定主线、确认大纲、应用验收修订（合规类修订须用户批准，主程序不擅自改合规相关内容）、定终稿。
- 读 `workflow-state.md` 自检门禁状态，未通过绝不越级。
- 维护 `parking-lot.md`（可由主程序或子代理追加）。

## 四、子代理边界表

| 子代理 | 职责（一句话） | 可写文件 | 禁止 |
|---|---|---|---|
| `web-searcher` | 多渠道联网搜索，返回资料 | 无（只返回结果给主程序） | 读写文件、执行脚本、自用正文决策 |
| `reader-perspective` | 从目标读者画像出发，说清读者最关心/最期待什么 | `perspective-reports/reader-perspective.md` | 写正文、决定主线、执行脚本 |
| `practitioner-perspective` | 一线实践者视角，判断议题能否落地、操作难点 | `perspective-reports/practitioner-perspective.md` | 写正文、决定主线、宏大抽象、执行脚本 |
| `realist-perspective` | 现实主义者，用数据/统计客观呈现现状与观点占比 | `perspective-reports/realist-perspective.md` | 主观评价、写正文、决定主线、执行脚本 |
| `skeptic-perspective` | 怀疑论者，提出有证据支撑的质疑与反面论证 | `perspective-reports/skeptic-perspective.md` | 为反对而反对、情绪化、否定选题、写正文、执行脚本 |
| `economist-perspective` | 经济/利益结构视角，分析商业模式、激励、价值 | `perspective-reports/economist-perspective.md` | 阴谋论、无证据揣测动机、写正文、执行脚本 |
| `historian-perspective` | 历史学家视角，找历史类比与演化规律 | `perspective-reports/historian-perspective.md` | 强行类比、写正文、执行脚本 |
| `communication-perspective` | 传播学视角，判断议题传播性、如何更好传播 | `perspective-reports/communication-perspective.md` | 写正文、决定主线、执行脚本 |
| `editorial-structure` | 编辑视角，设计文章结构、叙事弧、情绪起伏、顿悟点 | （输出结构方案给主程序，由主程序落入 outline） | 写正文、决定主线、执行脚本 |
| `contradiction-analysis` | 汇总多视角报告，识别共同结论、冲突、证据强弱 | `contradiction-map.md` | 编写/修改正文、决定主线 |
| `research-synthesis` | 综合资料与视角，产出可供主线/大纲使用的简报 | `research-brief.md` | 写正文、决定主线 |
| `quality-acceptance` | 读草稿，检查个人语言/排版/错别字，出验收报告 | `review-report.md` | 写正文、自行定终稿 |
| `compliance-check` | 公众号合规/敏感词审查，返回风险清单+安全替换建议 | 无（只读，返回给主程序） | 写正文、定主线、改终稿 |

## 五、阶段流程

```
访谈(topic-interview)
   └─> topic-card.md
读者确认(audience-confirm)
   └─> audience-card.md
   ═══════ Gate A: audience_locked ═══════
研究编排(research-orchestration)
   ├─ web-searcher        ─> source-map.md
   ├─ 7 视角子代理         ─> perspective-reports/*.md
   ├─ contradiction-analysis ─> contradiction-map.md
   └─ research-synthesis    ─> research-brief.md
主线锁定(direction-lock)
   └─> direction-lock.md
   ═══════ Gate B: direction_locked ═══════
大纲设计(outline-design)
   ├─ editorial-structure（结构方案）
   └─ outline.md
   ═══════ Gate C: outline_locked ═══════
正文撰写(write-article)
   └─> draft.md
质量验收(quality-gate)
   ├─ quality-acceptance（口吻/排版/错别字）
   ├─ compliance-check（合规/敏感词）
   └─> review-report.md
   ═══════ Gate D: review_passed ═══════
终稿
   └─> final.md
   └─ current_stage: done

parking-lot.md —— 贯穿全程，任何阶段发现偏题但有价值的内容均追加。
```

## 六、门禁说明（软约定）

门禁是**软约定**，不写 Hook。靠主程序读 `articles/<文章标题>/workflow-state.md` 自检：未通过的门禁标志为 `false` 时，不得推进到该门禁之后的阶段。

| 门禁 | 标志 | 进入条件（置为 true 的前提） | 退出后允许进入 |
|---|---|---|---|
| Gate A | `audience_locked` | audience-card.md 已选定目标读者画像并 `confirmed: true` | research |
| Gate B | `direction_locked` | direction-lock.md 已选定主线并 `locked: true` | outline |
| Gate C | `outline_locked` | outline.md 已与用户确认并 `confirmed: true` | writing |
| Gate D | `review_passed` | review-report.md 已出具且主程序判定 `passed: true` | final |

> 门禁四行固定写在 workflow-state.md 的代码块中，格式稳定，便于主程序 grep 自检。

## 七、目录规则

**工作区（中间产物）—— 每篇文章自包含：**
- **文章工作目录**：`articles/<文章标题>/`，直接以公众号标题命名（如 `articles/AI时代，普通人到底该不该焦虑被淘汰？/`）。每篇独占一个标题文件夹，互不污染。
- **自包含结构**：每个文章工作目录内自带一份 `_templates/`（本篇的模板副本）+ 14 个工作产物（含 `perspective-reports/`）。一句话：一篇文章的所有中间产物 + 它自己的模板，全收在一个标题文件夹里。
- **新建文章时**（由 `topic-interview` 技能执行）：创建 `articles/<标题>/`，把模板复制进 `articles/<标题>/_templates/`（**来源**：仓库内任一已有文章的 `_templates/`；若尚无文章，从首个样本 `articles/AI时代，普通人到底该不该焦虑被淘汰？/_templates/` 复制）。
- **当前活动文章指针**：`.claude/active-article`，主程序创建文章时写入相对路径（如 `articles/AI时代，普通人到底该不该焦虑被淘汰？`）。
- **视角报告子目录**：`<文章工作目录>/perspective-reports/`，每个视角代理一个文件；各报告结构对齐本目录内的 `_templates/`（不是别处的共享模板）。

**最终交付（定稿）—— 单独的标题文件夹放在项目根目录：**
- **最终交付文件夹**：`P:\article_writing_plus\<文章标题>\`（项目根目录下，与 `articles/` 同级），以标题命名。
- **文件夹内**：放入定稿文章文件（从工作区 `final.md` 整理而来——用真实标题做 H1、去掉流程元数据）+ 一个 `image/` 子目录（存放文章依赖的配图）。
- 即每篇文章最终有**两个**标题文件夹：`articles/<标题>/`（工作区/中间产物）与项目根的 `<标题>/`（最终交付 + 配图）。

**其他：**
- **个人语言参考**：`.claude/reference/`（含 `个人性格.md`、`个人语言习惯与表达特征.md`），写 draft/final 时须贴合。
- **公众号合规规范**：`.claude/reference/公众号合规规范.md`，是 compliance-check 的审查依据（验收阶段必读）；本项目文章均为 AI 辅助写作，终稿发布前须按平台要求标识 AI 辅助创作。
- `articles/` 文件夹另有 `articles/CLAUDE.md`，载明工作区结构细则；进入该目录工作时会自动加载。

## 八、14 产物清单

每篇文章必须产全以下 14 个产物：

`workflow-state.md` · `topic-card.md` · `audience-card.md` · `research-task.md` · `source-map.md` · `perspective-reports/`（含 7 份视角报告 + 1 个模板）· `contradiction-map.md` · `research-brief.md` · `direction-lock.md` · `outline.md` · `draft.md` · `review-report.md` · `final.md` · `parking-lot.md`

---

*详细 SOP 见 `.claude/skills/`，子代理定义见 `.claude/agents/`。*

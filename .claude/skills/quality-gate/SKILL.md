---
name: quality-gate
description: 公众号写作流程的最后一步技能。在 draft.md 完成后、定稿前使用。调用 quality-acceptance 子代理产出诊断与修订建议，主程序逐条审视并应用到草稿生成 final.md，翻转 Gate D（review_passed=true），向用户交付终稿。
when_to_use: write-article 完成 draft.md 后，需要质量验收与定稿时。终稿必须经验收，review_passed 未置 true 前不算完成。
allowed-tools: Read Write Agent
---

# quality-gate — 质量验收与定稿技能

此阶段是最后一道关。**终稿必经验收**，`review_passed` 未置 true 前，文章不算完成。诊断来自 quality-acceptance 子代理，**但最终取舍归主程序**——认可的应用，不认可的说明理由。

## 严格纪律
- 终稿必经验收，不允许跳过。
- 子代理只给诊断与建议，**采纳与否由主程序决定**（核心观点与取舍归主程序）。
- 不认可的修订必须留理由（写在 review-report.md 或交付说明里），不能默默忽略。
- **两类发现区别处理**：
  - **quality-acceptance 的发现**（口吻/排版/错别字，属机械修订）：主程序可逐条审视，认可的应用、不认可的留理由。
  - **compliance-check 的合规发现**（涉微信公众号平台安全/合规规范）：主程序**不直接修改**，一律先**告知用户、由用户决定是否修复**，主程序**只应用用户明确批准的修改**；用户未批准的合规项，不得擅自改 final.md。

## SOP 步骤

### 步骤 1：前置自检
确认 `articles/<文章标题>/draft.md` 存在且内容完整。不存在则停下，提示先跑 `/write-article`。

### 步骤 2：调用 quality-acceptance
调用 `quality-acceptance` 子代理（subagent_type: `quality-acceptance`），传入：
- `draft.md`（待验收草稿，绝对路径）
- `outline.md`（语境：结构预期）
- `direction-lock.md`（语境：核心观点是否到位）

要求它按设计文档的诊断维度产出诊断 + 建议修订，至少覆盖：
1. **个人语言特性**：有无作者个人的语言习惯、语气、口吻等个人特征表达（对照两份个人语言参考）
2. **排版规则**：是否单句成段、段间空行（列表 / 序号除外）
3. **文字准确**：有无错别字、漏字、病句
4. **主线贴合**：是否偏离锁定的核心观点（对照 direction-lock）

quality-acceptance 把诊断报告写入 `articles/<文章标题>/review-report.md`，并返回要点给主程序。

### 步骤 3：调用 compliance-check（合规 / 敏感词审查）
与 quality-acceptance 并行（或紧随其后）调用 `compliance-check` 子代理（subagent_type: `compliance-check`），传入：
- `draft.md`（待审查草稿，绝对路径）
- （必要时）`outline.md` / `direction-lock.md`（语境）

要求它扫描草稿是否存在微信公众号平台合规风险（政治与网络管控、平台规则、医疗/金融/健康、未核实数据/案例等类别），返回**风险清单表（风险点+类别+风险等级+安全替换建议）**。compliance-check 只读、不写文件，把清单直接返回给主程序。

### 步骤 4：主程序逐条审视并应用
主程序逐条审视 review-report.md 的诊断与建议，但**两类发现区别处理**：

**(A) quality-acceptance 的发现**（口吻/排版/错别字，属机械修订）——主程序自行取舍：
- **认可的**：直接应用到 draft，生成 `articles/<文章标题>/final.md`。
- **不认可的**：在该条旁注明不采纳理由（取舍归主程序，例如"这条会削弱作者真实口吻，不采纳"）。
- **部分认可的**：折中处理后写入 final.md。

**(B) compliance-check 的合规发现**（涉微信公众号平台安全/合规规范）——**主程序不擅自改**，须告知用户、由用户定夺：
- 主程序把 compliance-check 返回的合规风险清单并入 `review-report.md`，新增"**合规 / 敏感词检查**"段，整理成统一表格：

  | 风险点（原文片段 + 位置） | 类别 | 风险等级（高/中/低） | 建议处理 |
  |---|---|---|---|

- **然后用 `AskUserQuestion` 把该表呈现给用户**，让用户对每一条逐条（或批量）作出决定：
  - **修复**（按建议安全替换处理，或用户给出自己的改法）
  - **不改保留**（用户明确接受该风险，同意原样发布）
  - **自定义**（用户给出其它处理意见）
- **只把用户明确批准（"修复"或"自定义"）的修改应用到 final.md**；用户未批准（包括尚未回答、未逐项决定）的合规项，主程序**一律不得擅自修改 final.md**，也不得自行按"建议处理"默认替换。
- 把用户的每条决定（修复 / 保留 / 自定义 + 用户原话）追加到 review-report.md 对应条目下。

把审视结论（采纳 / 不采纳 + 理由；合规类则附用户的决定）追加到 review-report.md 的对应条目下。

### 步骤 5：翻转 Gate D 并更新 workflow-state.md
- `review_passed: true`  ← **关键门禁翻转**
- `current_stage: done`
- 日志追加：`[quality-gate] 验收通过，生成 final.md，review_passed=true，Gate D 通过，文章完成`

> **Gate D（review_passed=true）要求**：`quality-acceptance` 与 `compliance-check` 两项均无未解决的硬风险。其中**合规硬风险必须已经过用户审阅**——用户已对每一条合规发现逐项作出决定（"修复"或明确"接受保留"），而非由主程序自行消解或默认替换。**未告知用户、未由用户决定的合规发现，不得直接置 `review_passed=true`**。

### 步骤 6：向用户交付
向用户交付：
- `final.md` 的内容摘要（核心观点 + 结构 + 字数）
- `review-report.md` 的要点（诊断了什么、采纳了哪些、不采纳哪些及理由）

明确告知用户：**四个门禁全部通过，文章已定稿，路径为 `articles/<文章标题>/final.md`**。

## 完成标志
final.md 存在；review-report.md 存在且含审视结论；workflow-state.md 中 `review_passed: true`、current_stage=done。

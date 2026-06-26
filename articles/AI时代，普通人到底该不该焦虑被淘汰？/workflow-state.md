# 工作流状态 —— ai-vs-ordinary

## 元信息

- **slug**: ai-vs-ordinary
- **title**: AI时代，普通人到底该不该焦虑被淘汰？
- **created**: 2026-06-24
- **topic**: AI时代普通人该不该焦虑被淘汰；辨析真伪焦虑 + 可落地破局

## 当前阶段

```
current_stage: done
```
<!-- 取值: interview | audience | research | direction | outline | writing | review | final | done -->

## 门禁状态

```
audience_locked: true
direction_locked: true
outline_locked: true
review_passed: true
```

> 主程序每次推进前 grep 本块自检：任一未达 true 的门禁，其后阶段不得推进。

## 子代理产出勾选清单

- [x] `source-map.md`（资料地图）
- [x] `perspective-reports/reader-perspective.md`
- [x] `perspective-reports/practitioner-perspective.md`
- [x] `perspective-reports/realist-perspective.md`
- [x] `perspective-reports/skeptic-perspective.md`
- [x] `perspective-reports/economist-perspective.md`
- [x] `perspective-reports/historian-perspective.md`
- [x] `perspective-reports/communication-perspective.md`
- [x] `contradiction-map.md`（矛盾地图）
- [x] `research-brief.md`（研究简报）
- [x] `review-report.md`（质量验收报告）

## 日志区

- [2026-06-24] interview 完成 → topic-card.md（模拟访谈，基于阿霄人设）
- [2026-06-24] audience-confirm 完成 → audience-card.md，选定 B 类读者，**Gate A 翻转 audience_locked=true**，current_stage=research
- [2026-06-24] research-orchestration 完成：web-searcher→source-map；7 视角并行→perspective-reports；contradiction-analysis→contradiction-map；research-synthesis→research-brief。current_stage=direction
- [2026-06-24] direction-lock 完成：3 候选(A/B/C)，【模拟用户选 A】，**Gate B 翻转 direction_locked=true**，current_stage=outline
- [2026-06-24] outline-design 完成：editorial-structure→结构方案；主程序出 outline.md；【模拟用户确认通过】，**Gate C 翻转 outline_locked=true**，current_stage=writing
- [2026-06-24] write-article 完成：主程序读 outline+research-brief+两份个人语言参考，按阿霄口吻写 draft.md（~2000字）。current_stage=review
- [2026-06-24] quality-gate 完成：quality-acceptance 诊断 draft→review-report.md，passed=true（5条建议级修订，无硬伤）；主程序应用 5 条认可修订生成 final.md；补齐 parking-lot.md。**Gate D 翻转 review_passed=true**，current_stage=done。**全流程完成，14 产物齐备。**
- [2026-06-24] 合规修订：根据用户反馈移除正文敏感词"翻墙"（→"国际工具的访问门槛"/"用国内就能直接打开的工具"），同步 final.md / draft.md / 交付文件夹；新增 compliance-check 子代理纳入 Gate D。
- [2026-06-24] 合规审查：compliance-check 依《公众号合规规范》审查 final.md，发现 3 项可优化（①AI生成标识-发布前须在公众号打"AI辅助创作"标识[高/流程性]；②未核实数字"4天入账20万/50万罚单"建议加信源[中]；③"年入百万"建议加"号称"[低]）。按新规则（合规发现告知用户、由用户定夺）呈现给用户，【用户决定：本篇暂不修改（明确接受保留）】。Gate D 经用户审阅有效，文章正文保持现状（"翻墙"已于先前合规修订修复）。
- [测试备注] 新建的项目子代理需会话重载才能作为 subagent_type 调用；本轮视角/矛盾/综合/编辑结构/验收经 general-purpose 代入角色执行（角色与边界取自 .claude/agents 定义）。

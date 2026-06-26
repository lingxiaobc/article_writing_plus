# Research Task（研究任务书）— ai-vs-ordinary

> 主程序在进入研究阶段前填写，作为派发给子代理的统一输入。

## 议题（传给所有子代理）
**AI时代，普通人（非技术从业者）到底该不该焦虑被淘汰？** 背景：2023 年以来生成式 AI 快速普及，"AI 取代人类""不学 AI 就被淘汰"的言论铺天盖地，大量普通人陷入焦虑。本议题要回答：这种焦虑在多大程度上是合理的？哪些是"伪焦虑"？普通人真正能做什么？

## 目标读者（摘要自 audience-card）
B 类："用得不深的焦虑型 AI 实践者"——已在用 AI 但没体系、被贩卖焦虑、不知往哪使劲、需要辨清真伪焦虑 + 可落地动作（非宏大预言）。

## 主线倾向（供子代理参考，非最终决定）
多数人焦虑错了对象（怕"被替代"，其实该怕"不开始用"）；真正的分水岭是用户思维 + 动手；用 AI 补短板而非卷长板。**注意：子代理可质疑、可反对这个倾向，结论以证据为准。**

## web-searcher 搜索清单
1. 各机构/权威对"AI 对就业影响"的预测与数据（麦肯锡/WEF/高盛等报告口径）。
2. 真实案例：哪些岗位/任务已被 AI 实质改变或替代，哪些没有。
3. 普通人焦虑的现状：相关调查、社交平台（微博/小红书/知乎）上的高赞焦虑表达与典型话术。
4. "贩卖 AI 焦虑"的利益链：知识付费、课程、自媒体如何利用焦虑变现。
5. 历史上技术冲击就业的案例（纺织机械、ATM、自动化）及其后续真实走向。

## 视角代理派发清单（并行）
| 子代理 | 输入 | 输出文件 |
|---|---|---|
| reader-perspective | 议题 + 读者摘要 | perspective-reports/reader-perspective.md |
| practitioner-perspective | 同上 | perspective-reports/practitioner-perspective.md |
| realist-perspective | 同上 | perspective-reports/realist-perspective.md |
| skeptic-perspective | 同上 | perspective-reports/skeptic-perspective.md |
| economist-perspective | 同上 | perspective-reports/economist-perspective.md |
| historian-perspective | 同上 | perspective-reports/historian-perspective.md |
| communication-perspective | 同上 | perspective-reports/communication-perspective.md |

> 注：source-map 由 web-searcher 返回后由主程序写入；本轮测试中各视角代理可自行联网核实（不阻塞等待 source-map）。

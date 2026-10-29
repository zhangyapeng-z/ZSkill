# 回归执行记录

## 2026-04-22 · UC-DEMO-BILL-01

| 项 | 内容 |
|----|------|
| **目的** | 验证 `requirements-to-prd` 七层模板能否将「个人日账+自动分类/标签+分析建议」需求落成完整 PRD。 |
| **输入** | [input-requirement.md](input-requirement.md)（固定用户原文**字面**） |
| **产出** | [expected-prd.md](expected-prd.md)（金样；含 §0 原文/推断/待补充、EARS FR、GWT、MoSCoW、Mermaid 流程/状态/ER、Out of Scope） |
| **CHECKLIST 结果** | 对照 [../SKILL.md](../SKILL.md) 成稿后自检：已覆盖问题回写、EARS+编号、数据+NFR+权限、GWT 主成功+关键失败、MVP+Out of Scope+上线指标、diagram-guide 应配图（流程+状态+数据/ER，状态图已标注与 V1 草稿二选一） |
| **待人工复核** | 金样与产品真实口径是否一致；端形态与是否上云待业务确认。 |

## 2026-06-03 · UC-DEMO-BILL-03（追溯 + OQ）

| 项 | 内容 |
|----|------|
| **目的** | 验证 ID 约定（`AC-01`）与追溯矩阵、OQ 登记对人机/下游友好。 |
| **产出** | [expected-traceability.md](expected-traceability.md) + 更新 [expected-requirement-analysis.md](expected-requirement-analysis.md) §9 OQ |
| **CHECKLIST 结果** | FA/FR/AC/OQ 表与 PRD 金样一致；无 `AC-001` 混用 |

## 如何追加新一次回归

复制上一节表格块，改日期/用例ID/简述差异即可。

## 2026-05-16 · UC-DEMO-BILL-02

| 项 | 内容 |
|----|------|
| **目的** | 验证新版 `requirements-to-prd` 能否从同一原始需求输出「需求分析文档 + PRD」两份文档，并保持功能原子、FR、AC 的追溯关系。 |
| **输入** | [input-requirement.md](input-requirement.md)（固定用户原文字面） |
| **产出** | [expected-requirement-analysis.md](expected-requirement-analysis.md) + [expected-prd.md](expected-prd.md) |
| **CHECKLIST 结果** | 新版金样覆盖需求来源、问题定义、功能原子化、方案可行性、AI/传统适配判断；PRD 金样保留 EARS、GWT、MoSCoW、Mermaid、Out of Scope。 |
| **待人工复核** | `expected-prd.md` 仍是历史完整金样，后续可按新版 PRD 表格化模板进一步压缩。 |

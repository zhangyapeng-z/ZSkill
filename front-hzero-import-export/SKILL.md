---
name: front-hzero-import-export
description: 当任务涉及 HZERO 企业前端导入、导出、模板下载或错误明细时使用，覆盖 Import 抽屉、ExcelExportPro、templateCode、tenantContext、结果反馈、权限、验证和 production replacement。
---

# HZERO 导入导出前端规范

## Scope
- 本 skill 只负责导入导出领域事实，不替代 Design、Task、Implementation、Review、Verification 或 Handoff owner。
- 新实现固定使用 `Import` / `components/Import` 和 `ExcelExportPro` / `components/ExcelExportPro`，或内部仍使用对应标准组件的 confirmed current wrapper。
- `CommonImport/Route`、旧 `ExcelExport` 和基于它们的 wrapper 只作为迁移输入与 Review finding，不是生成候选。
- templateCode、endpoint、权限、tenantContext 和运行状态必须来自用户、FDS/TDS/API、目标工程或运行证据；参数缺失时使用 generatedCandidate 并进入 replacement，不改变组件类型。

## Workflow
1. 判断当前阶段，只读取 `references/operational-rules.md` 路由到的单个 reference。
2. 直接消费 Standard Component Coordinates，不探索项目 wrapper 来替代标准入口。
3. 只有已有 confirmed current wrapper 时才读取其 props、权限、请求和文件名策略。
4. 发现旧入口时生成迁移任务；Implementation 不得继续沿用或新增双分支。

## Reference Routing
- 设计与契约：`references/operational/design.md`
- 实现与修复：`references/operational/implementation.md`
- 审查与拒收：`references/operational/review.md`
- 验证：`references/operational/verification.md`
- 领域字段：`references/operational/domain.md`

## Shared Governance
- 最终状态、question、replacement 和 Handoff 口径归 `front-hzero-enterprise-process-control`。
- 本 skill 只输出当前领域证据、finding、validator 和未验证项。

# 企业前端流程控制 - Review

## 阅读路由
- 进入 `frontend-review-agent` 时读取本文件和 `templates/review-report.md`。
- Review 默认只消费 changedFiles、touched tasks、Design/Task required acceptance、Implementation validators 和有效 `ownerReferenceCapsule`。
- 领域细节按 risk domain 读取对应 owner 的 `operational/review.md`；静态 ruleId 读取 `frontend-validator-rule-index.md`，不得把规则正文复制回 Agent 或 Review 报告。

## Review 模式
- `targeted-blocking`：普通页面和 demo-slice 默认模式，只检查本轮 changedFiles、required acceptance 和 Handoff 会消费的阻塞事实。
- `repair-fast-lane` 仍使用 `targeted-blocking`，但固定只审 source finding / exact user feedback、最多 2 个 changed files、targetFilesPreflight、既有合同不变证明和 invalidated static gates；任何新 risk domain、范围扩大或 contract delta 都退出 fast lane。
- `integration-contract-review`：并行 slice/shared-first/integration task 已有 integration smoke 时，优先消费 smoke、consumerProof 和 shared contract freeze。
- `fix-package-recheck`：只复查原 finding、root cause、targetFiles、修复 diff 和 invalidated static gates。
- `final-delta`：代码 diff 未变且只新增 Verification/Handoff 事实时，不重复代码宽扫描。
- `reuse-existing-review`：scope fingerprint、代码、设计、任务和 accepted findings 均未变化时复用。
- `full-scan`：仅 changedFiles/contract/task/design 扩大、出现新风险域、source Review 缺 coverage 或用户明确要求完整审查时启用，并记录 invalidation reason。

## Findings-first 算法
1. 先验证审查对象、changedFilesSource、writeScopeAudit、task mapping 和 required validator evidence。
2. 根据 touched risk domains 选择最小 owner reference；未命中域不展开空 checklist。
3. 输出按 blocking/major/minor/info 排序的 findings，每项包含文件/行、影响、root cause、目标阶段和关闭条件。
4. 当前 write scope 内可闭合的代码问题生成 `recommendedFixPackage`；合同、任务、设计、范围或用户取舍问题生成 `progressionDecision.backfillPackage`。
5. 自动修复包必须先做 `targetFilesPreflight` 和 affected static gate scan；`severity=blocking` 不自动等于 `fixRouting=owner-needed`。
6. 输出 task-status update proposal、Verification gaps 和 residual risk；Review 不改业务代码、不运行 build。

## 专项检查索引
- `query-table`、`row-actions`、`master-detail` -> `front-hzero-choerodon-ui`。
- `f-layout`、`customization` -> `front-hzero-enterprise-page`；`performance` -> `front-hzero-build-deploy`。
- route/menu/runtime、mock-request、renderer、PermissionButton、Attachment、import/export、common components 分别归对应 owner。
- 页面区域、按钮语义、滚动、DataSet transport、i18n/permission、mock production boundary 等检查只在 changedFiles、acceptance 或 finding 命中时展开。

## 修复路由
- `fixRouting=direct-fix`：确定性静态小修，由主编排最小修复并 targeted recheck。
- `fixRouting=owner-needed`：需要 Implementation owner，必须携带 `targetStage=IMPLEMENTATION`。
- `design-needed/user-needed/blocked`：不得包装成代码修复包。
- 自动返工预算与是否允许第二轮由 `frontend-auto-agent` 管理；Review 只报告稳定 finding、root cause 和目标文件充分性。

## 阶段硬边界
- Review 只输出 findings 和结构化修复/回退包，不声明最终 `production-ready`。
- Final Review 只允许在规则命中时执行，不把普通 Review 扩展成重复全量审查。
- 缺上下文时输出阻塞 finding，不做全仓漫游。

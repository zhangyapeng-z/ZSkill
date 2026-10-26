# 企业前端流程控制 - Implementation

## 阅读路由
- 进入 `frontend-implementation-agent` 时读取本文件。
- 本文件只定义阶段通用执行算法；DataSet、route、mock、Attachment、import/export、PermissionButton、renderer、HZERO common components、F 型布局、master-detail、customization 和 performance 的细则按 `specialtyTriggers[]`、`ownerReferenceCapsule` 与本轮 risk domains 增量读取对应 owner reference。
- 输出形态读取 `templates/implementation-result.md`；确定性检查直接运行对应 validator，不把 validator 规则全文复制进 Implementation prompt。

## 阶段算法
1. 判定 `direct-no-task`、`repair-fast-lane` 或 Task-driven 模式。Task-driven 必须消费 canonical Task、task-status、当前 execution group/slice/integration task、dispatch validation 和有效 lease；repair-fast-lane 只复用既有 Task/Design/Contract，必须有 source finding / exact user feedback、targetFilesPreflight、最多 2 个既有文件和全部 contract delta=false。
2. 将写入权限收敛到 `allowedWriteFiles`。只读材料进入 `readOnlyRefs`；发现范围不足时输出 backfill，不自行扩展。
3. 只实现当前 Todo。并行模式一次只实现一个 slice；shared/integration 文件只由持锁任务写入。
4. 按 Design/Task 已冻结的 UI、route、service/DataSet、mock、permission、i18n 和 component contract 编码；不得重新探索或重新设计。
5. changed files 触发新的 risk domain 时，仅加载对应 owner reference 增量；已有有效 `ownerReferenceCapsule` 时复用摘要，不预载专项 skill。
6. 修改完成后执行当前 Task required 或 changed-file-triggered 的 V0 静态检查；compile/build 留给 Verification，但 Implementation 必须返回候选命令和已知执行目录。
7. 回写或提出 `task-status-updates`，输出 changedFiles、write-scope audit、validators、blockers 和下一步。

## 合同缺口
- import/path、类型、静态 API、mock handler 接线等当前 write scope 内的确定性实现错误可以直接修。
- routeOpenMode、字段规则、response shape、权限码、Target Placement、Task 写入授权或 production contract 缺失时，输出稳定 `blockerKey`、唯一 `targetStage`、`requiredBackfillFields` 和 `evidenceAlreadyChecked`；不得边写边猜。
- backfill/repair 次数只由 `frontend-auto-agent` 管理，Implementation 不递增预算、不自行回调上游 agent。
- repair-fast-lane 一旦触发 shared file、route/permission/API/DataSet/i18n/mock/production contract 变化、范围扩大或新 risk domain，立即返回 `repair-fast-lane-ineligible`，恢复标准 regular-change，不把快路径当作契约变更通道。

## 专项触发索引
- `query-table`、`row-actions`、`master-detail` -> `front-hzero-choerodon-ui`。
- `f-layout`、`customization` -> `front-hzero-enterprise-page`。
- `performance` -> `front-hzero-build-deploy`。
- `mock-request`、`renderer`、`permission-button`、`attachment`、`import-export`、`hzero-common-components` 分别归对应 owner skill。
- trigger 只决定增量 reference 路由，不自动产生领域路由 Agent 调用。

## 阶段硬边界
- 不修改 Todo 以外文件，不把 readOnlyRef 转成可写，不让一个 agent 吞掉多个并行 slice。
- 不把 generatedCandidate 升级为 confirmed，不决定 production replacement 完成，不声明 production-ready。
- 不执行 Review、Verification 或 Handoff；只提供这些阶段可消费的事实。

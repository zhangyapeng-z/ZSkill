# Frontend Write Scope Control

本文是企业前端子流程的运行时写入范围控制参考，用于判断 Implementation 是否可以修改已有前端文件、什么时候需要人工确认、以及各阶段 `edit` 权限的使用边界。它不是业务交付产物，也不写入 feature workspace。

## 阅读路由

- 写入前先阅读“核心原则”和“必须暂停并确认的情况”；形成或审查 `write-scope manifest` 时阅读“`edit` 权限边界”。

## 核心原则

- 不按“已有文件 / 新文件”决定是否人工确认，而按“是否在已确认写入范围内”决定。
- 已有前端文件只要位于已确认目标工程/模块内，并已出现在任务文件映射表，或小范围 `regular-change` direct 的 `targetFiles` 中，且类型为 `修改`，Implementation 可以直接编辑，不需要逐文件向用户确认。
- 写入范围必须来自用户目标、已确认设计、Task Breakdown 文件映射、`parallel-slices.writeFiles`、`integrationTaskId` 或 Review 返回且 `是否需要用户决策=否` 的修复包。
- 目标工程路径只有一个基线：`targetRoot` 必须是已确认的目标前端工程根，所有业务写入字段必须是相对 `targetRoot` 的规范路径。不得把 workspace-relative 的工程名前缀带入写入授权，例如 `targetRoot=/Users/david/Desktop/sdd-all/h0-demo-test` 只能配合 `packages/prm/...`，`h0-demo-test/packages/prm/...` 必须在写入前以 `implementation_dispatch_target_root_prefix_repeated` 拒绝。
- 任何阶段不得把只读参考文件、相似页面、Figma/PageSchema、工程证据或运行态 Todo 自动升级为可写文件。

## 可直接修改已有文件的条件

同时满足以下条件时，修改已有前端文件不触发额外人工确认：

- 目标前端工程、父工程 / 子模块落点和页面目录已确认。
- 文件在 `task-breakdown.md` 文件映射表中，类型为 `修改`；或小范围 `regular-change` 的 `direct-no-task` 已明确列入 `targetFiles`。
- 当前任务、slice 或 integration task 拥有该文件的写入权。
- 文件不在锁定中的 `shared-file-locks.readOnlySlices` 中。
- 修改不引入新的 API、字段、权限、路由菜单、LOV/lookup、附件 bucket、导入导出模板、production-ready / mock-demo 状态变化。
- 修改不扩大到未列入映射表的 shared service、shared constants、runtime config、mockPluginIntegration/mockHandlerRegistration、test entry 或父应用注册入口。
- 当前工作树中没有与本任务冲突且无法自动合并的外部改动。

## 必须暂停并确认的情况

命中任一情况时，不得继续直接写业务代码，必须回到 `frontend-auto-agent` / Lite 人工确认，或先回 Task Breakdown / Frontend Design 修正边界：

- 目标工程、父工程 / 子模块落点、页面目录或 feature root 不明确。
- 待写文件不在文件映射表、`targetFiles`、`parallel-slices.writeFiles` 或 `integrationTaskId` 中。
- 需要把只读参考文件改为写入文件。
- 需要修改共享文件，但没有串行 integration task 或共享文件锁未释放。
- 多个并行 slice 需要写同一文件，或 changedFiles 与 task-status 不一致。
- 修改会改变 API 契约、字段 shape、route/menu、permissionCode、i18nCode、LOV/lookup、附件、导入导出、状态流转或生产替换判断。
- 从 mock/demo 切到真实 API 时，超出 `front-hzero-mock-request` 的 production switch 合同 replacement slice 的 API/transport/field-shape/query-mode 范围。
- 当前文件存在用户或外部工具产生的相关未合并改动，且会影响本任务判断。
- 需要用户接受与原目标冲突的非默认条件性交付、临时契约或其它有条件交付。不得请求用户接受 `code-only`。仅因缺目标工程依赖或默认 mock demo 缺外部页面运行态证据而按流程输出 `conditional` 时，只记录未验证项、`manualVerificationRequired` 和前端服务提示，不触发本项人工确认。

## `edit` 权限边界

需要落盘的阶段必须显式声明 `edit: allow`，但写入范围不同：

| 阶段 | 允许写入 | 禁止写入 |
| --- | --- | --- |
| Explore / Figma Evidence | `sdd-workspace/changes/{change-id}/frontend/evidence/`、`figma-cache/` | 目标前端工程业务代码 |
| Frontend Design | `sdd-workspace/changes/{change-id}/frontend/design/` 设计契约和澄清产物；精确文件 `frontend/evidence/task-optimization-inputs.json` | 其它 `frontend/evidence/**`、目标前端工程业务代码 |
| Task Breakdown | `sdd-workspace/changes/{change-id}/frontend/tasks/`；精确文件 `frontend/evidence/optimization-execution-manifest.json`、`frontend/evidence/optimization-execution-task-validation.json` | 根级 `frontend/task-breakdown.md` / `frontend/task-status.md`、`frontend/evidence/generated/**`、目标前端工程业务代码 |
| Implementation | 已确认目标前端工程文件、`task-status.md`、实现摘要、blocker log | 映射表外文件、锁定共享文件、未确认契约文件 |
| Review | `review/`、`task-status.md`、artifact index、blocker log | 目标前端工程业务代码 |
| Verification | `verification/`、`task-status.md`、artifact index、blocker log | 目标前端工程业务代码或测试文件，除非用户明确要求并回到 Implementation |
| Handoff | `handoff/`、artifact index、production replacement checklist、task-status 汇总 | 目标前端工程业务代码 |

`edit: allow` 不是自动写入授权。每个 agent 仍必须遵守自身角色边界、文件映射表、共享文件锁和用户确认策略。

## 写入范围声明与审计

任何带 `edit: allow` 的阶段，在实际写入前必须先形成最小 `write-scope manifest`，并在阶段输出中回填 `write-scope audit`。

`write-scope manifest` 至少包含：

| 字段 | 说明 |
| --- | --- |
| stage | Explore / Figma / Frontend Design / Task Breakdown / Implementation / Review / Verification / Handoff |
| editPurpose | 本阶段写入目的：evidence / design-contract / task-status / business-code / review-report / verification-report / handoff |
| allowedArtifactRoots | 本阶段允许写入的 `sdd-workspace` 产物目录 |
| allowedBusinessWriteFiles | 仅 Implementation 可非空；来自文件映射表、`targetFiles`、`parallel-slices.writeFiles` 或 `integrationTaskId` |
| readOnlyRefs | 只读参考文件，包括相似页面、工程证据、Figma/PageSchema、review/verify 输入 |
| sharedFileLocks | 本阶段读取或持有的共享文件锁；无则写 `not-applicable` |
| targetPlacement | 新增/改造页面、子模块或微前端必填：placementType、packageDir、businessDomain、pageGroup、pageDir、routePrefix、menuGroup、packageInternalAmbiguity、parentRegistrationPath、parentSrcWritePolicy、forbiddenBusinessPaths、status |
| confirmationSource | 用户确认、设计确认、Task Breakdown、Review 修复包或 `not-required + reason` |

阶段输出中的 `write-scope audit` 至少包含：

| 字段 | 说明 |
| --- | --- |
| changedFiles | 本阶段实际新增或修改的文件 |
| changedFilesSource | 每个文件来源：`artifact-root` / `file-mapping` / `targetFiles` / `parallel-slices.writeFiles` / `integrationTaskId` / `recommendedFixPackage` |
| outOfScopeFiles | 不在允许范围内的文件；无则写 `[]` |
| businessCodeTouched | 是否修改目标前端工程业务代码 |
| targetPlacementAudit | package 落点与 changedFiles 是否一致；父工程 `src/pages/**` 是否命中 forbiddenBusinessPaths；父工程 registration/config 是否有来源 |
| policyResult | `pass / blocked / not-applicable` |
| next | `continue / return-to-implementation / return-to-task-breakdown / user-confirmation / blocked` |

非 Implementation 阶段若 `businessCodeTouched=true`，本阶段结果必须为 `blocked`，不得继续写 `production-ready`、`usable=true` 或 DONE；除非用户明确要求由主流程转入 Implementation 修复。Implementation 阶段若存在 `outOfScopeFiles`，必须回到 Task Breakdown / Integration task / 用户确认，不得把越界文件纳入已完成改动。

Frontend Design 与 Task Breakdown 的上述 evidence 路径是阶段合同内置的窄授权，不需要在工具执行后再临时扩大 write scope。Design 只拥有结构化 `task-optimization-inputs.json`；Task 只拥有 optimization manifest 和 Task gate result，不拥有 generated draft。任一阶段不得借该授权写入其它 evidence 文件。Task write-scope preflight 必须在生成任务正文前完成；缺授权时 fail-fast，不得先写根级兼容副本或完成 Task 后再补跑工具。

新增/改造页面或子模块实现时，`edit: allow` 只表示可按合同写入，并不允许任意选择落点。`placementType=new-package/existing-package` 时，业务代码 changedFiles 必须在 `packageDir` 下，并与已确认的 `businessDomain/pageGroup/pageDir/routePrefix` 一致；父工程 `src/pages/**` 默认是禁写业务路径，除非 `parentSrcWritePolicy=allowed-with-reason` 且 File Mapping 明确列入。确认 packageDir 不能替代包内业务落点确认；`packageInternalAmbiguity` 未 resolved 时不得直接写业务代码。父工程 `config/packages-config.*`、根 workspace/package 配置、micro/runtime 注册等只能作为 `parent-registration` / `integration-write` 文件写入。

Handoff 和 Lite 汇合前必须按 `schema-checklist.md` 校验 `changedFilesSource`。无法证明 changedFiles 全部来自允许范围时，交付状态只能是 `blocked` 或 `conditional`，不得写 `production-ready`；非 canonical 交付状态必须返回原 owning stage，无可运行目标时写 `blockedReason=non-runnable-target`。

## direct-no-task

小范围 `regular-change` 的 `direct-no-task` 可以不生成完整 Task Breakdown，但必须满足：

- 用户目标中已明确目标文件或主流程已给出 `targetFiles`。
- 成功标准和验证入口明确。
- 不涉及 Feature Root、页面新建/改造、多模块、多文件页面交付、共享 route/menu/i18n/API/权限/DataSet、demo-slice 或状态回写要求。
- Implementation 结果必须记录例外原因、实际 changedFiles、只读参考文件和未验证项。

一旦发现需要新增文件映射、共享文件写入、状态台账或跨阶段交付产物，应暂停直接实现并回到 Task Breakdown。

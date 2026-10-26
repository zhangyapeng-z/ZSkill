# Process Control Gate Question Templates

用于执行期、验证期和交付期需要用户确认时，统一 question 内容。Design 阶段的设计确认、契约缺口、导入/导出入口模式和 request 例外确认仍使用 `front-hzero-enterprise-design` 的 question gate 模板。

通用选项文案规则：question 的用户可见选项标题不得追加 `（推荐）`、`推荐`、`默认推荐` 或等价引导标记。若系统需要表达当前候选、排序依据或风险倾向，只能写在确认摘要、选项描述、`recommendationEvidence` / `candidateEvidence` / `排序依据` 记录中，并必须说明适用前提、选择后果和剩余风险；不得让“推荐”标记代替用户对执行范围、写入授权或交付口径的判断。

## Frontend Project Confirm
owner=`hzero-auto-agent-lite`。Explore 只返回候选工程/package 和 `requiredQuestionDomain=frontend-project`，不得调用 question 或生成 payload；`frontend-design-agent` 只消费 resolved 结果，不得代管本 gate。

适用场景：用户发出前端需求，但当前上下文无法唯一确定目标前端工程、父工程、已有 `packages/<module>` 或是否需要新建子模块。该 gate 只确认目标工程边界和候选 package 层级，不确认功能级业务目录、页面根、路由前缀、菜单分组、route/menu、详情打开方式、导入导出、mock/demo、真实 API 或设计冻结。

强制调用条件：
- `frontendRoot / parentFrontendRoot / packageDir / placementType` 无法从用户输入、已确认设计、Feature Workspace、工程证据或平台资料唯一确定。
- workspace、目录、`@` 引用或文档根下存在多个前端工程、多个父工程或多个 `packages/<module>` 候选，且继续推进会影响设计、任务拆分或写入范围。
- 用户只说“前端 / 子模块 / 微包 / 页面”但未指定目标工程路径或目标 package。
- 有参考模块、相似模块、空项目或无可采纳参考模块时都适用；参考质量不能代替目标工程选择。

不适用：
- 目标前端工程和 package 已由用户、FDS/TDS、Feature Workspace 或工程证据明确唯一确认。
- 仅缺 package 内 `businessDomain / pageRoot / pageGroup / pageDir / routePrefix / menuGroup` 等功能级落点；此时使用 `Target Placement Confirm`，不得回退到本 gate。

question：
- 标题：`前端工程`
- 问题：`请确认本轮前端变更要落在哪个前端工程或子模块边界内？`
- 覆盖范围：列出候选 `frontendRoot / parentFrontendRoot / packageDir / packageName / placementType`、来源证据和未确认前禁止写入的路径。
- 选项：
  - `使用父工程`：本轮目标是父工程自身；只确认 `frontendRoot/parentFrontendRoot`，不确认父工程内页面目录或 route/menu。
  - `使用已有子模块`：本轮目标是候选 `packages/<module>`；只确认 `packageDir/packageName`，不确认 package 内业务域、页面根或路由前缀。
  - `新建子模块`：本轮需要在已确认父工程下规划新 `packages/<module>`；只确认子模块边界，后续仍需按子模块基线和 Target Placement 完成功能级落点。
  - `补充工程路径`：暂停下游设计/写入，用户补充或修正目标前端工程路径、父工程或 package 信息。

记录要求：
- `questionGate.template=Frontend Project Confirm`。
- `frontendProjectConfirmationSource=user-question`。
- `frontendRoot / parentFrontendRoot / packageDir / packageName / placementType`：confirmed / missing / conflict / generatedCandidate。
- `selectedFrontendBoundary`：parent-frontend / existing-package / new-package / needs-path。
- `blockedBeforeConfirm`：Explore / Design / Task / Implementation / Review / Verification / Handoff / write operations。
- 本 gate resolved 后，若 package 内业务域、页面根、页面目录、route prefix 或 menu group 仍不唯一，必须另起独立 `Target Placement Confirm`；不得把本 gate 的回答升级为 `targetPlacement.status=confirmed`。
- 本 gate 不得关闭 `Route Menu Confirm`、`Open Interaction Confirm`、`Import Component Mode Confirm`、`Export Component Mode Confirm`、`Missing Contract Confirm` 或 `Frontend Design Confirm`。

## Input Root Range Confirm
适用场景：用户提供目录、workspace、`@` 引用上下文、文档根路径或其它可展开输入根，只读枚举后发现多个候选模块/功能，继续推进需要用户选择执行范围或多候选执行策略。

不适用：只发现单个候选，且候选的模块、feature root、文档状态和写入范围均已确认；或用户只要求“先分析/先看一下”，本轮不会进入设计、任务、编码、Review、Verify、Handoff、后端编码实现或任何写操作。

强制调用条件：
- `inputRootDiscovery.status=multi-candidate-needs-user`。
- 候选模块/功能超过一个，且用户未明确选择单个、多个指定项或全部。
- 多候选执行范围包含 shared-scope、全局配置、route/menu/i18n/shared service/mock registry/runtime/config 及 test entry 等潜在共享写入，需要用户确认 shared-first 或串行策略。
- 输入根无法唯一解析为真实目录、模块或 feature root，且继续推进会影响设计或写入范围。

question：
- 标题：`执行范围`
- 问题：`当前输入范围下发现多个候选模块/功能。请选择本轮要推进的范围和执行策略。`
- 选项：
  - `选择单个候选`：本轮只推进用户指定的一个模块/功能；其它候选仅保留在候选清单中，不进入设计或写操作。
  - `选择多个候选`：用户指定多个候选；默认采用 shared-scope 串行先行、feature-scope 分 lane 推进、handoff 串行收口。
  - `全部候选`：本轮覆盖全部候选；若存在 shared-scope 或写入范围冲突，必须先串行处理共享项，不能并行写入共享文件。

记录要求：
- `questionGate.template`：Input Root Range Confirm。
- `inputRootDiscovery.resolvedRoot`：真实扫描根目录。
- `inputRootDiscovery.candidateModules[]`：候选模块/功能、文档状态、完成度、关键缺口。
- `selectedRange`：single / multiple / all。
- `selectedCandidates[]`：用户选择的候选列表。
- `executionStrategy`：shared-first-lane-model / serial-only / read-only-analysis / blocked。
- `rangeConfirmationSource`：user-question。
- `blockedBeforeConfirm`：Design / Task / Implementation / Review / Verification / Handoff / backend implementation / write operations。

## Production Replacement Confirm
本模板不用于企业前端编排的首次真实 API 切换。用户在 Lite / frontend-auto 阶段提出“后端 API 好了 / 切真实 API / 接真实 service”时，不弹出替换范围选项，不创建 replacement slice；完成 Mock demo 后输出独立 `hzero-local-integration-test` 入口。

独立联调测试的开始确认应展示固定顺序：Mock 模式启动与验收、后端服务启动/可用确认、仅设置 `<MODULE>_USE_MOCK=false` 重启、观察 Network、按实际失败定向返修。首次试连不让用户选择 adapter、字段、LOV、权限、菜单、i18n、`API_HOST`、proxy 等主动替换项。

只有真实试连已经产生证据，且定向修复需要用户决定契约取舍、扩大写入范围或接受降级时，才使用对应的 `Missing Contract Confirm`、`Write Scope Confirm` 或业务决策 gate；不得重新使用本模板把多类生产改造打包确认。

记录要求：
- `mockAcceptance`：passed / failed / not-run。
- `backendIntegrationSignal`：service-started / user-confirmed-service-available / missing。
- `switchAction`：env-only / not-run。
- `sourceChangesDuringInitialSwitch`：none。
- `integrationTrialStatus`：waiting-backend-integration / real-api-trial / feedback-pending / blocked。

## Write Scope Confirm
适用场景：Implementation 或修复阶段需要写入的文件超出已确认写入范围、只读参考文件需要转为可写、共享文件锁冲突、目标落点不清、dirty/conflict 文件影响当前任务，或 Review 修复包需要扩大写入范围。

不适用：已有前端文件已位于已确认目标工程/模块内，且已列入 `task-breakdown.md` 文件映射、小范围 `regular-change` 的 `direct-no-task.targetFiles`、当前 `parallel-slices.writeFiles` 或串行 `integrationTaskId`，并且不改变契约/生产边界、不触碰非本任务持有的锁定共享文件、不存在相关外部冲突时，不需要逐文件确认。当前执行任务等于 `shared-file-locks.lockOwnerTaskId` 或 `integrationTaskId`，且待写文件全部在该串行 integration task 写入范围内时，视为持锁写入，不触发 `Write Scope Confirm`。

强制调用条件：
- `writeScopeAudit.policyResult=blocked` 且不能自动回 Task Breakdown / Integration task / Frontend Design 修正边界，需要用户选择继续方式。
- `outOfScopeFiles` 非空，且不能只通过回 Task Breakdown / Integration task 修正。
- 待写文件不在 file mapping、`targetFiles`、`parallel-slices.writeFiles` 或 `integrationTaskId`。
- 只读参考文件、相似页面、工程证据、Figma/PageSchema、review/verify 输入需要转为可写。
- 共享文件锁冲突，或需要写 route/menu/i18n/shared service/mock registry/runtime/config 及 test entry 等共享文件但当前任务不是锁持有者且没有可执行的 integration task。
- 当前文件存在用户或外部工具产生的相关 dirty/conflict，影响当前任务判断。
- Review finding 需要扩大写入范围、改变产品交互、接受降级交付或新增契约，无法作为自动代码修复包处理，只能通过 `progressionDecision.backfillPackage` 或用户确认推进。

question：
- 标题：`写入范围`
- 问题：`当前实现需要修改已确认范围之外的文件或处理写入冲突。请选择处理方式。`
- 选项：
  - `回任务调整`：回到 Task Breakdown / Integration task，补 file mapping、shared-file-locks、targetPlacement 或修复包边界后再实现。
  - `授权本次写入`：仅授权本轮列出的 out-of-scope 文件或 dirty/conflict 处理；必须记录 confirmationSource、affectedFiles、reason 和生产风险。
  - `保持范围`：不扩大写入范围，当前实现标记 partial/blocked，保留后续项。

记录要求：
- `writeScopeConfirmationSource`：user-question / task-breakdown / design-confirmation / review-fix-package / not-applicable。
- `selectedPath`：return-to-task-boundary / authorize-current-write / keep-current-scope。
- `writeScopeIssueType`：out-of-scope-file / readonly-ref-to-write / shared-file-lock-conflict / dirty-conflict / target-placement-unclear / expanded-fix-scope / other。
- `affectedFiles`：本次请求写入或冲突的文件列表。
- `allowedBusinessWriteFilesAfterConfirm`：确认后允许写入的文件；未授权写 `[]`。
- `writeScopeAudit`：policyResult / changedFilesSource / outOfScopeFiles / businessCodeTouched / next。
- `questionGate.template`：Write Scope Confirm。

## Verification Partial Notice
适用场景：Verification 为 `partial`，例如 `buildable=true`，但 `reachable` 或 `usable` 为 `unknown/false`。

本场景不调用 question，也不要求用户选择交付口径。Verification 只输出事实、未验证项、前端服务提示和建议下一阶段；是否最终交付由 Artifact 汇总为 `conditional` 或 `blocked`。

输出提示：
- `当前只证明了 buildable，页面 reachable/usable 仍未验证。已按有条件交付记录未验证项，后续请进入目标前端工程按项目约定启动服务并自测页面。`
- 默认 `demo-slice` / mock demo / `minimum-codable` 且用户未要求 production-ready、完整验收或页面运行态专项验证时，直接记录 `done=false`、未验证项、`manualVerificationRequired=true` 和补跑建议后进入 `conditional` Handoff。
- 仅因目标工程依赖未安装导致 partial 时，按 `environment-prerequisite-notice` 处理。
- 用户明确要求 production-ready、完整验收或页面运行态专项验证但目标信息不足时，不询问是否接受降级；输出 `not-run-in-verification + runtime-outside-verification + missing-browser-target/missing-runtime-input`，并回主流程安排独立 runtime acceptance 或等待用户手工证据，不得回到 Verification 启动服务，也不得把该目标包装成已接受的条件性交付。

记录要求：
- `可用性状态`：`buildable / reachable / usable` 三态。
- `是否 runnable`：只能写 `未证明 runnable`、`mock-demo runnable`、`production runnable` 或 `non-runnable`。
- `done=false`：条件性交付必须写；`code-only` 不再作为可选交付口径。

## Browser Verification Question Deprecated
Verify 阶段不再提供页面运行态专项验证选择题。默认 mock demo、普通 Verification、缺依赖或只需手工清单时，不把页面运行态放入标准命令矩阵，只输出前端服务提示：`请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面`；不得替用户选择或列出运行态启动命令。

即使用户已明确要求页面级验证，Verify 阶段也不执行页面运行态专项验证；URL/dev server、账号/租户/权限、验收流程和运行边界足够明确时，只作为独立 runtime acceptance 的输入或用户手工证据来源。信息不足时写 `not-run-in-verification + runtime-outside-verification + missing-browser-target/missing-runtime-input`，不得调用 question 让用户选择是否运行页面级验证。

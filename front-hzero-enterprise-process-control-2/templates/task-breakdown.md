# Task Breakdown Template
建议路径：`sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md`
用途：仅用于 `taskProfile=expanded / audit` 且存在 production-ready、多模块完整验收、复杂 shared-scope 或用户明确要求完整审计矩阵。普通 `taskProfile=compact` 必须使用 `task-breakdown.compact.md`。本文件保存文件映射、依赖、并行切片、执行组调度、共享文件锁、任务验收和实现交接信息；高频状态变化写入 `tasks/task-status.md`。
## Document Status
- Feature：
- Feature Root：`sdd-workspace/changes/{change-id}/`
- Frontend Root：`sdd-workspace/changes/{change-id}/frontend/`
- Frontend Index：`frontend/index.md`
- Design Source：`frontend/design/frontend-design.md`
- Contract Check：`frontend/design/contract-check.md`
- Compliance Manifest：`frontend/design/frontend-compliance-manifest.md`
- Task Status：`frontend/tasks/task-status.md`
- frontendExecutionMode：demo-slice / regular-change
- taskProfile：compact / expanded / audit
- taskCount：Task Overview 中真实任务行数量
- taskSizeHint：direct / standard / large
- taskProfileReason：none / multi-page / multi-module / master-detail-import-export-attachment / production-ready / user-audit / other + evidence
- engineeringExploration：engineeringExplorationRequired yes / no / null；engineeringExplorationLevel E1 minimal / E2 standard / E3 submodule / not-applicable
- engineeringEvidenceReuse：engineeringEvidenceSourcePath `frontend/evidence/evidence.md` / embedded-in-design / frontend-evidence-packet / missing + reason；engineeringEvidenceCoverage target-placement / directory-plan / route-menu-permission / component-import-map / enum-map / validation-handoff-candidates / similar-page-quality / mock-request-path / partial + missingItems；engineeringExplorationReusePolicy task-reuse-only / targeted-delta-allowed / blocked-by-missing-evidence / not-applicable；targetedDeltaExploreScope none / target-placement / validation-handoff-candidate / mock-request-path / component-import-map / enum-map / similar-page-quality / file-mapping / changed-files-plan；targetedDeltaExploreResult not-run / pass / partial / blocked + reason；ownerReferenceCapsule ready / reused / invalidated / missing；specialtyTriggers trigger-only / owner-loaded / not-applicable；validationHandoff intent / riskDomains / acceptanceSignals / candidateVerificationEntries / unresolvedVerificationInputs / downstreamOwners；optimizationExecutionManifest schemaVersion=1.1
- standardBaselineApplied：true / false
- designCompletenessPolicy：继承 `frontend-design.md#First-pass Completeness Policy`
- firstPassTaskBreakdownStatus：complete-skeleton / needs-task-backfill / blocked
- taskSelfCheckStatus：pass / failed + reason
- coverageConservationStatus：pass / failed + missingLedgerIds
- taskMappingConservationStatus：pass / failed + missingTaskIds
- taskCompletenessPolicy：minimum-executable / production-complete / blocked
- firstPassGapClassification：blocking / generatedCandidate / verification / mapping / not-applicable summary
- targetedTaskBackfillScope：none / design-coverage-mapping / file-mapping / changed-files-plan / acceptance-ref / execution-groups / validator-task / validation-handoff-candidate
- targetedTaskBackfillAttemptCount：0 / 1
- baselineComparisonStatus：not-needed / ready / partial / blocked / needs-confirmation
- similarPageEvidenceQualityStatus：ready / partial / missing / not-applicable
- assetBaselineStatus：active / not-applicable / blocked + reason
- assetBaselineSource：[按 `hzerojs-asset-baseline.md` 填写；不适用时写 not-applicable + reason]
- goldenBaselineStatus：confirmed / not-confirmed / rejected / conflict / not-applicable
- baselineConfirmationSource：user-explicit / owner-doc / design-confirmed-from-owner / none / not-applicable
- baselineHealthCheck：pass / partial / failed / not-run / not-applicable
- assetBaselineDecision：follow-asset-baseline / not-applicable
- questionGatePreservationStatus：required / clear / blocked
- mockOnlyDataTransport：allowed-only-when-authorized / blocked / not-applicable
- uiContractDowngradeAllowed：no / not-applicable
- cumulativeFallbackPolicy：assetBaseline / generatedCandidate / mock-demo / figma-unverified / questionGate / productionReplacement 为累积状态；不得串行短路或互相覆盖
- targetPlacementStatus：confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable
- targetPlacementEvidenceStatus：ready / partial / missing / conflict / not-applicable
- targetPlacementUserConfirmStatus：confirmed / needs-confirmation / missing / conflict / not-applicable
- componentImportMapStatus：ready / partial / missing / not-applicable
- componentApiProvenanceStatus：ready / partial / missing / conflict / not-applicable
- enumImportMapStatus：ready / partial / missing / not-applicable
- choerodonEnumTypeContractStatus：ready / partial / missing / blocked / not-applicable
- submoduleConfigValidatorPlan：required / not-applicable / missing
- mockRequestValidatorPlan：required / not-applicable / missing
- lovCandidateContractValidatorPlan：required / not-applicable / missing
- mockRequestPathContractPrecheck：pass / failed / not-applicable + reason
- c7nComponentApiValidatorPlan：required / not-applicable / missing
- hzeroChoerodonComplianceTarget：production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable
- productionComplianceGate：pass / partial / failed / not-applicable
- complianceManifestStatus：ready / partial / missing / blocked / not-applicable
- Created At：
- Last Updated At：
- Last Updated Stage：
- Can Enter Implementation：yes / no + reason
- scopePartitionStatus：ready / partial / blocked / not-applicable
- sharedContractStatus：frozen / updated-after-drift / missing / blocked / not-applicable
- integrationContractSmokeStatus：pass / failed / not-run / not-applicable + reason
- sharedContractVersion：
- sharedScopeTaskIds：[]
- featureLaneIds：[]
- parallelFeasibilityDecision：parallel-ready / shared-first-required / serial-only / blocked / not-applicable
- parallelFeasibilityMatrixStatus：ready / missing / partial / not-applicable
- serialOnlyDecisionEvidence：not-applicable / present / missing
- blockedBySharedScope：[]
- backfillKey：none / stable key
- backfillPackage.attemptCount：non-negative integer
- backfillPackage.repairDiagnosisRevision：non-negative integer
- backfillPackage.repairPlanFingerprint：stable fingerprint
- backfillPackage.repairMode：evidence-backfill / not-applicable
- backfillPackage.repairBudgetClass：execution-proof / result-contract-backfill / not-applicable
- backfillPackage.consumesRepairBudget：false
- backfillPackage.contractDiffDomains / businessChangedFiles：[]
- taskLoopGuardStatus：clear / backfill-allowed / re-diagnosis-required / terminal-gate / not-applicable
- stopCondition：none / identical-fingerprint-consumed / terminal-block-whitelist / not-applicable
规则：`Document Status` 只记录任务拆分基线需要暴露的阶段状态；字段语义、累积降级关系和消费者口径以 stage-result schema、governance note 和 owner reference 为准，不得新增无消费者的自定义状态名。Task Breakdown 默认复用 Frontend Design 工程探索证据，不重新全仓探索；仅 Task 映射/执行证明缺口允许内部 backfill。并行启动前冻结 Design/Contract 事实缺失或冲突必须返回 `design-closeout-internal-repair` 给编排器，由原 Design owner 闭合；不得由 Task 自行回写 Design 或把 `generatedCandidate/missing` 升级为 `confirmed`。内部 backfill 必须填写 `backfillKey/sourceRevisionHash/attemptCount/repairDiagnosisRevision/repairPlanFingerprint/resumeStage/invalidateStages/preserveArtifacts` 和 `stopCondition`；同一 fingerprint 只执行一次，复查失败后重新诊断并生成新 fingerprint。repair budget/timebox 不得增加 Lite 外层调用，也不得形成 terminal blocker。
## First-pass Task Self-check Policy
本节记录任务拆分不全时的强制自检方式。Task 的目标是首轮形成可执行任务骨架和完整缺口承接，不是把所有任务升级为 production-complete；轮次不是质量标准，`coverageConservationStatus` 和 `taskSelfCheckStatus` 才是放行标准。

| gapClass | 典型事项 | Task 处理 | 是否允许 runnable task |
| --- | --- | --- | --- |
| blocking | Target Placement 冲突、影响当前 Mock demo 的关键业务契约冲突、Mock 接线无法形成、写入范围不明、Design Confirm 缺失且不可豁免 | 只拆确认 / backfill / blocked task，写 `backfillKey` 和 stopCondition | no |
| generatedCandidate | route/menu、权限码、i18n key、LOV/lookup code、mock 参数、附件 bucket/template、导入导出参数 | 保留候选状态，映射到 implementation acceptance、replacement 和 validator/verification gate | yes for `minimum-codable` demo/mock；no for `production-complete` |
| verification | 页面运行态目标、账号、测试数据、Network、build 可达性 | 拆 Verification task/checklist 或 not-run 记录方式 | yes，除非 production-complete 要求该验证先闭合 |
| mapping | Design Coverage Ledger 映射、File Mapping、changedFilesPlan、acceptanceRef、execution-groups、validator task 缺失 | Task agent 当前 closeout 自动补齐；补不齐进入 targeted task backfill 或 blocked | yes only after mapping fixed |
| not-applicable | 本轮明确不涉及能力 | 写 reason，不拆任务 | not-applicable |
规则：`taskCompletenessPolicy=minimum-executable` 适用于普通 `demo-slice / regular-change`，候选/验证类缺口必须有 downstream owner，不得触发 full design refine；`taskCompletenessPolicy=production-complete` 只用于后续 production-ready 稳定化；`blocked` 只允许回补设计/契约/确认。`demo-slice` 默认 compact task mode，只保留 shared contract / route-registration、page slice、mock-request data path、integration closeout、validator-first/verification、production replacement advisory 六类交付物型任务组；advisory 只生成提示，不创建真实 API 切换实现任务。每组只写 `changedFilesPlan`、`acceptanceRef`、`validatorPlan`、`preReviewStaticGate`、`statusUpdateProposalRequired` 和 replacement/blocker，不复制完整设计/审计矩阵。所有 required ledger 行必须落到 `taskId / replacement-advisory / verification / blocker / not-applicable + reason`；所有 runnable task 必须有 `coverageRefs / changedFilesPlan / acceptanceRef / verificationPlan / validatorPlan / preReviewStaticGate / statusUpdateProposalRequired`。任一 required 行消失、只挂页面总任务或只写“按设计实现”，`coverageConservationStatus` 必须 failed。
## Design Coverage Ledger Mapping
来源：继承 `frontend/design/frontend-design.md#Design Coverage Ledger`。本节只做设计台账到任务的映射；映射细则以 `frontend-task-agent` 和 `schema-runtime-gates.md` 为准。

| ledgerId | sourceRef | requirement | requirementType | uiRegion | expectedCodeSurface | required | designStatus | taskId | implementationAcceptance | reviewEvidence | verificationEvidence | mappingStatus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DCL-001 |  |  | field / action / query / layout-container / line-filter / table-toolbar / row-action / route-behavior / save-redirect / replacement / other |  | file/component/DataSet/service/rou../dev-mock/handoff target | yes / no | confirmed / generatedCandidate / missing / conflict / blocked / not-applicable | FE-001 / backfill / replacement / no-code |  | static-code / not-run | runtime/network/manual-checklist/not-run | mapped / backfill-only / replacement-only / blocked / not-applicable |

门禁：`required=yes` 的 confirmed/generatedCandidate 行必须映射到可执行 task、backfill、replacement 或 no-code reason；可执行映射必须与任务详情 `coverageRefs` 双向引用，并有 Implementation / Review / Verification 验收证据。FDS/TDS 中每个按钮区必须守恒到独立 ledger 行：列表/明细表章节下的“列表头按钮区”映射为 `table-toolbar`，“列表行按钮区/明细表行按钮区”映射为 `row-action`；同名按钮不得合并成一个 `action` 行。FDS/TDS/Figma/用户确认中的容器承载语义必须守恒到 `layout-container` 任务映射；`组件类型=<容器类型> + 标签内组件/容器内组件=<来源子组件>` 必须拆出结构承载验收，要求来源容器存在且来源子组件位于该容器内，不能只把子组件映射到页面总任务。

## Target Placement Contract
来源：继承 `frontend/design/frontend-design.md#Target Placement Contract`。本节只记录任务继承字段和阻塞结论；落点规则以 `front-hzero-enterprise-design`、`target-placement-backfill-checklist.md`、`hzerojs-submodule-development.md`、`hzerojs-asset-baseline.md` 和 `hzerojs-submodule-runtime-gate.md` 为准。

| fieldGroup | required fields | status | source | taskImpact |
| --- | --- | --- | --- | --- |
| placement | placementType / placementIntentSource / targetProject / packageName / packageDir / businessDomain | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  |  |
| page | pageRoot / pageRootSource / pageRootDecision / pageRootEvidencePaths / pageGroup / pageDir / routePrefix / menuGroup | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  |  |
| package | packageInternalAmbiguity / packageTemplate / packageRequiredScripts / packageFilesPolicy / packageBuildArtifactPolicy / packageDependencyFieldsSource | ready / partial / missing / blocked / not-applicable |  |  |
| registration | routeConfigPath / parentRegistrationPath / registerRegex / parentSrcWritePolicy / forbiddenBusinessPaths | ready / partial / missing / blocked / not-applicable |  |  |
| confirmation | evidenceStatus / userConfirmStatus / confirmationSource | ready / partial / missing / conflict / needs-confirmation / not-applicable |  |  |

门禁：package 落点下业务文件必须在 `packageDir`；未确认、冲突或存在包内歧义时只拆确认/backfill；父工程 `src/pages/**` 仅按 `parentSrcWritePolicy` 允许 registration-only 或 confirmed exception。

## HZERO Choerodon Production Compliance
来源：继承 Production Compliance Contract、`frontend/design/frontend-compliance-manifest.md`、ownerReferenceCapsule 和已落盘 Contract Check。任务合规等级统一以 `frontend-compliance-manifest.md`、`hzero-choerodon-production-compliance-gate.md`、`generated-code-static-quality-gate.md`、企业模板和已加载 owner reference 为准；未加载专项 owner 只能作为 trigger/riskDomain，不得在 Task 阶段整包读取或当成新的事实源。

| field | value | status | source | taskImpact |
| --- | --- | --- | --- | --- |
| complianceTarget | production-compliant / production-candidate / mock-demo-compliant / non-compliant | confirmed / generatedCandidate / missing / conflict / not-applicable |  |  |
| queryMode | production-transport / mock-request / partial / blocked / not-applicable |  |  |  |
| activeParentRegistries | `config/packages-config.js` / `.hzerorc.js` / workspace / other |  |  |  |
| parentRegistrationStatus | complete / partial / missing / conflict / not-applicable |  |  |  |
| permissionCoverage | complete / partial / missing / not-applicable |  |  |  |
| i18nCoverage | complete / partial / missing / not-applicable |  |  |  |
| valueSetLovLocalOptionsPolicy | production / generatedCandidate / local-options-demo / missing / not-applicable |  |  |  |
| globalDependencyPolicy | forbidden-unless-mapped / mapped-and-approved / not-applicable |  |  |  |
| handoffLimit | production-ready / conditional / blocked |  |  |  |

## Frontend Compliance Manifest Inheritance
来源：`frontend/design/frontend-compliance-manifest.md`。Task Breakdown 必须把适用 gate 映射到具体 task、targetFiles、acceptanceImpact 和 backfill/replacement；不得只写“按规范处理”。

| manifestGateGroup | gates | sourceStatus | implementationTask | acceptanceImpact | backfillRequired |
| --- | --- | --- | --- | --- | --- |
| request-and-query | serviceRequestContract / listQueryContract / lineQueryContract / routeContextEditModeContract | pass / partial / missing / conflict / blocked / not-applicable |  | DataSet、filterBar/fuzzyQuery、routeContext、service request 验收 | yes / no |
| ui-and-field | fieldUsageMatrix / detailRegionCoverage / detailCollectionContract / drawerModalContract / styleNecessityContract | pass / partial / missing / blocked / not-applicable |  | 字段、详情区、集合、弹层、样式必要性验收 | yes / no |
| action-and-permission | masterDetailDataContract / statusActionMatrix / actionEntryMatrix / buttonSemanticMatrix / buttonPermissionContract / rowActionContract | pass / partial / missing / blocked / not-applicable |  | 主从、状态动作、按钮语义、行操作、权限、禁用原因、selection 刷新验收 | yes / no |
| platform-and-component | i18nCoverage / lovLookupBindingContract / dataSetBindingGraphContract / componentApiProvenance / choerodonEnumTypeContract / modalLifecycleContract / componentTypeContract | pass / partial / missing / blocked / not-applicable |  | i18n、LOV/lookup、DataSet bind graph、组件 API、enum/type、Modal 生命周期验收 | yes / no |
| specialized | hzeroCommonComponentContract / attachmentContract / importExportContract / generatedCodeStaticGate | pass / partial / missing / blocked / failed / not-run / not-applicable |  | 通用组件、附件、导入导出、静态质量门禁 | yes / no |

门禁：`missing/blocked/failed/unapproved/unknown` 只能拆 backfill、确认、replacement 或 blocked task；标准实现形态不得因 `partial/generatedCandidate` 降级，具体拒收项以 gateId、`frontend-validator-rule-index.md` 和 owning reference 为准。

## Choerodon Enum / Type Acceptance Task
来源：`contract-check.md#Choerodon Enum / Type Contract`。命中 Choerodon/DataSet/Table/Form/Button/Lov/Attachment、renderer/helper 或 enum-like props 时必填。

| taskId | coverageRefs | targetFiles | enumStrategy | stringFallbackPolicy | typeContract | implementationAcceptance | reviewAcceptance | verificationAcceptance | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-C7N-ENUM-TS | Contract Check: Choerodon Enum / Type Contract |  | project-enum-confirmed / asset-baseline-enum / dataSet-confirmed-string / blocked / not-applicable | DataSet confirmed-string targets / component-props-forbidden / not-applicable | ColumnProps/renderer/buttons/DataSet options type source | component enum props must use enum shape; DataSet strings require local provenance; no broad `as any/as unknown`; no raw DataSet options array without provenance | Review maps findings to this task | run c7n component API validator and record status | Todo / Blocked / Done |

## Required Validator Execution Tasks
来源：`schema-checklist.md#Validator Evidence Close Guard`、`frontend-context-handoff-control.md#Required Validator Auto Repair Matrix` 和 `frontend-validator-fix-routing.md`。本表是 Implementation / Verification 的脚本执行硬任务；validator 证据字段写入 `frontend-stage-result.validators`。required validator 默认实行 validator-first：Implementation 完成当前 slice 后、Review 前先运行或记录 `not-run + reason`；`demo-slice/regular-change` 对支持 profile 的命令追加 `--gate-profile delivery`，`production-ready/full audit` 追加 `--gate-profile strict`。blocking/failed 不得进入 Review；delivery 下仅 advisory 的 `passed=true + clean=false` 必须携带 issuesSummary 进入 Review，但不生成 repairDispatch 或等待。失败项可定位且符合 Auto Repair Matrix 时，Implementation 必须同轮修复，或由 Verification 生成带 `fixRouting` 的 repairDispatch：确定性静态小修走 direct-fix，owner-needed 才回 Implementation；不符合时回 Task Breakdown / Frontend Design / 用户确认修正 validator target、契约或写入范围。

| taskId | validator | requiredWhen | targetFiles | validatorCommand | validatorTarget | required | sourceAgent | implementationAcceptance | verificationAcceptance | rejectionCriteria | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-VALIDATE-SUBMODULE | submoduleConfigValidator | 新建/改造 `packages/<module>`、子模块 route/config/mock 注册或父工程 registry 变更 |  | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_submodule_config.py --root <frontend-root> --module <module>` | `<frontend-root>` | yes / no | frontend-implementation-agent / frontend-verify-agent | 记录 status/command/target/module/issueCount/sourceAgent | Verification 缺失、failed、not-run 或 stale 时运行或降级 | 禁止 `pass-static/partial/manual-pass/static-pass` | Todo / Blocked / Done / not-applicable |
| FE-VALIDATE-MOCK | mockRequestValidator | `queryMode=mock-request`、default mock demo、mock handler/plugin、servicePrefix 或 DataSet/service mock request |  | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_mock_request.py --root <frontend-root> --package-dir packages/<package> --mock-namespace <namespace> --mock-env-var <switchEnvVar>` | `<frontend-root>/packages/<package>` | yes / no | frontend-implementation-agent / frontend-verify-agent | 完成 mock 接线后运行；env key 从 Contract Check 读取 | 复用未过期 passed 或重跑；Network/HTTP smoke 另行记录 | failed/not-run/missing/stale 不得 mock-completed / reachable=true / usable=true | Todo / Blocked / Done / not-applicable |
| FE-VALIDATE-LOV-CANDIDATE | lovCandidateContractValidator | `frontend/design/lov-candidate-contracts.json` 存在 |  | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_lov_candidate_contract.py --manifest <feature-root>/design/lov-candidate-contracts.json` | `<feature-root>/design/lov-candidate-contracts.json` | yes / no | frontend-design-agent；下游只消费 | Design closeout 必须 passed；Task 不复制或改写 | mock-request 与 contract-fidelity 必须附带同一 manifest | 禁止 composite status、question gate、平台全局 LOV 和 Implementation N/A | Todo / Blocked / Done / not-applicable |
| FE-VALIDATE-LOCAL-IMPORT | localImportPathValidator | 新增或修改 `src/**/*.{ts,tsx,js,jsx}` import |  | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_local_import_paths.py --root <frontend-root-or-packageDir> [--source-root src] [--source-alias <confirmed-alias>]` | `<frontend-root-or-packageDir>` | yes / no | frontend-implementation-agent / frontend-verify-agent | `--source-alias` 仅来自 `sourceRoot/sourceAlias/aliasEvidence`；无 alias 时省略 | 复用未过期 passed 或重跑 | unresolved 必须回 Implementation；delivery 下可解析 parent-relative-with-alias 为 advisory | Todo / Blocked / Done / not-applicable |
| FE-VALIDATE-C7N | c7nComponentApiValidator | HZERO + Choerodon 页面、DataSet/Form/Table、Lov/Attachment、Modal、Upload、行操作或 enum-like props |  | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_c7n_component_api_ast_grep.py --root <frontend-root-or-packageDir>` | `<frontend-root-or-packageDir>` | yes / no | frontend-implementation-agent / frontend-verify-agent | 可先跑并修复静态 finding | 必须记录完整 validator 证据并同步 affectedStaticGateScan | build/typecheck 通过不能覆盖 failed；not-run 时保持 `conditional` 并写未验证项 | Todo / Blocked / Done / not-applicable |
| FE-VALIDATE-IMPORT-EXPORT | importExportPermissionsValidator | Design/Task 已声明 Import、ExcelExportPro、导入/导出入口或 import-export risk domain |  | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzero_import_export_permissions.py --root <frontend-root-or-packageDir>` | `<frontend-root-or-packageDir>` | yes / no | frontend-implementation-agent / frontend-verify-agent | 只在命中导入导出入口的 task/slice 后运行 | 复用同 scope passed；failed 只窄修入口/权限 prop | 普通 TSX 不得触发；不得用 Review 人工判断代替 | Todo / Blocked / Done / not-applicable |
| FE-VALIDATE-CONTRACT-FIDELITY | contractFidelityValidator | 详情/主从、保存后跳转、状态动作、权限承载、generatedCandidate/对象 LOV、只读动作、导入导出、mock ID/enum 或附件 carrier |  | 并行 slice 先写 `<feature-root>/evidence/contract-fidelity/slices/<sliceId>.json`，primary 运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/merge_frontend_contract_fidelity.py --fragment ... --out <feature-root>/evidence/contract-fidelity.json --result-out <feature-root>/evidence/contract-fidelity-merge.json`，再运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_contract_fidelity.py --manifest <feature-root>/evidence/contract-fidelity.json [--require-master-detail] [--lov-candidate-manifest <feature-root>/design/lov-candidate-contracts.json]` | slice fragments + `<feature-root>/evidence/contract-fidelity.json` | yes / no | frontend-implementation-agent 写独占 fragment；primary 只做确定性 merge | schemaVersion=1.1 六项 deterministicChecks 全部声明并通过；LOV manifest 存在时 generatedCandidates/lovObjectBindings 必须 required | Review 只消费结果和抽查 delta | 禁止并行 slice/Design 共写 canonical manifest；不保留 schema 1.0 canonical 或 LOV self-declared N/A | Todo / Blocked / Done / not-applicable |
## Similar Page Evidence Quality
来源：继承 `frontend/evidence/evidence.md#Similar Page Evidence Quality` 和 Frontend Design `baselineComparison`。详细采纳/拒绝规则以 `Reference Module Quality Gate`、`frontend-context-handoff-control.md` 和专项 owner reference 为准。

| path | evidenceQuality | adoptedPatternItems | rejectedPatternItems | taskImpact | source |
| --- | --- | --- | --- | --- | --- |
| none | not-applicable | [] | [] | not-applicable | not-applicable |

## File Mapping
| filePath | action | module | responsibility | placementScope | placementPolicy | designSource | sharedRisk | writePolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 新建 / 修改 / 只读参考 / 验证产物 |  | page / component / dataset / service / route / i18n / mock / style / test / docs(artifact-or-business-doc-only) | package / parent-registration / parent-src / artifact / read-only | allowed / forbidden / registration-only / allowed-with-reason | FDS/TDS/FDS-UI/UI Contract/P-* | none / shared / integration-only | slice-write / integration-write / read-only |

规则：
- Implementation 不得写入 File Mapping 之外的文件；新发现必须写入的文件，应先回到 Task Breakdown 更新 File Mapping，再进入实现。共享文件必须进入 `shared-file-locks`，并由串行 integration task 写入。
- File Mapping 必须与 Target Placement Contract 一致；package 落点下的业务文件不能落到父工程 `src/pages/**`。`docs` / `验证产物` 只能用于 `placementScope=artifact/read-only`，或用户明确要求写入目标工程且与业务运行交付相关的正式文档；AI 流程自查、Review、Verify、Handoff、blocker 或 design-deviation 记录不得用 `docs`、`验证产物`、`package` 或 `parent-src` 包装进目标工程。
- File Mapping 命中 `packages/<module>/src/routes/**` 时，必须反向引用 Target Placement Contract 中的 `pageRootEvidencePaths`；新建/生成页面或无参考基线下不得把 `src/routes/**` 作为 package 业务文件映射。缺证据时该行只能标记 `placementPolicy=forbidden` 或拆 backfill，不得进入实现写入范围。
- `generatedCodeStaticGate`、Implementation 自查、`design-deviation-report`、`unverified-items`、blocker log、Review/Verification/Handoff 摘要只能作为 `task-status.md`、`frontend/index.md`、`review/`、`verification/`、`handoff/` 或阶段结果中的证据；不得在目标前端工程 `src/**`、`packages/**/src/**`、页面目录或 route 目录下生成 `__implementation-self-check__.md`、`__review*.md`、`__verify*.md`、`design-deviation*.md`、`unverified*.md` 等流程记录文件。

## Runnable Task Execution Contract
每个 runnable implementation task 必须包含以下执行合同；backfill / confirmation / blocked task 不适用时写 `not-applicable + reason`，不得留空。

| taskId | executionGroupId | dispatchMode | sliceId | integrationTaskId | acceptanceRef | changedFilesPlan | sharedFilesPolicy | verificationPlan | statusUpdateProposalRequired | blockedImpact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-001 | G1 / not-applicable | serial-task / parallel-slice / serial-integration / not-applicable | not-applicable | not-applicable | task-breakdown.md#FE-001 | [] | none / read-only / integration-write |  | yes | none |

每个 runnable task 的步骤固定为：
1. **确认上下文与复用点**：列出必须阅读的设计摘录、目标文件、相似实现、owner skill 规则、复用组件/DataSet/service/helper，以及禁止重复实现的能力；按钮任务必须列出 `sourceRegion/uiArea/visibleWhen/enabledWhen/disabledReasonSource/selectionReactivePolicy`。
2. **准备或补充失败验证 / 基线验证**：列出实现前可运行的验证命令、静态扫描或手工基线；不适用时写 reason。
3. **实现当前任务**：路径统一为相对绝对 `targetRoot` 的 frontend-root-relative；只写 `changedFilesPlan`、`parallel-slices.writeFiles` 或当前 `integrationTaskId` 持有文件，禁止重复目标工程目录名；shared setup 输出写入 `prerequisiteOutputs/sharedPrerequisiteFiles/integrationWriteFiles`，不得混入普通 feature slice `writeFiles`。
4. **复跑验证与静态自查**：列出任务级验证、owner validator、affected static gate scan 和未运行记录方式。
5. **状态回写建议**：必须输出 `task-status-updates` proposal，包含 `taskId`、`sliceId`、`integrationTaskId`、`changedFiles`、`changedFilesSource`、`sharedFilesTouched`、`blockersOpened`、`resolvedBlockers`、`evidence` 和 `next`。

规则：
- `changedFilesPlan` 中每个文件必须能反查 File Mapping；共享文件只能由 integration task 写入。
- 缺少 `acceptanceRef`、`changedFilesPlan`、验证动作、拒收条件或状态回写建议字段时，`Can Enter Implementation` 必须为 `no + task-not-executable`。
- Implementation 新发现必须写入计划外文件时，必须先回 Task Breakdown 更新 File Mapping、changedFilesPlan 和依赖/并行边界；不得在 Implementation 中自行扩大范围。

## Execution Groups
存在多模块、多页面、多能力切片、`parallel-slices` 或 shared-scope/integration 收口时必填；不适用写 `not-applicable + reason`。

| executionGroupId | groupType | sliceIds | taskIds | prerequisites | sharedPrerequisiteFiles | integrationWriteFiles | contractFidelityRequired | dispatchMode | requiredOwningAgentDispatchCount | expectedDelegatedAgent | serialFallbackPolicy | completionGate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| G1 | serial / parallel / integration | [] | [] | none | [] | [] | yes / no | serial-task / parallel-slice / serial-integration | 0 | frontend-implementation-agent / not-applicable | blocked / serial-fallback-with-reason / not-applicable |  |

规则：
- `groupType=parallel` 且 `sliceIds` 中有 2 个及以上 `canRunInParallel=yes` slice 时，`dispatchMode=parallel-slice`，`requiredOwningAgentDispatchCount` 必须等于可并行 slice 数量，`expectedDelegatedAgent=frontend-implementation-agent`。
- parallel execution group 的每个 slice 必须由 `frontend-auto-agent` 单独创建当前 Todo并直调一个 `frontend-implementation-agent`。运行期 `serial-fallback` 仍逐 slice 直调 owning Agent，不因调度降级增加 General 中转；Task Breakdown 不得把多个 slice 合并成一个 Implementation 当前 Todo。
- `frontend-general-agent` 不参与正常并行 fan-out、serial fallback、dispatch plan/lease 或同组修复；这些均由 primary 逐 slice 直调 owning Agent。
- 设计/Task 时已知无法并行，不得标 `parallel-ready`，必须写 `groupType=serial` 或 `serialFallbackPolicy=serial-fallback-with-reason` 并记录原因。Task 冻结后才出现的运行期限制只改 dispatch plan/lease，不回写 Task DAG。
- shared-scope、route/menu/i18n/mock registry/runtime/config 及 test entry、最终验证和 Handoff 收口必须是 `groupType=integration` 或串行 task，并通过 `sharedPrerequisiteFiles` / `integrationWriteFiles` 暴露给后续组授权检查。

## Action / Button / Route Acceptance
来源：继承 UI Contract、Action Entry Matrix、Button Semantic Matrix 和 Route Context / Edit Mode Contract；缺失适用项时不得进入 Implementation。

| matrix | required fields | blocking rule |
| --- | --- | --- |
| Action Entry Matrix | actionId / label / actionExistsSource / statusActionRef / chosenEntryLocation / uiArea / pageModes / entryStatus / targetFiles / acceptanceImpact | 动作存在不等于 Header 可见；`generatedCandidate/needs-confirmation/missing/conflict` 的业务状态动作只能拆确认、隐藏或 replacement |
| Button Semantic Matrix | buttonId / label / location / uiArea / semanticKind / action / navigationTarget / businessMutation / statusActionRef / targetFiles / acceptanceImpact | `page-toolbar` 对应 Header children，`table-toolbar` 对应 Table buttons；同文案不同语义必须拆任务 |
| Route Context / Edit Mode | pageMode / routePattern / idSource / editableAuthority / generatedFieldsVisibility / saveRedirectPolicy / acceptanceImpact | `/create` 为新建默认；`editableAuthority` 不得写 DataSet `editFlag`；后端生成字段的显隐和提交策略按 Field Visibility / Editability Matrix 合同逐字段验收 |
| Basic Info Form Layout Contract | formRegion / containerWidthPolicy / columns / columnsSource / responsiveColumns / labelLayout / labelWidthPolicy / layoutAdjustmentReason / field colSpan / valueOverflowPolicy / acceptanceImpact | 仅当基础信息 / HeaderForm 已确认、输入只给出高层结构且缺布局细节、并且原型/Figma、用户/项目基线未覆盖时，继承 `default-form-layout-by-design-rule`：`content-available`、`xs=1, sm=1, md=2, lg=3`、`lg=3` 列、`labelWidth=120`、横向标签；短字段初始 `colSpan=1`、长值 Lov 可优先评估两列、长字段优先跨当前整行。可根据可用宽度、字段密度、标签/值长度或字段语义记录 `layoutAdjustmentReason` 后调整 `3/2/1` 列、labelWidth、跨度或断点，不需外部布局来源，也不设字段数自动阈值。审计/后端生成字段的显隐、只读和提交策略另按 Field Visibility / Editability Matrix 验收，不属于布局默认。固定 max-width、居中仍需来源；字段顺序和卡片化由独立合同验收 |
| List Columns / Operation Column | `widthPolicy` / fixedWidth sourceRef / minWidth or flex carrier / operationColumnLock / operationColumnWidth | 普通业务列无 `widthPolicy` / `columnWidthSource` 不得写固定 `width`；至少一个主文本列按 UI Contract 使用 `minWidth` / flex / project auto-fit；行操作列必须最后一列并使用 `ColumnLock.right` 或 confirmed 等价 enum，禁止 `fixed`、`lock: true`、`lock: 'right'` 或只配 `width` |
详细运行期消费与拒收以 UI runtime gate、permission-button、renderer 和 Choerodon row-actions scenario reference 为准。
## Dependency Graph
```text
FE-001 -> FE-002
FE-002 -> FE-INT-001
```

## Scope Partition
多模块、多 feature、多 package 或任何计划并行实现的任务必须填写；单 feature 且无共享写入时写 `not-applicable + reason`。

| scopeId | scopeType | ownerTaskId | files | contractKeys | status | reason |
| --- | --- | --- | --- | --- | --- | --- |
| SHARED-001 | shared-scope / feature-scope / handoff-scope | FE-INT-001 |  | packageName/routePrefix/menuGroup/permissionPrefix/i18nPrefix/mockMountPath | ready / partial / blocked / not-applicable |  |

规则：
- `shared-scope` 包含父工程配置、根 workspace/package/lockfile、packages 注册、route/microConfig 聚合、全局权限/i18n、公共组件、公共 service/helper、公共 mock/plugin 聚合入口或同一共享文件。
- `feature-scope` 只能包含自身模块/feature 内部页面、DataSet、service、model、mock handler、局部样式、局部组件和局部 i18n。
- `handoff-scope` 只能包含 Review/Verify/Handoff 产物、artifact index、production replacement checklist 和集成验证记录。
- `shared-scope` 必须由串行 integration task 持有；不得分配给普通并行 feature lane。

## Parallel Feasibility Matrix
存在多页面、多模块、多能力切片、列表/详情/明细/附件导入导出等可拆能力，或存在 `shared-scope-present` 时必填；完全单文件小修且无并行候选时写 `not-applicable + reason`。
| candidateId | candidateScope | candidateTaskIds | initialRisk | proposedLaneType | writeFiles | readOnlySharedFiles | integrationTaskId | canRunInParallel | rejectionReason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAND-001 | list / detail / line-tab / attachment-imex / page / module / shared-setup / integration / other | [] | shared-scope-present / dependency / contract-missing / none | shared-serial / feature-parallel / integration-serial / blocked | [] | [] | FE-INT-001 / not-applicable | yes / no | none / reason |
规则：`shared-scope-present` 不得直接推出 `serial-only`；能移入 integration task 的共享写入不得阻止 feature lane 并发；`rejectionReason` 必须具体到文件、契约、依赖、工具限制或用户选择；两个及以上 `feature-parallel` candidate 可并发时，后续 `Parallel Slices` 和 `Execution Groups` 必须生成 `dispatchMode=parallel-slice`，除非另有 `serialFallbackReason`。

## Serial Only Decision Evidence
仅当 `parallelFeasibilityDecision=serial-only` 时必填；否则写 `not-applicable + reason`。
| reasonId | attemptedSharedFirstStep | candidateIds | blockingCause | evidence | fallback |
| --- | --- | --- | --- | --- | --- |
| SO-001 | shared serial patch / shared contract freeze / candidate lane split / integration merge | [] | same-file-write / hard-order-dependency / unresolved-contract / unmovable-shared-write / tool-limit / user-selected-serial / other | file paths / contract keys / task ids / session note | serial-task / blocked / user-confirmation |
规则：`serial-only` 必须证明已评估 shared-first lane model；缺少本节或只有笼统原因时，Execution gate 必须 failed。

## Shared Contract Freeze
存在 shared-scope 或多个 feature lane 时必须填写；无 shared-scope 时写 `not-applicable + reason`。

| field | value | sourceTaskId | status | consumerLaneIds |
| --- | --- | --- | --- | --- |
| sharedContractVersion |  | FE-INT-001 | frozen / updated-after-drift / missing / blocked / not-applicable |  |
| packageName |  |  |  |  |
| packageDir |  |  |  |  |
| routePrefix |  |  |  |  |
| menuGroup |  |  |  |  |
| permissionPrefix |  |  |  |  |
| i18nPrefix |  |  |  |  |
| mockMountPath |  |  |  |  |
| parentRegistrationFiles |  |  |  |  |
| allowedSharedFiles |  |  |  |  |

规则：
- `sharedContractStatus=frozen/updated-after-drift` 前，依赖该 contract 的 feature lane 不得进入并行 Implementation。
- feature lane 只能消费本表冻结的 contract，不得新增 shared-scope 写入。
- Review/Verify 发现父工程注册遗漏、mock plugin 聚合遗漏、全局权限/i18n namespace 冲突或公共配置缺口时，必须新增 `shared-scope finding`，暂停受影响 lane，回到串行 integration task 更新本表。

## Parallel Slices
| sliceId | laneType | module/page | taskIds | writeFiles | evidenceWriteFiles | prerequisiteOutputs | sharedFiles | prerequisites | canRunInParallel | sharedContractVersion | integrationTaskId | verificationScope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| not-applicable | shared-serial / feature-parallel / handoff-serial / not-applicable |  |  |  | [] |  |  |  | no |  | not-applicable |  |

规则：
- `laneType=feature-parallel` 的 slice 不得写 sharedFiles；sharedFiles 只能只读，或由 `integrationTaskId` 持有。
- `laneType=shared-serial` 必须先于依赖它的 feature lane 完成，并负责生成或更新 shared contract。
- `canRunInParallel=yes` 只允许用于 writeFiles 不交叉、sharedContractVersion 已冻结、且 sharedFiles 均为 read-only 的 feature lane。
- feature lane 发现新增 shared-scope 需求时，必须把当前 slice 标记为 blocked-by-shared-scope，并回到 Shared Contract Freeze / Integration task。
- 详情页可候选拆为 `detail-contract` 与 `detail-ui`，但不是默认拆分。只有 DataSet/service、页面级 mock fixture/handler、LOV contract fragment 与 response shape 已冻结，且两个 lane 的 `writeFiles`、`evidenceWriteFiles`、可写目录完全不重叠时才允许。`detail-contract` 持有上述数据/契约文件，并把 contract reference、fixture reference、字段 shape 写入 `prerequisiteOutputs`；`detail-ui` 只能持有 Form、LineTable、Attachment、layout、交互组件和局部样式，且必须把 `detail-contract` 作为 prerequisite。
- shared mock plugin registration、shared mock store、跨页面 response schema 与 parent config 固定归 integration task；页面私有且文件不重叠的 handler/fixture 可以归 feature lane。若 contract 无法先冻结、任一文件重叠，或 UI 需要反向定义同一 DataSet/service/mock 文件，则必须合并为同一 owning slice 或串行，不得以伪并行增加 dispatch 数。

## Production Replacement Advisory
存在 `backendApiReadiness`、Mock demo 或 production replacement checklist pending 项时必须填写提示；该表不生成当前 execution slice。无提示项写 `not-applicable + reason`。

| advisoryId | readinessStatus | apiScope | pendingItems | currentQueryMode | initialIntegrationAction | sourceChangesAllowed | nextStage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FE-PR-ADVISORY | closed / partial / missing / conflict / not-applicable | list / detail / write / options | API / field-shape / mock-runtime-path / platform-config | mock-request | Mock acceptance -> backend signal -> `<MODULE>_USE_MOCK=false` | none | independent-local-integration-test |

规则：
- `backendApiReadiness.status=closed + implementationStatus=completed + runtimeAvailability=verified` 且存在 pending replacement items 时，只更新联调测试 advisory；不得创建或复用 production replacement slice。当前 Task 仍完成 Mock demo，nextStage 指向独立本地联调测试。
- `backendApiReadiness.status=partial` 时，记录 `implementation-complete-runtime-unverified` 或逐 API 缺口；不得在企业前端 Task 中拆 list/detail/write/options 真实 replacement slice。
- advisory 必须列出未覆盖 API、平台配置提示和后续验证点；`dev-mock/**` 源码保留不属于残留成功路径。
- 任一当前 Mock demo 必需契约缺失时，仍按当前 Task gate 修复；只影响真实 API 的缺口不创建 Implementation 任务。
- 初始集成动作固定 env-only，应用源码变更为 none。后续只有实际失败证据才能生成定向修复任务。

## Shared File Locks
| sharedFile | lockHolderTaskId | allowedWriteStage | releaseCondition | blockedSliceIds | sharedContractField | notes |
| --- | --- | --- | --- | --- | --- | --- |
|  | FE-INT-001 | Shared Serial / Integration / Finalization | all dependent slices completed |  | parentRegistrationFiles / allowedSharedFiles |  |

## Shared Drift Findings
Review、Verify 或并行实现中发现遗漏公共区域改造点时必须填写；无漂移写 `none`。

| findingId | sourceStage | sharedScopeImpact | affectedLaneIds | requiredSerialTaskId | sharedContractUpdate | status |
| --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable |  | not-applicable | no | not-applicable |

规则：
- `status=open` 时，受影响 feature lane 必须暂停；不得继续并行实现或验证。
- `requiredSerialTaskId` 完成并更新 `sharedContractVersion` 后，受影响 lane 才能恢复。
- 不允许某个 feature lane 顺手修改公共配置来关闭 drift finding。

## No-Reference Default Slices
当 `assetBaselineStatus=active`、`assetBaselineSource=hzerojs-asset-baseline` 或 `assetBaselineDecision=follow-asset-baseline` 时，Task Breakdown 默认至少拆出以下切片；只有项目证据或用户确认允许合并时，才可合并，并必须写 reason、影响和 Review 验收。

| sliceId | goal | typicalFiles | runnableCondition |
| --- | --- | --- | --- |
| FE-SCAFFOLD | 页面域骨架、Target Placement、route/menu/active registry 集成 | `src/pages/<PageGroup>/**`、route config、registration files | Target Placement confirmed |
| FE-CONSTANTS | constants、权限码、lov/lookup、状态动作矩阵、i18n 候选 | `constants.ts`、`platform-locale-keys.json` / Compliance Manifest | 字段/按钮来源明确，平台 key 状态可追踪 |
| FE-SERVICE-MOCK | service adapter、mock prefix、runtime store、mock handler、mock plugin 和父工程注册闭环 | `src/services/**`、`src/utils/servicePrefix.ts`、`dev-mock/<module>-dev-mock.js`、`dev-mock/<module>-dev-mock-plugin.js`、父工程 `config/config.ts` 或父工程聚合 plugin | queryMode/tenantContext/mock auth 明确，且 `parentMockPluginRegistrationEvidence / mockPluginTemplateCompliance / mockPluginSelfCheck / mockPrefixOriginPolicy` 可验收 |
| FE-LIST | queryDS、列表页、表格列、查询行为 | `stores/queryDS.ts`、`List/index.tsx` | List Contract ready |
| FE-DETAIL | detailDS、详情页、route context、头行保存 | `stores/detailDS.ts`、`Detail/index.tsx` | Detail Contract ready |
| FE-LINE | lineQueryDS、LineTable、主从行操作 | `stores/lineQueryDS.ts`、`components/LineTable.tsx` | Master Detail Contract ready |
| FE-ATTACHMENT-IMEX | 附件 wrapper、导入导出标准入口或有 `wrapperJustification` 的动作组件 | `components/*Attachment.tsx`、按需 `ImportExportActions.tsx` | Attachment/ImportExport contract 至少 partial；单个导入/导出默认直渲染标准组件，不拆薄封装 |
| FE-INTEGRATION | shared route/menu/i18n/mock registration、静态扫描和 replacement 收口 | shared files + artifact references | 前置 slices done |

规则：无参考基线下不得把 `queryDS/detailDS/lineDS` 合并成单个全局 DS；required 附件、导入、导出必须有独立文件边界；`FE-SERVICE-MOCK`、`FE-LINE`、`FE-ATTACHMENT-IMEX` 的细则分别回 mock-request、master-detail scenario、attachment/import-export owner reference。HZERO 业务 i18n 只允许任务规划 `platform-locale-keys.json` / Compliance Manifest pending entries；`src/locales/**`、`src/locale/**`、`locales/zh_CN/**` 不得进入 File Mapping / changedFilesPlan / shared-file-locks，validator 必须报告 `task_execution_local_locale_forbidden`。

## Task Overview
| taskId | type | priority | sliceId | integrationTaskId | title | lane | status | acceptanceRef | dependencies | blockers | reviewStatus | verificationStatus | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-001 | story/task/bug/spike | P1 | not-applicable | not-applicable |  | Backlog | pending | task-breakdown.md#FE-001 | [] | [] | not-run | not-run | Ready |

计数规则：`taskCount` 必须等于本表真实任务行数量且至少为 1，taskId 不得重复。任务数量只设上限，不设下限；任务按独立写入所有权、真实依赖和可独立验收结果拆分，不改变并发计划。不得为了制造并发而机械拆任务，也不得因任务数收敛删除 `parallelFeasibilityDecision`、`parallel-slices`、`execution-groups`、`sliceId` 或 shared/integration lane。`taskSizeHint=direct` 仅用于小范围 `regular-change + taskProfile=compact`，最多 3 项；`taskProfile=compact + taskSizeHint=standard` 最多 7 项；`taskProfile=expanded + taskSizeHint=large` 最多 12 项且必须写非空 `taskProfileReason`；`taskProfile=audit + taskSizeHint=large` 用于用户明确完整审计或高风险交付并必须写原因。超过上限必须回 Task Breakdown 合并或切片，不得用固定 FE 编号补足任务数。

说明：AI 驱动任务不维护 `owner` 字段；外部依赖归属只写入 Blockers 的 `externalOwner`，例如 user / backend / platform / main-flow。

## Task Details
### FE-001 - <title>

| fieldGroup | required fields |
| --- | --- |
| task identity | type / priority / sliceId / integrationTaskId / relatedFiles / dependencies / blockers / designSource |
| coverage | coverageRefs / blockedDesignCoverageItems / contractMetadata / pendingReplacementItems |
| data contract | queryMode / mockResponseValuePolicy / mockValueSourceLedger / tenantContext / backendApiReadiness / productionReplacementTrigger |
| route and tab | routeOpenMode / parentTabKey / targetDetailPath / navigationApi / tabIdentityPolicy / keyPathRelation / recordIdSource / pageModeSource / reusableTabContextPolicy / tabTitle / tabTitlePolicy / runtimeTitleSource / titleFormat / displayField / technicalIdField / tabTitleFallback / routeMode / dws / queryStateKey / routeContext / editableAuthority / pageMode |
| mock request | parentMockPluginRegistrationEvidence / mockPluginTemplateCompliance / mockPluginSelfCheck / mockPrefixOriginPolicy |
| compliance state | productionComplianceTarget / parentRegistrationStatus / permissionCoverage / i18nCoverage / globalDependencyPolicy / handoffLimit / complianceManifestGates / complianceGateIds |
| UI and static gates | actionEntryMatrix / buttonSemanticMatrix / fieldEditabilitySource / enumProvenance / typescriptRenderContract / contractFidelityCheck / mustPassBeforeMockCompleted / staticRejectionScan |
| placement and baseline | targetPlacement / similarPageEvidenceQuality / emptyProjectBaseline |

`coverageRefs` 可执行任务不得为空；`queryMode=local-filter/inline mock` 只能触发 cleanup/rework blocker；C7N / Choerodon 组件、DataSet 页面、组件 wrapper 或相似页面迁移必须包含 `GCSQ-COMPONENT-API-001` 和 `c7nComponentApiAstGrepScan` 计划。

#### Implementation Requirements
- 覆盖 `coverageRefs` 中每个 required ledgerId 的实现要求；不得只写“按设计实现”。
#### Contract Acceptance
- 字段/API/权限/路由/i18n/LOV/附件/导入导出/mock-store/queryMode 验收：
- 覆盖 `coverageRefs` 中每个 required ledgerId 的契约验收；不适用时写 `not-applicable + reason`，不能留空。
- 逐项继承 list/detail/action/button/field/compone../dev-mock/static gate，并把当前任务命中的 gateId、owner reference、required evidence、replacement item 和 blocked reason 写入验收。
- `contractFidelityCheck` 必须反查 changed files 与 Field Usage / Status Action / Action Entry / Button Semantic 矩阵；存在 missing、renamed、forbiddenAlias、copy/status/rowAction drift 时，本任务不得标为完成。
- mock、组件 API、类型、附件、导入导出和 HZEROJS 子模块 runtime 细则回 owning reference；本节只保留当前 task 的可验证断言。

#### UI Acceptance
- UI Contract、字段顺序、组件选型、Modal/Drawer/Overlay、manual checklist 验收：
- 覆盖 `coverageRefs` 中每个 UI / interaction / region 类 required ledgerId 的 UI 验收；不适用时写 `not-applicable + reason`。
- 可见区域验收必须继承 UI Contract / Compliance Manifest 的 `expectedSurface / forbiddenSurface / requiredVisibleByDefault`，并写成可检查断言。详情/主从页默认要求基本信息 Form 在 `Content` 内默认可见且不进入 `Tabs.TabPane`；明细 Tab 只承载明细/附件等子区域。基础信息 / HeaderForm 命中 `Basic Info Form Layout Contract` 且满足默认布局的统一触发条件时，UI Acceptance 必须验收 `containerWidthPolicy=content-available`、`xs=1, sm=1, md=2, lg=3`、`lg=3` 列、`labelWidth=120`、横向标签和字段 `colSpan/valueOverflowPolicy`，或验收合理的 `layoutAdjustmentReason`。审计/后端生成字段另按 Field Visibility / Editability Matrix 的显隐、只读和 `submitPolicy` 写成可检查断言。调整列数、labelWidth、跨度或断点不因缺外部设计来源拒收，也不使用字段数自动阈值；固定 max-width、居中仍需来源。字段顺序、卡片化按独立合同验收。若设计确认例外，任务必须写明来源和负向验收。
- 详细 UI 运行期规则统一以 `frontend-ui-runtime-gates.md` 为准。此处至少要把当前任务命中的 `pageMode / fieldVisibility / fieldEditability / emptyDerivedFieldUx / editableAuthority / componentApiProvenance / modalLifecycleContract / enumProvenance / modal-drawer choice / HZERO page layout / scroll boundary / manual checklist` 映射成明确验收项。

#### Verification Acceptance
- buildable / reachable / usable / Network / runtime evidence / manual checklist / not-run reason：
- 覆盖 `coverageRefs` 中每个 required ledgerId 的验证证据或未验证阻塞原因。

#### Rejection Criteria
- `coverageRefs` 为空、与 Design Coverage Ledger Mapping 不一致，或任一 required ledgerId 未在四类验收中形成可验证断言。
- Task Acceptance Scan、`contractFidelityCheck`、`detailRegionCoverage`、`mustPassBeforeMockCompleted` 或 required owner validator 未执行、未记录、failed/stale，或被包装成 `mock-completed` / `usable=true` / `Implementation Complete`。
- required UI 区域未声明或未验证 `expectedSurface / forbiddenSurface / requiredVisibleByDefault`，实现把区域落到 `forbiddenSurface`，或为闭合某个缺口新增无来源容器/Tab/Toolbar/Wrapper。
- mock-request、placement、route/editMode、field visibility、component API、enum/type、attachment/import-export、local-filter、dependency drift 等命中 owner gate 的问题，按对应 gateId 严重级别拒收。
- 内部 HZERO route / hash route 使用 `window.open` 打开浏览器新标签页，除非设计明确确认为 `browser-new-tab` 且说明不是 HZERO 应用内 Tab。

#### Expected Status Update
- laneFrom / laneTo / statusFrom / statusTo / requiredEvidence：

## Rework / Repair Rules
- 小范围修复回原 task 并记录 blocker / changedFiles / resolvedBlockers；跨文件但仍在冻结合同内的问题新增 `FE-FIX-*` / `FE-REV-*`。Task 验收映射缺口在 Task Breakdown 内修正；Task 发生在并行启动前，frozen UI/业务契约缺失或冲突时返回 `design-closeout-internal-repair` 给编排器，由原 Design owner 同一 run 闭合，Task 不直接回写 Design。

## Task Breakdown Gate
| gate | result | evidence | requiredAction |
| --- | --- | --- | --- |
| Readiness | pass / failed | Design Confirm、Contract Check、Target Placement、关键 UI/API/route/mock/replacement 机器合同足以拆 runnable task | failed 时返回 `design-closeout-internal-repair` 给编排器，不拆补设计/确认 task，不触发用户授权 |
| Mapping | pass / failed | File Mapping、changedFilesPlan、machine Design Coverage Ledger mapping、coverageRefs、acceptanceRef 守恒 | failed 时自动窄修 Task 映射；仍证明 frozen 上游事实无效则返回 Design closeout internal repair |
| Execution | pass / failed | parallel-slices、shared-file-locks、execution-groups、writeFiles、prerequisiteOutputs、integrationWriteFiles、targetRoot/packageDir/pathBaseline 可执行且路径口径一致 | failed 时修正执行合同，不得放行 Implementation |
| Dispatch | pass / failed / not-applicable | implementation dispatch validation 与 dispatch lease 均通过 | failed 时不得创建 Implementation Agent 调用 |
| Closeout | pass / failed | Task Ready validation 通过；task-status 初始状态由 Task owner 内部同步 | failed 时只窄修 canonical Task、并发/依赖合同或失效 source hash |

任一必需 gate 为 failed 时，不得返回“可进入 Implementation”。

Task Ready 的 `firstDispatchClosure` 固定包含 `fileMapping / mockEndpointMapping / contractFidelityPlan / validatorPlan / writeScope / dispatchPlanPreparation`。适用项只能为 `passed`，不适用项必须为 `not-applicable + reason`；validation 同时绑定 task-ready-result、task-breakdown、task-status、design-canonical-state 和 design-coverage-ledger 当前 hash。任一源变化后必须重跑 Task Ready，再生成当前 execution group 的 dispatch validation / lease，不得修一次派发一次。

## Implementation Handoff Metadata
- featureRoot / frontendRoot / taskBreakdownPath / taskStatusPath / implementationOrder / parallelSlices / integrationTasks / blockedItems / verificationPoints：

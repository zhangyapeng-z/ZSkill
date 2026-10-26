# 前端 Review 报告

<!-- frontend-canonical-state
{"schemaVersion":"1.0","sourceType":"review-report","frontendAutoRunId":"missing","status":"not-run","repairDispatchStatus":"not-applicable","repairClosureHash":"not-applicable"}
-->

Feature：<feature>
目标工程：<target-project>
建议路径：`sdd-workspace/changes/{change-id}/frontend/review/review-report.md`
路径规则：`sdd-workspace/changes/{change-id}/frontend/` 位于当前 SDD 项目根目录下，不位于目标前端工程内部或目标前端工程平级外部目录。

## Review Result

reviewStatus：pass / conditional / blocked / insufficient-context
blockReasonClass：none / finding-blocking / contract-gap / validator-failed / insufficient-context / timeout / other
failureObserved：none / review-finding / validator-failed / source-unreadable / empty-task-result / other
failureSource：none / review / validator / implementation / frontend-auto-agent / other
reviewMode：targeted-blocking / integration-contract-review / full-scan / fix-package-recheck / final-delta / reuse-existing-review
reviewPurpose：pre-review / final-review / targeted-recheck
reviewedByAgent：frontend-review-agent
sourceReviewPath：`frontend/review/review-report.md` / `frontend/review/pre-review.md` / `frontend/review/final-review.md` / null + reason
reviewScopeFingerprint：changedFiles + taskIds + contract/design/task source versions/hash 摘要
reviewedChangedFiles：[]
acceptedReviewFindings：[]
reviewFindingsCount：blocking=0 / major=0 / minor=0 / info=0 / accepted=0
reviewCostTelemetry：queueWaitMs / owningReviewMs / reportWriteMs / fixPackageBuildMs / fixPackageHandoffMs / implementationFixMs / recheckMs / readFileCount / readOutputChars 必须为数值；scopeExpansionReason 可为 null
costGovernanceStatus：verified / unverified（unverified 仅为 report-only downgrade）
reviewCostAnomaly：targeted-review-over-budget / none
reviewCostAction：scope-frozen / fix-package / backfill-package / continue-within-budget
reviewScopeExpansionAllowed：true / false
nextStageRecommendation：回到 Implementation / 回到 Task Breakdown / parallel-baseline-invalidated -> LITE_PARALLEL_AMENDMENT / 进入 Verification / 进入 Handoff / 外层白名单用户确认

规则：首次 Review、`fix-package-recheck` 和 Final Review 每次落盘时，都必须在同一次写入中更新顶部 `frontend-canonical-state`。`status` 必须与 `reviewStatus` 一致；修复链闭合后必须原样复制 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py --repair-closure-stage-result <frontend-stage-result.json>` 输出的 `frontendAutoRunId/repairDispatchStatus/repairClosureHash`，不得自行计算 hash。不得保留修复前状态块，也不得由 Handoff primary 代写 Review 状态；helper 失败只修 Review 状态，不重新执行 Review。

## Agent Dispatch Evidence

| stage | dispatchVia | delegatedAgent | stageResult | artifactPath | sessionOrToolEvidence |
| --- | --- | --- | --- | --- | --- |
| Review | direct-owning-agent / frontend-general-agent fallback | frontend-review-agent | completed / partial / blocked | `frontend/review/review-report.md` | session/tool id or not-available + reason |

## Scope

| item | value | evidence |
| --- | --- | --- |
| taskIds |  | task-status / task-breakdown |
| sliceId / integrationTaskId |  | task-breakdown |
| contractSources |  | contract-check / frontend-design |
| changedFilesSource |  | task-status / diff / implementation summary |
| productionOrMockStatus |  | contract-check / handoff metadata |

## Findings

| findingId | severity | relatedTaskId | file | line | issue | impact | recommendation | targetStage | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | none |

## Modal Open Pattern Check

| item | value |
| --- | --- |
| checkedFiles | [] |
| jsxVisibleModalHits | [] |
| modalOpenHits | [] |
| drawerResizableStatus | pass / failed / not-applicable / not-run |
| lifecycleEvidence | modalLifecycleContract / componentApiProvenance / not-applicable / missing |
| allowlistReason | legacy-compatible / project-wrapper-internal / Modal.confirm-or-Popconfirm / component-library-source / not-applicable |
| result | pass / finding / blocked / not-applicable / not-run |

## Table Toolbar Surface Check

| item | value |
| --- | --- |
| checkedFiles | [] |
| sourceRegions | [] |
| buttonIdsOrLabels | [] |
| buttonsArrayVariables | [] |
| tableButtonsPropEvidence | `<Table buttons={buttons}>` / project-wrapper evidence / missing / not-applicable |
| headerChildrenHits | [] |
| externalToolbarHits | [] |
| result | pass / finding / blocked / not-applicable / not-run |
| findingIds | [] |

## Affected Static Gate Scan

| item | value |
| --- | --- |
| scanMode | targeted-blocking / integration-contract-review / full-scan / fix-package-recheck / final-delta / not-run |
| validatorCommand | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_c7n_component_api_ast_grep.py --root <frontend-root-or-packageDir>` / `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_i18n_locale_ledger.py --root <frontend-root-or-packageDir> --manifest <manifest-or-handoff>` / `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_integration_contract_smoke.py --root <frontend-root-or-packageDir> --manifest <integration-contract-smoke.json>` / manual-scan / not-run |
| validatorTarget | `<frontend-root-or-packageDir>` / changedFiles / targetFiles / not-applicable |
| checkedFiles | [] |
| rulesChecked | [] |
| rulesHit | [] |
| issueCount | 0 |
| result | pass / failed / blocked / not-run / not-applicable |
| notRunReason |  |

规则：`integration-contract-review` 必须优先记录 integration smoke validator 命令、manifest、scope fingerprint、consumerProof、capabilityEntries、sharedContractFreeze、rulesChecked[] 和 rulesHit[]；validator 已通过且 fingerprint 匹配时，不重复人工追踪完整页面组合入口。`fix-package-recheck` 必须记录 `rootCause.riskDomains`、`affectedStaticGateScan.rulesChecked[]`、`rulesHit[]`、`newRiskDomains[]` 和 `targetFilesPreflight`，只扫描本轮 targetFiles 可见且与 rootCause 风险域相交的 validator ruleId / owner reference；`autoFixEligible=true` 时 `rulesChecked[]` 不得超过 8 条，且 `targetFilesPreflight.checkedFiles[]` 必须覆盖 `targetFiles[]`。命中新静态 blocker、新风险域或规则命中与 rootCause 不相交时，必须生成 finding、升级 full-scan 或进入止损。不得默认重扫 query/filterBar、Attachment/import、renderer/helper、row-actions、i18n/locale、permission copy、enum/type 和 DataSet boundary 全套规则，除非它们属于 rootCause 风险域或本轮 diff 新引入。

## recommendedFixPackage

packageId：
repairAttemptKey：
repairAttemptCount：0
repairOrdinal：1 / 2 / 3 / N（审计字段，不参与授权）
priorRepairAttemptKeys：[]
repairMode：code-repair
repairBudgetClass：code-repair
consumesRepairBudget：true
autoFixEligible：true / false
requiresUserDecision：true / false
targetStage：IMPLEMENTATION
contractDiffDomains：[]
businessChangedFiles：[]
sourceReviewPath：`frontend/review/review-report.md` / null + reason
reviewRecheckMode：fix-package-recheck / final-delta / not-applicable
findingIds：[]
rootCause：
  symptom：
  cause：
  evidencePaths：[]
  affectedFiles：[]
  targetFilesClosure：
  riskDomains：[]
affectedStaticGateScan：
  riskDomains：[]
  rulesChecked：[]
  rulesHit：[]
  newRiskDomains：[]
  targetFilesEnough：true / false
targetFilesPreflight：
  status：pass / failed / not-run
  checkedFiles：[]
  writeScopeSource：File Mapping / changedFilesPlan / direct-no-task / missing
  placementSource：Target Placement Contract / packageDir / pageRoot / not-applicable / missing
  rejectedFiles：[]
  failureReason：
targetFiles：[]
completionCriteria：[]
structuralChangeScope：none / same-region-only / requires-design-backfill
repairDiagnosisRevision：
repairPlanFingerprint：
stopCondition：none / terminal-block-whitelist / requires-user-decision / contract-missing / write-scope-expanded

规则：`recommendedFixPackage` 只承载当前实现范围内可自动闭合的代码修复，必须同时写 `packageId`、`repairAttemptKey`、`repairAttemptCount=0`、`repairDiagnosisRevision`、`repairPlanFingerprint`、`repairMode=code-repair`、`repairBudgetClass=code-repair`、`consumesRepairBudget=true`、`contractDiffDomains[]`、非空 `businessChangedFiles[]`、`autoFixEligible`、`requiresUserDecision`、`fixRouting`、`findingIds`、`rootCause`、`affectedStaticGateScan`、`targetFilesPreflight`、`targetFiles`、`completionCriteria`、`structuralChangeScope`、`stopCondition`、`sourceReviewPath` 和 `reviewRecheckMode=fix-package-recheck`。同一 `repairPlanFingerprint` 只允许执行一次；复查失败时保持 `repairAttemptKey`、递增诊断版本并生成新 fingerprint，不得仅凭次数止损。只有重新诊断命中 Terminal Block Whitelist 才允许 terminal stopCondition。

## progressionDecision.backfillPackage

backfillKey：
sourceStage：REVIEW
targetStage：TASK_BREAKDOWN / FRONTEND_DESIGN / CONTRACT_CHECK / USER_CONFIRMATION
reasonClass：design-contract-gap / task-contract-gap / result-contract-gap / user-decision
repairMode：evidence-backfill / not-applicable
repairBudgetClass：execution-proof / result-contract-backfill / not-applicable
consumesRepairBudget：false
blockingFindingIds：[]
requiredBackfill：[]
affectedFiles：[]
contractDiffDomains：[]
businessChangedFiles：[]
sourceRevisionHash：
attemptCount：
resumeStage：REVIEW
invalidateStages：[]
preserveArtifacts：[]
sourceReviewPath：`frontend/review/review-report.md` / null + reason
allowedNext：Task Breakdown / Frontend Design / Contract Check / 用户确认
requiresUserDecision：true / false
reason：

规则：该包只表达补合同、补任务、补设计事实、补写入范围或用户取舍；固定 `consumesRepairBudget=false`，不得进入 `repairDispatch`，也不计入 `repairAttemptCount`。`reasonClass=result-contract-gap` 时固定 `repairBudgetClass=result-contract-backfill + contractDiffDomains=[] + businessChangedFiles=[] + requiresUserDecision=false`，可回原 Implementation owning context 补 completion bundle/fragment，但不得作为代码 repair Todo。补齐后由主编排按 `resumeStage/invalidateStages/preserveArtifacts` 增量恢复，不重跑未失效阶段。

## repairDispatch

sourceStage：Review
sourceResultPath：`frontend/review/review-report.md` / null + reason
targetStage：IMPLEMENTATION / not-applicable
sameStageDeltaFastPath：true / false
fixRouting：direct-fix / owner-needed / not-applicable
generalDispatchRequired：true / false
implementationAgentRequired：true / false
targetFilesPreflightStatus：pass / failed / not-applicable
verificationRerunTargets：[]
evidenceCapsule：conclusion + evidencePaths + keyLines<=20 + fullOutputPath

## Verification Gaps

| gapId | relatedFindingId | requiredVerification | ownerStage | status |
| --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | none |

## Residual Risk

- 无 / 待填写

## Task Status Updates

- Review 完成后必须回写或结构化输出 `task-status-updates`，覆盖 Review Links、Blockers、Status Updates 和每个 finding 的 taskId/sliceId 映射。
- Review 通过但 Verification 未通过的任务不得在 checklist 中勾选最终完成，只能推进到 Verify。

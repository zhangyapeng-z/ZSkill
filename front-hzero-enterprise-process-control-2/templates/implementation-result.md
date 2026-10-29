# Frontend Implementation Result

用户可见文本只投影本轮 Todo 的关键事实；`implementation-result.json` 是唯一机器事实源，未命中的条件对象不展开。

```text
status: completed / partial / blocked
taskIds: []
sliceId: value / not-applicable
integrationTaskId: value / not-applicable
changedFiles: []
resultPath: evidence/implementation-results/<sliceId-or-taskId>.json
blockers: []
nextStageRecommendation: Review / Verification / Task Breakdown / Frontend Design / blocked
```

每个 slice / integration task 同时落盘 `evidence/implementation-results/<sliceId-or-taskId>.json`，并通过 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_result.py --input <implementation-result.json> --out <implementation-result-validation.json>`：

```text
schemaVersion: 1.0
owner: frontend-implementation-agent
status: completed / partial / blocked
sliceId / integrationTaskId / taskIds
changedFiles / changedFilesSource
writeScopeAudit: status / allowedFiles / checkedFiles / outOfScopeFiles
completionEvidence:
  contractFidelity: passed + evidencePaths / not-applicable + reason
  mockRequest: passed + evidencePaths / not-applicable + reason
  permissionActions: passed + evidencePaths / not-applicable + reason
  importExport: passed + evidencePaths / not-applicable + reason
  validators: passed + evidencePaths / not-applicable + reason
taskStatusUpdates: []
blockers: []
nextStageRecommendation: Review / Verification / Task Breakdown / Frontend Design / blocked
inputCapsule:
  canonicalSources: [] # <= 8
  ownerReferenceIdentities: [] # <= 6
  allowedSourcePaths: [] # <= 16
telemetry: readFileCount / skillLoadCount / ownerReferenceReloadCount / ownerReferenceReloadReason
```

文本投影中的 status、task/slice identity、changedFiles、blockers 和 next 必须直接复制 completion bundle；除 `resultPath` 指向 bundle 文件外，不得在文本中维护第二套 machine 字段。completion bundle 缺任一证据域属于 Implementation result gap，必须在当前 slice 内补齐后再进入 Review。`readFileCount > 12`、`skillLoadCount > 4` 或 reference reload 缺 reason 只产生 cost-governance warning，不重跑业务代码。

命中合同缺口时附加：

```text
progressionDecision.backfillPackage:
  blockerKey:
  targetStage: TASK_BREAKDOWN / FRONTEND_DESIGN / CONTRACT_CHECK / USER_CONFIRMATION
  repairMode: evidence-backfill / not-applicable
  repairBudgetClass: execution-proof / result-contract-backfill / not-applicable
  consumesRepairBudget: false
  contractDiffDomains: []
  businessChangedFiles: []
  affectedTaskIds: []
  affectedFiles: []
  missingContract: []
  whyImplementationCannotProceed:
  requiredBackfillFields: []
  evidenceAlreadyChecked: []
```

命中 repair Todo 时附加 `repairAttemptKey`、source Review/Verification path、findingIds/failureIds、completionCriteria 和 rerun targets；不得复制完整 source report。

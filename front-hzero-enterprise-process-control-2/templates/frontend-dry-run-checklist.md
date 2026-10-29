# Frontend Dry-run Checklist

用途：用一个小场景回放前端流程，验证规则、模板和门禁是否可执行。本文是流程验证模板，不是业务交付产物；除非用户要求留痕，否则不需要写入 feature workspace。

## Scenario

| item | value |
| --- | --- |
| scenarioId |  |
| scenarioType | direct-regular-change / minimal-evidence / standard-page / submodule-page / mock-request / production-transport |
| targetFeature |  |
| targetFrontendProject |  |
| featureRoot | `sdd-workspace/changes/{change-id}/` / not-applicable |
| expectedOutcome | pass / blocked / partial / draft-only |

## Input Readiness

| item | expected | actual | result | notes |
| --- | --- | --- | --- | --- |
| FDS / PRD / user requirement | required / optional / not-applicable |  | pass / missing / not-applicable |  |
| TDS / API / backend handoff | required / optional / not-applicable |  | pass / missing / not-applicable |  |
| MDS / FSS / platform assets | required / optional / not-applicable |  | pass / missing / not-applicable |  |
| Frontend Evidence Packet | required / optional / not-applicable |  | pass / missing / not-applicable |  |
| target files / diff | required / optional / not-applicable |  | pass / missing / not-applicable |  |

## Engineering Exploration Gate

| item | expected | actual | result | notes |
| --- | --- | --- | --- | --- |
| engineeringExplorationRequired | yes / no / null |  | pass / failed / not-applicable | yes=依赖目标工程事实或将写业务前端代码；no=明确不依赖且不写代码 |
| engineeringExplorationLevel | E1 / E2 / E3 / not-applicable |  | pass / failed / not-applicable |  |
| evidencePath | path / null + reason |  | pass / missing / not-applicable |  |
| baselineComparisonStatus | not-needed / ready / partial / blocked / needs-confirmation |  | pass / failed / not-applicable |  |
| similarPageEvidenceQualityStatus | ready / partial / missing / not-applicable |  | pass / failed / not-applicable |  |
| targetPlacementEvidenceStatus | ready / partial / missing / conflict / not-applicable |  | pass / failed / not-applicable |  |
| legacyRisk handling | none / recorded / blocked / fixed-by-baseline |  | pass / failed / not-applicable |  |

## Stage Gates

| stage | gate | expected | actual | result | rollback |
| --- | --- | --- | --- | --- | --- |
| Explore / Evidence | evidence is enough for next stage | pass / blocked / not-applicable |  | pass / failed | Explore |
| Frontend Design | FD-G1~FD-G10 | pass / blocked |  | pass / failed | Frontend Design |
| Task Breakdown | Readiness / Mapping / Execution / Dispatch / Closeout gates | pass / blocked |  | pass / failed | Task Breakdown |
| Implementation | write scope + targetPlacement + exploration gate + UI Contract | pass / blocked / draft-only |  | pass / failed | Implementation |
| Review | findings-first catches targetPlacement drift / legacy-risk / UI anti-patterns | pass / blocking / major |  | pass / failed | Review |
| Verification | targetPlacementVerification + buildable / reachable / usable are separated | pass / partial / not-run |  | pass / failed | Verification |
| Handoff | status is production-ready / conditional / blocked |  |  | pass / failed | Handoff |

## Specific Checks

| check | expected | actual | result |
| --- | --- | --- | --- |
| 代码实现终点裁剪或实现后阶段裁剪只设置 `flowCutoff=after-implementation`，不跳过 Task Breakdown | yes / not-applicable |  | pass / failed / not-applicable |
| 页面交付、demo-slice 或状态回写任务的链路为 Frontend Design -> Design Confirm -> Task Breakdown -> Implementation -> Stop，不得为 Frontend Design -> Implementation-only | yes / not-applicable |  | pass / failed / not-applicable |
| `taskBreakdownDecision=skipped/not-generated` 的来源不是实现后阶段裁剪；若用户明确跳过任务拆分，必须有 user-explicit-task-skip 和 question/blocked 记录 | yes / not-applicable |  | pass / failed / not-applicable |
| `frontend/index.md` 区分 terminalStageRequested、flowCutoff、skippedPostImplementationStages、requiredPreImplementationStages 和 taskBreakdownDecision | yes / not-applicable |  | pass / failed / not-applicable |
| mock-request uses HZERO devServer mock API | yes / not-applicable |  | pass / failed / not-applicable |
| `_smock/smock/sproxy` are not read or used by standard mock-request; only existence signal is recorded unless user explicitly requests legacy audit | yes / not-applicable |  | pass / failed / not-applicable |
| mock-request uses isolated namespace `/_mock/<module>/v1/{organizationId}/...` | yes / not-applicable |  | pass / failed / not-applicable |
| mock-request service/DataSet baseUrl and middleware listen path are consistent | yes / not-applicable |  | pass / failed / not-applicable |
| mock-request does not use `<unconfirmed-gateway-prefix>`, `/api/v1/demo-org`, hardcoded `demo-org`, or unconfirmed aliases | yes / not-applicable |  | pass / failed / not-applicable |
| Umi middleware is registered by `api.addBeforeMiddlewares(() => [middleware])` or proven equivalent entry; parent-managed package has parent config mock plugin | yes / not-applicable |  | pass / failed / not-applicable |
| mock list response shape matches confirmed consumer shape: bare array / page-response `content / totalElements / size / number` / data-envelope as applicable | yes / not-applicable |  | pass / failed / not-applicable |
| mock-request Network targets current dev server origin, not remote `API_HOST` | yes / not-applicable |  | pass / failed / not-applicable |
| local-filter / inline mock is flagged as blocking cleanup | yes / not-applicable |  | pass / failed / not-applicable |
| mock/production switch defaults to mock and only `<MODULE>_USE_MOCK=false` switches to production | yes / not-applicable |  | pass / failed / not-applicable |
| production URL separates resourcePath `/v1/...` from confirmed servicePrefix `/<servicePrefix>` | yes / not-applicable |  | pass / failed / not-applicable |
| servicePrefix source follows priority: common config, similar service, backend service-code candidate, or missing | yes / not-applicable |  | pass / failed / not-applicable |
| no hard dependency on non-existent common package; local `src/utils/servicePrefix.ts` only when common config is absent | yes / not-applicable |  | pass / failed / not-applicable |
| similar pages are rated before reuse | yes / not-applicable |  | pass / failed / not-applicable |
| UrlHistoryProvider/page-level Provider without source is rejected | yes / not-applicable |  | pass / failed / not-applicable |
| thin wrappers/runtimeAdapters/buttonProps/local t/fake import-export are rejected unless project-level evidence exists | yes / not-applicable |  | pass / failed / not-applicable |
| production-transport has serviceRequestContract | yes / not-applicable |  | pass / failed / not-applicable |
| tenantContext is confirmed when needed | yes / not-applicable |  | pass / failed / not-applicable |
| HZEROJS submodule baseline covers package/tsconfig/config/routes/packages-config | yes / not-applicable |  | pass / failed / not-applicable |
| HZEROJS submodule package.json has required scripts, trimmed files, and sourced dependency fields | yes / not-applicable |  | pass / failed / not-applicable |
| Target Placement Contract keeps submodule business code under packages/<module> | yes / not-applicable |  | pass / failed / not-applicable |
| parent src/pages is forbidden for package placement business files | yes / not-applicable |  | pass / failed / not-applicable |
| registerRegex is prefix-scoped | yes / not-applicable |  | pass / failed / not-applicable |
| UI Contract blocks hand-written query form / self-made overlay / div-grid detail | yes / not-applicable |  | pass / failed / not-applicable |
| task-status checklist only checks Done after Review + Verify | yes / not-applicable |  | pass / failed / not-applicable |

## Findings

| id | severity | stage | issue | rootCause | recommendedAssetChange | required |
| --- | --- | --- | --- | --- | --- | --- |
| DR-001 | blocking / major / minor / info |  |  | design / task / implementation / review / verify / template / agent |  | yes/no |

## Dry-run Result

- result：pass / pass-with-minor-follow-up / failed / blocked
- canUseForRealScenario：yes / no + reason
- fieldsTooHeavy：
- missingTemplateFields：
- gateTooStrict：
- gateTooLoose：
- recommendedNext：

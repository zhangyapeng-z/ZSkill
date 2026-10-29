# Target Placement Backfill Checklist

用途：历史已生成的 feature 前端产物缺少 `Target Placement Contract`、`Target Placement Evidence` 或 `targetPlacementVerification` 时，用本清单补齐落点合同。本文是补合同检查模板，不是业务交付物；可内嵌到 `frontend-design.md` / `task-breakdown.md` / `verification-report.md`，复杂或需留痕时可保存到 `sdd-workspace/changes/{change-id}/frontend/design/target-placement-backfill-checklist.md`。

## Trigger

| trigger | result | evidence | action |
| --- | --- | --- | --- |
| frontend-design.md 缺 `Target Placement Contract` | yes / no |  | run-backfill / not-applicable |
| evidence.md 缺 `Target Placement Evidence` | yes / no |  | return-to-Explore / not-applicable |
| task-breakdown.md 缺 `targetPlacement` 或 File Mapping placementScope | yes / no |  | return-to-Task / not-applicable |
| implementation changedFiles 已存在但无法判定落点 | yes / no |  | block-implementation / review-existing |
| verification-report.md 缺 `targetPlacementVerification` | yes / no |  | add-verification-gate / not-applicable |

## Backfill Inputs

| input | path/source | status | notes |
| --- | --- | --- | --- |
| user intent |  | explicit / implicit / missing / conflict | 是否提到子模块、独立子模块、微前端、packages |
| FDS / PRD |  | confirmed / partial / missing |  |
| TDS / backend handoff |  | confirmed / partial / missing | 后端 TDS 只能作为 hint，不单独决定落点 |
| Frontend Evidence | `frontend/evidence/evidence.md` | ready / partial / missing / conflict |  |
| target project structure |  | ready / partial / missing |  |
| packages evidence |  | ready / partial / missing / not-applicable |  |
| package internal business domains |  | ready / partial / missing / conflict / not-applicable | package 内业务目录、route prefix、菜单分组候选 |
| parent src/pages evidence |  | candidate / confirmed-parent-page / not-applicable |  |
| parent registration evidence |  | ready / partial / missing / not-applicable |  |

## Decision Matrix

| condition | placementDecision | requiredAction |
| --- | --- | --- |
| 用户明确“子模块/独立子模块/微前端/packages 模块”，且发现或可新建 `packages/<module>` | `placementType=new-package/existing-package` | 补 `Target Placement Contract`；父工程 `src/pages/**` 设为 forbidden/registration-only |
| 已确认 `packages/<module>`，但 package 内存在多个业务域、多个 route prefix 或多个候选页面 | `needs-confirmation` / `conflict` | 触发 `Target Placement Confirm`；补 `businessDomain/pageGroup/pageDir/routePrefix/menuGroup` |
| HZEROJS 空项目、参考资产缺失/不可读或无可采纳参考模块，历史设计或 TDS 候选把页面落到 `src/routes/**` | `invalid-baseline-label` / `conflict` | 固定回填为 `pageRoot=src/pages`、`pageRootSource=asset-baseline`；不得把 `src/routes` 作为新建/生成页面的用户确认项 |
| 用户明确父工程页面目录，且无 packages 子模块意图 | `placementType=parent-src-page` | 补合同并写 `parentSrcWritePolicy=allowed-with-reason` |
| 只有父工程 `src/pages/**` 相似页面证据，但用户意图是子模块 | `needs-confirmation` / `missing` | 不得自动降级；回 Frontend Design，若缺工程证据则 `deltaExploreReason=missing-target-placement` + `targetedDeltaScope=target-placement` |
| 同时存在 package 候选和 parent src/pages 候选，且来源冲突 | `conflict` | question 或 blocked |
| Evidence 不足以判断 | `missing` | 只允许 targeted evidence backfill：`deltaExploreReason=missing-target-placement`、`targetedDeltaScope=target-placement`，补 `Target Placement Evidence` |

## Required Backfill Fields

| field | value | status | source |
| --- | --- | --- | --- |
| placementType | new-package / existing-package / parent-src-page / integration-only / unknown | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  |
| placementIntentSource | user-explicit / user-implicit / FDS / TDS / evidence / generatedCandidate |  |  |
| targetProject |  |  |  |
| packageName |  |  |  |
| packageDir | `packages/<module>` / not-applicable |  |  |
| businessDomain |  | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  |
| pageRoot | `src/pages` / `src/routes` / custom | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable | 无参考基线默认 `src/pages` |
| pageRootSource | asset-baseline / project-evidence / adjacent-module / existing-file / user-confirmed | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable | `src/routes` 不允许用于新建/生成页面；只允许已有页面改造的 existing-file / project-evidence / adjacent-module 来源 |
| pageGroup |  | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  |
| pageDir |  |  |  |
| routePrefix |  | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  |
| menuGroup |  | confirmed / generatedCandidate / missing / not-applicable |  |
| packageInternalAmbiguity | none / multiple-business-domains / multiple-route-prefixes / multiple-candidates / missing-evidence / not-applicable |  |  |
| routeConfigPath |  |  |  |
| parentRegistrationPath |  |  |  |
| registerRegex |  |  |  |
| parentSrcWritePolicy | registration-only / forbidden / allowed-with-reason / not-applicable |  |  |
| forbiddenBusinessPaths | `src/pages/**` / not-applicable |  |  |
| evidenceStatus | ready / partial / missing / conflict / not-applicable |  |  |
| userConfirmStatus | confirmed / needs-confirmation / missing / conflict / not-applicable |  |  |
| confirmationSource | user-question / requirement-doc / FDS / TDS / platform-menu / none / not-applicable |  |  |

## Progression Decision

缺少 target placement 相关字段时，下游阶段必须输出结构化回退，不得只写自然语言说明：

```text
progressionDecision.status=blocked-by-missing-target-placement
recommendedRollback=Explore / Frontend Design / Task Breakdown
requiredBackfill=Target Placement Contract
allowedNext=backfill-only
reason=
```

允许继续的唯一条件：
- `Target Placement Evidence` ready 或 not-applicable。
- `Target Placement Contract` 无 conflict，且进入 runnable Implementation / Verify / Handoff 前 `userConfirmStatus=confirmed`。若仅为 `generatedCandidate` 或 `evidenceStatus=ready`，只允许 backfill / Target Placement Confirm，不允许 runnable implementation。
- `pageRoot/pageRootSource` 无 conflict。无参考基线或 `assetBaselineSource=hzerojs-asset-baseline` 时，新建/生成页面最终必须是 `pageRoot=src/pages`。若出现 `pageRoot=src/routes`，只能是改造已存在的 `src/routes/**` 存量页面，并必须有 existing-file / project-evidence / adjacent-module 证据；模糊确认“当前落位”或用户偏好不满足继续条件。
- Task File Mapping 已带 placementScope / placementPolicy。
- Implementation changedFiles 与合同一致。
- Verify 已记录 `targetPlacementVerification` 或明确 not-applicable reason。

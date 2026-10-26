# Frontend Evidence Packet

建议路径：`sdd-workspace/changes/{change-id}/frontend/evidence/evidence.md`

用途：记录 Explore 阶段可复用的工程事实、候选事实、参考质量和验证命令候选。本文是结构模板，不承载业务契约、组件写法或生产合规规则；字段语义以 `frontend-context-handoff-control.md`、`input-root-multi-module-discovery.md`、`schema-runtime-gates.md` 和 owning skill/reference 为准。

普通 `medium` Evidence Packet 采用最小实例化：只保留 `Evidence Status`、`Scope`、当前 Design/Task 所需的 `Decision Evidence Minimum`、命中的专项证据段和 `Unknowns And Follow-up`。未触发的 Baseline、Reference Module、Enum Map、Mock、Service Prefix 等长表可以省略并在摘要写 `not-applicable + reason`，不得为了模板完整度生成空矩阵、重复来源或追加用户等待。

## Evidence Layer Summary

| layer | 本模板职责 | 缺失处理 |
| --- | --- | --- |
| Decision Evidence | 记录目标工程/落点/write scope、当前能力涉及的 route/API/permission/data/service 和验证命令来源 | 只对会迫使下游猜测的缺口 targeted explore/backfill |
| Execution Proof | 不由 Explore 生成；hash、lease、trace、validator result 由后续脚本/owning Agent 生成 | 不得要求用户补 proof |
| Audit Telemetry | 只在 `stageSummary.telemetry` / cost report 记录 | warning，不进入本 Packet 长表 |
| Runtime Acceptance | 只记录候选 route/command，不证明 reachable/usable | 默认 conditional；独立 Runtime Acceptance 消费 |

## Decision Evidence Minimum

| decisionArea | status | valueOrCandidate | sourceType | source | downstreamAction |
| --- | --- | --- | --- | --- | --- |
| target project / placement | confirmed / candidate / missing / conflict / not-applicable |  |  |  | continue / targeted-backfill / return-to-lite-frontend-project-confirm / return-to-design-target-placement-confirm |
| write scope / target files | confirmed / candidate / missing / conflict / not-applicable |  |  |  | continue / Task backfill / Write Scope Confirm |
| route / permission | confirmed / candidate / missing / conflict / not-applicable |  |  |  | continue / Design backfill / business-choice |
| API / field / data path | confirmed / candidate / missing / conflict / not-applicable |  |  |  | continue / Contract backfill / default-mock-policy |
| required acceptance / command source | confirmed / candidate / missing / conflict / not-applicable |  |  |  | continue / conditional / targeted scripts evidence |

只有本轮 changed scope 实际读取、写入或验收的 decisionArea 才 required。标准 import/enum/component/helper 可由 owner reference 唯一推导时，直接在 Design/Task 自动继承，不要求 Explore 找项目样例。

## Evidence Status
- evidenceStatus：ready / partial / not-persisted / blocked
- notPersistedReason：
- featureRoot：`sdd-workspace/changes/{change-id}/`
- frontendRoot：`sdd-workspace/changes/{change-id}/frontend/`
- scopeFingerprint：`sha256:<64hex>` / missing；由 Lite 对规范化后的 `changeId + 确认后的目标工程绝对路径 + parentFrontendRoot + packageDir + pageScope` 生成；这里的目标工程路径不是本模板上一行的 SDD `frontendRoot` 产物目录，目标范围未变化时必须稳定
- generatedBy：frontend-explore-agent
- explorationDepth：quick / medium / thorough / targeted-delta / reused
- engineeringExplorationRequired：yes / no / null
- engineeringExplorationLevel：E1 minimal / E2 standard / E3 submodule / not-applicable
- explorationSkipReason：not-applicable / user-provided-evidence / target-file-direct / target-unreadable / user-requested-draft / other
- evidenceReuseSource：new-explore / existing-evidence / user-provided-packet / targeted-delta-explore / existing-evidence-conflict / not-applicable
- evidenceReuseStatus：reusable / stale / conflict / missing-required-field / target-changed / not-applicable
- deltaExploreReason：null / target-changed / index-evidence-conflict / missing-target-placement / missing-validator-command / missing-component-import-map / missing-enum-map / missing-similar-page-quality / missing-package-route-registration / missing-mock-request-path / missing-baseline-comparison / missing-scripts / write-scope-unclear / open-item-requested / other
- targetedDeltaScope：null / target-placement / validator-command / component-import-map / enum-map / similar-page-quality / package-route-registration / mock-request-path / baseline-comparison / scripts / write-scope / other
- targetedDeltaRequests：[] / `{ deltaKey, targetedDeltaScope, deltaExploreReason, requiredFields[], blockingDesignDomains[] }[]`；Design 所需多个工程事实缺口必须一次批量提交
- targetedDeltaResults：[] / `{ deltaKey, status, resolvedFields[], remainingGaps[], sourceRefs[] }[]`；与 requests 按 deltaKey 一一对应
- nextExploreAllowed：none / targeted-delta / full-reexplore / user-confirmation-required
- confidence：high / medium / low
- standardBaselineApplied：true / false / not-applicable
- baselineComparisonStatus：not-needed / ready / partial / blocked / needs-confirmation
- goldenBaselineStatus：confirmed / not-confirmed / rejected / conflict / not-applicable
- baselineConfirmationSource：user-explicit / owner-doc / design-confirmed-from-owner / none / not-applicable
- fullExploreForbiddenReason：ready-evidence-reusable / targeted-delta-only / target-scope-unchanged / not-applicable
- contaminationStatus：clean / mixed / quarantined / unknown
- contaminationSignals：none / legacy-risk / anti-pattern / generatedCandidate / recent-change / untracked / demo / local-filter / disabled-noop / as-any / thin-wrapper / page-level-provider-without-source / other
- blockedPatternReuse：none / route / DataSet / service / i18n / permission / component-wrapper / mock / provider / build-config / all
- similarPageEvidenceQualityStatus：ready / partial / missing / not-applicable
- targetPlacementEvidenceStatus：ready / partial / missing / conflict / not-applicable
- enumImportMapStatus：ready / partial / missing / not-applicable
- nextAgent：

## Pre-Design Evidence Decision

`preDesignEvidenceDecision` 是 Lite、Explore 与 Design 之间唯一的前置证据路由合同，不新增独立产物：

```yaml
preDesignEvidenceDecision:
  status: reuse-ready | initial-explore | targeted-delta | full-reexplore | needs-user | blocked
  scopeFingerprint: sha256:<64hex> | missing
  evidencePath: frontend/evidence/evidence.md | null
  reason:
  requestedExploreMode: reused | medium | thorough | targeted-delta | not-applicable
  targetedDeltaRequests: []
  fullExploreAttemptCount: 0 | 1
  targetedDeltaAttemptKeys: []
  nextOwner: frontend-explore-agent | frontend-design-agent | hzero-auto-agent-lite | none
```

决策规则：
- `reuse-ready`：Evidence ready/reusable 且 `scopeFingerprint` 一致，直接进入 Design，不调度 Explore。
- `initial-explore`：当前 scope 尚无可复用 Evidence，首次调度 medium/thorough Explore。
- `targeted-delta`：已有 Evidence 只缺明确工程字段；所有缺口必须合并到一次 `targetedDeltaRequests[]` 调度。
- `full-reexplore`：`target-changed` 必须按新范围产生新的 `scopeFingerprint`；`index-evidence-conflict` 必须保留原 fingerprint 和冲突证据，且仅在该 fingerprint 的 `fullExploreAttemptCount=0` 时允许执行。
- `needs-user`：多个真实目标工程、父工程或 package 候选会改变搜索/写入边界，由 Lite 执行 `Frontend Project Confirm`；Explore 不生成 question payload。
- `blocked`：目标不可读、权限不足、scope 无法形成或预算已耗尽且仍不能安全降级。

同一 `scopeFingerprint` 的 `fullExploreAttemptCount` 不得超过 1。Design 返回多个工程缺口时，Lite 只能形成一次批量 targeted-delta，并把该批全部 key 一次写入 `targetedDeltaAttemptKeys[]`；该数组一旦非空，不得追加第二批或新 key。回填后仍缺失的项由 Design 分类为 `missing / generatedCandidate / needs-user / blocked`，不得再次进入 Explore。

## Source Type Rules

| sourceType | may confirm | must remain candidate |
| --- | --- | --- |
| userInput | 用户明确给出的工程事实或范围 | 与输入无关的业务契约推断 |
| filePath / routeConfig / packageScript | 文件、路由、脚本、配置存在性 | 字段语义、生产 API、权限、菜单、LOV、附件参数 |
| similarPage | 只在 Reference Module Quality Gate 允许时复用局部模式 | 未评级、legacy-risk、anti-pattern、unknown-quality 模式 |
| generatedCandidate | 可按规范生成的候选值 | 平台已登记或生产已确认事实 |

规则摘要：Explore 只确认工程事实和候选，不确认业务生产契约；参考质量、污染隔离和下游复用策略以 `frontend-context-handoff-control.md` 为准。

## Scope
- 探索目标：
- 目标范围：
- 目标工程：
- 目标模块/微包：
- 目标落点候选：
- 页面范围：
- 关键词：

## Engineering Exploration Gate
| item | value | reason | source |
| --- | --- | --- | --- |
| engineeringExplorationRequired | yes / no / null |  |  |
| engineeringExplorationLevel | E1 / E2 / E3 / not-applicable |  |  |
| requiredForNextStage | yes / no |  |  |
| skipOrDowngradeAllowed | yes / no |  |  |
| skipOrDowngradeReason | not-applicable / user-provided-evidence / target-file-direct / target-unreadable / user-requested-draft / other |  |  |
| blocksRunnableImplementation | yes / no |  |  |

## Target Placement Evidence
用于为 Frontend Design 的 `Target Placement Contract` 提供工程证据。Explore 只记录事实和候选，不单独确认业务落点。

| item | value | status | sourceType | source | confidence | notes |
| --- | --- | --- | --- | --- | --- | --- |
| placementIntent | parent-src-page / existing-package / new-package / unknown | confirmed / candidate / missing / conflict | userInput / filePath / routeConfig / similarPage / unknown |  | high / medium / low |  |
| targetProject |  | confirmed / candidate / missing / conflict |  |  |  |  |
| packageName |  | confirmed / candidate / missing / not-applicable |  |  |  |  |
| packageDir | `packages/<module>` / not-applicable | confirmed / candidate / missing / not-applicable |  |  |  |  |
| packageBusinessDomains |  | confirmed / candidate / missing / conflict | filePath / routeConfig / similarPage / unknown |  |  |  |
| pageGroup |  | confirmed / candidate / missing / conflict |  |  |  |  |
| pageDir |  | confirmed / candidate / missing / conflict |  |  |  |  |
| routePrefix |  | confirmed / candidate / missing / conflict | routeConfig / userInput / generatedCandidate / unknown |  |  |  |
| menuGroup |  | confirmed / candidate / missing / not-applicable | userInput / routeConfig / platform-export / unknown |  |  |  |
| packageInternalAmbiguity | none / multiple-business-domains / multiple-route-prefixes / multiple-candidates / missing-evidence | confirmed / candidate / conflict / missing | filePath / routeConfig / unknown |  |  |  |
| parentPageDir | `src/pages/<page-or-module>` / not-applicable | confirmed / candidate / missing / not-applicable |  |  |  |  |
| routeConfigPath |  | confirmed / candidate / missing / conflict |  |  |  |  |
| parentRegistrationPath |  | confirmed / candidate / missing / not-applicable |  |  |  |  |
| forbiddenBusinessPathsCandidate | `src/pages/**` / not-applicable | candidate / not-applicable | generatedCandidate / userInput / filePath |  |  |  |

## Confirmed Project Facts
| fact | value | sourceType | source | confidence |
| --- | --- | --- | --- | --- |
| none | not-yet-confirmed | not-applicable | not-applicable | not-applicable |

## Candidate Project Facts
| fact | value | sourceType | source | confidence | whyCandidateOnly |
| --- | --- | --- | --- | --- | --- |
| none | not-yet-discovered | not-applicable | not-applicable | not-applicable | not-applicable |

## Baseline Comparison
| area | projectEvidence | standardBaselineApplied | baselineRule | difference | evidenceQuality | goldenBaselineStatus | baselineConfirmationSource | baselineScope | baselineHealthCheck | decision | adoptedPatternItems | rejectedPatternItems | legacyRisk | confirmationNeeded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| submodule-structure |  | true / false / not-applicable | hzerojs-submodule-development.md |  | golden-baseline / project-compatible / asset-baseline / legacy-risk / anti-pattern / unknown-quality | confirmed / not-confirmed / rejected / conflict / not-applicable | user-explicit / owner-doc / design-confirmed-from-owner / none / not-applicable | package / page-pattern / route-pattern / DataSet-pattern / wrapper-pattern / other / not-applicable | pass / partial / failed / not-run / not-applicable | follow-project / follow-baseline / follow-asset-baseline / merge / block / not-applicable | [] | [] | yes/no | yes/no |
| route-registerRegex |  | true / false / not-applicable | hzerojs-submodule-development.md |  | golden-baseline / project-compatible / asset-baseline / legacy-risk / anti-pattern / unknown-quality |  |  | route-pattern |  |  | [] | [] | yes/no | yes/no |
| UI/component-pattern |  | true / false / not-applicable | frontend-ui-contract-guardrails.md |  | golden-baseline / project-compatible / asset-baseline / legacy-risk / anti-pattern / unknown-quality |  |  | wrapper-pattern / other |  |  | [] | [] | yes/no | yes/no |
| mock-request |  | true / false / not-applicable | front-hzero-mock-request Design Contract |  | golden-baseline / project-compatible / asset-baseline / legacy-risk / anti-pattern / unknown-quality |  |  | mock |  | follow-baseline / follow-asset-baseline / block / not-applicable | [] | [] | yes/no | yes/no |

## Reference Module Quality Gate
用于把参考子模块从“默认样板”降级为“受控证据源”。详细采纳/拒绝规则以 `frontend-context-handoff-control.md` 和 `baseline-comparison-rubric.md` 为准。

| referenceModule | sourceType | evidenceQuality | qualityBasis | contaminationStatus | contaminationSignals | adoptedPatternItems | rejectedPatternItems | blockedPatternReuse | downstreamPolicy | decision | scanReport | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | none | [] | [] | none | not-applicable | not-applicable | not-run | no reference module |

结构化项：`adoptedPatternItems[] / rejectedPatternItems[] = { area, pattern, policy, basis, scope, reason }`，是唯一有效的模式采用/拒绝合同。`adoptedPatterns / rejectedPatterns` 属于无效旧字段。

## Similar Page Evidence Quality
| path | sourceType | reason | evidenceQuality | contaminationStatus | contaminationSignals | goldenBaselineStatus | baselineConfirmationSource | baselineScope | baselineHealthCheck | adoptedPatternItems | rejectedPatternItems | blockedPatternReuse | confidence | downstreamPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-yet-discovered | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | [] | [] | not-applicable | not-applicable | not-applicable |

## Entry Points
| type | pathOrName | sourceType | source | notes |
| --- | --- | --- | --- | --- |
| route |  |  |  |  |
| menu |  |  |  |  |
| permission |  |  |  |  |
| i18n |  |  |  |  |

## Similar Pages
| path | reason | evidenceQuality | reusablePattern | rejectedPattern | confidence |
| --- | --- | --- | --- | --- | --- |
| none | not-yet-discovered | not-applicable | not-applicable | not-applicable | not-applicable |

## Candidate Files
| path | role | reason | readStatus |
| --- | --- | --- | --- |
| none | not-yet-discovered | not-applicable | not-read |

## Component / Data / Service Evidence
| area | evidence | sourceType | source | notes |
| --- | --- | --- | --- | --- |
| component |  |  |  |  |
| DataSet/service |  |  |  |  |
| request helper |  |  |  |  |
| serviceRequestContract evidence | request helper / API_HOST strategy / envSource / servicePrefix / nativeHttp project pattern |  |  |  |

## Choerodon Enum Import Map
| enumDomain | enumName / prop | projectStyle | importPath | sampleUsage | sourceType | source | confidence | recommendedGeneration | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DataSet | FieldType / DataSetSelection / DataToJSON / RecordStatus / DataSetEvents | enum / string / mixed / not-found |  |  | filePath / similarPage / generatedCandidate / unknown |  | high / medium / low | enum / string / missing / not-applicable |  |
| Table | ColumnLock / ColumnAlign / TableEditMode / TableQueryBarType / TableCommandType | enum / string / mixed / not-found |  |  | filePath / similarPage / generatedCandidate / unknown |  | high / medium / low | enum / string / missing / not-applicable |  |
| Form / Field | ShowHelp / LabelLayout / FormLayout / ValueChangeAction / TriggerViewMode | enum / string / mixed / not-found |  |  | filePath / similarPage / generatedCandidate / unknown |  | high / medium / low | enum / string / missing / not-applicable |  |
| Component | ButtonColor / FuncType / TabsType / Placements / Lov ViewMode / AttachmentButtonType | enum / string / mixed / not-found |  |  | filePath / similarPage / generatedCandidate / unknown |  | high / medium / low | enum / string / missing / not-applicable |  |

## Package And Scripts
| item | value | sourceType | source | notes |
| --- | --- | --- | --- | --- |
| packageManager |  |  |  |  |
| scripts |  |  |  |  |
| lockfile |  |  |  |  |

## Service Prefix Evidence
| item | value | sourceType | source | notes |
| --- | --- | --- | --- | --- |
| commonServiceConfigCandidate | @common/utils/config / src/utils/config / src/config/servicePrefix / getEnvConfig / missing / unknown / not-applicable | filePath / importPath / unknown | project source |  |
| similarServicePrefixCandidate | /<servicePrefix> / missing / unknown / not-applicable | filePath / grep / unknown | existing service |  |
| backendServiceCodeCandidate | HSPD -> /hspd / generatedCandidate / missing / not-applicable | FDS / TDS / MDS / API doc / unknown | backend contract |  |
| resourcePathCandidate | /v1/{organizationId}/... / missing / unknown / not-applicable | API doc / service / unknown | backend API resource |  |
| servicePrefixHelperCandidate | existing-common-config / packages/<module>/src/utils/servicePrefix.ts / missing / not-applicable | filePath / generatedCandidate / unknown | target package |  |
| switchEnvVarCandidate | <MODULE>_USE_MOCK / missing / not-applicable | generatedCandidate / filePath / unknown | servicePrefix helper |  |

## Mock DevServer Evidence
| item | value | sourceType | source | notes |
| --- | --- | --- | --- | --- |
| devServerExtensionPoint | confirmed / missing / unknown / not-applicable | filePath / packageScript / unknown | webpack / Umi / HZERO wrapper |  |
| targetPlacementCandidate | parent-managed-package / standalone-app / unknown / not-applicable | filePath / contract / unknown | target placement evidence |  |
| startupEntryCandidate | parent-root-start / package-start / unknown / not-applicable | packageScript / filePath / unknown | root package.json / package package.json / docs |  |
| requestBypassPrefixCandidate | /_mock/<module> / none / unknown / not-applicable | filePath / unknown | request helper / DataSet adapter |  |
| businessApiPathCandidate | /v1/{organizationId}/... / unknown / not-applicable | generatedCandidate / filePath / unknown | service / API contract |  |
| mockApiMountCandidate | /_mock/<module>/v1/{organizationId}/... / unknown / not-applicable | generatedCandidate / filePath / unknown | isolated mock namespace + business API path |  |
| mockMiddlewareCandidate | api.addBeforeMiddlewares / devServer.before / project-equivalent / missing / unknown / not-applicable | filePath / packageScript / unknown | Umi plugin / webpack config / HZERO wrapper |  |
| mockHandlerCandidate | dev-mock/<module>-dev-mock.js / project-equivalent / unknown / not-applicable | generatedCandidate / filePath / unknown |  |  |
| mockPluginCandidate | packages/<module>/dev-mock/<module>-dev-mock-plugin.js / config/dev-mock-plugin.js aggregator / project-equivalent / unknown / not-applicable | generatedCandidate / filePath / unknown |  |  |
| serviceMiddlewarePathConsistencyCandidate | pass / failed / unknown / not-applicable | filePath / unknown | service + middleware |  |
| pageResponseShapeCandidate | content / totalElements / size / number / unknown / not-applicable | generatedCandidate / filePath / unknown | mock handler / Network sample |  |
| mockOwnerScope | parent-project / micro-package / packageDir / unknown | filePath / unknown |  |  |
| productionBuildImpact | none / risk / blocked / unknown | filePath / diff / unknown |  |  |

## Verification Command Candidates
| command | cwd | source | confidence | notes |
| --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | no command discovered yet |

## Cannot Be Confirmed By Explore
- 字段真实业务语义：
- 生产 API 契约：
- 真实菜单登记：
- 权限码登记：
- LOV/lookup/bucket/templateCode：
- 是否 production-ready：

## Contract Boundary
- Explore 只能确认工程结构、文件位置、脚本、相似实现和技术模式。
- 相似实现必须先经过 evidenceQuality 评级；未评级、legacy-risk 或 anti-pattern 不得作为 Design/Task/Implementation 的默认范式。
- 下游 Design / Contract Check 必须重新消费本证据并完成契约判定；不得把 Candidate Project Facts 直接写成 confirmed contract。

## Unknowns And Follow-up
| item | impact | owner | recommendedNext |
| --- | --- | --- | --- |
| none | not-applicable | not-applicable | none |

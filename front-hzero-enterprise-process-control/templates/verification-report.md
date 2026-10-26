# 前端验证报告

Feature：<feature>
目标工程：<target-project>
建议路径：`sdd-workspace/changes/{change-id}/frontend/verification/verification-report.md`
路径规则：`sdd-workspace/changes/{change-id}/frontend/` 位于当前 SDD 项目根目录下，不位于目标前端工程内部或目标前端工程平级外部目录。

用户提示：无 / environment-prerequisite-notice；缺依赖时必须使用下方“缺依赖用户可见提示”格式。
验证结果：passed / failed / partial / not-run
交付状态建议：production-ready / conditional / blocked
buildable：true / false / unknown，证据：（缺依赖未运行 build 时必须写 unknown，不得写 false）
reachable：true / false / unknown，证据：
usable：true / false / unknown，证据：
manualVerificationRequired：true / false，原因：
frontendServiceNotice：无 / 请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面
runtimeAcceptance：object；至少包含 `required`、`status=passed / failed / not-run / not-required`、`source`、`evidencePath`、`routeLoad`、`primaryRender`、`responseConsumerShape`、`requiredInteractions`、`runtimeErrors`；缺外部页面运行态证据时不得用 build、服务启动或静态扫描替代
是否 runnable：production runnable / mock-demo runnable / 未证明 runnable / non-runnable
queryMode：mock-request / production-transport / partial / blocked / unknown
productionComplianceState：production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable
productionComplianceVerification：pass / partial / failed / blocked / not-applicable
complianceManifestPath：`sdd-workspace/changes/{change-id}/frontend/design/frontend-compliance-manifest.md` / null + not-applicable reason
complianceManifestVerification：pass / partial / failed / blocked / not-applicable
detailRegionCoverage：pass / partial / missing / failed / blocked / not-applicable，证据：
backendApiReadiness：`closed` 需要 `implementationStatus=completed + runtimeAvailability=verified + runtimeEvidence`；CTS 仅完成代码时为 `partial + implementation-complete-runtime-unverified`
productionReplacementTrigger：pending / triggered / completed / blocked / not-applicable
pendingReplacementItems：[]
状态分组建议：
- 运行态未验证：无 / reachable=unknown、usable=unknown、manualVerificationRequired=true、页面自测清单
- 生产替换未闭合：无 / API、route/menu/permission/title/i18n、LOV/lookup、导入导出、附件等 pending replacement
- 并行汇合待判定：无 / backendApiReadiness 与 queryMode/productionReplacementTrigger/pendingReplacementItems 的关系
targetPlacementVerification：pass / failed / blocked / not-applicable
pageLayoutScrollVerification：pass / failed / blocked / not-applicable
tableToolbarSurfaceCheck：pass / failed / blocked / not-run / not-applicable
Handoff 门禁：通过 / 有条件 / 阻塞 / 用户确认
Handoff 接受来源：无 / 用户已接受非默认条件性交付 / not-applicable / environment-prerequisite-notice
verificationCostTelemetry：queueWaitMs / owningVerificationMs / commandDiscoveryMs / v0Ms / v1Ms / repairHandoffMs / rerunMs / commandRunCount / reusedCommandCount / invalidatedCommandRunCount / retryCount 必须为数值；retryCount>0 时必须有 retryReason
costGovernanceStatus：verified / unverified（unverified 仅为 report-only downgrade）
verificationCostAnomaly：verification-over-budget / none
verificationCostAction：reuse-only / failure-package / environment-blocked / stop-expansion / continue-within-budget
verificationScopeExpansionAllowed：true / false

## Verification Reuse
| item | value |
| --- | --- |
| verificationScopeFingerprint | hash(changedFilesHash + command + validatorTarget + packageDir + mockNamespace + envKey) / missing |
| changedFilesHash |  |
| command |  |
| validatorTarget |  |
| packageDir |  |
| mockNamespace |  |
| envKey |  |
| sourceVerificationReportPath | `sdd-workspace/changes/{change-id}/frontend/verification/verification-report.md` / none |
| reuseStatus | new-run / reused / invalidated / not-applicable |
| invalidationReason |  |
| resultJsonPath | `sdd-workspace/changes/{change-id}/frontend/verification/verification-result.json` / not-written + reason |
| aggregatedFrom | command ids / validator ids / manual checklist ids |
| validatorsSynced | true / false / not-applicable |

规则：同一指纹且 source report 可读时，只复用命令级 validator/build/typecheck 结果；页面运行态观察不得复用为 passed，只能复用为 checklist、历史观察或 not-run reason。
规则：若写入 `resultJsonPath`，必须同步 `aggregatedFrom`；存在 `validators` 对象时 `validatorsSynced=true`，并由聚合脚本写入 `repairCanonicalState` 与 `canonicalState.schemaVersion/sourceType/frontendAutoRunId/status/repairDispatchStatus/repairClosureHash`。repair canonical fields 必须复用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py --repair-closure-stage-result <frontend-stage-result.json>` 的同一确定性逻辑，不能手算；helper 为 open/invalid 时聚合失败，只修 repair/status source，不重跑已通过命令。Handoff preflight 直接读取该对象，不接受手写 observed/sync 状态；Handoff 优先读取该 JSON，不回读完整命令日志。推荐用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/aggregate_frontend_verification_result.py --stage-result <frontend-stage-result.json> --out frontend/verification/verification-result.json` 生成。

## 工程证据
| item | value | evidence |
| --- | --- | --- |
| 执行目录 |  |  |
| 包管理器 / scripts |  |  |
| 依赖就绪状态 | ready / missing-node-modules / workspace-link-missing / resolver-failed / unknown | 缺依赖时写用户提示、依赖型命令未运行范围和前端服务提示；不得归因为业务代码失败 |
| workspaceResolverStatus | passed / failed-missing-dependencies / failed-link-missing / failed-name-mismatch / failed-but-build-passed / not-run | 记录 `require.resolve('<module>/package.json')` 分类结果；build 已通过时 resolver 失败只能作为风险，不覆盖 buildable |
| 最终编译命令 | HZEROJS Umi 子模块固定 `npm run build:ms -- <module>` / not-run + reason | 不接受 yarn、pnpm 或其它 build 命令替换；缺根 `build:ms` script 时写 `missing-required-build-ms-script` |
| 目标页面路径 |  |  |

## 缺依赖用户可见提示

目标前端工程未安装依赖时，必须在报告靠前位置输出以下结构；不得要求用户当前运行 build，不得把 `build:ms` 或页面运行态验证作为缺依赖场景的主要下一步。

```text
用户提示：目标前端工程依赖未安装，本轮跳过依赖型 lint/typecheck/build。
已继续完成 V0 静态检查和工程契约对账。

依赖就绪状态：missing-node-modules
buildable：unknown，未运行 build；原因 blocked-by-missing-dependencies
验证结果：partial
交付状态建议：conditional
reachable：unknown，未运行页面运行态专项验证
usable：unknown，未运行页面运行态专项验证
manualVerificationRequired：true
是否 runnable：未证明 runnable

下一步：
安装依赖后，请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面。
```

## Target Placement Verification
| item | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| placementType | new-package / existing-package / parent-src-page / integration-only / not-applicable |  | Target Placement Contract | pass / failed / blocked / not-applicable |
| packageDir / businessDomain / pageGroup / pageDir / routePrefix | confirmed or not-applicable |  | Target Placement Contract / File Mapping | pass / failed / blocked / not-applicable |
| packageInternalAmbiguity | none / not-applicable |  | Target Placement Contract / Evidence | pass / failed / blocked / not-applicable |
| evidenceStatus / userConfirmStatus / confirmationSource | ready + confirmed or not-applicable |  | Target Placement Evidence / Contract | pass / failed / blocked / not-applicable |
| parentSrcWritePolicy | registration-only / forbidden / allowed-with-reason / not-applicable |  | File Mapping | pass / failed / not-applicable |
| businessChangedFiles / parentRegistrationFiles | placement compliant |  | changedFiles / task-status | pass / failed / not-applicable |
| violatedFiles | none |  |  | pass / failed / blocked |

## HZERO Page Layout / Scroll Verification
| item | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| pageRoot | HZERO `Header` 与 `Content` 结构符合 UI runtime gate |  | changedFiles / JSX / DOM | pass / failed / blocked / not-applicable |
| businessContainer | 页面业务容器和样式边界在 `Content` 内或有项目证据 |  | JSX / CSS / baseline evidence | pass / failed / not-applicable |
| scrollContainer | 长内容可滚到底部，固定区不遮挡内容 |  | runtime-manual/screenshot/DOM | pass / failed / not-run / not-applicable |
| detailLineTableHeight | 详情/头行明细 Table 高度策略符合 UI runtime gate |  | changedFiles / DOM / UI Contract | pass / failed / not-run / not-applicable |
| bottomScrollStability | 小视口和长内容下滚动稳定 |  | runtime-manual/screenshot/video | pass / failed / not-run / not-applicable |

## Table Toolbar Surface Check

| item | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| sourceRegions | `table-toolbar` / 明细表列表头按钮区 / 表格工具栏来源 |  | UI Contract / Button Semantic Matrix | pass / failed / not-applicable |
| buttonIdsOrLabels | 来源按钮逐项列出 |  | design/task/source text | pass / failed / not-applicable |
| buttonsArrayVariables | 按钮数组变量可定位 |  | changedFiles / static evidence | pass / failed / not-run / not-applicable |
| tableButtonsPropEvidence | `<Table buttons={...}>` 或项目 confirmed wrapper |  | changedFiles / DOM / wrapper evidence | pass / failed / not-run / not-applicable |
| headerChildrenHits | 表格工具栏按钮不得出现在 Header children |  | changedFiles / DOM | pass / failed / not-run / not-applicable |
| externalToolbarHits | 不得以 Table 上方独立 DOM toolbar 替代 `Table.buttons` |  | changedFiles / DOM | pass / failed / not-run / not-applicable |

## HZERO Choerodon Production Compliance Verification
| item | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| queryMode | production-transport / mock-request / partial / blocked |  | task/design/Network | pass / partial / failed / blocked |
| activeParentRegistries / parentRegistration | active registry 已识别且当前模块注册闭合 |  | config / packages-config / workspace | pass / partial / failed / blocked / not-applicable |
| submoduleRuntime | registerRegex、config.dev.ts、route config、package scripts 按 runtime gate 闭合 |  | package config / route config | pass / failed / blocked / not-applicable |
| permissionCoverage / i18nCoverage | 适用动作和文案覆盖或有 replacement |  | manifest / changedFiles / locale | pass / partial / failed / not-applicable |
| valueSetLovLocalOptions / dependencyDrift | 本地 options、LOV、依赖漂移已归因 |  | manifest / replacement / git diff | pass / partial / failed / blocked / not-applicable |
| complianceState | 四态之一 |  | 本表汇总 | production-compliant / production-candidate / mock-demo-compliant / non-compliant |

## Frontend Compliance Manifest Verification
| gate | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| manifestPath | 命中门禁时存在 manifest |  | design / task-status / artifact-index | pass / failed / blocked / not-applicable |
| serviceRequestContract / runtimeDataEntryContract / queryModeBoundary | 合同闭合或 replacement/blocker 明确 |  | manifest / service / DataSet / mock | pass / partial / failed / blocked / not-applicable |
| listQueryContract / fieldUsageMatrix / detailRegionCoverage | 列表、字段、详情区域覆盖闭合 |  | manifest / UI Contract / changedFiles / browser | pass / partial / failed / blocked / not-applicable |
| actionEntryMatrix / buttonSemanticMatrix / buttonPermissionContract | 动作、按钮语义、权限闭合 |  | manifest / UI / Network / changedFiles | pass / partial / failed / blocked / not-applicable |
| i18nCoverage / lovLookupBindingContract | i18n、LOV/lookup 覆盖或 replacement 明确 |  | manifest / locale / DataSet fields | pass / partial / failed / blocked / not-applicable |
| componentApiProvenance / modalLifecycleContract / componentTypeContract | 组件来源、弹层生命周期和字段组件闭合 |  | manifest / changedFiles / static scan / browser | pass / partial / failed / blocked / not-applicable |
| hzeroCommonComponentContract / attachmentContract / importExportContract / rowActionContract | 专项能力 gate 闭合 |  | manifest / changedFiles / browser | pass / partial / failed / blocked / not-applicable |
| routeRedirectGate / generatedCodeStaticGate | route 与静态质量 gate 通过或阻塞明确 |  | route config / review / static scan | pass / partial / failed / blocked / not-applicable |
| missingOrBlockedGates | production-ready 时为空 |  | 本表汇总 | pass / failed / blocked |

## Affected Static Gate Scan
| item | value |
| --- | --- |
| scanMode | verification-v0 / fix-package-recheck / final-delta / not-run |
| validatorCommand | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_c7n_component_api_ast_grep.py --root <frontend-root-or-packageDir>` / `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_i18n_locale_ledger.py --root <frontend-root-or-packageDir> --manifest <manifest-or-handoff>` / manual-scan / not-run |
| validatorTarget | `<frontend-root-or-packageDir>` / changedFiles / targetFiles / not-applicable |
| checkedFiles | [] |
| riskDomains | [] |
| rulesChecked | [] |
| rulesHit | [] |
| newRiskDomains | [] |
| targetFilesEnough | true / false / not-applicable |
| issueCount | 0 |
| result | pass / failed / blocked / not-run / not-applicable |
| notRunReason |  |

规则：V0 静态扫描运行后必须填本节，并把 `rulesHit[]` 同步到对应 validator 字段；具体 ruleId 和严重级别以 `frontend-validator-rule-index.md` 为准。若本节用于 `recommendedFixPackage` 或 `rootCauseTrace` 的返修依据，必须写 `riskDomains[]`、`newRiskDomains[]` 和 `targetFilesEnough`，并按 `frontend-context-handoff-control.md#Required Validator Auto Repair Matrix` 与 `frontend-validator-fix-routing.md` 判断 `repairMode`、`repairBudgetClass`、`consumesRepairBudget` 以及应走 `direct-fix` 还是 `owner-needed`。纯 validator/result schema/evidence 缺口固定 `repairMode=evidence-backfill + consumesRepairBudget=false`，不得建立 `repairDispatch`；`newRiskDomains[]` 非空、`targetFilesEnough=false`、需要新增契约或扩大写入范围时不得生成自动代码修复包；不得只因 `severity=blocking` 把修复入口绑定到 Implementation。

## Mock Request Verification
| item | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| queryMode / mockApiRequestVerified | mock demo 必须为 `mock-request`；运行态请求证据只消费外部 runtime acceptance |  | contract / external runtime evidence | pass / failed / not-run-in-verification / not-applicable |
| networkMockApiUrl / origin / path / method / bodyOrQuery | 若有外部 Network 或 HTTP smoke，记录真实 devServer mock API |  | external browser Network / external HTTP smoke | pass / failed / not-run-in-verification / not-applicable |
| targetPlacement / buildEntry | 父工程托管、Target Placement 和 build 入口来源明确 |  | placement evidence / build scripts | pass / failed / not-run / not-applicable |
| requestEntryEvidence | DataSet/request adapter/service-action 触发链路静态可追溯；运行态触发只消费外部证据 |  | changedFiles / external runtime evidence | pass / failed / not-run-in-verification / not-applicable |
| middlewareRegistration / mockPluginSourceCheck | mock middleware 和 plugin 源码接线闭合 |  | changedFiles / parent config evidence | pass / failed / not-run / not-applicable |
| responseShape / serviceMiddlewarePathConsistency | 响应结构和路径一致 |  | changedFiles / contract / external runtime evidence | pass / failed / not-run-in-verification / not-applicable |
| stateTransitionVerified / runtimeStoreConsistency / stateTransitionGuard | 有状态动作运行态一致性只消费外部 runtime acceptance；代码守卫可静态记录 |  | external runtime evidence / changedFiles | pass / failed / not-run-in-verification / not-applicable |

## Mock To Production Switch Verification
| item | expected | actual | evidence | result |
| --- | --- | --- | --- | --- |
| resourcePath / servicePrefix | 资源路径和真实 API 前缀分离且来源明确 |  | contract-check / evidence / changedFiles | pass / partial / failed / not-run / not-applicable |
| servicePrefixHelper / switchEnvVar | helper 和切换变量闭合 |  | changedFiles / env / external smoke evidence | pass / failed / not-run / not-applicable |
| mockPrefixUrl / productionPrefixUrl | mock 和 production URL 均可追溯 |  | changedFiles / external Network or HTTP smoke | pass / failed / not-run-in-verification / not-applicable |
| sharedBaseUrl | 列表、详情、动作从同一 baseUrl 派生 |  | service/DataSet source / external Network evidence | pass / failed / not-run-in-verification / not-applicable |
| demoVerifiedGate | replacement checklist ready 且必填项通过 |  | 本表汇总 / production replacement checklist | pass / failed / blocked / not-applicable |

## 已运行命令
| 等级 | 命令/动作 | 结果 | 证据 | evidenceCapsule / 说明 |
| --- | --- | --- | --- | --- |
| V0 | 静态扫描 | not-run | - | - |
| V1 | lint | not-run | - | - |
| V2 | typecheck | not-run | - | - |
| V4 | build | not-run | - | build 未运行，不能声明产物态可交付 |
## 手工测试清单
- 前端服务提示：请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面。
- 访问路径：
- checklistPath：`sdd-workspace/changes/{change-id}/frontend/verification/manual-checklist.md` / not-persisted + reason
- 列表首屏数据：未验证
- 查询/重置/分页：未验证
- 详情跳转：未验证
- 手动刷新：未验证
- console/network 错误：未验证

## 页面区域行为验证矩阵
| 页面 | 区域/行为 | expected | actual | evidence | result | unverifiedReason |
| --- | --- | --- | --- | --- | --- | --- |
| 列表 | 查询、重置、分页、工具栏、行操作 | 按 Design Coverage Ledger 和 manifest gate 验收 | not-run | - | not-run | 页面运行态未运行 |
| 详情 | Header、基本信息、Tabs、明细表、附件、保存后 route | 按 Detail Region Coverage 和 UI runtime gate 验收 | not-run | - | not-run | 页面运行态未运行 |
| 弹层 | 打开、关闭、保存后关闭、长值可读性 | 按 Modal Lifecycle Contract 验收 | not-run | - | not-run | 页面运行态未运行 |
| 数据链路 | mock-request / production-transport / runtime store | 按 Mock Request Verification 验收 | not-run | - | not-run | 页面运行态未运行 |
| 专项能力 | HZERO 通用组件、附件、导入导出、row actions | 按 owning reference 验收 | not-run | - | not-run | 页面运行态未运行 |

## 失败反馈
- 无 / 待填写

## manualFindings
| issueId | category | severity | evidence | fixedBy | status |
| --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | none |

## uiRegression
| 区域 | expected | actual | source | fixedBy | status |
| --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | none |

## 未验证项
- 待填写

## 判定说明
- 目标前端工程缺 `node_modules`、workspace link 未安装或 resolver 因未安装依赖失败时，属于验证环境前置未满足；依赖型 lint/typecheck/build 写 `not-run + blocked-by-missing-dependencies`，`buildable=unknown`、`reachable=unknown`、`usable=unknown`、`是否 runnable=未证明 runnable`，并按“缺依赖用户可见提示”输出固定下一步：`安装依赖后，请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面。` 不得写 `buildable=false`，不得把 `Can't resolve 'choerodon-ui/pro'` 等包解析失败直接归因为 Choerodon import 缺陷，不得要求用户当前运行 build；安装依赖后仍失败时才按真实 build/typecheck 错误归因。
- `require.resolve('<module>/package.json')` 是 workspace/link 证据，不是业务页面代码证据。若 `build:ms -- <module>` 已实际通过但 resolver 检查失败，`buildable` 保持 `true`，`workspaceResolverStatus=failed-but-build-passed`，未验证项写执行目录、package name、root `workspace:*` 依赖或 link 刷新风险；不得因此生成 Implementation 页面修复包。若 package name、root dependency、workspace 配置或父工程 registry 确认缺失/冲突，才作为 scaffold/integration 缺口回 Implementation 修复。
- 默认 `demo-slice` / mock demo / `minimum-codable` 且用户未要求 production-ready 或完整验收时，缺外部页面运行态证据不触发用户确认；写 `reachable=unknown`、`usable=unknown`、`manualVerificationRequired=true`、`是否 runnable=未证明 runnable`、`验证结果=partial`、`交付状态建议=conditional`、`done=false` 和前端服务提示。不得为了补齐页面运行态证据主动调用页面级验证 question。
- build 成功只能证明 `buildable=true`，不能推导 `reachable=true` 或 `usable=true`。
- `production-ready` 必须同时满足 Review、Verification、targetPlacement、productionCompliance、complianceManifest、replacement 和 blockers 的汇合条件；细则以 `schema-runtime-gates.md#Merge Status Gates` 为准。
- `reachable=true` 和 `usable=true` 必须有可运行证据；mock demo 还必须通过 Mock Request Verification。
- `backendApiReadiness.status=closed + runtimeAvailability=verified` 只表示后端可用于替换，不等于前端已完成 production transport；CTS 仅完成代码或运行可达性未验证时不得进入真实 transport。
- 任一适用 compliance gate 为 failed/blocked/missing 时，不得声明 `production-ready`；任一核心页面区域未验证时，不得声明 `usable=true`。
- 用户接受降级交付时，必须记录 Handoff 接受来源；`code-only` 不是合法验证结论。

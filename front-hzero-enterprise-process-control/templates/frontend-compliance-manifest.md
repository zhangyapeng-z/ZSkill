# Frontend Compliance Manifest Template

建议路径：`sdd-workspace/changes/{change-id}/frontend/design/frontend-compliance-manifest.md`

用途：作为 HZERO + Choerodon 新增/改造页面的跨阶段合规清单。Design 生成初版，Task Breakdown 映射到任务验收，Implementation 回写偏差，Review/Verification/Handoff 按同一清单判断交付状态。

manifest gate 的准入、owner 和模板边界见 `references/frontend-compliance-manifest-governance.md`。专项 gate 细则以 `hzero-choerodon-production-compliance-gate.md`、`frontend-ui-runtime-gates.md`、`generated-code-static-quality-gate.md` 和对应 owning reference 为事实源；本模板只保留状态、证据和修复阶段。

## 使用规则
- 只有影响 `production-compliant / production-candidate / mock-demo-compliant / non-compliant` 判断的稳定 gate 才进入本清单。
- gate 细则写在 owning reference；本模板只记录状态、阻塞原因、修复阶段和证据入口。
- 缺少适用项时必须写 `missing / blocked / not-applicable + reason`。
- 用户可见标题和表头可使用 `中文显示名（englishKey）`；gate 名、字段 key、枚举值、ownerReference、gateId 和 ruleId 保持英文原值，避免跨阶段引用和 validator 证据失配。

## Document Status
- 功能（Feature）：
- 功能根目录（Feature Root）：
- 前端根目录（Frontend Root）：
- 设计来源（Design Source）：`frontend/design/frontend-design.md`
- 契约检查（Contract Check）：`frontend/design/contract-check.md`
- 合规清单（Compliance Manifest）：`frontend/design/frontend-compliance-manifest.md`
- 适用范围（Applies To）：HZERO + Choerodon page / package submodule / mock-demo / production replacement / not-applicable
- 合规状态（complianceState）：production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable
- 数据请求模式（queryMode）：production-transport / mock-request / partial / blocked / not-applicable
- 交付上限（handoffLimit）：production-ready / conditional / blocked
- 最近更新阶段（Last Updated Stage）：Design / Task / Implementation / Review / Verification / Handoff
- 可进入可运行实现（Can Enter Runnable Implementation）：yes / no + reason
- 可声明生产就绪（Can Claim Production Ready）：yes / no + reason

## Hard Gate Summary
| 门禁（gate） | 状态（status） | 阻塞原因（blockingReason） | 修复阶段（requiredFixStage） | 证据（evidence） | 规则来源（ownerReference） |
| --- | --- | --- | --- | --- | --- |
| serviceRequestContract | confirmed / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-enterprise-design / hzero-request-service-contract |
| runtimeDataEntryContract | confirmed / partial / missing / conflict / blocked / not-applicable |  | Design / Task / Implementation / Review |  | hzero-choerodon-production-compliance-gate |
| queryModeBoundary | pass / partial / failed / blocked / not-applicable |  | Design / Implementation / Verification |  | front-hzero-mock-request |
| activeParentRegistries | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | hzerojs-submodule-runtime-gate |
| parentPackageRegistryEntry | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review |  | hzerojs-submodule-runtime-gate |
| listQueryContract | pass / partial / missing / conflict / blocked / not-applicable |  | Design / Task / Implementation / Review / Verification |  | front-hzero-choerodon-ui scenarios/query-table |
| fieldUsageMatrix | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review |  | schema-field-contract-gates |
| fieldVisibilityMatrix | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Verification |  | schema-field-contract-gates |
| detailRegionCoverage | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review / Verification |  | frontend-ui-runtime-gates |
| styleNecessityContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review / Verification |  | frontend-ui-runtime-gates |
| masterDetailDataContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-choerodon-ui scenarios/master-detail |
| statusActionMatrix | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | hzero-choerodon-production-compliance-gate |
| actionEntryMatrix | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review |  | hzero-choerodon-production-compliance-gate |
| buttonSemanticMatrix | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | hzero-choerodon-production-compliance-gate |
| buttonPermissionContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-permission-button |
| i18nCoverage | pass / partial / missing / blocked / not-applicable |  | Design / Implementation / Verification |  | hzero-choerodon-production-compliance-gate / locale ledger validator |
| lovLookupBindingContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-choerodon-ui |
| componentApiProvenance | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review |  | front-hzero-choerodon-ui / generated-code-static-quality-gate |
| modalOpenPatternCheck | pass / failed / blocked / not-run / not-applicable |  | Implementation / Review / Verification |  | frontend-ui-runtime-gates |
| modalLifecycleContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review / Verification |  | frontend-ui-runtime-gates |
| typescriptRenderContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation / Review / Verification |  | front-hzero-renderer / front-hzero-choerodon-ui |
| componentTypeContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-choerodon-ui |
| routeRedirectGate | pass / failed / blocked / not-applicable |  | Design / Task / Implementation / Review / Verify / Handoff |  | front-hzero-route / hzerojs-submodule-runtime-gate |
| hzeroCommonComponentContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-common-components |
| attachmentContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-attachment |
| importExportContract | pass / partial / missing / blocked / not-applicable |  | Design / Task / Implementation |  | front-hzero-import-export |
| rowActionContract | pass / partial / missing / blocked / not-applicable |  | Design / Implementation / Review |  | front-hzero-choerodon-ui scenarios/row-actions / front-hzero-renderer |
| dependencyDrift | none / approved / user-owned / unapproved / unknown / not-applicable |  | Task / Review / Handoff |  | hzero-choerodon-production-compliance-gate |
| submoduleConfigValidator | pass / failed / blocked / not-run / not-applicable |  | Implementation / Verification / Handoff |  | hzerojs-submodule-runtime-gate |
| mockRequestValidator | pass / failed / blocked / not-run / not-applicable |  | Implementation / Verification / Handoff |  | front-hzero-mock-request |
| generatedCodeStaticGate | pass / failed / blocked / not-run |  | Implementation / Review |  | generated-code-static-quality-gate |

规则：任一适用 gate 为 `missing / blocked / failed / unapproved / unknown` 时，`Can Claim Production Ready=no`。`queryMode=mock-request` 最高只能 `mock-demo-compliant`，并必须存在 production replacement 清单。

## Service Request Contract
| item | value | status | source | implementationPolicy |
| --- | --- | --- | --- | --- |
| requestMode | hzero-request / project-helper / native-http-explicit / mock-request / blocked | confirmed / partial / missing / blocked / not-applicable |  |  |
| requestHelperImport |  | confirmed / missing / not-applicable |  |  |
| baseUrlStrategy | request-adds-api-host / explicit-api-host-required / dev-server-mock / unknown | confirmed / partial / missing |  |  |
| resourcePath | /v1/{organizationId}/... / not-applicable | confirmed / partial / missing / not-applicable |  |  |
| servicePrefix |  | confirmed / generatedCandidate / missing / not-applicable |  |  |
| switchEnvVar | <MODULE>_USE_MOCK / not-applicable | confirmed / missing / not-applicable |  | default mock; exact string false switches production |
| tenantContext | current-tenant / site / user-organization / not-applicable | confirmed / partial / missing / conflict |  |  |
| responseShape | page/content / rows/total / object / custom-adapter / unknown | confirmed / partial / missing |  |  |
| errorHandling | getResponse / project-helper / custom / missing | confirmed / partial / missing |  |  |

## DataSet And Field Usage Matrix
| field | canonicalField | runtimeFieldPolicy | storedField | renderedField | usedBy | ownerDataSetOrRecord | visibleIn | submitPolicy | dataSource | declaredIn | type | semanticClass | displayField | labelSource | componentPolicy | renderer | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | FDS/TDS/API canonical / not-applicable | canonical-only / not-applicable |  |  | queryField / listTableColumn / detailFormField / lineTableColumn / record.get / record.set / actionGuard / submitPayload / routeParam | headerDs / detailDs / lineDs / queryDs / record / not-applicable / missing | create/edit/copy/detail/approval/readonly visibility | include / exclude / display-only / not-applicable | API / DataSet fields / queryFields / UI Contract / generatedCandidate | file/section | string / number / currency / dateTime / object | master-data-lov / business-enum-lookup / attachment / audit-generated / date / amount / free-text / other |  | current-field / stored-field / explicit-props / i18n-key / missing / not-applicable | Lov / Select / Attachment / Output-display / TextField / generatedCandidate / missing | none / TagRender / project-renderer / custom | confirmed / generatedCandidate / missing / conflict / not-applicable |  |

## List Query Contract
| item | value | status | source | implementationPolicy |
| --- | --- | --- | --- | --- |
| queryAreaPolicy | required-filter / required-fuzzy / none-by-design / project-wrapper-confirmed / missing / blocked | confirmed / generatedCandidate / missing / conflict / not-applicable | UI Contract / FDS / TDS / Figma / user-confirmed |  |
| tableQueryBar | filterBar / project-wrapper / missing / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable | UI Contract / project evidence |  |
| fuzzyQueryRequired | true / false | confirmed / missing / not-applicable | FDS / TDS / Figma / user-confirmed |  |
| fuzzyQueryFields | field list / not-applicable | confirmed / missing / conflict / not-applicable | UI Contract / QueryDS / queryFields |  |
| queryFieldsLimit | number / project-default / not-applicable | confirmed / generatedCandidate / missing / not-applicable | UI Contract / project evidence |  |
| queryResetRefreshBehavior | query-first-page / reset-clear-first-page / refresh-keep-page | confirmed / missing / not-applicable | UI Contract / project evidence |  |

## Detail Region Coverage
| region | requiredItems | owner | implementationSurface | confirmPolicy | asyncLoadingPolicy | status | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| header-buttons | save / submit / withdraw / cancel / back / other | Action Entry Matrix / Status Action Matrix / Button Contract | page header / toolbar / hidden-with-source | destructive confirm / not-required / not-applicable | action-level pending + repeat guard + finally release / not-applicable | pass / partial / missing / blocked / not-applicable |  |
| header-fields | required head fields, display-only fields, editable fields | Detail Contract / Field Usage Matrix | DataSet fields + Form name + visibleIn + expectedSurface + forbiddenSurface + requiredVisibleByDefault | pass / partial / missing / blocked / not-applicable |  |
| detail-tabs | tab ids / tab titles / no-tabs reason | Detail Contract / Figma / UI Contract | Tabs.TabPane / project tabs / not-applicable + tabsScope + expectedSurface + forbiddenSurface | pass / partial / missing / blocked / not-applicable |  |
| line-filter | line query fields / reset behavior / query trigger | Master Detail Data Contract / List Query Contract | lineQueryDS + queryFields + queryBar | pass / partial / missing / blocked / not-applicable |  |
| save-route-context | headerId/id route补齐 / view-edit path / query cleanup | Route Context / Edit Mode Contract | history/openTab/router update after save | pass / partial / missing / blocked / not-applicable |  |

## Style Necessity Contract
| target | layoutNeed | componentFirstDecision | styleFilePolicy | styleScope | fileMapping | reason | source | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| page / content / section / form / table / modal / drawer / line-table / other | page-skeleton / spacing / scroll-boundary / background / fixed-height / responsive / visual-state / none | component-props-sufficient / existing-project-class-sufficient / style-required / unknown | no-new-style / reuse-existing-style / modify-existing-style / new-local-style / block-and-confirm | none / Content-inner-only / section-only / table-container-only / modal-body-only / other | no-file / existing-file / new-style-file / not-applicable |  | Figma / UI Contract / project baseline / HZERO runtime gate / user-confirmation / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable |  |

## Master Detail Data Contract
| item | value | status | source | implementationPolicy |
| --- | --- | --- | --- | --- |
| headerPrimaryKey / linePrimaryKey / headerLineForeignKey |  | confirmed / generatedCandidate / missing / not-applicable |  |  |
| lineDataMode | embedded-local-lines / line-query-transport / mixed / missing | confirmed / generatedCandidate / missing / not-applicable |  |  |
| lineQueryDataSet | required / optional / forbidden / missing | confirmed / generatedCandidate / missing / not-applicable |  |  |
| headerRead / lineRead | DataSet transport / service action / mock request / blocked | confirmed / partial / missing / not-applicable |  |  |
| saveGranularity | header-cascade-lines / header-only / line-separate / blocked | confirmed / partial / missing / not-applicable |  |  |
| lineDeleteMode | local-remove-before-save / replace-all-on-save / service-delete / mixed / missing | confirmed / partial / missing / not-applicable |  |  |
| handPayloadPolicy | dataset-submit / shared-payload-builder / generatedCandidate-normalizer / blocked | confirmed / generatedCandidate / missing / not-applicable |  |  |

## Status Action Matrix
| action | statusField | statusEnumMap | sourceStatus | visibleWhen | enabledWhen | disabledReasonSource | disabledTooltipPolicy | actionGuard | serviceAction | mockHandler | successTargetState | refreshTarget | failureHandling | permissionCode | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| create / save / save-lines / submit / withdraw / cancel / delete-header / header-import / header-export / lineAdd / lineDelete / line-import / line-export | authorizationStatus / status / not-applicable | code=meaning/color/source |  |  |  | source text / helper / missing / not-applicable | Tooltip / title / project-wrapper / not-required / missing / not-applicable |  |  |  |  | list / detail / lineTable / none |  |  | confirmed / generatedCandidate / missing / conflict / not-applicable |

## Button Permission Contract
| action | actionExistsSource | sourceRegion | chosenEntryLocation | entryStatus | uiArea | semanticKind | navigationTarget | businessMutation | statusActionRef | permissionRequirement | permissionCode | codeStatus | visibleSource | enabledSource | disabledReasonSource | disabledTooltipPolicy | selectionReactivePolicy | notApplicableReason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | FDS / TDS / API / status-flow / Figma / project evidence / user-confirmation | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | Header / toolbar / row-action / detail-header / table-toolbar / line-row / import / export / attachment / hidden / not-confirmed | confirmed / generatedCandidate / needs-confirmation / missing / conflict | page-header / page-toolbar / table-toolbar / row-action / modal-footer / other | navigation / business-state-action / data-edit / table-operation / import-export / attachment / other |  | none / creates / updates / deletes / status-change / import-export / upload |  | required / not-applicable / unknown |  | confirmed / generatedCandidate / missing / conflict |  |  | source text / helper / missing / not-applicable | Tooltip / title / project-wrapper / not-required / missing / not-applicable | DataSet select-events / React state / project-wrapper / not-required / missing |  |

## LOV Lookup Binding Contract
| field | semantic | codeType | code | codeStatus | valueField | textField | bind | displayField | submitField | lovParaRequired | lovParaMode | paramName | paramSourceField | paramSourceExpression | sourceTiming | emptyValueBehavior | cascadeClearPolicy | confirmedSource | replacementRequired |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | employee / department / organization / supplier / customer / item / status / type / free-text / other | lovCode / lookupCode / local-options / not-applicable |  | confirmed / generatedCandidate / missing / conflict / not-applicable |  |  |  |  |  | required / not-required / unknown / not-applicable | none / static / dynamicProps / missing / not-applicable |  | current record field / query field / route context / tenant context / missing / not-applicable | `record.get('field')` / queryDataSet current / context value / missing / not-applicable | before-query / parent-change / record-create / route-enter / not-applicable / missing | block-query / pass-empty / clear-child / prompt-user / not-applicable / missing | clear-dependent-fields / keep-existing / prompt-user / not-applicable / missing | FDS / TDS / API / UI Contract / project evidence / user-confirmed / missing | yes / no |

规则：后端 `@LovValue` / 平台值集术语进入前端前，必须在本表按前端组件语义落成 `codeType=lovCode / lookupCode / local-options`，并记录 `semantic/code/source/confirmedSource`；若设计映射表、编码候选表和 DataSet 示例对同一字段的 `codeType` 不一致，`lovLookupBindingContract` 必须为 `conflict/blocked`，不得进入 runnable production implementation。父子级联、组织/租户/公司/岗位范围、供应商/客户业务类型过滤、查询区与表格编辑区参数来源不同、同一 `lovCode` 多处过滤条件不同，`lovParaRequired` 必须为 `required` 或写明 `not-required + source`。缺 `paramName/paramSourceField/sourceTiming/emptyValueBehavior/cascadeClearPolicy/confirmedSource` 时，`lovLookupBindingContract` 最高为 `partial/missing`，只能进入 replacement / handoff risk，不得声明 production-ready。主数据语义字段使用 `lookupCode` 或绑定无关状态/类型值集编码时，不能写 pass；应记录 conflict/failed 和修复目标。

## Component Type Contract
| field | semantic | requiredComponent | implementedComponent | status | source |
| --- | --- | --- | --- | --- | --- |
|  | date / amount / quantity / ratio / attachmentUuid / master-data-lov / business-enum-lookup / text | DatePicker / DateTimePicker / NumberField / Currency / Attachment / Lov / Select / TextField / Output-display |  | confirmed / generatedCandidate / missing / conflict / not-applicable |  |

## I18n Coverage
| area | usedIntlKeys | hardcodedUserCopy | assetPath | coverage | pendingKeys |
| --- | --- | --- | --- | --- | --- |
| route-title / page-title / query-fields / table-columns / form-fields / buttons / confirms / notifications / validation / sections / modal-drawer / tabs / record-table-fields / empty-state |  |  | `platform-locale-keys.json` / HZERO `/hpfm/prompt` / confirmed 项目公共 locale | pass / partial / missing / not-applicable |  |

## Platform Locale Keys
| key | defaultMessage | platformStatus | platformSource | evidence |
| --- | --- | --- | --- | --- |
|  |  | confirmed / pending | HZERO `/hpfm/prompt` / platform export / user confirmation / generated scaffold |  |

规则：新生成 HZERO 业务 key 默认进入平台多语言清单，不生成未被目标工程加载的本地 locale 源文件。`pending` 只表示 key 已进入 ledger，`i18nCoverage` 仍为 partial/missing；只有逐 key `confirmed` 且有平台来源证据时才可计入 pass。目标工程明确加载本地 locale 时可保留 legacy 资产，但不能与平台译文双写后分别维护。

## Attachment Contract
| item | value | status | source |
| --- | --- | --- | --- |
| attachmentComponentMode | Attachment / Attachment.Dragger / project-wrapper / Upload fallback / missing / not-applicable | confirmed / generatedCandidate / missing / blocked / not-applicable |  |
| importPath / exportShape / importUsage |  | confirmed / missing / not-applicable |  |
| attachmentField / valueStructure |  | confirmed / generatedCandidate / partial / missing / not-applicable |  |
| bucketName / bucketDirectory / storageCode |  | confirmed / generatedCandidate / missing / not-applicable |  |
| contractValueCarrier | constants / wrapper-props / replacement-only / missing / not-applicable | confirmed / generatedCandidate / missing / not-applicable |  |
| previewDownloadRemove | component-managed / service-contract / missing / not-applicable | confirmed / partial / missing / not-applicable |  |

## HZERO Common Component Contract
| component | importPath | hzeroFrontVersion | bindingMode | valueOrUploadProtocol | attachmentConfig | runtimeStatus | replacementRequired |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ChunkUploader / NewRichTextEditor / RichTextViewer / project-wrapper / not-applicable |  | confirmed / generatedCandidate / missing | upload-button / controlled / dataset-field / viewer / project-wrapper / not-applicable | confirmed / generatedCandidate / missing / blocked / not-applicable | importPath / exportShape / targetProp / wrapperApi / not-applicable | not-run / partial / verified / blocked | yes / no |

## Import Export Contract
| capability | componentMode | entryWrapperPolicy | endpointOrTemplate | params | permissionCode | tenantContext | parentIdPolicy | unresolvedParentBehavior | invalidPlaceholderPathPolicy | refreshTarget | status | replacementRequired |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| header-import / header-export / line-import / line-export | standard-component / project-wrapper / missing / blocked / not-applicable | standard-component-direct / project-wrapper / custom-modal-confirmed / blocked / not-applicable |  | query / body / path / selectedRows / parentId |  |  | required / optional / forbidden / not-applicable | hidden / disabled-with-reason / blocked / not-applicable | forbidden / generatedCandidate-risk / not-applicable | list / lineTable / none | confirmed / generatedCandidate / partial / missing / blocked / not-applicable | yes / no |

## Row Action Contract
| table | actions | actionLabels | sourceRegions | statusGuards | disabledReasonPolicy | permissionCodes | destructiveConfirm | asyncLoadingPolicy | repeatClickGuard | finallyReleasePolicy | refreshTarget | rendererPolicy | operatorPayload | rowButtonTypePolicy | overflowPolicy | operationColumnPolicy | baselineDecision | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | detail/edit/delete/submit/withdraw/other | sourceText/exact-source or override | 列表行按钮区 / 明细表行按钮区 / generatedCandidate / not-applicable | visible/enabled/actionGuard source | disabledReasonSource + Tooltip/title/project-wrapper / not-required / missing | per action | delete/withdraw/cancel/void confirm policy | row-level / batch-level / action-level pending / not-applicable | disabled / handler-guard / both / not-applicable | try-finally / promise-finally / wrapper-guaranteed / not-applicable | list/detail/lineTable/none | c7nOperatorRender / operatorRender / single-direct-render / project-override / missing | key-ele-len-title + filtered / project-override / missing | row-actions-text / project-override / drift / missing | helper-overflow / dropdown / not-applicable | last-column + right-lock / conditionally-hidden / missing | golden-baseline / project-compatible / follow-baseline / legacy-risk / anti-pattern / unknown-quality / not-applicable | pass / blocked / missing / not-applicable |

## Static Gate Result
| check | result | evidence | fixStage |
| --- | --- | --- | --- |
| hardcoded i18n / generated constants / local-filter / component API / attachment / import-export / row actions / dependency drift | pass / failed / blocked / not-run |  | Implementation / Review / Verification |

## Production Replacement Items
| item | current | requiredProductionValue | owner | status |
| --- | --- | --- | --- | --- |
| API / permission / i18n / lov / lookup / attachment / import-export / mock-runtime-path / status-machine / active-registry / dependency-drift |  |  | frontend / backend / platform / user | open / pending / closed / not-applicable |

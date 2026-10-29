# Schema Field Contract Gates

用途：承接 `templates/schema-checklist.md` 中字段级 contract 的长规则，特别是 route/open interaction、field/editability/visibility、style necessity、component/type/provenance 等。`schema-checklist.md` 只保留字段名、最小值域和回退动作。

## 阅读路由
- 需要判断 route/open interaction/page mode 字段怎么收口时读 `Route And Interaction Fields`。
- 需要判断 field/editability/visibility/empty-state 字段怎么收口时读 `Field And UX Fields`。
- 需要判断 style/component/enum/type/provenance 字段怎么收口时读 `Component And Style Fields`。
- 需要判断哪些细则应继续回到 design/runtime/compliance reference 时读 `Owning References`。

## Route And Interaction Fields

以下字段的细则以本节、`front-hzero-enterprise-design` 的 route context/edit mode 合同、`references/data-service-runtime-gates.md`、`references/frontend-ui-runtime-gates.md` 和 `references/schema-runtime-gates.md` 为准：

- `routeOpenMode`
- `detailViewInteractionMap`
- `parentTabKey`
- `targetDetailPath`
- `reusableTabContextPolicy`
- `navigationApi`
- `tabTitle`
- `routeMode`
- `queryStateKey`
- `routeContext`
- `pageMode`
- `editableAuthority`

最低要求：

- route/open interaction 的合法值、来源、是否已确认和是否可 runnable，必须由设计契约或 question gate 支撑。
- `menu-current`、`hzero-openTab-path-params`、`hzero-openTab-reusable-fixed-path`、`dynamic-tab`、`browser-new-tab` 不能靠实现阶段自行决定。
- `hzero-openTab-path-params` 只能证明 create/view/edit route path 可匹配，不能单独证明详情页签复用；若要声明可复用，必须有运行态页签数量证据或改用 `hzero-openTab-reusable-fixed-path`。
- `hzero-openTab-reusable-fixed-path` 必须补齐 `reusableTabContextPolicy`：固定 create path、固定 detail path、context 来源、写入时机、刷新/聚焦更新机制、缺 context 降级、标题同步和保存后跳转。缺该字段时不得进入 runnable implementation 或不得声明 reusable 已闭合。
- `routeContext` 是页面业务模式和编辑态的权威来源，不允许靠 `window.location.hash`、散落 query 解析或 DataSet 字段反向控制。

## Field And UX Fields

以下字段的细则以本节、`references/frontend-ui-runtime-gates.md`、`references/data-service-runtime-gates.md`、`references/hzero-choerodon-production-compliance-gate.md` 和 `templates/frontend-compliance-manifest.md` 为准：

- `fieldUsageMatrix`
- `fieldEditability`
- `fieldVisibility`
- `emptyDerivedFieldUx`
- `actionEntryMatrix`
- `semanticFieldClassification`
- `masterDetailModeContract`
- `attachmentContractCarrier`
- `placeholderRequestPathPolicy`

最低要求：

- 字段展示、编辑态、空态、派生态、状态动作入口和主从 contract 都必须有明确来源。
- `*Meaning/*Name/displayField` 展示字段必须有 label/display 来源。
- 审计/后端生成字段、附件 carrier、fake path policy、line query / line delete / payload contract 不能靠实现默认值闭合。

## Component And Style Fields

以下字段的细则以本节、`references/frontend-ui-runtime-gates.md`、`references/hzero-choerodon-production-compliance-gate.md`、`references/generated-code-static-quality-gate.md` 和对应专项 skill/reference 为准：

- `styleNecessityContract`
- `componentApiProvenance`
- `modalLifecycleContract`
- `enumProvenance`
- `typescriptRenderContract`
- `componentImportMapStatus`
- `enumImportMapStatus`
- `hzeroCommonComponentContract`
- `attachmentContract`

最低要求：

- 样式新增必须先证明组件 props 或既有样式不足。
- 组件 import、静态子组件、renderer/helper、enum-like props、render contract 都必须有来源。
- `Modal.open` / Drawer / 业务弹层的自定义关闭、保存后关闭、记录级导航和 update 行为必须记录 `closeApiSource` 与目标项目证据；记录级导航只指同一详情表面内业务主记录身份变化，分页、轮播、步骤向导、Tab/区块切换、附件/图片预览翻页不适用。无证据的 `modal.close()`、`Modal.close(key)`、`destroyAll` 或私有 close/update API 不能作为 pass。
- `as any`、未导入 symbol、无来源 enum/string 混用、无来源 renderer 形态、无来源 Modal close/update 都不能作为 pass。

## Owning References

当 `schema-checklist.md` 命中以下字段时，优先回看对应事实源，而不是继续向 checklist 内堆规则：

- route/edit mode：`front-hzero-enterprise-design` 的 route context/edit mode 合同
- request/service/runtime：`references/data-service-runtime-gates.md`
- UI / field / modal / layout / button：`references/frontend-ui-runtime-gates.md`
- production compliance：`references/hzero-choerodon-production-compliance-gate.md`
- generated code static gate：`references/generated-code-static-quality-gate.md`
- attachment / import-export / common components / renderer：对应专项 skill

# Frontend Validator Rule Index

用途：定义 hzero-spec 内置前端静态 validator 的 ruleId 到 gate、owner skill、fixture 和处理阶段的索引。新增或调整 C7N component API validator 规则时必须同步本文件或说明不适用原因。

## Gate Profile 与结果语义

- 支持 `--gate-profile` 的 validator 默认使用 `strict`，保持历史“任一 finding 即失败”的资产审计行为；`production-ready`、full audit、schema audit 和仓库 `audit/check` 必须使用默认值或显式 `--gate-profile strict`。
- `demo-slice` 与普通 `regular-change` 的阶段推进使用 `--gate-profile delivery`：`blocking/error/critical` 才阻断，`major/minor/warning/unverified/info/advisory` 保留在 `issues`，结果为 `passed=true + clean=false + advisory_count>0`，必须进入 Review/未验证项，但不得仅因此输出等待或把前后端并行改成串行。
- `severity` 决定门禁，`confidence`（若 rule 输出）只表示机械识别可信度，不得单独升级或降低门禁；缺 `confidence` 视为 `unknown`，不影响既有 severity。权限缺失、未解析 import、契约漂移、共享写冲突、占位实现、错误目标落点等仍必须是 blocking。
- 退出码 `0/1` 分别表示 selected gate passed、failed。只有退出码 `2` 与结构化 `status=not-run + notRunReason` 同时出现时才表示 not-run；`delivery` 可继续 conditional Handoff，`strict` 仍阻断。裸退出码 `2`、参数错误、非 JSON 异常或缺 reason 均按 failed 处理。聚合结果同时读取 `passed/clean/gate_profile/blocking_count/advisory_count`，不能只看 issue 总数。

## 目录

- C7N Component API Validator：Choerodon / HZERO 页面静态代码 rule 索引。
- HZERO Import/Export Permission Validator：导入导出标准组件权限放置和权限载荷 rule 索引。
- Integration Contract Smoke Validator：跨 slice / shared contract 产物消费 smoke rule 索引。
- LOV Candidate Contract / Contract Fidelity Validator：默认 mock/demo 候选 LOV 的 Design 冻结合同与 Implementation 消费一致性索引。
- Local Import Path Validator：生成源码的 source-root alias、相对路径和可解析性 rule 索引。
- Mock Request Validator：mock-request devServer / request 边界 rule 索引。

## C7N Component API Validator

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_c7n_component_api_ast_grep.py --root <frontend-root-or-packageDir>
```

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `c7n_component_api_ast_grep_unavailable` | validator runtime | `front-hzero-enterprise-process-control` | blocking | not-applicable | 优先定位 hzero-spec bundled ast-grep；也可用 `--sg`、`node_modules/.bin/sg` 或 PATH。仍不可用时只能 not-run 并降级 |
| `c7n_component_api_ast_grep_failed` | validator runtime | `front-hzero-enterprise-process-control` | blocking | not-applicable | 修复 validator 执行异常或记录 not-run 降级 |
| `c7n_component_api_foreign_prop` | componentApiProvenance | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/table-pollution.tsx` | 改回 C7N/confirmed wrapper API；若确为项目 confirmed API，补代码近邻结构化 `componentApiProvenance`，不得用文件级笼统声明放行；另见 `invalid/select-file-level-provenance-bypass.tsx` |
| `c7n_component_api_foreign_static_option` | componentApiProvenance | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/modal-upload-pollution.tsx` | 改回 C7N/confirmed static API；若确为项目 confirmed static API，补代码近邻结构化 `componentApiProvenance` |
| `c7n_pro_table_foreign_data_adapter` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table | blocking | `invalid/table-pollution.tsx` | 使用 `dataSet` / confirmed Pro wrapper |
| `c7n_dataset_datetime_direct_render_*` | `GCSQ-RENDER-001` | `front-hzero-renderer` | major | `invalid/datetime-direct-render.tsx` | 日期/时间字段先格式化为 string/ReactNode |
| `hzero_detail_collection_native_dom_without_fallback` | `GCSQ-DETAIL-COLLECTION-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/detail-collection-native-dom.tsx` | 表格型详情集合命中 `front-hzero-choerodon-ui` owner 规则，必须改用 Choerodon Pro Table；项目只读表格、薄 wrapper 和原生 table/list DOM 都不是合法 fallback |
| `hzero_detail_collection_contract_field_alias_shape` | `GCSQ-DETAIL-COLLECTION-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-design` | major/blocking by impact | `invalid/detail-collection-native-dom.tsx` | 集合列改回 MDS/TDS/API item 字段名；删除 alias、双 shape 和兼容 adapter |
| `c7n_table_buttons_page_toolbar_surface_mismatch` | buttonSemanticMatrix | `front-hzero-choerodon-ui` scenario:query-table | major | `invalid/page-toolbar-table-buttons.tsx` | page-toolbar 动作放 Header children，不放 Table.buttons |
| `c7n_table_toolbar_external_surface_mismatch` | buttonSemanticMatrix | `front-hzero-choerodon-ui` scenario:query-table | major | `invalid/table-toolbar-external-buttons.tsx` | table-toolbar 动作放 Table.buttons 或 confirmed wrapper |
| `c7n_table_querybar_missing_filterbar` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/table-querybar-missing-filterbar.tsx` | 查询需求证据存在时补 Table filterBar 查询形态，或补 `queryAreaPolicy=none-by-design + sourceRef/reason` |
| `c7n_table_querybar_not_filterbar` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/table-querybar-not-filterbar.tsx` | 默认改为 Table filterBar 查询形态；若设计/契约明确要求非 filterBar，记录同 mode 的 sourceRef/reason；代码必须使用 enum 形态 |
| `c7n_table_fuzzy_query_disabled` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/table-fuzzy-query-disabled.tsx` | required fuzzy search 时启用 `fuzzyQuery=true` |
| `c7n_table_querybarprops_invalid_fuzzy_query_field` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/table-fuzzy-query-field-prop.tsx` | 删除 `queryBarProps.fuzzyQueryField/fuzzyQueryFields`；字段映射保留在 QueryDS/queryFields 和 UI Contract `fuzzyQueryFields`，Table 只写 `fuzzyQuery` / `fuzzyQueryPlaceholder` |
| `c7n_table_querybarprops_unknown_prop` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/table-querybarprops-unknown-prop.tsx` | 删除未在 Choerodon UI Pro Table query bar typed surface 中确认的 `queryBarProps` key；确为项目 wrapper 扩展时补项目源码/类型/样例证据 |
| `c7n_table_filterbar_bypassed_by_external_form` | `HZUI-LIST-001` | `front-hzero-choerodon-ui` scenario:query-table/master-detail | major/blocking by impact | `invalid/detail-line-filter-form*.tsx` | 删除手写查询 Form，改用 QueryDS/queryFields/filterBar |
| `c7n_table_column_name_missing_dataset_field` | `GCSQ-CONTRACT-FIDELITY-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/table-column-missing-dataset-field.tsx` | 普通 Table `columns[].name` 补入绑定主 DataSet `fields`；`queryFields` 不能替代表格列字段元数据 |
| `c7n_asset_baseline_table_jsx_column_children` | `GCSQ-ASSET-TS-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/asset-baseline-table-jsx-column-children.tsx` | 常规列改为函数组件/自定义 Hook 内的 `useMemo<ColumnProps[]>` + `Table columns={columns}`；仅 confirmed wrapper、递归/运行时动态列或版本兼容约束可保留 JSX 子列，且代码近邻必须记录 `tableColumnComposition=jsx-children`、相对 validator root 可读取的 `sourceRef` 和 reason |
| `c7n_asset_baseline_table_columns_not_memoized` | `GCSQ-ASSET-TS-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/asset-baseline-table-columns-module-scope.tsx` | `columns={columns}` 的资产基线 Table 在同一函数组件/自定义 Hook 内使用 `useMemo<ColumnProps[]>` 声明列配置；不得使用模块级或未 memo 的列数组 |
| `c7n_asset_baseline_table_columns_missing_typed_surface` | `GCSQ-ASSET-TS-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/asset-baseline-table-columns-untyped.tsx` | 资产基线下 Table columns/renderer 补 `ColumnProps[]` 和 `ColumnRenderProps` typed surface |
| `c7n_table_command_function_shape` | `GCSQ-RENDER-001` | `front-hzero-renderer` / `front-hzero-choerodon-ui` scenario:row-actions | major/blocking by impact | `invalid/operator-render-payload-and-header.tsx` | 使用 renderer/helper 合同，禁止 command 函数误用 |
| `c7n_table_command_naked_row_actions` | `GCSQ-RENDER-001` | `front-hzero-renderer` / `front-hzero-choerodon-ui` scenario:row-actions | major/blocking by impact | `invalid/table-command-naked-row-actions.tsx` | 多动作走 `c7nOperatorRender` / confirmed helper |
| `c7n_table_renderer_naked_row_actions` | `GCSQ-RENDER-001` | `front-hzero-renderer` / `front-hzero-choerodon-ui` scenario:row-actions | major/blocking by impact | `invalid/table-renderer-naked-row-actions.tsx` | 多动作走 helper payload |
| `c7n_operator_render_payload_naked_jsx` | `GCSQ-RENDER-001` | `front-hzero-renderer` | major/blocking by impact | `invalid/operator-render-payload-and-header.tsx` | payload item 改为 `{ key, ele, len, title }` |
| `c7n_operator_render_action_ele_not_react_node` | `GCSQ-RENDER-001` | `front-hzero-renderer` / `front-hzero-choerodon-ui` scenario:row-actions | major/blocking by impact | `invalid/operator-render-payload-and-header.tsx` | `ele` 改为 helper 可渲染的行操作 ReactNode；required 权限动作使用 `ButtonPermission type="text"` / confirmed 权限按钮，文案放 children 和同源 `title` |
| `c7n_operator_render_options_permission_list` | `GCSQ-RENDER-001` | `front-hzero-renderer` / `front-hzero-permission-button` | major/blocking by impact | `invalid/operator-render-payload-and-header.tsx` | required 权限放入每个 `ele` 内按钮组件，不用 helper options 承载 |
| `c7n_operator_render_action_missing_title` | `GCSQ-RENDER-001` | `front-hzero-renderer` / `front-hzero-choerodon-ui` scenario:row-actions | major/blocking by impact | `invalid/operator-render-payload-and-header.tsx` | 为每个 action object 补同源 `title` |
| `c7n_renderer_record_get_without_guard` | `GCSQ-RENDER-001` | `front-hzero-renderer` | major | `invalid/renderer-record-get-without-guard.tsx` | 使用 `record?.get` 或显式 guard |
| `c7n_pro_table_operation_column_detail_header` | `HZUI-LIST-003` | `front-hzero-choerodon-ui` scenario:row-actions | major | `invalid/operator-render-payload-and-header.tsx` | 操作列 header/title 不得漂移为详情等业务动作文案 |
| `c7n_pro_table_operation_column_missing_right_lock` | `HZUI-LIST-003` | `front-hzero-choerodon-ui` scenario:row-actions | major/blocking by impact | `invalid/table-operation-column-lock.tsx` | 操作列最后一列并使用 `ColumnLock.right` 或项目 confirmed 等价 enum |
| `c7n_pro_table_operation_column_lock_true` | `HZUI-LIST-003` | `front-hzero-choerodon-ui` scenario:row-actions | major | `invalid/table-operation-column-lock.tsx` | 禁止 `lock: true` |
| `c7n_pro_table_operation_column_uses_fixed` | `HZUI-LIST-003` | `front-hzero-choerodon-ui` scenario:row-actions | major | `invalid/table-operation-column-lock.tsx` | 禁止 antd/hzero-ui `fixed` 冒充 C7N lock |
| `c7n_table_business_column_fixed_width_without_policy` | `HZUI-LIST-010` | `front-hzero-choerodon-ui` scenario:query-table / `front-hzero-enterprise-design` | major/blocking by impact | `invalid/table-business-column-fixed-width.tsx` | 普通业务列删除无来源固定 `width`，改用 `minWidth` / 自适应主文本列 / 项目 auto-fit，或补 `widthPolicy` / `columnWidthSource` 固定宽度来源 |
| `c7n_dataset_query_dataset_not_instance_*` | `GCSQ-QUERY-DS-001` | `front-hzero-choerodon-ui` scenario:query-table | major/blocking by impact | `invalid/dataset-query-dataset-config.tsx` | `queryDataSet` 传 `DataSet` 实例 |
| `c7n_dataset_fields_object_shape` | `GCSQ-DATASET-SHAPE-001` | `front-hzero-choerodon-ui` | blocking | `invalid/dataset-fields-object-shape.tsx` | `fields/queryFields` 必须是数组，每项写 `{ name: '<field>', ...props }`，禁止对象 map |
| `c7n_dataset_field_component_prop_host_mismatch` | `GCSQ-DATASET-FIELD-PROP-001` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-field-component-props.tsx` | 删除 DataSet `fields/queryFields` 中的 Lov/Table/Form/Attachment/Configure 宿主 props；`noCache: false` 属于冗余默认值，组件行为 props 必须归位到 Lov JSX、全局配置或专项合同并补证据 |
| `c7n_dataset_read_object_first_arg_business_params` | `GCSQ-DATASET-READ-001` | `front-hzero-choerodon-ui` | major | `invalid/dataset-read-business-object.tsx` | 业务参数进 factory/queryParameter，不作为 read page 参数 |
| `c7n_dataset_query_object_first_arg_business_params` | `GCSQ-DATASET-READ-001` | `front-hzero-choerodon-ui` | major | `invalid/dataset-read-business-object.tsx` | 同上 |
| `c7n_dataset_transport_returns_promise_call` | `GCSQ-ADAPTER-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/dataset-transport-service-promise.tsx` | DataSet `transport.read/create/update/destroy/submit` 必须返回 `{ url, method, params/data }` 等 request config；不得直接调用 `request(...)`、`queryXxx(...)`、`saveXxx(...)` 等业务 service / Promise 数据函数 |
| `c7n_dataset_transform_response_stringifies_object` | `GCSQ-ADAPTER-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/dataset-transform-response-stringify.ts` | DataSet `transport.transformResponse` 必须返回当前 DataSet/request adapter 可消费的对象或数组；除非有项目 request adapter 源码证据确认必须返回字符串，不得对已解析响应 `JSON.stringify`，也不得用兜底包装覆盖已对齐的 `content/totalElements` |
| `hzero_line_dataset_activation_missing` | `HZC-LINE-DATASET-ACTIVATION-001` | `front-hzero-choerodon-ui` scenario:master-detail | major/blocking by impact | `invalid/detail-line-dataset-no-activation.tsx` | 独立行/集合 DataSet 绑定详情 Table 且存在 `transport.read`，或 read/config 带 `parentId/headerId/*LineId`、`/lines` 等主从集合特征时，补 `autoQuery: Boolean(parentId/headerId)`，或在父 ID ready、主记录切换、保存/提交后显式触发行 DataSet `query()`；另覆盖 detail-collection 命名 fixture |
| `c7n_enum_like_string_without_provenance_*` | `HZUI-ENUM-001` | `front-hzero-choerodon-ui` | major | `invalid/enum-like-string-without-provenance.tsx` | 组件 enum-like props 必须使用 enum import / 项目 confirmed 等价 enum；DataSet 配置类字符串只允许局部 confirmed-string provenance；`asset-baseline-enum` / empty baseline 场景不得用 confirmed-string 注释放行 |
| `c7n_enum_type_escape_*` | `HZUI-ENUM-002` | `front-hzero-choerodon-ui` | major | `invalid/enum-like-string-without-provenance.tsx` | 移除 broad `as any/as unknown` |
| `c7n_table_selection_mode_wrong_enum_domain` | `HZUI-ENUM-003` | `front-hzero-choerodon-ui` | major | `invalid/table-selection-mode-dataset-enum.tsx` | Table `selectionMode` 必须使用 `SelectionMode.*` from `choerodon-ui/pro/lib/table/enum`；`DataSetSelection.single/multiple` 只用于 DataSet `selection` |
| `c7n_dataset_field_array_options_without_provenance` | `GCSQ-LOOKUP-004` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-array-options.tsx` | 用 `new DataSet({ data })` 或 confirmed wrapper provenance |
| `c7n_dataset_options_dynamic_require_dataset` | `GCSQ-LOOKUP-004` | `front-hzero-choerodon-ui` | major | `invalid/dataset-options-dynamic-require.tsx` | 静态导入 `DataSet` |
| `c7n_dataset_options_local_dataset_missing_paging_false` | `GCSQ-LOOKUP-004` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-options-local-dataset-paging.tsx` | 本地固定候选 `options: new DataSet({ data })` 必须补 `paging: false` 和 `selection: false`，避免静态数组被默认分页逻辑误处理 |
| `c7n_dataset_lov_string_field_direct_lov_code` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-string-field.tsx` | 新生成 LOV 使用 `FieldType.object` 容器承载 `lovCode/textField/valueField`，再通过 `bind` 回填 `*Id/*Name`；禁止 `FieldType.string + lovCode` |
| `c7n_dataset_lov_field_missing_explicit_object_type` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-string-field.tsx` | 新生成 LOV 必须显式 `type: FieldType.object`；禁止依赖缺省 `auto` 或非 object 类型承载 `lovCode` |
| `c7n_dataset_lov_object_missing_text_field` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-string-field.tsx` | object LOV 必须显式声明 `textField`，并与返回对象展示字段、display bind 字段一致；`lovCode` 本身不证明展示字段契约 |
| `c7n_dataset_lov_object_missing_value_field` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-string-field.tsx` | object LOV 必须显式声明 `valueField`，并与返回对象提交字段、submit bind 字段一致；`lovCode` 本身不证明提交字段契约 |
| `c7n_dataset_lov_object_missing_bind` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-string-field.tsx` | object LOV 必须在同一 `fields/queryFields` 数组内通过 `bind` 回填 `*Id/*Name`、`*Code/*Meaning` 等提交/展示字段；禁止只生成 `xxxObj + lovCode/textField/valueField` 却没有业务字段回填闭环 |
| `c7n_dataset_lov_object_container_name` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-object-container-name.tsx` | object LOV 容器必须以 `*Obj` 或 `*Lov` 命名；不得用 `itemCategoryId`、`itemId` 等 API 叶子字段承载对象，再生成 `*IdValue/*CodeValue` 替代原提交字段 |
| `c7n_dataset_lov_bind_generated_value_alias` | `GCSQ-LOOKUP-002` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-page` | major/blocking by impact | `invalid/dataset-lov-object-container-name.tsx` | LOV `valueField` 不得绑定到生成的 `*IdValue/*CodeValue` 别名；空溯源反例见 `invalid/dataset-lov-object-incomplete-alias-provenance.tsx`。真实后端别名必须在目标字段对象内记录非空 `lovBindingAlias=confirmed`、`sourceRef` 和 `reason` |
| `c7n_dataset_field_duplicate_name` | `GCSQ-LOOKUP-005` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-binding-cycle.tsx` | 每个 `fields` / `queryFields` 区域内的字段名必须唯一；LOV object 容器不得与提交、展示或查询叶子字段重名 |
| `c7n_dataset_bind_self_cycle` | `GCSQ-LOOKUP-005` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-binding-cycle.tsx` | 禁止 `name=X` 的字段再写 `bind: 'X.<property>'`；LOV 容器必须使用独立名称并单向回填叶子字段 |
| `c7n_dataset_bind_cycle` | `GCSQ-LOOKUP-005` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-binding-cycle.tsx` | `bind` 图必须无间接环；任意 `X -> Y -> ... -> X` 都必须重构为独立容器到叶子字段的单向映射 |
| `c7n_dataset_lookup_code_on_master_data_field` | `GCSQ-LOOKUP-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/dataset-lookup-master-data.tsx` | 申请人、部门、组织、供应商、客户、物料、物料类别等主数据字段不得用 `lookupCode` 或状态/类型值集编码替代 object LOV |
| `c7n_dataset_props_invalid_import_source` | `HZC-DATASET-PROPS-IMPORT-001` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-props-invalid-import.tsx` | `DataSetProps` 从 `choerodon-ui/pro/lib/data-set/DataSet` 单独导入，不从 `choerodon-ui/pro` 聚合、`choerodon-ui/dataset/data-set/DataSet` 或 enum 路径导入 |
| `c7n_dataset_enum_invalid_import_source` | `HZC-DATASET-ENUM-IMPORT-001` | `front-hzero-choerodon-ui` | major/blocking by impact | `invalid/dataset-enum-invalid-import.tsx` | `DataSet` 可从 `choerodon-ui/pro` 导入；`FieldType` 等 DataSet enum 不从 `choerodon-ui/pro` 聚合入口导入，必须改用内置标准坐标 `choerodon-ui/pro/lib/data-set/enum` |
| `c7n_dataset_enum_nonstandard_import_source` | `HZC-DATASET-ENUM-IMPORT-001` | `front-hzero-choerodon-ui` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/dataset-enum-nonstandard-import.tsx` | `FieldType` 等 DataSet enum 必须从标准坐标 `choerodon-ui/pro/lib/data-set/enum` 导入；`choerodon-ui/dataset/enum`、`choerodon-ui/dataset/data-set/enum` 等兼容 re-export 只是历史兼容/冲突证据，不能用 project-confirmed evidence 覆盖内置生成规则 |
| `hzero_attachment_ambient_module_declaration` | `HZUI-ATTACH-001` | `front-hzero-attachment` | blocking by impact | `invalid/attachment-ambient-module-shim.d.ts` | 删除精确或通配 ambient shim，改用目标版本确认的 Choerodon Attachment import 或 confirmed React component wrapper |
| `hzero_attachment_config_object_rendered_as_jsx` | `HZUI-ATTACH-001` | `front-hzero-attachment` | blocking by impact | `invalid/attachment-config-jsx.tsx` | 改用目标版本确认的 Choerodon Attachment import 或 confirmed wrapper |
| `hzero_attachment_config_import_name_ambiguous` | `HZUI-ATTACH-001` | `front-hzero-attachment` | major | `invalid/attachment-config-ambiguous-name.tsx` | 配置对象命名为 `hzeroAttachmentConfig` 等 config 语义 |
| `hzero_front_hfile_attachment_import_invalid` | `HZUI-ATTACH-001` | `front-hzero-attachment` | major/blocking by impact | `invalid/hzero-front-hfile-attachment-import.tsx` | 禁止 `hzero-front-hfile` 作为业务 Attachment JSX 来源 |
| `hzero_attachment_visible_contract_placeholder` | `HZUI-ATTACH-001` | `front-hzero-attachment` | major/blocking by impact | `invalid/attachment-visible-placeholder.tsx` | 删除页面可见治理占位，回 manifest/handoff |
| `hzero_front_deep_import_bypasses_mf_shared` | `HZC-HZERO-FRONT-MF-SHARED-001` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/hzero-front-mf-shared-deep-import.tsx` | HZERO Page / UrlHistoryProvider / intl / notification 使用项目 barrel/alias，如 `components/Page`、`utils/intl`、`utils/notification`；禁止 `components/Page/Header` 等 Page alias 子路径和 `hzero-front/lib/...` 深层入口绕过 MF shared |
| `hzero_intl_formatter_collections_named_import_invalid` | `HZC-HZERO-INTL-IMPORT-001` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | major/blocking by impact | `invalid/hzero-intl-formatter-collections-named-import.tsx` | `intl` 从 `utils/intl` 默认导入；`formatterCollections` 从 `utils/intl/formatterCollections` 默认导入，禁止 `import { formatterCollections } from 'utils/intl'` |
| `hzero_intl_formatter_collections_legacy_lang_invalid` | `HZC-HZERO-INTL-IMPORT-001` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | blocking | `invalid/hzero-intl-formatter-collections-legacy-lang.tsx` | `formatterCollections` 固定从 `utils/intl/formatterCollections` 默认导入；禁止 `@common/components/lang/index`、`components/lang` 等旧 `lang` 封装入口，避免隐藏 namespace 合同或触发项目 wrapper 探索 |
| `hzero_intl_formatter_collections_nonstandard_entry_invalid` | `HZC-HZERO-INTL-IMPORT-001` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | blocking | `invalid/hzero-intl-formatter-collections-project-wrapper.tsx` | 任意 import 标识符只要以 `xxx({ code: [...] })(...)` 形态消费为 formatterCollections HOC，来源必须是 `utils/intl/formatterCollections` 默认导入；禁止项目 wrapper、重命名 alias、`utils/intl` 默认导入冒充 HOC（覆盖 `invalid/hzero-intl-formatter-collections-default-utils-intl.tsx`）或相似页面封装 |
| `hzero_permission_button_import_shape_invalid` | `HZUI-PERM-IMPORT-001` | `front-hzero-permission-button` / `front-hzero-enterprise-process-control` | blocking | `invalid/hzero-permission-button-import-invalid.tsx` | `components/Permission` 导出 `Button`，固定权限按钮必须写 `import { Button as ButtonPermission } from 'components/Permission'`；禁止直接 named import `ButtonPermission`，否则渲染 `undefined` 会触发 React #130 白屏 |
| `hzero_permission_button_legacy_entry_invalid` | `HZUI-PERM-IMPORT-001` | `front-hzero-permission-button` / `front-hzero-enterprise-process-control` | blocking | `invalid/hzero-permission-button-legacy-entry.tsx` | 固定权限按钮禁止使用旧入口或项目封装入口，如 `@common/components/PermissionButton`、`components/PermissionButton`；required 权限按钮统一改为 `import { Button as ButtonPermission } from 'components/Permission'`，避免本地封装绕过 Provider/import 合同 |
| `hzero_i18n_hardcoded_user_visible_chinese_*` | `GCSQ-I18N-002` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | major | `invalid/hzero-i18n-hardcoded-copy.tsx` | 使用 `intl.get(fullKey).d(defaultValue)` |
| `hzero_i18n_locale_key_unresolved` | `GCSQ-I18N-001` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | major | `invalid/hzero-i18n-locale-key-unresolved.tsx` | 改为 literal、同文件静态 const `${preCode}.suffix`、可追溯 imported static const `${COMMON_PROMPT}.suffix`，或补 confirmed external provenance |
| `hzero_i18n_missing_locale_key_not_in_manifest` | `GCSQ-I18N-001` | `front-hzero-enterprise-page` / `front-hzero-enterprise-process-control` | major/blocking by claim | `../i18n-locale-ledger/invalid-missing-ledger` | 写入 `platform-locale-keys.json` / Compliance Manifest 并标记 pending/confirmed，或补 replacement ledger |
| `hzero_page_layout_business_wrapper_around_header_content` | HZERO page layout gate | `front-hzero-enterprise-page` | major/blocking by impact | `invalid/hzero-page-business-wrapper.tsx` | 保持 `Header` 与 `Content` 为相邻根节点 |

## Local Import Path Validator

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_local_import_paths.py --root <frontend-root-or-packageDir> [--source-root src] [--source-alias @]
```

`--source-alias` 只接收已由 `tsconfig paths`、Umi/HZERO 配置或项目证据确认的源码根 alias；未传时 validator 自动读取可解析的 tsconfig chain。HZERO 子模块继承父级 `@/* -> src/*` / `@src/* -> src/*` 且子级为 `rootDir=./src`、`baseUrl=./` 时，自动按 `hzero-submodule-package-local` 解析到当前包 `src`；平台 alias 不参与该重映射。无 alias 仍会检查相对导入是否真实可解析。

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `hzero_local_import_parent_relative_when_alias_available` | `GCSQ-LOCAL-IMPORT-001` | `front-hzero-enterprise-process-control` | warning | `invalid-parent-relative` | 已确认 source-root alias 时，把 `../` 跨目录源码导入改为 alias；路径真实可解析时 delivery 只提示，不按代码失败处理 |
| `hzero_local_import_source_alias_unresolved` | `GCSQ-LOCAL-IMPORT-001` | `front-hzero-enterprise-process-control` | blocking | `invalid-unresolved` | 修正 alias、目标文件或 export；生成结果必须能解析到实际本地模块 |
| `hzero_local_import_relative_unresolved` | `GCSQ-LOCAL-IMPORT-001` | `front-hzero-enterprise-process-control` | blocking | `invalid-relative-depth` | 根据实际 source/target 重新计算相对路径，或在 alias confirmed 后改用源码根 alias |
| `hzero_local_import_source_root_missing` | `GCSQ-LOCAL-IMPORT-001` | `front-hzero-enterprise-process-control` | blocking | not-applicable | 使用 `--source-root` 指定非标准源码目录；不得在未扫描任何源码时声明 validator passed |

## HZERO Import/Export Permission Validator

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzero_import_export_permissions.py --root <frontend-root-or-packageDir>
```

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `hzero_import_*` | `GCSQ-IX-001` | `front-hzero-import-export` / `front-hzero-permission-button` | major/blocking by rule impact | `invalid/list-actions.tsx` | 导入标准组件权限必须位于 `buttonProps.permissionList`，不能使用顶层权限、buttonPermissionText、children 权限外壳、合同占位或错误按钮形态 |
| `hzero_export_*` | `GCSQ-IX-001` | `front-hzero-import-export` / `front-hzero-permission-button` | major/blocking by rule impact | `invalid/list-actions.tsx` | 导出标准组件权限必须位于 `otherButtonProps.permissionList`，不能使用顶层权限、buttonProps.permissionList、buttonPermissionText、children 权限外壳、合同占位或错误按钮形态 |
| `hzero_import_permission_missing_button_props` | `GCSQ-IX-001` | `front-hzero-import-export` / `front-hzero-permission-button` | blocking | `invalid-no-permission-text-style/page-actions.tsx` | 标准 Import 必须把权限放入 `buttonProps.permissionList`；delivery 不允许缺权限绑定 |
| `hzero_export_permission_missing_other_button_props` | `GCSQ-IX-001` | `front-hzero-import-export` / `front-hzero-permission-button` | blocking | `invalid-no-permission-text-style/page-actions.tsx` | 标准 ExcelExportPro 必须把权限放入 `otherButtonProps.permissionList`；delivery 不允许缺权限绑定 |
| `hzero_import_permission_list_invalid_shape` | `GCSQ-IX-001` | `front-hzero-import-export` / `front-hzero-permission-button` | blocking | `../hzero-import-export-permission/invalid/list-actions.tsx` | 导入 `buttonProps.permissionList` 改为 `{ code, type: 'button', meaning }` 对象数组，不用字符串数组、权限码常量数组或缺 `code/type` 的对象数组 |
| `hzero_export_permission_list_invalid_shape` | `GCSQ-IX-001` | `front-hzero-import-export` / `front-hzero-permission-button` | blocking | `../hzero-import-export-permission/invalid/list-actions.tsx` | 导出 `otherButtonProps.permissionList` 改为 `{ code, type: 'button', meaning }` 对象数组，不用字符串数组、权限码常量数组或缺 `code/type` 的对象数组 |

## Integration Contract Smoke Validator

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_integration_contract_smoke.py --root <frontend-root-or-packageDir> --manifest <integration-contract-smoke.json> [--require-master-detail]
```

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `hzero_integration_artifact_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/unconsumed` | 冻结合同要求该能力时内部补 artifact/Task 映射；若 frozen capability 本身错误则返回 `parallel-baseline-invalidated` |
| `hzero_integration_artifact_consumer_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/unconsumed` | 修正 integration manifest 的 consumer file，或补目标页面 |
| `hzero_integration_artifact_unconsumed` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/unconsumed` | 将 required 组件/能力 import 并渲染到目标页面，或回 integration task 补 consumer proof |
| `hzero_integration_artifact_imported_not_rendered` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/unconsumed` | 删除无效 import 或把组件实际接入 JSX / action wiring |
| `hzero_integration_capability_entry_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/unconsumed` | required 导入/导出/附件/明细能力必须有页面入口或 entry proof |
| `hzero_integration_status_code_drift` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/drift` | 实现偏差时使用 Shared Contract Freeze 中的状态码；冻结状态码错误时返回 `parallel-baseline-invalidated` |
| `hzero_integration_permission_code_drift` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` | blocking | `invalid/drift` | 实现偏差时使用 Shared Contract Freeze 中的权限码；冻结权限码错误时返回 `parallel-baseline-invalidated` |
| `hzero_master_detail_assertions_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` / `front-hzero-choerodon-ui` | blocking | `invalid/master-detail` | 主从页合同必须声明 Detail/Line/Mock 的机械 assertion，不能只写自然语言 acceptance |
| `hzero_master_detail_contract_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` / `front-hzero-choerodon-ui` | blocking | `invalid/master-detail-omitted` | 主从页运行必须使用 `--require-master-detail`；缺整个 masterDetailContracts 时直接回 Task/Implementation |
| `hzero_master_detail_assertion_file_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` / `front-hzero-choerodon-ui` | blocking | `invalid/master-detail` | 为 assertion 补目标文件，或回 Task 修正 File Mapping |
| `hzero_master_detail_assertion_target_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` / `front-hzero-choerodon-ui` | blocking | `invalid/master-detail` | 目标文件缺失时回对应 slice Implementation，不进入 integration |
| `hzero_master_detail_required_wiring_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` / `front-hzero-choerodon-ui` | blocking | `invalid/master-detail` | 补 Tabs/LineTable、lineDataSet、lineList、保存/提交或删除 request shape 的 required wiring |
| `hzero_master_detail_alternative_wiring_missing` | `GCSQ-INTEGRATION-001` | `front-hzero-enterprise-process-control` / `front-hzero-choerodon-ui` | blocking | `invalid/master-detail` | 在合同允许的等价 wiring 中至少实现一种，并保留 token/provenance 证据 |

## Slice Quality Gate Validator

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_slice_quality_gates.py --task-breakdown <task-breakdown.md> --gate-result <slice-quality-gates.json> --root <feature-root> [--slice-id <current-group-slice> ...] --out <slice-quality-gates-validation.json>
```

组级 validator 统一通过 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/run_frontend_group_validator.py` 执行并写入 scoped result；同一 scope fingerprint 在一个 execution group 内最多执行一次。TypeScript 调用必须传 `--package-dir <packageDir>`，不得把 `tsconfig.typecheck.json` 传给 package-dir；runner 对旧调用缺参或错误传入 config 路径时从显式值、validator target 或 `tsc -p` 最近的 `package.json` 自动归一化并记录来源。

并行 slice 的 contract-fidelity evidence 先通过 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/merge_frontend_contract_fidelity.py --fragment <feature-root>/evidence/contract-fidelity/slices/<sliceId>.json ... --out <feature-root>/evidence/contract-fidelity.json --result-out <feature-root>/evidence/contract-fidelity-merge.json` 确定性汇合；`contract_fidelity_fragment_*` identity conflict、缺失或 canonical evidence 无效固定为 `fixRouting=owner-needed + reasonClass=result-contract-gap + targetStage=IMPLEMENTATION + repairMode=evidence-backfill + repairBudgetClass=result-contract-backfill + consumesRepairBudget=false`，不能回 Design、不能进入 `repairDispatch`、不能由 primary 猜测补值。

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `slice_quality_gate_*` | `G3.5` | `front-hzero-enterprise-process-control` | blocking | `invalid/not-run` | 任一当前 execution group 的 planned slice 缺失、not-run/failed、组结果缺失、scope fingerprint 过期或重复执行、局部 review 未通过、owner capsule 重复加载时暂停当前组并回对应 slice 或 group-local repair；不得要求其它 execution group 提前完成，不得把 invocation defect 返回为用户可见 blocker；组级边界另由 optimization tool harness 覆盖 |

## LOV Candidate Contract And Fidelity Validators

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_lov_candidate_contract.py --manifest <feature-root>/design/lov-candidate-contracts.json
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_contract_fidelity.py --manifest <feature-root>/evidence/contract-fidelity.json --lov-candidate-manifest <feature-root>/design/lov-candidate-contracts.json
```

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `lov_candidate_*` | `GCSQ-LOOKUP-002` / Design candidate freeze | `front-hzero-enterprise-page` / `front-hzero-mock-request` | blocking | `invalid/blocked-and-platform-routed.json` | Design closeout 内为 `fixRouting=design-needed` 并在并行前修复；`parallelGroupStarted=true` 后为 `fixRouting=baseline-invalidated + reasonClass=parallel-baseline-invalidated + targetStage=LITE_PARALLEL_AMENDMENT`，不得回 Frontend Design |
| `contract_fidelity_*` | `GCSQ-CONTRACT-FIDELITY-001` | `front-hzero-enterprise-process-control` / `front-hzero-enterprise-page` | blocking | `invalid/contract-fidelity.json` | 先区分纯证据缺口与业务实现漂移：fragment/manifest/canonical evidence 缺失走 `repairMode=evidence-backfill + consumesRepairBudget=false`；code/object/bind/runtime/fixture 漂移走 `repairMode=code-repair + consumesRepairBudget=true`。两类 fact owner 均可为 Implementation，但只有后者进入 `repairDispatch`；候选 manifest 自身无效按上一行 Design owner 路由 |

## Index Rules

- 新增 validator rule 必须同步本索引、相关 owner skill 和至少一个 invalid fixture。
- Review / Verification 的 `affectedStaticGateScan.rulesChecked[]` 应引用本索引中的 ruleId。
- frontend agents、process-control references/templates 及查询表格、附件、renderer、row-actions、Choerodon owner skill 中出现的 `validatorRuleId`、`rulesChecked[]`、`rulesHit[]` 会由 frontend validator rule index 校验对账；新增静态 rule 引用不得绕过本索引。
- `severity` 是默认静态严重度；若导致页面不可用、权限绕过、核心功能不可达、运行时崩溃或误报 demo/production ready，应提升为 blocking。
- `severity` 只控制交付出口，不控制修复调度；修复调度必须按 `frontend-validator-fix-routing.md` 输出 `fixRouting=direct-fix / owner-needed / design-needed / baseline-invalidated / user-needed / blocked`。不得因为 `severity=blocking` 默认强制进入专项代码编写 agent；确定性静态小修可走 `direct-fix`，但 blocking 在 targeted validator 通过前仍阻断 Handoff / production-ready / DONE。
- 业务 `intl.get(fullKey).d(defaultValue)` 已按规则消费但 HZERO 平台 key 尚未确认时，不作为 C7N component validator 的失败 rule；必须进入 `platform-locale-keys.json` / Compliance Manifest 并标记 pending，进入 production replacement 和生产闭合门禁。`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_i18n_locale_ledger.py --root <frontend-root-or-packageDir> --manifest <manifest-or-handoff>` 对账逐 key confirmed/pending 和 replacement ledger；未登记时报告 `hzero_i18n_missing_locale_key_not_in_manifest`。直接中文硬编码、动态 suffix、运行时 prefix 或无法追溯为静态字符串的 imported namespace 仍由 C7N component validator 报告。
- 外部 locale namespace 不在本索引维护；由 `frontend-locale-external-allowlist.md` 维护并被 validator 读取。

## Mock Request Validator

命令：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_mock_request.py --root <frontend-root> --package-dir packages/<package> --mock-namespace <namespace> --mock-env-var <switchEnvVar>
```

| ruleId | gateId | ownerSkill | severity | fixture | requiredAction |
| --- | --- | --- | --- | --- | --- |
| `mock_*` | mock-request devServer / request boundary | `front-hzero-mock-request` | major/blocking by rule impact | not-applicable | 细分规则由 `validate_hzerojs_mock_request_negative.py` 和 `tests/assets/frontend/hzerojs-mock-request/*` 维护；命中后回 mock-request owner reference 修复路径、父工程注册、service prefix、pagination、lookup guard 或 plugin 自检 |
| `mock_legacy_umi_mock_dir_location` | mock-request devServer boundary | `front-hzero-mock-request` | blocking | `invalid-umi-mock-dir` | 将 `packages/<package>/mock/*-dev-mock*.js` 迁到 `packages/<package>/dev-mock/`，父工程 `config/config.ts` 改用 `require.resolve('../packages/<package>/dev-mock/<namespace>-dev-mock-plugin')`；`mock/` 目录只允许 Umi 标准 route mock config |
| `mock_handler_organization_id_fixed_tenant` | mock-request tenant path boundary | `front-hzero-mock-request` | blocking | `invalid-hardcoded-organization` | handler 的列表、parents/LOV、export、详情和 action 分支改为动态解析 `/v1/{organizationId}/...`；删除 `/v1/0`、`demo-org` 等高置信固定租户路径，删除 `organizationId` / `tenantId` / `orgId` 与固定字面量比较形成的硬拒绝 |
| `mock_query_mode_runtime_source_forbidden` | `GCSQ-MOCK-002` | `front-hzero-mock-request` | major/blocking by claim | `invalid-query-mode-runtime-param` | 删除业务源码中的 `queryMode`；该字段只允许存在于 SDD / stage result，不得进入 DataSet/service query、request body、URL builder、mock handler 或 mock/real 开关 |

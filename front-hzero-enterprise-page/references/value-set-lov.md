# HZERO Value Set And LOV Patterns

## Scope
Use this reference for HZERO value sets, LOV, dropdown options, code-to-text rendering, query fields, DataSet lookup/lov integration, or record selection.

These patterns are non-runnable until verified. Never invent `lovCode`, `lookupCode`, value meanings, returned fields, tenant scope, or query parameters. When a project coding convention provides enough generation inputs, a code may be produced only as `generatedCandidate`, not as `confirmed`.

## Common Helper Names
HZERO projects may expose helpers with names such as:
- `queryIdpValue`
- `queryUnifyIdpValue`
- `queryMapIdpValue`
- `queryLov`
- `queryLovData`
- `recordLov`
- `queryRecord`

Confirm imports and signatures from project source before use.

## Value Set
- Use value set APIs/helpers for fixed option lists only after `lookupCode` is confirmed.
- 已确认 `lookupCode` 的业务枚举字段必须在 DataSet field/queryField 上直接消费该 `lookupCode`，不得再用本地静态 `options DataSet`、硬编码常量数组或 mock-only meaning 字段替代。只有运行环境明确缺值集服务且交付目标是 mock/demo 时，才可额外提供 local mock options，并必须保留 confirmed `lookupCode`、标记 `localOptionsReplacement=required` 和生产替换项。
- Confirm whether the project expects array options, map options, or unified IDP values.
- Use existing render helpers when present instead of hand-written text mapping.
- Do not hardcode option arrays unless the requirement explicitly provides the values.
- 字段名为 `*Code` 且字段语义是状态、类型、用途、来源、渠道、等级、类别等固定业务枚举时，默认是 lookup/value set 候选；实现阶段不得无来源退化为普通 TextField 或本地 options。
- 状态字段应同时建模 code 与 meaning：code 用于提交和状态机判断，meaning 用于展示。只返回 meaning 或只在表格展示 meaning 时，必须把 code 字段列为接口/字段契约待确认。
- 多选值集字段必须确认提交结构：数组、逗号分隔字符串、重复参数或后端自定义结构；缺失时只能 generatedCandidate/missing，不得自行猜测。

## LOV
- Use LOV APIs/helpers for searchable, backend-driven selection only after `lovCode` is confirmed.
- 已确认 `lovCode` 的主数据字段必须落成 `FieldType.object + lovCode + textField/valueField + bind` 的 LOV 容器；不得把 `applicantId/deptId/itemCategoryId/itemId` 等主数据字段整体降级为本地静态 options、普通 Select 或 TextField。缺 `textField/valueField/lovPara` 等绑定参数时，仍保留 object LOV 候选并登记缺口，不能删除 `lovCode` 语义。
- Confirm query parameter names, returned fields, display field, value field, and multiple-selection behavior.
- For Choerodon DataSet fields, prefer confirmed `lookupCode` / `lovCode` configuration over manual dropdown state wiring.
- 若 `generated-code-conventions.md` 已提供服务简码、功能英文名/页面目录、字段用途和候选生成规则，允许为申请人、部门、物料类别、物料等字段生成 `generatedCandidate` `lovCode`。默认 mock/demo 必须把候选集中写入 `frontend/design/lov-candidate-contracts.json`，同时以独立字段记录 `runtimeScope=mockOnly`，不得再使用 `generatedCandidate/mockOnly` 复合状态，也不得因候选合同生成用户问题。
- 只有 `generatedCandidate lovCode` 还不足以完成生产 LOV：返回字段、display/value 字段、查询参数、租户范围和多选行为仍必须进入 manifest 与 production replacement；Implementation 必须按冻结 manifest 把候选 code 接入 DataSet object LOV 容器字段，再通过 `bind` 回填提交/展示字段，但不得声明 production-ready，也不得把 manifest 已要求的检查自报为 not-applicable。
- 若缺少服务简码、功能英文名、字段用途或项目命名规范，则不得生成候选 `lovCode`，只能列为 `missing`。
- 字段名为 `*Id` 且 label/业务语义是申请人、员工、部门、组织、服务站、办事处、分公司、客户、供应商、物料、物料类别、采购组织、库存组织、岗位等主数据时，默认是 LOV 候选。
- LOV 字段必须确认或列入待确认：`lovCode`、`valueField`、`textField`、回填字段、查询参数、租户/组织范围、单选/多选和展示字段。新生成代码必须使用 `xxxObj: FieldType.object + lovCode + textField/valueField` 作为 LOV 容器，并用 `bind` 回填 `xxxId/xxxName`；只把 `xxxId` 做成 string 输入，或把 `lovCode` 直接挂到 `xxxId: FieldType.string` 上，都会按 Select primitive 值模式运行，是反例，不满足生产 LOV 契约。省略 `type` 依赖 `auto` 推断也不是合格生成形态。
- confirmed/production LOV 的 `lovDefineUrl` / `lovQueryUrl`、批量 define 配置和全局 Lov 请求配置必须来自项目/后端确认。默认 mock/demo 的 generatedCandidate LOV 是唯一例外：Design 按 manifest 为候选字段冻结 current-origin `/_mock/<namespace>/v1/{organizationId}/lov-definitions|lov-data`，Implementation 只在对应字段配置 field-level URL，并在 dev-mock 实现 define/query/fixture；禁止修改 HZERO 全局 LOV 配置或请求远端平台 LOV。
- `lovPara` / 查询参数必须确认参数名、来源字段、来源时机、空值行为、级联清理策略和确认来源；动态参数应通过 DataSet `dynamicProps` 从当前 record/query field/context 读取。不得从业务名词推导参数名，也不得用固定空字符串、当前页面状态或未绑定字段冒充已确认级联过滤。只要存在父子 LOV、组织/租户/公司/岗位范围、供应商/客户业务类型过滤、查询区与表格编辑区参数来源不同、或同一 `lovCode` 多处过滤条件不同，就必须把 `lovParaContract` 写入 `LOV Lookup Binding Contract`；缺契约时只能标记 `missing/partial + replacement`，不能声明 production-ready。
- `combo` Lov 仍必须保持 object LOV 容器与 `bind` 回填契约；复合输入值若需要提交，必须说明如何按 `textField/valueField` 构造对象或回填提交字段。
- `xxxName`、`xxxMeaning`、`xxxDescription` 等展示字段一般不作为提交值；若由 LOV 回填，应在字段映射里说明。
- 若用户或 FDS 明确该字段是自由文本而非主数据选择，应记录 `lovRequirement=not-applicable` 和 reason。

## LOV 示例边界
- 推荐形态：`xxxObj: FieldType.object + lovCode + textField/valueField`，`xxxId/xxxName` 使用 `bind: 'xxxObj.<field>'` 回填，页面编辑态使用 `<Lov name="xxxObj" />`，只读态展示 `xxxName` 或合同指定 display field。
- 级联参数形态：子 LOV 使用 `dynamicProps.lovPara` 从已确认父字段读取，例如物料 LOV 依赖已回填的 `itemCategoryId`；父字段未选择时是否禁止查询、传空、清空子值或提示用户，必须由契约确认。
- 缺参数契约形态：保留 object LOV 容器和 `bind`，但不生成猜测型 `lovPara`；在 Manifest / replacement 中记录 `lovParaContract=missing`、待确认 `paramName/paramSourceField/sourceTiming/emptyValueBehavior/cascadeClearPolicy/confirmedSource`。
- 树形 LOV：只有后端 define 返回 `treeFlag/idField/parentIdField`，或合同确认嵌套数据 `childrenField`，或确认可用 `tableProps={{ mode: 'tree' }}` 时才生成树形配置。
- `combo`：只在需求明确允许输入新增选项时启用；必须处理复合输入对象重建和 submit/display bind，不能退化为普通 string 输入。

## Output Checklist
- Confirmed `lookupCode` or `lovCode`.
- Confirmed helper import and signature.
- Confirmed value/display field mapping.
- Confirmed `lovPara` parameter names, source fields, empty-value behavior, and cascade clearing policy when applicable.
- Confirmed tenant/organization scope.
- Confirmation items for missing codes or backend contracts.

## Temporary Contract Follow-up
- If the user allows temporary `lovCode` or `lookupCode`, keep the values centralized and mark them as non-production.
- Final delivery must list each temporary code, the field using it, expected real code source, return/display/value mapping still to confirm, and replacement file location.
- Do not describe temporary `lovCode` or `lookupCode` as confirmed just because the page runs.
- `generatedCandidate` 与 `mockOnly` 是两个正交机器字段：前者表示合同来源状态，后者表示当前 runtime scope。默认 mock/demo 候选保持正常业务候选 code，不追加 `.mock/demo/TEMP`，同时通过 field-level current-origin endpoint 与生产 LOV 隔离；真实 API 集成或 production-ready 前必须替换为平台确认合同。

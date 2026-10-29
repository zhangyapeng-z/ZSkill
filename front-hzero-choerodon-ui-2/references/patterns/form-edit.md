# Choerodon 表单编辑

用于单记录新增、编辑或详情表单。

## 最小形态
- `DataSet` 负责 `fields`。
- `Form` 绑定到该 `DataSet`。
- 字段组件优先使用 `name` 绑定。
- 在选择 `autoCreate`、详情加载行为、只读字段和提交序列化前，必须先明确 create/edit/detail 模式。

## 职责边界
- 页面容器负责创建或注入 `DataSet`、派生 `pageMode`、加载/刷新记录、调用 `validate()`，以及保存、提交、返回等页面动作。头行、主从、多 Tab 或复用的基础信息表单默认拆成纯展示 `HeaderForm` / `DetailForm`，只接收 `dataSet`、`mode` 和必要的局部组件参数。
- `DataSet.fields` 是字段契约唯一入口：label、type、required、validator、defaultValue、lookup/lov/options、bind、dynamicProps 和 transport 归属都在此处。Form JSX 只选择与字段语义匹配的 Pro 组件、字段顺序和布局，不得复制字段规则、维护竞争性的 local state，或在展示组件内发起页面级保存/查询。
- `pageMode` 的权威来源是 routeContext、UI Contract 和业务状态守卫。展示 Form 不得自行解析路由、重建 DataSet 或把 DataSet 中的 `editFlag` 当成 UI 编辑态来源。
- `Form disabled` 只可作为已确认全局只读态的展示保护；创建、编辑、审批、权限锁定或字段级只读差异应由 DataSet `readOnly` / `dynamicProps` 和 Field Editability Matrix 表达，不能用一个永久 disabled Form 掩盖应编辑字段。
- 简单且无复用需求的单记录页面可以将容器与 Form 同文件实现，但仍必须保持上述字段契约、页面动作和布局职责分离，并在 UI Contract 记录 `formComposition=simple-page-co-located` 与 reason。

## Create/Edit/Detail 流程
- Route Context: page mode and editability should come from a centralized `getRouteContext(location, params)` or project equivalent wrapper, using `useLocation()` and `useParams()` where available. Do not derive business state only from `window.location.hash`, hash regex, or scattered query/params parsing.
- Create route: generated pages must use `/create`; `/detail/create` is an invalid ambiguous route and must be migrated to `/create`. Create mode must default to `isCreate=true`, `editable=true`, and `pageMode=create`; route/query `editFlag` must not be generated or read.
- Create: create a clean record only when the page or modal is opened for create; initialize confirmed defaults with DataSet/record APIs, not scattered local state.
- Edit: load detail or pass selected record according to confirmed page pattern; if detail API is needed, confirm URL/method/params and response shape first.
- Create/Edit/Copy editable fields: fields that are editable by FDS/TDS/UI Contract must render with editable Choerodon Pro field components such as `TextField`、`NumberField`、`Select`、`DatePicker`、`Lov`、`Upload/Attachment` or project equivalents, bound by `name` to Form/DataSet metadata. Do not reuse readonly `Output` for required or editable create/edit fields.
- Readonly/disabled fields in create/edit: only use `Output`、`readOnly`、`disabled` or equivalent readonly display when the field has an explicit source and reason, for example audit field, generated number, immutable primary key, status lock, approval readonly, permission lock or backend-controlled masked field.
- Detail: prefer readonly `Form + Output` or project equivalent readonly Form mode; do not use scattered `div/grid` for business fields, and do not keep submit logic in a readonly-only detail page unless the requirement includes approval/action buttons.
- Detail arrays: experience, education, language, awards and other tabular repeated records must use Choerodon Pro Table. Project readonly tables, thin wrappers, HZERO non-table components, and native HTML DOM fallback must not replace tabular detail collections. Attachments follow the attachment component rules. Single-object fields stay in `Form + Output`. Use the backend contract field name from TDS/MDS/API/DTO for the array and each item column, and keep mock/demo data on the same field names. Alias or dual-shape reads are contract conflicts and must be migrated, not wrapped in a compatibility adapter. Do not flatten repeated records into `ul/li`, comma-joined text, JSON strings, hand-written summary sentences, raw `<table>`, or generic `title/organizationName/timeRange/description` shapes unless the UI Contract explicitly requires a separate non-tabular summary.
- Detail sections: section order and field grouping must follow FDS/UI Contract. Do not add summary headers, stat cards, profile cards or decorative blocks without FDS/TDS/TBS source.
- Submit: prefer DataSet `submit()` or project service boundary; validation failure and request failure must not be treated as success.
- Serialization: choose `dataToJSON` only from contract evidence; `dirty`, `all`, `normal`, self variants and custom adapters change payload shape.
- Refresh: after successful submit, confirm whether to close modal/drawer, navigate back, refresh parent list, or update current record in place.
- Save redirect: if the workflow should stay editable after create/save, preserve edit params according to the route context contract; if it should enter readonly detail, record the business source.

## Non-runnable 骨架
- DataSet：只有在 create/edit 流程确实需要一个当前 record 时才使用 `autoCreate`。
- Fields：字段名、标签、必填规则、校验器、lookup/lov/options 和联动都待确认。
- Form：绑定 `dataSet`；只有在字段契约存在后，字段组件才使用已确认的 `name`。
- Submit：待确认，暂不配置。

## 护栏规则
- required 规则、validator、lookup/lov/options 和联动应保留在 `fields` 中。
- 在契约确认前，不实现 submit 协议。
- 必须维护 page mode / field editability 边界：`create`、`edit`、`copy` 页面中的可编辑字段不得被实现为 `Output` 或永久 `readOnly/disabled`；`detail/readonly` 页面不得保留无来源编辑入口。
- 必须维护 routeContext / editableAuthority 边界：UI 编辑态以 routeContext、UI Contract 和业务状态守卫为准；DataSet 中的 `editFlag` 只能作为展示/提交字段，不能作为 UI 编辑态权威来源。
- 每个表单字段应能追溯 `editability`：`editable` / `readonly` / `disabled` / `hidden`、适用 page modes、原因来源和组件类型。缺少来源时按 editable 需求保守处理，不能自行降级为只读。
- 后端生成编号、状态、合计、审计和提交时间等字段必须按 Field Visibility Matrix / Field Editability Matrix 逐字段决定 create/edit/detail 展示时机、readonly/hidden 原因和 `submitPolicy`；参考页 create 态隐藏不能升级为默认要求。当前 mode 无可显示值时，不能为了填满三列渲染空 `Output` 或 disabled 输入框。
- 不要编造 detail、create、update 或 submit 的 service helper。
- 当下拉/状态字段本应属于 DataSet `fields` 时，不要用本地 `value/onChange` 建模。
- 当后端要求不同的 ID、版本字段、审计字段或状态流转时，不要静默复用 create payload 去做 edit。
- 只读字段必须追溯字段来源和分组；无来源字段不得展示，确需展示时标记 `generatedCandidate`。
- 敏感字段只消费后端返回的 `*Masked` 或已确认脱敏字段；前端不得自行造脱敏逻辑。

## Modal/Drawer 表单补充
- Modal/Drawer 的触发方应使用 `Modal.open` 或已确认等价 wrapper 管理打开、关闭和销毁生命周期；内容组件只管理当前 record、校验、提交回调和必要清理。
- 如果使用 hook/provider 的 modal 模式，应确认 `ModalProvider` 或项目 wrapper 要求。
- 表单弹层形态必须来自需求/设计/工程证据/用户确认；普通 Modal 和 Drawer 都必须通过项目 `Modal.open` 或等价 wrapper 打开。所有业务弹层宽度严格按设计要求；设计未指定宽度时，普通表单 Modal 默认使用 `size=small`（约 520px 或项目 small 等价值）；详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并必须记录 readabilityRisk、Form columns/colSpan 与 `valueOverflowPolicy`。弹层宽度必须写在 confirmed Modal/Drawer API 入口（如 `size`、`width` 或 wrapper `drawerWidth/modalSize`）；只写 `style.width`、内容容器或 CSS class 不能证明弹层宽度正常。
- 详情 Drawer 应由点击事件触发，或用严格受控 effect；避免初始渲染自动覆盖列表或数据更新时重复打开。
- `onOk` 应负责校验/提交，并在校验失败或请求失败时阻止关闭。
- 当 `destroyOnClose=false` 时，切换 record 需要显式 reset 策略。
- 关闭后的父列表刷新必须属于已确认的交互设计一部分。

## 验证
- 验证 required 校验、readonly/disabled 规则、create/edit/copy 可编辑字段可输入、初始值、提交失败行为、提交成功行为以及父级刷新/跳转。
- 验证 routeContext/editMode：列表进入编辑、刷新编辑 URL、`/create` 无 query 新建、保存后跳转、切换不同 id 时编辑态均符合设计；`/detail/create` 命中即失败并迁移。
- 详情验证需覆盖 `Form + Output`、数组 Table、区块顺序、关闭后列表无遮挡、筛选和分页状态保留。
- 最终交付仍需目标 build/compile，或明确给出阻塞/未验证说明。

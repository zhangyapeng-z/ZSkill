# Renderer - 审查与反模式

## 阅读路由
- Renderer Review、自查、反模式、finding 或合规判断时读取。

## Review Checklist
- 搜索 `<TagRender`、`<enableRender`、`<yesOrNoRender`、`<dateRender`、`<dateTimeRender`、`<numberRender`、`<operatorRender`、`<c7nOperatorRender`。大写 helper JSX 化会把 props 对象传入函数；小写 helper JSX 化会被当作 intrinsic tag，不会调用 imported helper。缺同名组件 props 契约时至少 major；导致空标签、错误展示、操作列失效或运行时异常时 blocking。
- 检查 `TagRender` 是否误把 props 对象、meaning、value 或 record 作为第一个参数；第一个参数应是状态值。
- 检查状态标签列是否使用 `TagRender`；出现本地 `statusClass`、手写 `<span className=...>`、自造色值映射或普通 Tag fallback 时至少 major，误报生产规范闭合时 blocking。
- 检查详情 Form 状态字段是否留在 UI Contract 指定字段位置。`authorizationStatusMeaning`、`statusMeaning` 或 `statusText(...)` 被拼接到 section title / Header title，且缺少标题辅助展示来源或与 Form 字段重复时，按 UI Contract 偏差处理；若还绕过 `TagRender` 标准状态展示，按 renderer-helper finding 处理。
- 检查 import/export 是否可解析；缺 export 或 alias 不通时应修复 import 或阻塞，不得把 helper 降级为 candidate/fallback。
- 检查 `statusList`、颜色和 fallback text 是否来自已确认值集、状态矩阵、项目相似页面或明确候选；`statusList` 必须提供 `{ status, color, text }` 或项目 confirmed 等价 shape，不得把 Select/DataSet 下拉 `{ value, meaning }` options 直接传给 `TagRender`。不得用 mock/demo 文案伪装 confirmed。
- 检查 `dateRender` / `dateTimeRender` 是否被当成 Choerodon DataSet 日期字段的通用 renderer adapter。若出现 `renderer: dateRender`、`renderer: dateTimeRender`，或 `FieldType.date/dateTime/time/week/month/year` 字段在 Table/Form/Output renderer 中直接返回 `value`、`record.get(dateField)`、moment-like 对象，按 `HZC-DATETIME-RENDER-001` 处理；已出现 React #31、详情/列表不可用或仍声明 `usable=true` / production-ready 时 blocking。
- 检查 DataSet 日期字段调用 HZERO 字符串 helper 时是否证明入参是裸日期字符串；未证明时必须改为显式适配：moment-like 值用 `value.format(format)`，字符串值再调用 `dateRender` / `dateTimeRender` 或项目 confirmed date adapter。
- 检查 Table/Form/Output renderer 是否使用 DataSet Record API 读取渲染期字段；不要用 `toData()` / `toJSONData()` 作为展示取值入口。renderer 参数中的 `record` 可能为空，出现 `renderer={({ record }) => record.get(...)}`、`TagRender(record.get(...))` 或等价未保护读取时至少 major；已出现 `Cannot read properties of undefined (reading 'get')`、详情/create/未加载态崩溃或仍声明 usable=true 时 blocking。
- 检查 `c7nOperatorRender` / `operatorRender` 是否按函数调用、operators 是否过滤、item shape 是否符合内置 `{ key, ele, len, title }` 或目标项目扩展；每个 action object 必须显式带 `title`，且 `title` 与 `ele` 按钮文案同源。`ele` 必须是 ReactNode 行操作按钮 JSX，不得是 `intl.get(...).d(...)`、字符串或文案变量；required 权限必须在 `ele` 内的 `ButtonPermission` / confirmed 权限按钮上，不得只塞进 helper options。`not-applicable` 权限动作使用普通 C7N `Button type="text"`、链接态按钮或确认组件时，必须能追溯 Button Contract reason。不得把裸 JSX 元素数组直接传给 helper，否则 `action.ele` 为空会被过滤成空操作列。同时核对 `len` 是否足以展示 `title` / `ele` 的实际文案，`limit` 内可见按钮不得被截断。多动作操作列在 `renderer/render/command` 中直接返回多个按钮、链接、Fragment 或按钮数组至少 major，影响 overflow、权限或可达性时 blocking。
- Review 遇到“设计降级”“generatedCandidate”“partial”“待核，可先页面内实现”等来源时，不得据此放行标准 helper 缺失；这些来源本身应回写为设计/任务缺陷。多动作操作列的唯一通过条件是标准 helper 链路或 confirmed project-override。

## Cross References
- helper 签名、调用形态和拒收项见 `references/renderer-helpers.md`。
- 页面 tsconfig paths 合同按 `front-hzero-enterprise-page`。
- 操作列权限、状态守卫、二次确认和更多菜单语义按 `front-hzero-choerodon-ui` 的 row-actions scenario reference。

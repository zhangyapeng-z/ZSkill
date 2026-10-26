# Renderer - 实现与工程证据

## 阅读路由
- Renderer 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## Implementation Rules
1. 先检查 import 路径和导出；`utils/*` alias 存在不等于 `utils/renderer` 和目标 helper 存在。检查失败时阻塞或修复 import，不得改成本地 fallback。
2. 普通 renderer helper 必须按函数签名调用，不得写成 JSX 组件。
3. `TagRender` 内置签名为 `TagRender(status, statusList = [], text = '', fontColor)`；第一个参数是状态值，第三个参数是展示文本。`statusList` 必须是 `{ status, color, text }` 或目标项目 confirmed 等价标签配置；不得把 Select/DataSet 下拉用的 `{ value, meaning }` options 直接传给 `TagRender`。状态列需要标签展示时必须优先使用 `TagRender`，不得用本地 `statusClass + span` 或手写 Tag 替代。
4. Table/Form/Output `renderer` 中状态字段若需要从 renderer 参数 `record` 读取，必须先做空值保护：使用 `record?.get('statusField')`、`record && record.get('statusField')` 或显式 guard；展示文本优先用 `value`、`record?.get('*Meaning')` 或已确认 display field。不得在 create、数据未加载或组件探测渲染时直接调用 `record.get(...)`。详情 Form Mode 声明为 `Tag/Output` 的状态字段，必须保留在字段位置渲染；除非 UI Contract 明确要求标题旁状态，否则不得把状态 meaning 拼接到 section title、Header title 或摘要头中作为替代/重复展示。
5. `enableRender`、`yesOrNoRender`、`numberRender` 等若目标项目证明为函数 helper，也按函数调用或直接作为 renderer 函数引用，不改造成 `<EnableRender />` 等组件。`dateRender` / `dateTimeRender` 在 HZERO 标准实现中是字符串 helper；只有确认 renderer 入参就是日期字符串时，才允许 `({ value }) => dateRender(value)` / `({ value }) => dateTimeRender(value)`。Choerodon DataSet `FieldType.date/dateTime/time/week/month/year` 字段必须按 `dateTimeRenderContract`、组件默认展示、项目 confirmed date adapter，或显式 `value?.format(format)` 转为 string / ReactNode；不得直接返回 `value`、`record.get(dateField)` 或 moment-like 对象。
6. `operatorRender` / `c7nOperatorRender` 必须按内置函数 helper 签名调用：`operatorRender(actions, record, options)` / `c7nOperatorRender(operators, record, options)`；不得写成 `<operatorRender ... />` / `<c7nOperatorRender ... />`。
7. `operators` 每项默认 shape 为 `{ key, ele, len, title }`，生成 action object 时必须显式写 `title`，并与 `ele` 内按钮文案同源，优先复用同一个 `intl.get(...).d(...)` 表达式或同一个文案变量；`ele` 必须是 ReactNode 行操作按钮 JSX。Button Contract 判定 `permissionRequirement=required` 时默认使用 `<ButtonPermission type="text" ...>...</ButtonPermission>` 或 confirmed 权限按钮；`not-applicable` 且有来源 reason 时可使用 C7N `Button type="text"`、链接态按钮、确认组件包裹后的 ReactNode 或项目 confirmed row-action 控件。不得把 `ele` 写成 `intl.get(...).d(...)`、字符串、文案变量或 `{ label, onClick }`；`len` 必须覆盖 `title` / `ele` 的实际用户可见文案宽度；`options.limit` 默认只用于控制可见数量和溢出入口，不用于修复可见按钮截断。项目 helper 实现或相似页面可补充字段，但不能把多动作操作列降级为裸 Fragment，也不能把裸 JSX 元素数组直接传给 helper。动态 operators 必须过滤 null/false/undefined 后再传入 helper。required 权限必须落在 `ele` 内的 `ButtonPermission` / confirmed 权限按钮上，不得只把 `permissionList` 放进 helper options 来替代按钮权限组件。
8. Choerodon Pro Table 自定义多动作行操作应通过 `renderer` 调用 helper；历史代码若使用 `command: ({ record }) => [ ... ].filter(Boolean)` 直出多个按钮，必须按裸操作列处理并迁移到 helper 链路。只有目标项目 wrapper 源码或类型明确把 `command` 函数转译为 renderer 时，才可记录 confirmed project override；不得把“相似页面存在”或“设计 partial/generatedCandidate”作为继续使用 command 函数的理由。
9. `operatorRender` / `c7nOperatorRender` 只负责操作列渲染入口；动作清单、权限、更多菜单和状态守卫按 `front-hzero-choerodon-ui` 的 row-actions scenario reference。
10. 禁止将 `dateRender` / `dateTimeRender` 直接写成 Choerodon renderer 回调引用，例如 `renderer: dateRender`、`renderer: dateTimeRender`。Choerodon renderer 传入的是参数对象而非裸日期值；必须写成显式适配函数，并在函数内处理 moment-like 与字符串两类值。

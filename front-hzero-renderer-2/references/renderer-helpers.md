# HZERO Renderer Helper Reference

## 阅读路由
- 命中 `TagRender`、`operatorRender`、`c7nOperatorRender`、`dateRender`、`dateTimeRender` 或 HZERO `utils/renderer` helper 调用形态时读取。
- 需要确认 helper 签名和普通函数调用形态时读“内置标准 helper”和“调用形态”。
- 涉及 Choerodon DataSet 日期 / 时间字段时读“日期 / 日期时间 helper”规则。
- 审查或排障时读“证据规则”和“拒收项”。

## 适用范围
本参考覆盖 HZERO `utils/renderer` / `hzero-front/lib/utils/renderer` 中常见展示 helper 的调用形态和拒收项。

## 内置标准 helper
- `TagRender(status, statusList = [], text = '', fontColor)`：状态标签。`status` 是状态值，`statusList` 是 `{ status, color, text }` 列表，`text` 是展示文案。
- `enableRender(value)`：启用/禁用展示，具体值域以目标项目 helper 实现为准。
- `yesOrNoRender(value)`：是否展示，具体值域以目标项目 helper 实现为准。
- `dateRender(dateStr)` / `dateTimeRender(dateTimeStr)`：日期和日期时间展示；HZERO 标准实现按后端日期/日期时间字符串解析，不能直接等同于 Choerodon DataSet 日期字段 renderer adapter。
- `numberRender(value)`：数值展示，精度和千分位以目标项目 helper 实现为准。
- `operatorRender(actions, record, options)`：普通 HZERO Table 操作列 helper，按函数调用。
- `c7nOperatorRender(actions, record, options)`：HZERO + Choerodon Pro Table 操作列 helper，按函数调用。

`TagRender`、`operatorRender`、`c7nOperatorRender` 是 HZERO 列表渲染的内置标准合同，不需要用户或设计阶段再次确认签名。实现前只检查目标项目 import/export 是否可解析；不可解析时修复 import 或阻塞，不得降级为本地样式、裸按钮 Fragment 或 candidate fallback。

## 调用形态
普通 helper 函数：

```tsx
renderer: ({ record, value }) =>
  TagRender(record?.get('authorizationStatus'), statusList, value)
```

`statusList` 与 Select/DataSet 下拉 options 不是同一个结构。下拉候选常见 `{ value, meaning }` 只能用于 `textField/valueField`；传给 `TagRender` 的列表必须提供 helper 可匹配的 `status`，并提供 `color` 和展示文案来源，例如 `{ status: 'SUBMITTED', color: 'blue', text: '已提交' }`。如果要复用同一组状态定义，应显式派生两份数组：一份 `{ value, meaning }` 给 Select options，一份 `{ status, color, text }` 给 TagRender，不要把 `requisitionStatusOptions` 这类下拉数组直接传入 `TagRender`。

详情 Form 中的状态字段如果在 UI Contract 中声明为 `Tag/Output`，也应在该字段 renderer / Output 位置按函数 helper 展示。除非 UI Contract 明确要求“标题旁状态”或独立摘要区，不要把 `authorizationStatusMeaning`、`statusMeaning` 或 `statusText(record)` 拼接到 `基本信息` 等 section title 后。

`renderer` / `render` / `Output renderer` 的参数对象可能在 create 模式、DataSet 未加载完成、只读 Output 首次渲染或组件内部探测渲染时不带 `record`。从 renderer 参数读取记录字段时必须使用 `record?.get(...)`、`record && record.get(...)` 或先判断 record；不得直接调用 `record.get(...)` 后再传给 `TagRender`、`enableRender`、`dateRender` 或 JSX。缺 record 时按空值、`value` 参数或合同定义的 fallback 展示，不得让页面崩溃。

错误的 JSX 组件化写法：

```tsx
renderer: ({ record, value }) => (
  <TagRender status={record?.get('authorizationStatus')} statusList={statusList} text={value} />
)
```

React 会把 props 对象作为第一个参数传给大写函数组件，导致 `TagRender` 收到的 `status` 不是状态值，而是 `{ status, statusList, text }` 对象。

日期 / 日期时间 helper：

```tsx
renderer: ({ value }) => dateRender(value)
renderer: ({ value }) => dateTimeRender(value)
```

以上写法只在 `value` 已证明为后端字符串时成立。Choerodon DataSet `FieldType.date` / `FieldType.dateTime` / `FieldType.time` / `FieldType.week` / `FieldType.month` / `FieldType.year` 运行时可能把字段值转成 moment-like 对象；此时必须显式取值并转成 string / ReactNode：

```tsx
renderer: ({ value }) => (value ? value.format('YYYY-MM-DD') : '-')
renderer: ({ record }) => {
  const value = record?.get('creationDate');
  return value ? value.format('YYYY-MM-DD HH:mm:ss') : '-';
}
```

如果字段可能同时来自后端字符串和 DataSet moment 值，应先判断 `value?.format`，再对字符串调用 `dateRender` / `dateTimeRender`，不得把对象直接返回为 React child。

错误的 DataSet 日期 renderer 写法：

```tsx
renderer: dateRender
renderer: dateTimeRender
renderer: ({ record }) => record?.get('creationDate')
renderer: ({ value }) => value
```

`renderer: dateRender` / `renderer: dateTimeRender` 会把组件库 renderer 参数对象传给 helper，而不是裸日期值；`record.get(...)` / `value` 在 DataSet 日期字段中可能是 moment-like 对象，直接作为 JSX children 会触发 React #31。

## 操作列 helper 写法
常见 `c7nOperatorRender` 函数调用：

```tsx
renderer: ({ record }) =>
  c7nOperatorRender(operators.filter(Boolean), record, { limit: 3 })
```

Choerodon Pro Table 历史代码可能使用 `command` 承载行按钮。当前 HZERO 目标中 `column.command` 按命令数组/可迭代集合消费，不是自定义 renderer 函数入口；自定义多业务动作如果写成 `command: ({ record }) => [<PermissionButton ... />, ...].filter(Boolean)`，可能触发 `forEach is not a function`，必须按裸操作列处理并迁移到 `renderer -> operators -> c7nOperatorRender(...)`，或记录 confirmed project wrapper override。

常见 `operators` item 结构：

```tsx
{
  key: 'edit',
  ele: <PermissionButton type="text">编辑</PermissionButton>,
  len: 2,
  title: '编辑',
}
```

注意：
- `operators` item 标准 shape 为 `{ key, ele, len, title }`；生成、返工和审查时不得省略 `title`。`title` 必须与 `ele` 内按钮的用户可见文案同源，优先复用同一个 `intl.get(...).d(...)` 表达式或同一个已命名文案变量，不能只写 `key/ele/len` 后依赖按钮 children 反推。
- `ele` 必须是 helper 最终渲染的行操作 ReactNode。Button Contract 判定 `permissionRequirement=required` 的动作默认使用 `<ButtonPermission type="text" ...>...</ButtonPermission>` 或 confirmed 权限按钮；`not-applicable` 且有来源 reason 的动作可使用 C7N `Button type="text"`、链接态按钮、确认组件包裹后的 ReactNode 或项目 confirmed row-action 控件。不得把 `ele` 写成 `intl.get(...).d(...)`、字符串字面量、按钮文案变量、`title` 文案或 `{ label, onClick }` 这类非 JSX payload；这会让 helper 把文案当组件渲染或把 action 当无效节点处理，可能触发 React #130 或空操作列。
- `len` 是 helper 计算可见按钮宽度的合同字段，不是装饰字段。`len` 必须覆盖 `title` / `ele` 的实际用户可见文案宽度，长文案如“提交审批”“撤回审批”不得沿用短按钮的 `len`。
- `operators` 数组元素必须是 action object，不是裸 React element。`c7nOperatorRender` / `operatorRender` 会读取 `action.ele`；若传入 `[<Button ... />, <PermissionButton ... />]`，`action.ele` 为 `undefined`，按钮会被过滤为空，表现为操作列标题存在但下面没有按钮。
- 按钮为空时不得把 helper 删除后改为 `renderer` 返回 Fragment / 多个 Button / JSX 数组。HZERO + Choerodon Pro Table 多动作操作列的修复方向是保留 `c7nOperatorRender` / `operatorRender`，并修正 operators payload、过滤、`len/title`、按钮 type 和列宽合同。
- `options.limit` 只控制直接可见动作数量和溢出入口，不用于修复可见按钮自身截断。发现 `limit` 内按钮文案被省略时，优先校准对应 item 的 `len`、`title` 和操作列 `width`；不得通过提高 `limit` 掩盖宽度合同错误。
- `ele` 是最终渲染的行操作按钮或确认组件包裹的行操作按钮。行操作里的 `Button` / `PermissionButton` 默认使用 `type="text"`；Header/Toolbar 的 `type="c7n-pro"`、默认主按钮样式或相似页面遗留样式不能带入 `operators`。
- required 行操作权限必须落在 `ele` 内部的 `ButtonPermission` / confirmed 权限按钮上；不得把 `permissionList` 只放到 `c7nOperatorRender(..., options)` 里替代每个按钮的权限组件。权限不适用的行操作仍必须有 Button Contract 的 `not-applicable + reason`，不能用 helper options 冒充权限结论。helper options 默认只承载 `limit`、overflow 或项目 confirmed helper 配置。
- 权限按钮、状态守卫、Popconfirm 和“更多”业务语义归 `front-hzero-choerodon-ui` 的 row-actions scenario reference；本文件只规定 helper payload 和调用形态。
- 动态 operators 必须先 `filter(Boolean)` 或等价过滤，再传给 helper。
- 不得写 `<c7nOperatorRender operators={operators} record={record} />`；小写 JSX tag 会被当作 intrinsic element，不会调用 imported helper。
- 修复裸操作列时不能只把原按钮数组塞进 helper 后结束；必须同时检查 item shape、过滤、`limit`、`title/len`、按钮 type、权限、状态守卫和可见按钮宽度是否仍符合行操作合同。

## 证据规则
- `import { TagRender } from 'utils/renderer'` / `import { c7nOperatorRender } from 'utils/renderer'` 用于证明 import/export 可解析；helper kind 和标准签名由本参考内置为普通函数。
- 只有目标项目存在同名 React 组件、props 类型或相似页面 JSX 组件用法强证据时，才允许把 helper 标为 `project-override`，否则按函数调用。
- 目标项目存在同名 React 组件、props 类型或相似页面 JSX 组件用法时，才允许 `<TagRender ... />`。
- 项目里其它页面使用 `TagRender(statusValue, statusList, text)` 是函数调用证据。
- 项目里其它页面对 DataSet 日期字段使用 `value.format(...)`、组件默认展示或项目 confirmed date adapter，是 DataSet 日期 renderer 证据；不能仅凭 `dateRender` / `dateTimeRender` export 存在，证明其可直接作为 Choerodon DataSet renderer。

## 拒收项
- `<TagRender ... />`、`<c7nOperatorRender ... />`、`<operatorRender ... />` 等普通 helper JSX 化。
- `renderer={({ record }) => TagRender(record.get('status'), ...)}`、`renderer={({ record }) => record.get('xxx')}` 或 `Output` renderer 中直接调用 `record.get(...)`；create 模式、数据未加载或组件探测渲染时会触发 `Cannot read properties of undefined (reading 'get')`。必须改为 `record?.get(...)`、显式 guard 或使用已确认的 `value` 参数。
- `TagRender(value, [], meaning)` 中第一个参数传了 meaning/display text，而不是状态值。
- `TagRender(status, requisitionStatusOptions, text)` 中第二个参数传入 `{ value, meaning }` 下拉 options，缺少 `{ status, color }` 标签配置，导致状态匹配和颜色展示不可控。
- 详情 Form 已有状态字段时，又把 `authorizationStatusMeaning`、`statusMeaning` 或 `statusText(...)` 无来源拼接到 section title / Header title 后，造成设计外重复展示。
- 状态列使用本地 `statusClass + span`、手写 Tag、硬编码 class/color 映射，或把 `TagRender` 降级成 candidate/fallback。
- 多动作 Choerodon Pro Table 操作列在 `renderer`、`render` 或 `command` 中直接返回多个 Button/PermissionButton/a/Fragment 或按钮数组，未使用 `c7nOperatorRender`、`operatorRender` 或已记录的 project-override helper。
- operators 传入 `{ label, onClick }`、普通数组、未过滤的 false/null 项，或 action object 缺 `title` 并声明符合标准 helper。
- operators item 的 `ele` 传入 `intl.get(...).d(...)`、字符串字面量、按钮文案变量或其它非 ReactNode 文案 payload，而不是行操作按钮 JSX。
- operators 传入裸 JSX 元素数组，例如 `c7nOperatorRender([<Button ... />], record, options)`，导致 `action.ele` 为空、操作列按钮全部被过滤。
- 因上述 payload 错误导致按钮为空后，改成 `renderer: () => <>...buttons...</>`、`return [<Button />]` 或直接返回多个 `<a>`；这会绕过 HZERO 操作列 overflow、权限、宽度和一致性合同，按 blocking/major 处理。
- operators item 的 `len` 小于 `title` / `ele` 实际文案宽度，导致 `limit` 内可见按钮被截断；或把这类问题误修成提高 `limit` / 展示更多动作。
- `c7nOperatorRender` / `operatorRender` 的 `operators.ele` 里复制 Header/Toolbar 按钮样式，例如行操作 `PermissionButton type="c7n-pro"`、默认大按钮样式，或同一操作列内 text / pro 混用且无 UI Contract / project-override 来源。
- 未确认 `statusList` 却写死颜色和状态矩阵，并声明 confirmed。
- DataSet 日期 / 时间字段将 `dateRender` / `dateTimeRender` 直接作为 `renderer` 回调，或未证明入参是字符串时直接调用 HZERO 字符串 helper。
- DataSet 日期 / 时间字段 renderer 直接返回 `value`、`record.get(dateField)` 或其它 moment-like 对象作为 React child。
- renderer 中用 `toData()` / `toJSONData()` 读取展示字段。
- 操作列多动作在 `renderer/render/command` 中直接返回 Fragment 或按钮数组，且未使用 `operatorRender` / `c7nOperatorRender` / 已记录 `project-override` helper；该项同时归 `front-hzero-choerodon-ui` 的 row-actions scenario reference。

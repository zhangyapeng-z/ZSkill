# Renderer - 设计与契约

## 阅读路由
- Renderer 设计、契约冻结、question gate、事实确认或资源选择时读取。

## Design Gate
设计或任务中涉及 renderer/helper 时必须记录：
- `helperName`：`TagRender / enableRender / yesOrNoRender / dateRender / dateTimeRender / numberRender / operatorRender / c7nOperatorRender / project-helper`。
- `importPath`：HZERO 标准默认 `utils/renderer`；若项目 alias 不可用则使用 `hzero-front/lib/utils/renderer` 或项目等价 renderer 模块，并记录原因。
- `helperKind`：`TagRender`、`c7nOperatorRender`、`operatorRender` 默认 `function`；只有目标项目存在同名 React 组件定义和 props 契约强证据时才允许 `react-component/project-override`。
- `callSignature`：`TagRender(status, statusList = [], text = '', fontColor)`；`c7nOperatorRender(actions, record, options)`；`operatorRender(actions, record, options)`。这些是内置合同，缺 import/export 时阻塞，不改成候选 fallback。
- `valueSource`：Table/Form renderer 中展示值、状态值、meaning 字段、record.get 字段来源。
- `operatorPayload`：命中 `operatorRender` / `c7nOperatorRender` 时记录 action item shape、`ele` ReactNode 按钮来源、`title` 同源文案、`limit`、record 入参和 options 来源；动作语义仍归 `front-hzero-choerodon-ui` 的 row-actions scenario reference。`ele` 不得设计为按钮文案、字符串或 i18n 表达式；权限不得设计为只放在 helper options。

## Scenario Routing
- 状态标签、启用禁用、是否、日期时间、数字格式化、Table/Form renderer 展示：使用本 skill。
- `operatorRender` / `c7nOperatorRender` 的 import、函数签名、operators payload 结构、调用形态和 JSX 误用检查：使用本 skill。
- 操作列动作语义、更多菜单形态、权限按钮、状态守卫和二次确认：同时使用 `front-hzero-choerodon-ui` 的 row-actions scenario reference。
- 页面容器、i18n、权限、request/service 和 HZERO 页面整体契约：同时使用 `front-hzero-enterprise-page`。
- Choerodon DataSet/Form/Table 组件 API：同时使用 `front-hzero-choerodon-ui`；但 `utils/renderer` helper 的归属仍是本 skill。

## Source Priority
- HZERO 标准 renderer helper 合同由本 skill 内置：`TagRender(status, statusList = [], text = '', fontColor)` 与 `c7nOperatorRender(actions, record, options)` 默认视为普通函数 helper，不需要用户或设计阶段再次确认签名。本 skill 是 `operatorRender` / `c7nOperatorRender` 的 helper 合同、import、调用形态和 operators payload 的唯一规则来源。
- 目标项目源码、`hzero-front/lib/utils/renderer` 实际导出和相似页面证据用于确认 import/export 可用性、operators item shape 的项目扩展和异常覆盖，不用于把标准 helper 降级为 candidate。
- `generatedCandidate` 不适用于 `operatorRender` / `c7nOperatorRender` 的“是否使用”判断。多动作 Choerodon Pro Table 操作列命中时，设计只能在 `standard-helper`、`confirmed project-override`、`blocked/missing import` 中选择；不得输出“可先以等价 renderer/helper 方案实现”“页面内 command/renderer 方案”等放宽口径。
- 本规则只规定 HZERO renderer/helper 的导入、调用形态和静态拒收项；不生成业务字段、状态码、权限码、值集或按钮动作。
- 如果目标项目缺少对应 export、alias 不可用、或存在同名 React 组件强证据，必须记录 `helperContract=missing/blocked/project-override` 并返回补契约或修复 import；不得用本地 `span/className`、裸按钮 Fragment 或普通 helper fallback 静默替代。

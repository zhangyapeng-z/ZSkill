# HZERO 通用页面模式

## 适用范围
本参考用于通用页面工具、render helpers、日期/时间格式化、查询归一化、导航 helpers，以及代码风格预期。

导入前应先从目标项目确认 helper 是否存在。不要编造工具路径或 helper 签名。
确认 helper import 时，应优先读取目标工程或子模块 `tsconfig.json` 的 `compilerOptions.baseUrl` 和 `compilerOptions.paths`。例如 `utils/*` alias 可以作为 `utils/renderer` 的解析候选，但仍必须确认映射目标文件存在且导出所需 helper。

## 代码风格
- 遵循附近页面的文件结构、命名、model/service 模式和组件 wrapper。
- 页面局部业务逻辑应留在 page、service、model 或 DataSet 中。不要把普通页面逻辑搬进 runtime 扩展点或全局拦截器。
- 相比猜测性抽象，更优先小而明确的页面代码。
- 不要输出 `/api/TODO`、`CONFIRM_API` 这类占位 endpoint，或看似可运行的伪契约。

## 常见工具
HZERO 项目中的常见 helper 可能包括：
- `utils/notification`
- `parseParameters`
- `parseParameter`
- `filterNullValueObject`

常见 render helper 可能包括：
- `dateRender`
- `dateTimeRender`
- `numberRender`
- `enableRender`
- `yesOrNoRender`
- `TagRender`
- Choerodon 操作列 renderer helper

只使用项目源码中存在或项目依赖已确认的 helper。

## HZERO render helper 调用形态
HZERO `utils/renderer` / `hzero-front/lib/utils/renderer` helper 的 import、签名、状态标签、日期数值展示和 JSX 组件化误用规则归 `front-hzero-renderer`。本参考只保留页面公共模式入口；具体实现、审查和验证使用该 skill。

## 表格操作列渲染
- HZERO `hzero-ui` / 普通 Table、HZERO + Choerodon / `choerodon-ui/pro` Table 的操作列多按钮必须走 `front-hzero-renderer` 内置 `c7nOperatorRender` / `operatorRender` 或已记录 `project-override` helper。
- 操作列 renderer helper 的 import/export、operators payload 和 JSX 误用检查归 `front-hzero-renderer`；本参考不展开 helper 写法。
- 操作列位置、右锁定、动作语义、更多菜单、状态守卫和空操作列策略归 `front-hzero-choerodon-ui` 的 row-actions scenario reference。
- 操作列权限按钮可作为 `operators[].ele` 的内容；固定入口、Provider 入参字段和旧组件反模式统一按 `front-hzero-permission-button`。
- `PermissionButton type="text"` 只用于 Table 行操作列，包括详情页中的明细表、子表行操作列；行操作列不要使用 `type="c7n-pro"`。
- Header、PageHeader、页面级 Toolbar、表格上方工具栏、表单普通按钮或详情页非表格按钮不适用行操作列限制；C7N 场景下这些非行操作列 `PermissionButton` 按项目规范优先使用 `type="c7n-pro"`。
- 不得将固定 `ButtonPermission` 替换为旧组件、项目 wrapper 或 fallback；具体判定按 `front-hzero-permission-button`。
- 动态操作项的 payload 和过滤规则按 `front-hzero-renderer`；未过滤会让 helper 渲染风险扩大。

## 日期与时间
常见日期/时间格式：
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm:ss`
- `HH:mm:ss`

在转换值前，先确认字段类型、时区预期和后端格式。当项目已有 helper 时，应将展示格式化与请求参数序列化分离。

## 导航
常见 HZERO 导航 helper 可能包括：
- `openTab`
- `replaceTab`
- `closeTab`
- `refreshTab`
- `waitMenuDataLoad`
- `waitUserInfoLoad`
- `getMenuLeafData`

使用前先确认 import、route target、title 行为、query/state 参数以及 Tab 唯一性规则。

## HZERO front alias 与 MF shared
HZEROJS 微前端子模块中，Page 容器、Provider、intl 和 notification 属于平台 runtime / context / 全局工具入口，应优先使用项目 alias，让 hzero-front 插件的 `babelResolvePath` 和模块联邦 shared 映射生效：
- `Header` / `Content` 默认使用 `import { Header, Content } from 'components/Page'`。
- `intl` 默认使用 `import intl from 'utils/intl'`。
- `formatterCollections` 默认使用 `import formatterCollections from 'utils/intl/formatterCollections'`，不得写成 `import { formatterCollections } from 'utils/intl'`，也不得使用 `@common/components/lang/index`、`components/lang` 等旧 `lang` 封装，或任意 `xxx({ code: [...] })(...)` 项目 wrapper。
- `notification` 默认使用 `import notification from 'utils/notification'`。

不要在新增或修改页面中直接导入 `components/Page/Header`、`components/Page/Content`、`components/Page/BackBtn`、`hzero-front/lib/components/Page/Header`、`hzero-front/lib/components/Page/Content`、`hzero-front/lib/components/Page/BackBtn`、`hzero-front/lib/components/Page`、`hzero-front/lib/components/UrlHistoryProvider`、`hzero-front/lib/utils/intl/intl` 或 `hzero-front/lib/utils/notification`，除非目标工程明确证明该子路径或深层入口仍会被统一到同一 MF shared runtime。若浏览器报 `useUrlHistory must be used within a UrlHistoryProvider`，先排查这些子路径/深层导入是否导致子模块打包了第二份 `hzero-front` 或消费了另一份 Page runtime/context，不要先用页面级 `UrlHistoryProvider` 包住 `Header + Content`。

## 输出检查清单
- 已检查现有 helper 的导入路径；`TagRender`、`c7nOperatorRender`、`operatorRender` 签名按 `front-hzero-renderer` 内置合同，不列为待确认。
- 已确认字段格式和后端序列化方式。
- 已确认导航目标与 Tab 行为。
- 缺失的非 renderer helper 或协议列为待确认项；标准 renderer helper 缺 import/export 时按 `front-hzero-renderer` 阻塞或修复，不降级为 fallback。

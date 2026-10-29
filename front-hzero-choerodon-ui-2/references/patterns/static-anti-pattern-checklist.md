# Choerodon Static Anti-pattern Checklist

用于实现后、Review 前或用户手测返工时的轻量静态检查。它不是自动化脚本，但每条都可以通过代码检索、diff review 或 IDE 搜索快速确认。

## 目录
- 使用条件
- 快速检索建议

## 使用条件
- 修改了 Choerodon Pro Table、DataSet、Form、Modal/Drawer、PermissionButton、Attachment 或 mock/production transport。
- Review 或手测反馈命中 UI/组件/数据链路问题。
- 不能运行浏览器时，至少用本清单补足静态可检查项；browser/manual 只能由外部 runtime acceptance 或用户手工证据证明，不写成 Verify 阶段自动执行。

L1 纯 API 解释、单一 props 说明、无可见 UI 的 import 修复、注释修正或测试文案调整，不强制执行本清单；若 L1 修改了可见 UI 或 DataSet transport，执行命中的最小条目。

## 快速检索建议
按目标文件或本轮 changed files 执行最小检索，不全仓漫游：

| 反模式 | 检索线索 | 判定 |
| --- | --- | --- |
| 手写查询 Form | `Form` + `query` / `onSearch` / `onReset` / `useState` | 列表查询绕过 `Table + filterBar` 且无工程证据时 major/blocking |
| 未使用 filterBar | `queryBar` 缺失或非 `filterBar` | 普通管理列表无降级原因时 major |
| JSX 子列退回旧形态 | `<Table ...>` 内出现 C7N `<Column ... />`，但没有紧邻 `tableColumnComposition=jsx-children + sourceRef + reason` | 资产基线新增或重构 Table 默认应在函数组件/自定义 Hook 内改为 `useMemo<ColumnProps[]>` + `columns={columns}`。普通业务列、renderer、编辑态和操作列集中在 columns 数组；仅 confirmed wrapper、递归/运行时动态列或组件版本兼容约束可作为例外，`sourceRef` 必须是相对当前 validator root 可读取的源码路径，旧页面样式不是来源 |
| C7N 组件 API 被跨库污染 | `choerodon-ui/pro` / C7N 组件使用的 props、events、静态方法或数据入口只来自 `hzero-ui` / antd / `@ant-design/pro-*` / Arco / Fusion / Material UI / Element / 项目旧 wrapper 样例；典型如 Pro Table 同文件出现 `dataSource=` / `dataSource:` / `getCollection(` / `loadData(` | C7N 组件 API 必须由同一 import family、项目 confirmed wrapper 源码/类型或 C7N 参考证明。跨库样例只能作为 foreign/negative evidence。命中即 blocking；不得进入 runnable implementation、mock-completed、usable=true 或 production-ready |
| fuzzyQuery 缺失或关闭 | `fuzzyQuery` 缺失 / `fuzzyQuery: false` / `fuzzyQuery={false}` | 设计有关键字、搜索框或模糊搜索时 major；没有该需求时必须有 `not-applicable + reason` |
| 操作列位置错误 | `columns` 中操作列不在最后 | 影响操作可见性时 blocking |
| 操作列表头语义错误 | 操作列 `header/title` 使用 `详情` / `detail` | “详情”是行操作，不是整列标题；操作列标题应为 `操作` / action / operation 或项目 confirmed 等价文案。命中至少 major；导致用户误解或验收漂移时 blocking |
| 右锁定错误 | `lock: true` / `lock: 'right'` | 应改为 `ColumnLock.right` 或项目等价 enum |
| 操作列 command 函数误用 | `command: ({ record }) =>` / `command: record =>` / `command: function` | Choerodon Pro Table `column.command` 在当前 HZERO 目标中按命令数组/可迭代集合消费；自定义行操作函数必须迁移到 `renderer` 并调用 `c7nOperatorRender` / `operatorRender`，或提供 confirmed project wrapper override。已触发 `forEach is not a function`、首屏崩溃或仍声明 `usable=true`/production-ready 时 blocking |
| 多动作裸 renderer | `renderer` 返回多个 `Button` / `PermissionButton` / Fragment / JSX 数组 | HZERO + Choerodon Pro Table 多动作操作列必须使用 `front-hzero-renderer` 内置 `c7nOperatorRender` / `operatorRender` 或已记录 `project-override` helper。若前次问题是 helper payload 裸 JSX 导致按钮为空，正确修复是 `{ key, ele, len, title }` action object，不得删除 helper 后直接返回 Fragment |
| 动态操作项未过滤 | 多动作操作列存在条件 action item，但未按 `front-hzero-renderer` 过滤后传入 helper | 存在条件操作项时 major |
| operator helper payload 裸 JSX | `c7nOperatorRender([<Button` / `operatorRender([<PermissionButton` / helper 数组项为 JSX element | `c7nOperatorRender` / `operatorRender` 默认读取 `{ key, ele, len, title }` 的 `ele` 字段；裸 React element 没有 `ele`，会被过滤为空，表现为操作列标题存在但按钮不显示。必须改为 action object 或 confirmed project helper override；已复现按钮不可见或仍声明 ready 时 blocking |
| operator helper `ele` 非 ReactNode | `ele: intl.get(` / `ele: '详情'` / `ele: "编辑"` / `ele: detailText` | `ele` 必须是最终渲染的行操作 ReactNode。required 权限动作默认是 `ButtonPermission type="text"` 或 confirmed 权限按钮 JSX；权限不适用动作可用 C7N `Button type="text"`、链接态按钮或确认组件。按钮文案应放在按钮 children 和同源 `title` 中。把文案塞进 `ele` 可能触发 React #130、空操作列或权限失效，至少 major；首屏白屏或仍声明 ready 时 blocking |
| helper options 冒充按钮权限 | `c7nOperatorRender(..., record, { permissionList` | required 行操作权限必须落在每个 `ele` 内的 `ButtonPermission` / confirmed 权限按钮上；helper options 不能替代按钮权限组件。required 动作绕过权限按钮至少 major，权限失效或生产 ready 误报时 blocking |
| Table buttons 非数组 | `buttons={<` / `buttons={<>` / `buttons={button` / `buttons={condition &&` / `buttons={buttons as any}` | Choerodon Pro Table `buttons` / table toolbar buttons 必须是可迭代数组形态，数组元素可为标准按钮字符串、配置元组或项目确认自定义按钮；Fragment、单个 ReactNode、普通对象和条件表达式非数组至少 major，已触发 `forEach is not a function` 或页面初始化崩溃时 blocking |
| DateTime 对象直渲染 | `FieldType.dateTime` / `FieldType.date` / `FieldType.time` / `FieldType.week` / `FieldType.month` / `FieldType.year` + `renderer` / `Output` / JSX `{record.get(` / `({ value }) => value` / `record.get(dateField)` | DataSet 日期/时间字段运行时可能是 moment-like 对象；Table renderer、Output renderer、详情 JSX 或自定义展示不能直接返回 `value`、`record.get(...)` 或 moment-like 对象，必须按 `dateTimeRenderContract`、组件默认展示、项目 confirmed renderer，或显式 `value.format(format)` 转成 string/ReactNode。命中按 `HZC-DATETIME-RENDER-001`，已出现 React #31、详情/列表崩溃或仍声明 `usable=true`/production-ready 时 blocking |
| 行按钮类型错误 | 行操作 `PermissionButton type="c7n-pro"` | 行操作应使用 `type="text"` |
| Header 按钮类型误套 | Header/Toolbar `PermissionButton type="text"` | 无项目证据时 major |
| 页面/表格工具栏消费面混淆 | `uiArea=page-toolbar` 未由 `Header` children 消费，或出现在 `Table buttons`；`uiArea=table-toolbar` / `table-toolbar` 未进入对应 `Table buttons`，而是上提到 Header 或 Table 上方自建 toolbar | 页面工具栏按钮和表格工具栏按钮必须分区落到确认消费组件；页面工具栏按钮下沉到 `Table.buttons`、表格工具栏新建/保存/删除/导出上提或自绘独立区域至少 major，导致核心操作不可达或权限/验收漂移时 blocking。只看到明细表或页面有 Table 不自动触发表格工具栏，必须有表格工具栏按钮来源 |
| 权限组件契约错配 | `@common/components/PermissionButton` / `components/Permission` / `PermissionProvider` / `permission.check` / `permissionList` / `codeList` | 按 `front-hzero-permission-button` 检查固定入口、旧组件禁用、fallback 和 Provider 入参契约；命中至少 major，权限失效或运行时异常时 blocking |
| 页面级 Provider 无来源 | `UrlHistoryProvider` / `HistoryProvider` / `ConfigProvider` / `Provider` 包裹 `Header` + `Content` | HZERO 页面默认 Fragment 下相邻 `Header` 与 `Content`；缺 UI Contract、golden-baseline 或明确功能需求时 major；导致滚动、页签、路由状态异常时 blocking |
| 单组件过度封装 | module-prefixed wrapper pattern / `runtimeAdapters` / PermissionButton-or-Button fallback / `buttonProps` / `create*Props` / `build*Config` | HZERO/C7N 单组件应直接使用项目组件和明确 props；只转发 props、重命名 import、包装默认值、隐藏权限/组件 API/import/fallback/generatedCandidate 的 wrapper/helper 属于无意义封装，major；required 权限被普通 Button fallback 时 blocking |
| i18n helper 过度封装 | `const t =` / `function t(` / `intlLabel` / `intlPrefix` / `t('view.` / `t('model.` | 新生成 HZERO 页面默认直接 `intl.get(fullKey).d(defaultValue)`；局部 namespace helper 隐藏 key 来源、返回 key/对象而不是已解析文案，或与 `intl.get` 混用时 major |
| i18n key 被当作 label | `label: \`${preCode}.` / `label: '<namespace>.field.` / `label: { key` / `defaultValue:` | Choerodon DataSet/Form/Table 不会自动二次翻译 label key；字段会直接显示编码。应改成 `intl.get(fullKey).d(defaultValue)`，并对账 platform locale ledger / legacy locale |
| 非标准导入导出入口 | 导入入口不是 `Import` from `components/Import` 或内部使用它的 confirmed wrapper；导出入口不是 `ExcelExportPro` from `components/ExcelExportPro` 或内部使用它的 confirmed wrapper | required 导入导出必须输出 `ImportExportEntryProof` 并使用 canonical 组件或 confirmed current wrapper；`CommonImport/Route`、旧 `ExcelExport`、深层导入、永久 disabled/no-op/空组件至少 major，新增代码或声明能力完成时 blocking |
| TabPane 独立命名导入 | `import { Tabs, TabPane } from 'choerodon-ui/pro'` / `import { TabPane } from 'choerodon-ui/pro'` / `choerodon-ui/pro/lib/tab-pane` | Choerodon Pro `TabPane` 不作为 `choerodon-ui/pro` 独立命名导出使用；按需构建会解析到不存在的 `choerodon-ui/pro/lib/tab-pane`。应改为 `import { Tabs } from 'choerodon-ui/pro'` + `<Tabs.TabPane ...>`，或在项目健康证据确认后 `const TabPane = Tabs.TabPane`。已触发 Module not found 或详情 required 页签不可渲染时 blocking |
| 组件 API as any 逃逸 | `const { X } = Component as any` / `Component as any` / `Tabs.TabPane` | 未确认 import、静态子组件或组件命名空间 API 时 major；导致运行时 undefined 时 blocking |
| 未导入组件变量 | JSX 或静态访问使用未 import 的 `Tabs` / `Modal` / `Table` / `Form` / `Select` 等 | 运行时 `is not defined` 风险；命中即 major，已复现或生产路径为 blocking |
| 直接 hash 判断编辑态 | `window.location.hash` / `location.hash` / `hash.includes` + `editFlag` / `isCreate` / `pageMode` | 新建/编辑/复制/详情页应统一 routeContext；影响刷新、保存后跳转或切换 id 时 blocking |
| DataSet editFlag 控制 UI | DataSet/record 中 `editFlag` 直接决定 Form disabled、字段 readOnly 或页面 editable | UI 编辑态应来自 routeContext + UI Contract + 状态守卫；DataSet `editFlag` 仅展示/提交 |
| 新建页默认值污染 | `mode=create` / `isCreate` + `set(` / `defaultValue` / `detail-create` / `createTemplate` / `new Date()` | 业务输入字段默认应为空或来自 confirmed 默认值；mock seed、示例数据、历史详情数据、当前时间预填无来源时 major/blocking |
| 可编辑页误用 Output | create/edit/copy 表单字段使用 `Output`、永久 `readOnly` 或永久 `disabled` | 字段在 UI Contract 中可编辑且无只读来源时 blocking |
| div/grid 详情 | `div` / `Row` / `Col` 拼只读字段 | 只读详情应使用 `Form + Output` |
| 详情集合文本化 | `renderPlainList` / `ul` / `li` / `join(` / `JSON.stringify` 出现在详情集合区 | TDS/MDS/API 声明数组/集合字段时，表格型详情集合必须使用 Choerodon Pro Table；文本拼接至少 major，声明详情完成或影响核心阅读时 blocking |
| 详情集合字段名漂移 | 契约字段如 `*List` 与组件/mock/service 读取的 `*s` / `*Experiences` / 自造别名不一致 | mock/demo 和 UI 必须消费同一 API/MDS 字段名；别名只能在 service/adapter 集中转换并记录来源。组件内直接读无来源别名至少 major，真实接口切换会空白时 blocking |
| Form 布局 props 无来源 | `labelLayout` / `labelAlign` / `labelWidth` / `columns` / `colSpan` | 只确认 Form+Output 不等于确认 label/value 上下结构；缺 UI Contract/Figma/项目同类页面证据时 major |
| 长详情不可滚动 | `Content` / `Tabs` / `Table` / wrapper height/overflow/fixed/sticky 组合异常 | 需检查 Page/Content、业务 wrapper、Tabs/TabPane、Table body、父微前端容器；不可只归因于样式注释；无法滚到最后区块时 blocking |
| 详情明细动态 autoHeight | `autoHeight` + `TableAutoHeightType.maxHeight` / `type: TableAutoHeightType.maxHeight` / `heightType.*maxHeight` 出现在详情、表单、头行或 Tab 明细 Table | 页面级 `Content` 已承担主滚动时应移除动态 max-height；除非有稳定容器高度、UI Contract 来源和底部不抖动验证。滚到底部来回滚动时 blocking |
| 无来源摘要区 | `summary` / `overview` / `stat` / `profile` | FDS/TDS/UI Contract 无来源时 major |
| `HZC-MODAL-JSX-001` JSX/自绘弹层误用 | JSX `Modal` / `Drawer` / 自绘 Overlay + visible/open state；典型如 `<Modal drawer visible>`、`<Modal visible>`、`<Modal open>`、`<Drawer visible>` | 业务弹层应使用 `Modal.open` 或已确认等价 wrapper；新增或重构时命中至少 major；详情查看主链路不可用或仍声明完成时 blocking |
| `HZC-MODAL-OPEN-001` 业务弹层未用 Modal.open | `Modal`/`Drawer` JSX 常驻渲染、`visible`/`open` state 控制、或自定义弹层打开普通业务弹窗 | 普通 Modal 和 Drawer 业务弹层都必须用 `Modal.open` 或等价 wrapper；破坏性二次确认的 `Modal.confirm` / `Popconfirm` 例外。若只是为了支持上一个/下一个记录切换而引入 state，应改为内容组件维护当前记录或使用 confirmed modal update/recreate，不得退回常驻 JSX Drawer |
| `HZC-DRAWER-RESIZABLE-001` Drawer 缺少 resizable | `Modal.open` + `drawer: true` 但缺少 `resizable: true`，或 wrapper 未声明等价默认 | 查看详情和其它 Drawer 默认必须可调整宽度；缺失时 major，导致查看内容不可用时 blocking |
| 首屏自动弹层 | `useEffect` 中直接 `Modal.open` / `setVisible(true)` | 依赖未受控或初始打开时 blocking |
| 弹层宽度无来源 | `width: '60%'` / `width: '70%'` / `width: '80%'` / `width="80%"` / `width: '100%'` / `width: 980`，或 UI Contract 写 `60%~80%` 候选 | 普通表单 Modal 未有设计/Figma/项目基线/用户证据时默认 `size=small`；详情 Drawer / 高密度详情应记录项目默认尺寸或 confirmed baseline、readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`。无来源宽框 major，误报符合设计或 production-ready 时 blocking |
| 普通 Modal 缺 small 默认 | `Modal.open` / wrapper 调用用于普通表单 Modal，设计未指定宽度，且没有 `size: 'small'` / 项目等价 small 配置 / wrapper 默认 small 证据 | 普通表单 Modal 设计未指定宽度时默认 small；详情 Drawer / 高密度详情不套用本条。实际出现宽框或用户反馈宽度异常时 blocking |
| 长值缺溢出策略 | 详情/Drawer/Modal 只读 Form 中出现长文本、邮箱、公司名、职位名、地址、备注、经历描述等，但缺 `valueOverflowPolicy`，或通过放大弹层宽度替代字段溢出处理 | 短语义长值可单行省略 + Tooltip；备注/驳回原因/经历描述/富文本/长正文不得无来源单行截断。缺策略至少 major，导致不可读或仍声明 ready 时 blocking |
| 弹层宽度写错入口 | `Modal.open` / wrapper 调用只出现 `style: { width`、内容根节点 style width 或 CSS class width，未出现 confirmed `size` / `width` / `drawerWidth` / `modalSize` 等配置入口 | 这通常只影响内部内容或被容器覆盖，不算弹层宽度契约闭合；至少 major，用户反馈宽度异常或仍声明完成时 blocking |
| `HZC-MODAL-LIFECYCLE-001` Modal close API 无证据 | `modal.close()` / `Modal.close(` / `destroyAll` / 私有 container close/update 出现在自定义关闭、保存后关闭、记录级导航或 header/footer/children 逻辑中，但缺 `modalLifecycleContract.closeApiSource` 和目标项目证据；记录级导航只指同一详情表面内业务主记录身份变化，不包括分页、轮播、步骤向导、Tab/区块切换或附件/图片预览翻页 | 至少 major，出现 `close is not a function`、弹层无法关闭、只以 build passed 证明关闭正确或仍声明 ready 时 blocking |
| Modal lifecycle 命中未审计 | changed files 出现 `Modal.open`、`drawer: true`、`Modal.close(`、`.close()`、`destroyAll`、`header:`、`footer:`、`children:` 或 `onClose`，但实现/审查/验证结果没有 `modalLifecycleSelfCheck`、`modalLifecycleContract` 或关闭交互验证结论 | 视为执行链路缺口；不得写 clean / usable=true / production-ready，必须补 closeApiSource、closeApiEvidence 和关闭后 console/遮罩/状态验证 |
| 背景/层级穿透 | Modal/Drawer/Overlay content/body/wrapper 无背景、透明样式、错误 z-index 或错误 Portal 容器 | Header、固定表头、固定列、列表内容穿到弹层上方时 blocking |
| PageResponse 直塞 transport | `transport.read` 直接返回本地 `PageResponse` | local-filter 冒充请求链路时 blocking |
| data URL / 空 URL | `data:application/json` / `url: ''` | DataSet mock transport blocking |
| 绝对 localhost mock URL | `http://localhost` / `localhost:8000` | 只允许作为明确 HZERO 本地 devServer mock API；缺 queryMode、devServer 扩展点或 replacement 说明时按 mock 边界缺失处理，不得写 `usable=true`；不要表述为生产请求契约已闭合；production transport 中 blocking |
| mock 使用真实网关前缀 | `<unconfirmed-gateway-prefix>` + `mock` / `demo` / `dev-mock` / `transport.read` | 新生成 mock/demo 必须使用 `/_mock/<module>/v1/{organizationId}`；`<unconfirmed-gateway-prefix>` 默认是真实后端入口，作为 mock 前缀至少 major，导致请求落远端或误报 `usable=true` 时 blocking |
| mock 租户硬编码 | `/api/v1/demo-org` / `demo-org` / `tenantId = 0` | HZERO mock path 必须使用运行时 `organizationId`；硬编码租户导致真实/模拟链路分裂，至少 major |
| 子模块 mock 插件未被父工程注册 | `packages/<module>/dev-mock/*dev-mock-plugin` 存在，但父工程 `config/config.ts` 未显式注册子模块 plugin 或聚合 plugin | 父工程托管子模块的 mock plugin/handler 应归属与 `config` 平级的子模块 `dev-mock` 目录，但必须被父工程启动配置挂载；mock-request 最高只能 `conditional`，声明 `usable=true` 时 blocking |
| service/middleware mock path 分裂 | service `<unconfirmed-gateway-prefix>` + middleware `/api/v1` / resource path 或 organizationId 位置不一致 | DataSet/service 与 middleware 必须同源同路径；路径分裂时 mock 请求链路不成立 |
| 静态 mock 被拼 API_HOST | `/mock-data` / `mock-data` + 项目 request/DataSet adapter 自动拼 host | 静态 seed 不是标准 mock 实现；请求落到 API_HOST 时 mock-request 不成立 |
| adapter 被注释且无等价路径 | `transformResponse` / adapter / parse helper 只以注释形式存在，且 raw response + `dataKey/totalKey` 或项目 adapter 不能完成同等映射 | queryParameter、分页或详情组合不进入成功路径时 major/blocking；raw shape 已可直接消费时不因缺 `transformResponse` 单独判错 |
| queryParameter 从 params 取业务 ID | `transport.read: ({ params }) => ...params.requisitionHeaderId/headerId/parentId/id...`，且该 ID 来自 `queryParameter`、`setQueryParameter` 或 QueryDS | Choerodon `transport.read` 中业务查询条件在 `data`，分页/排序运行参数在 `params`；详情 path id 应来自闭包、route context 或 `data`。从 `params` 取业务 ID 会拼出 `/undefined` 或丢查询条件，按 `GCSQ-DATASET-READ-001` / `GCSQ-ADAPTER-001`，导致 404/详情无数据时 blocking |
| 详情普通对象配分页 DataSet | Detail/Header DataSet 使用 `pageSize: -1` 或默认 `paging: true`，但 mock/API 返回普通对象；或明细/子表返回数组却缺 `paging: false` / `dataKey` / `totalKey` / adapter | `pageSize: -1` 不等于关闭分页。单记录详情直接消费普通对象时应 `paging: false`；分页模式必须返回并配置可消费的分页 shape。接口有数据但 Form/Table 不显示时 blocking |
| mock runtime store 死链路 | `ensureRuntimeSeedsLoaded` / `ensureSeedLoaded` / `runtimeStore` / `mockRuntimeStore` 存在，但 DataSet read 成功路径不读取同一 store/service | store 只被保存/删除/提交等动作使用、列表/详情/明细读取绕过 store 时 major；动作后刷新旧数据复现或读写两套数据源时 blocking |
| 直接 fetch/axios | `fetch(` / `axios(` / `XMLHttpRequest` | mock-request 中仅允许请求 HZERO 本地 devServer mock API，并必须标明 queryMode、mock-only、devServer 扩展点和 replacement；不得因此判 production-ready。production 或未声明边界时，未确认 native-http/request adapter 为 major/blocking |
| loadData 唯一查询 | `loadData` + 无 `transport.read` / 无 query 边界 | mock/demo 中 blocking；即使用户明确内存演示也必须 cleanup/rework，不能作为可运行列表、降级分支或交付完成证据 |
| queryDataSet 配置对象误用 | `queryDataSet: create*DS()` / `queryDataSet: *Config` / `queryDataSet: { fields`，且右侧不是 `new DataSet(...)` 或显式 `create*DataSet()` | Choerodon `DataSetProps.queryDataSet` 需要 `DataSet` 实例；推荐 `create*DSConfig(): DataSetProps` + `create*DataSet(): DataSet`，兼容 `new DataSet(create*DS())`。误传配置对象会在运行时初始化查询字段时触发 `undefined.add` 等错误。命中至少 major，页面初始化已崩溃或仍声明 `usable=true`/production-ready 时 blocking |
| DataSet fields/queryFields 对象 map | `fields: { code: { ... } }` / `queryFields: { keyword: { ... } }` | Choerodon DataSet `fields/queryFields` 必须是数组，每项写 `{ name: '<field>', ...props }`；对象 map 没有 `forEach`，会在 DataSet 初始化时触发 `forEach is not a function`。命中 `c7n_dataset_fields_object_shape` blocking |
| DataSet bind 重名或闭环 | 同一 `fields` / `queryFields` 中重复 `name`；`name: 'X'` + `bind: 'X.<property>'`；或 `X -> Y -> ... -> X` | LOV object 容器与业务/查询叶子字段必须使用不同 `name`，并只允许 `container.property -> leaf` 单向绑定。必须回扫当前区域全部 bind edge；命中 `c7n_dataset_field_duplicate_name`、`c7n_dataset_bind_self_cycle` 或 `c7n_dataset_bind_cycle` 至少 major，已出现 `DataSet: Cycle binding fields[...]`、白屏或仍声明 usable/production-ready 时 blocking |
| Select lookup/options 非集合 | `lookupCode` 出现在 mock/demo 字段且无值集接口证据；`options:` 右侧为对象/raw response/Promise/JSX；`queryFields` 或 `fields` 中 Select 字段无选项来源记录 | Select / lookup 字段必须有 confirmed lookup 服务或本地数组/DataSet options。mock/demo 缺平台值集证据时应使用本地 DataSet/数组 options，并写入 replacement；raw response、分页对象或非集合 options 至少 major，已触发 `forEach is not a function` 时 blocking |
| 本地 options DataSet 缺分页关闭 | `options: new DataSet({ data: [...] })` 且缺 `paging: false` | 本地固定候选必须写成 `new DataSet({ data, selection: false, paging: false })` 并配套 `textField/valueField`；否则 DataSet 默认分页会把静态数组按分页响应处理，可能触发 `forEach is not a function`。命中 `c7n_dataset_options_local_dataset_missing_paging_false` 至少 major，已复现首屏崩溃时 blocking |
| options 动态 require DataSet | `options: new (require('choerodon-ui/pro').DataSet)(...)` | 本地 DataSet options 必须使用顶层静态 `import { DataSet } from 'choerodon-ui/pro'` + `options: new DataSet(...)`，动态 require 构造会破坏类型、import provenance 和构建优化。命中至少 major |
| forEach 运行时崩溃未回扫集合 props | 用户手测或浏览器日志出现 `forEach is not a function`，但返工只改单点代码，未回扫 `Table.buttons` / `column.command` / `columns` / `queryFields` / `fields[].options` / `lookupCode` / mock response shape | Choerodon 压缩栈难定位时必须按集合 props 顺序回扫并记录命中/排除结果；若 stack 指向 `TableCommandType`、`TableCellInner` 或操作列 chunk，优先检查 `column.command` 是否被写成函数；若 stack 指向 Select、lookup 或 options 初始化，优先检查本地 `options: new DataSet({ data })` 是否缺 `paging: false`、`lookupCode` 返回形态和 `textField/valueField`。缺回扫证据时返工最高 `partial-needs-rework`，声明已完成或 `usable=true` 时 blocking |
| QueryDS/ListDS 混管 | 单组件同时管理查询、列表、详情、同步状态 | 复杂页面 major |
| 枚举型 props 无来源 | `type` / `selection` / `dataToJSON` / `editMode` / `align` / `lock` / `queryBar` / `labelLayout` / `color` / `funcType` 等枚举型配置裸写且无项目/API 证据 | 组件 props 应导入确认 enum；DataSet 字符串风格必须有相似页面证据；同一 feature 混用字符串和枚举 major |
| 弱类型字符串风格冒充确认 | 相邻页面裸写 `type: 'string'`、`queryBar="filterBar"`、`funcType="raised"` 等，同时伴随 `as any`、无类型 renderer/columns、或 baselineComparison=legacy-risk，却被实现为新增页面默认风格 | 必须写入 `rejectedPatternItems`；组件 props 新增实现必须回 Design/Task 补 enumStrategy 或使用 asset/fallback enum；误报 project-string-confirmed 至少 major |
| 枚举布尔误用 | `lock: true`、布尔值代替方向/模式/类型枚举 | 已知错误配置 major；导致 UI 行为错误时 blocking |
| reference import 冒充项目证据 | 仅因 reference 中存在 enum import 路径就声明项目 confirmed | 必须追溯 Evidence enum import map、目标项目 import 或设计 generatedCandidate；缺项目证据时 major，production-ready blocking |
| enum mixed 未决策 | 同一 feature 中同类 prop 一处 enum、一处字符串，或 Evidence 标记 `projectStyle=mixed` 但设计未选策略 | 回到 Design/Task 选择单一策略并写 reason；Implementation 不得自行混用 |
| DataSet 配置 as any 逃逸 | `new DataSet({` + `} as any)` / `new DataSet(config as any)` | 包含 `fields[].type`、`queryFields[].type`、`selection`、`dataToJSON`、events 等 enum-like props 时，必须补 enumProvenance 或使用项目确认 enum/string 风格；整段逃逸 major |
| DataSetProps 导入错误 | `import { DataSetProps } from 'choerodon-ui/pro'` / `import { DataSetProps } from 'choerodon-ui/dataset/data-set/DataSet'` / `import { DataSetProps, FieldType } from 'choerodon-ui/pro/lib/data-set/enum'` / 从任意 `*/enum` 路径导入 `DataSetProps` | 必须改为 `import { DataSetProps } from 'choerodon-ui/pro/lib/data-set/DataSet'`，并将 `FieldType` 等 enum 保留在项目确认 enum 路径；命中 `c7n_dataset_props_invalid_import_source` 至少 major，导致 TS 编译失败或配合 `as any/as unknown` 规避时 blocking |
| DataSet enum 导入路径漂移 | `import { DataSet, FieldType } from 'choerodon-ui/pro'` / `import { FieldType, DataSetSelection } from 'choerodon-ui/pro'` / `import { FieldType } from 'choerodon-ui/dataset/enum'` | `DataSet` 可从 `choerodon-ui/pro` 导入，但 `FieldType` 等 DataSet enum 必须来自内置标准坐标 `choerodon-ui/pro/lib/data-set/enum`。聚合入口在部分版本不导出这些 enum，`FieldType.string` 会触发 `Cannot read properties of undefined (reading 'string')`，命中 `c7n_dataset_enum_invalid_import_source`；兼容 re-export 路径即使有旧项目样例也不能覆盖内置规则，命中 `c7n_dataset_enum_nonstandard_import_source`。至少 major，启动已崩溃时 blocking |
| Table props as any 逃逸 | `columns as any` / `queryBar={.*as any` / `queryBar=\\{.* as any\\}` | Table `queryBar`、`lock`、`align`、columns API 必须有 enum/string provenance；整段 props 逃逸 major |
| enum-map 冒充确认 | 代码导入 `FieldType` / `DataSetSelection` / `ColumnLock` 等但设计只有 `enum-map.md` fallback，无项目 import 证据 | reference 只能 generatedCandidate；production-ready blocking |
| 用户可见内部说明 | 页面 JSX / Modal / Alert / notification 中出现 `Verification(验证)`、`mock/demo`、`generatedCandidate`、`待替换`、`未接生产接口` 等 | 至少 major；暴露内部契约缺口或替代真实错误处理时 blocking |
| 业务按钮权限适用性缺失 | 新建/编辑/删除/提交/撤回/导入/导出/上传/审批等只用普通 `Button`，且 Button Contract 未说明 required / not-applicable / unknown | 权限边界不清 major；required 权限绕过或 production-ready 误报 blocking |
| 破坏性动作缺确认 | 删除/取消/撤回/作废等按钮直接调用 action，未见 `Popconfirm` / `Modal.confirm` / 项目确认组件 | 默认需要二次确认；只有 UI Contract 明确豁免或未保存本地草稿行可直接移除时才可放行 |
| 附件假按钮 | 附件区只有普通按钮、静态列表、自写 request/download、隐藏/禁用入口、占位附件区或无协议 Upload，未接 Attachment / 项目 Attachment wrapper、bucket、attachmentUuid 或文件协议 | 一律至少 major；声明附件能力完成时 blocking，并回 Design / Contract Check 补附件契约 |
| 调试或无效样式残留 | `console.log` / 整段业务样式被注释 / 关键实现以注释保留 | 影响交付质量 major；导致首屏、样式或数据不可用时 blocking |

## 输出要求
Review 或 Implementation 自查命中时，输出：

| 字段 | 说明 |
| --- | --- |
| checkId | 稳定编号，例如 `C7N-SA-001` |
| file/line | 命中文件和行号；无法定位写 `unknown` |
| antiPattern | 命中的反模式 |
| evidence | 代码片段、diff 或缺失证据 |
| severity | blocking / major / minor / info |
| fix | 建议修复动作 |
| relatedTaskId | 能映射则填写；不能映射写 `unmapped + reason` |

静态清单只能证明“代码没有明显反模式”或“命中反模式”；不能替代 browser/manual 的 usable 结论。

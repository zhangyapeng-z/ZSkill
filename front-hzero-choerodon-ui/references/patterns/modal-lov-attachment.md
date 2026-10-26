# Choerodon Modal、Lov 与 Attachment

用于弹窗新增/编辑流程、大对象选择和业务附件场景。

## 最小形态
- 弹窗提交流程的形态必须来自需求/设计/工程证据/用户确认；确认普通 Modal 或 Drawer 后，业务弹层统一使用项目已有 `Modal.open` 或已确认等价 wrapper 打开。Drawer 必须使用 `Modal.open({ drawer: true, resizable: true, ... })` 或等价 wrapper。
- 大数据量对象选择使用 `Lov`。
- 项目标准附件使用 `Attachment`。
- Lookup/值集字段使用 `lookupCode`、generatedCandidate/mockOnly lookup 参数或已确认的 `options`；大业务对象选择默认保留 `Lov` 形态，`lovCode`、返回结构和 bind 缺失时生成候选参数并进入 replacement，不退化为普通输入。

## Non-runnable 骨架
- Modal/Drawer/Overlay：lifecycle、destroy 行为、context/provider 要求、宽度或尺寸、Portal 容器、背景层级，以及关闭阻断策略待项目写法确认。
- Lov：object field、`lovCode`、display field、value field、returned object 和 `bind` mappings 待确认时，保留标准 `Lov` / lookup 组件候选，参数写 `generatedCandidate/mockOnly/placeholderParameter`，并进入 replacement。
- Attachment：attachment field、值结构、UUID lifecycle、bucket/template、preview/download 和 upload protocol 待确认时，保留标准 `Attachment` / confirmed wrapper 组件候选，参数写 `generatedCandidate/mockOnly/placeholderParameter`，并进入 replacement。
- Transport/upload：待确认，暂不配置。

## 护栏规则
- `lovCode`、返回结构、`bind`、UUID lifecycle、bucket 和 upload protocol 都应保留为待确认项。
- 当契约缺失时，不要输出看似可运行的 request 或 upload 配置。
- Modal / Drawer / Overlay 的形态必须来自需求/FDS/TDS、Figma/PageSchema、UI Contract、项目同类页面证据或用户确认；不得默认写死为 Drawer。业务弹层打开方式必须是工程既有 `Modal.open` 或已确认等价 wrapper；确认需要 Drawer 后使用 `Modal.open({ drawer: true, resizable: true, ... })` 或等价 wrapper；确认普通 Modal 后使用 `Modal.open({ ... })` 或等价 wrapper。不得默认改用 JSX Modal/Drawer、组件常驻渲染加 visible state 或自绘 Overlay。
- 详情查看抽屉的内容组件只渲染内容和必要回调；打开、关闭和销毁生命周期由调用方 `Modal.open` 管理，避免页面内常驻隐藏抽屉造成层级穿透或重复状态。
- 业务详情弹层若支持在同一 Modal / Drawer 内切换主业务记录，必须明确当前记录状态源和刷新策略：可以使用内容组件内 `currentRecord/currentDetail/currentId` state、确认过的 modal update/recreate 机制，或重新绑定 owner DataSet / record；不得只调用外层 `detailDS.loadData()` 后假定 `Modal.open` 创建时的 children 会自动重渲染。触发条件是同一详情表面中主记录身份变化，例如候选人、订单、申请单、单据头切换；不适用于列表分页、轮播、步骤向导、Tab/区块切换、附件/图片预览翻页等非业务主记录导航。
- 所有业务 Modal / Drawer / Overlay 的宽度严格按 UI Contract；设计未指定宽度时，普通表单 Modal 默认 `size=small`（约 520px 或项目 small 等价值），详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并记录 readabilityRisk、Form columns/colSpan 与 `valueOverflowPolicy`。medium、large、百分比宽度或 980px 等宽框只在设计/Figma/PageSchema/项目 confirmed baseline/用户明确要求时使用；不得为解决单个长字段而放大弹层。
- Modal / Drawer / Overlay 不得在 `visible=false` 时仍以可见层级覆盖页面；`Modal.open` 应由点击事件触发，或由受控 effect 严格限制生命周期。
- 使用 effect 打开 Modal / Drawer / Overlay 时必须评估依赖项，避免 loading、详情数据或列表刷新导致重复打开。
- Modal / Drawer / Overlay 的 content/body/wrapper 必须有不透明背景，并验证 mask、z-index、Portal 容器、背景层级和关闭后 Header/列表无遮挡。
- Header、固定表头、固定列、列表内容或页面容器出现在 Modal / Drawer / Overlay 内容层上方时，一律视为层级穿透；生产或 production-ready 任务中按 blocking 处理。

## LOV / Lookup / 值集流程
- `lookupCode`：后端/平台值集已确认时，用于值集/下拉类字段。
- `lovCode`：平台 LOV 已确认时，用于带弹窗/表格/搜索行为的对象选择。
- 后端 `@LovValue` / TDS 平台值集使用的 `lovCode` 术语进入前端前必须完成组件语义转换并记录来源：普通枚举/值集下拉可以是 `lookupCode`，主数据对象选择必须保留 `lovCode + object field + bind`。不得把同一字段在“值集/LOV 映射表”写成 `lovCode`、在 DataSet 示例写成 `lookupCode` 后继续交付；这种不一致必须回 Design/Contract Check 对账，不能让 Implementation 任选一个。
- 对象选择：返回对象 key 已知时按 confirmed key 建模并绑定返回字段；未知时按字段语义生成 generatedCandidate value/text/bind，并在 replacement 中标记待确认。
- 主数据字段如申请人、员工、部门、组织、供应商、客户、物料、物料类别，即使当前只拿到 generatedCandidate 编码，也不得降级成状态/类型 `lookupCode`；只能保留 object Lov 候选、local mock 展示值和 replacement。
- 表格展示：状态/lookup 字段可能需要 value、meaning、tag color 或 formatter 映射；渲染标签前要先确认展示来源。
- 查询字段：LOV/lookup 的查询值可能与表单提交值不同；应确认查询提交的是简单值、对象、code、ID 还是文本。
- code 缺失时：输出 `lovCode/lookupCode generatedCandidate` 或 `mockOnly lookup options`，并登记 `replacementRequired=true`、候选来源和生产替换原因；不要把缺 code、valueField、textField 或 bind 升级为流程阻塞，也不要把字段退化为普通 TextField。只有无法判断字段是否为自由文本、对象选择还是值集，或依赖/版本/编译证据明确否定标准 `Lov` / lookup 组件可导入或可实例化时，才回 Design / Contract Check。
- mock/demo 可用 generatedCandidate `lovCode/lookupCode`、本地 mock options 或 mock-only meaning 字段支撑演示；这些候选只能关闭组件级参数缺口，不能关闭 production LOV/lookup 契约。

## Attachment / Upload 流程
- 标准业务附件默认使用 `choerodon-ui/pro` `Attachment` 或目标项目已确认的 Attachment wrapper；当项目存在全局 attachment 配置时，上传、预览、下载、删除、历史记录、全部下载和分片能力优先通过该组件或 wrapper 承载。
- HZERO `components/Attachment` 默认导出在常见工程中是配置对象，合法用法通常是 `import hzeroAttachmentConfig from 'components/Attachment'` 后传给 `components/RichTextEditor` / `NewRichTextEditor`；它不等于标准业务附件 JSX 组件，不得直接 `<Attachment />` 渲染。
- 需确认 attachment 字段名、值结构、UUID lifecycle、bucket/storageCode/template、upload action、preview/download/remove/order 协议，以及是否启用分片上传。仅缺 bucket/storageCode/template/目录这类平台参数时，生成 `mockOnly/generatedCandidate` 常量继续接标准 `Attachment` / confirmed wrapper，并进入 replacement；不得把参数缺口升级成“附件组件不生成”。
- DataSet attachment 字段可能存储类似 UUID 的值，而不是文件数组；在建模字段类型和提交载荷前必须确认。
- 只有当 Attachment 或项目 wrapper 不是项目标准方案，或业务需求明确要求自管理上传流程且已有证据时，才使用更底层/自管理的 `Upload` / `FileUpload`；必须记录降级原因、组件 import、文件值结构和预览/下载协议来源。
- 不得用普通按钮、自写 request、自拼 `HZERO_FILE` URL、静态列表、隐藏/禁用入口或占位附件区实现真实附件预览/下载/删除；缺组件模式、字段/value 结构或组件无法实例化的必要协议时必须标为 missing/blocked 并回 Design / Contract Check 补附件契约。仅缺 bucket/storage/template 等平台参数时只降级参数，不阻塞流程。
- 分片上传需要已确认的 precheck、upload、merge/load、preview/download 和错误处理；仅有 `useChunk` 不够。

## Import / Export 触点
- 列表页导出按钮需要已确认的 permission code 和 endpoint/query 协议。
- DataSet `transport.exports` 只有在导出协议确认后才能使用；否则应将 export 保留为待确认。
- 导入动作需要 template/source、upload endpoint、结果处理、错误明细下载和 permission code；缺 `templateCode` 时只能生成 generatedCandidate/mockOnly 参数并进入 replacement，不得把推断值声明为 confirmed。

## 验证
- Lov/lookup：验证查询值、选中展示、bind/回填字段、清空行为以及提交载荷。
- Attachment/upload：验证上传、预览、下载、删除、校验、失败反馈以及提交后的 attachment 值。
- Modal：验证校验失败/请求失败时弹窗保持打开，以及成功提交后是否遵循已确认的关闭/刷新行为。
- Modal / Drawer / Overlay：验证不会首屏自动打开、不会重复打开、尺寸符合设计或项目证据、背景和层级不穿透、关闭后筛选和分页状态保留。
- 详情弹层主记录切换：刷新页面后打开详情，在同一弹层内切换到另一条主记录再切回；姓名/标题、基本信息 Form、详情区块、Tabs、子表和附件等来自当前记录的区域必须同步更新，首尾边界提示或按钮态符合合同。

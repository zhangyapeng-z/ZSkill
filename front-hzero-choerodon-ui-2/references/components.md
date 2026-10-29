# Choerodon 组件参考

## 目录
- 场景枚举 / 类型事实
- 事实边界
- 选择类组件
- Upload 与 Attachment
- Modal 与 Drawer
- 展示与反馈
- 导入偏好
- 需要确认的未定项

## 场景枚举 / 类型事实
- Pro 组件的枚举/类型事实应优先放在对应组件场景中，而不是拆成独立的 enum-first 检索路径。
- 高频 Pro 组件枚举领域包括 Button、Modal、Lov、Attachment/Upload、DatePicker、Dropdown、Pagination、Cascader、Trigger、ColorPicker，以及核心 tooltip/size 值。
- 当任务需要 Button、Modal、Lov、Attachment 或 Upload 常量时，优先参考当前组件场景和项目 import 风格；如果本文件未覆盖该事实，可用 `references/enum-map.md` 辨析候选枚举域，但生产确认仍应来自用户输入、官方资料或项目源码。
- `ButtonType`、`ViewMode`、`ColumnAlign`、`Placements`、`Size` 这类重名项，必须从目标组件实际使用的精确模块路径导入。
- 涉及组件枚举型 props 时，必须保留 enum provenance：Evidence enum import map、目标项目 import 证据、本文或 `references/enum-map.md` 的 generatedCandidate/fallback 或 not-applicable reason。组件 props 必须使用 enum 形态或项目 confirmed 等价 enum 导出；项目字符串风格只能作为存量风险记录，不能作为新增实现形态。不得把 reference import 单独标为项目 confirmed，也不得用 `as any`、未导入命名空间或静态子组件猜测来绕开 API 证据。

从枚举事实迁入的常见 Pro 组件导入与成员：
- `choerodon-ui/pro/lib/button/enum`
  - `ButtonColor`: `default`, `primary`, `secondary`, `gray`, `blue`, `red`, `green`, `yellow`, `purple`, `dark`.
  - `FuncType`: `flat`, `raised`, `link`.
  - `ButtonType`: `button`, `submit`, `reset`; this is the HTML button kind, not the base button visual type.
  - `IconPlacementType`: `start`, `end`.
  - Re-export: `Tooltip as ButtonTooltip` from `../core/enum`.
- `choerodon-ui/pro/lib/attachment/Attachment`
  - `AttachmentButtonType`: `download`, `remove`, `history`.
  - `AttachmentListType`: `text | picture | picture-card`.
  - `AttachmentButtons`: `AttachmentButtonType | [AttachmentButtonType, ButtonProps] | ReactElement<ButtonProps>`.
- `choerodon-ui/pro/lib/upload/interface`: `UploadFile.status` may include `error`, `success`, `uploading`, `done`, `removed`.
- `choerodon-ui/pro/lib/lov/enum`
  - `ViewMode`: `default`, `button`; `PrefixRule`: `start`, `end`, `include`.
  - `SearchAction`: `blur`, `input`; `SelectionsPosition`: `side`, `below`; `PopupSearchMode`: `single`, `multiple`.
  - Re-exports `LovFieldType` from `choerodon-ui/dataset/enum`.
- `choerodon-ui/pro/lib/modal/interface`: `ModalButtonTrigger.CLICK = 'click'`, `ModalButtonTrigger.MOUSEDOWN = 'mouseDown'`.
- `choerodon-ui/pro/lib/date-picker/enum`: `TimeUnit.hour = 'h'`, `minute = 'm'`, `second = 's'`, `a = 'a'`; re-exports `DateMode as ViewMode`.
- `choerodon-ui/pro/lib/dropdown/enum`: `Placements.bottomLeft`, `bottomCenter`, `bottomRight`, `topLeft`, `topCenter`, `topRight`.
- `choerodon-ui/pro/lib/pagination/enum`: `SizeChangerPosition.left/right`, `QuickJumperPosition.left/right`.
- `choerodon-ui/pro/lib/cascader/enum`: `ExpandTrigger.click`, `hover`, `dblclick`, `check`.
- `choerodon-ui/pro/lib/radio/enum`: `ViewMode.box`, `ViewMode.button`.
- `choerodon-ui/pro/lib/rich-text/enum`: `RichTextToolbarType.normal/none`, `RichTextMode.editor/preview`. 这只用于 Choerodon Pro rich-text；HZERO `NewRichTextEditor` / `RichTextViewer` 归 `front-hzero-common-components`。
- `choerodon-ui/pro/lib/board/enum`: `ViewMode.kanban/card/table`, plus board-specific view field constants; use only for Board scenarios.
- `choerodon-ui/pro/lib/board/enum`: `ViewModeIcon.kanban/card/table` maps to board mode icons; `ViewField` includes board view persistence keys such as `activeKey`, `viewProps`, `viewMode`, `viewName`, `id`, `groupField`, `cardWidth`, `cardLayout`, `buttonPosition`, `buttonSecPosition`, `buttonDisplay`, `commandsLimit`, `cardLayoutData`, `displayFields`, `showLabel`, `sort`, `viewHeight`, and `combineSort`.
- `choerodon-ui/pro/lib/code-area/enum`: `ThemeSwitch.idea`, `material`.
- `choerodon-ui/pro/lib/color-picker/enum`: `ViewMode.default/button`; `ColorUnit.hex/r/g/b/a`.
- DataSet enum 固定使用 `choerodon-ui/pro/lib/data-set/enum`。不得从 `choerodon-ui/pro` 聚合入口导入 `FieldType`、`DataSetEvents`、`RecordStatus`、`DataToJSON`、`CheckedStrategy`、`NumberRoundMode` 等 DataSet enum；`import { DataSet, FieldType } from 'choerodon-ui/pro'` 会在部分版本运行时得到 undefined enum，命中 `c7n_dataset_enum_invalid_import_source`。`choerodon-ui/dataset/enum` 等 re-export 不是生成坐标，即使目标工程存在旧样例也只作为历史兼容/冲突证据，命中 `c7n_dataset_enum_nonstandard_import_source`；若标准坐标不可用，blocked 并回 Choerodon owner 专项确认。
- `choerodon-ui/pro/lib/locale-context/enum` re-exports `Lang`; use project i18n configuration instead of copying full language lists into page code.
- `choerodon-ui/pro/lib/trigger/enum` re-exports base trigger `Action`, `ShowAction`, and `HideAction`.
- `choerodon-ui/pro/lib/core/enum`: `Tooltip.none/always/overflow`, `WaitType.throttle/debounce`, `FieldFocusMode.checked/focus`.

从枚举事实迁入的基础组件兜底导入：
- 只有当项目使用基础组件，或 Pro 明显不适用时，才使用基础 `choerodon-ui/lib/...` 枚举。
- `choerodon-ui/lib/_util/enum`：`Size.default`、`small`、`large`。
- `choerodon-ui/lib/bar-code/enum`：`CodeType.QR = 'qr'`、`CodeType.BAR = 'bar'`。
- `choerodon-ui/lib/carousel/index`：`CarouselTheme.DARK = 'dark'`、`CarouselTheme.LIGHT = 'light'`。
- `choerodon-ui/lib/image-crop/enum`：`ShapeCroper.rect`、`round`。
- `choerodon-ui/lib/progress/enum`：`ProgressType.line/circle/dashboard/loading`、`ProgressStatus.normal/success/active/exception`、`ProgressPosition.top/bottom/left/right`。
- `choerodon-ui/lib/responsive/enum`：`Breakpoint.xxl/xl/lg/md/sm/xs`。
- `choerodon-ui/lib/button/Button`：基础 `ButtonType` 为 `default | primary | ghost | dashed | danger`；基础 `ButtonFuncType` 为 `raised | flat`；基础 `ButtonHTMLType` 为 `submit | button | reset`。
- `choerodon-ui/lib/select/enum`：`SelectMode.default`、`multiple`、`tags`、`combobox`。
- `choerodon-ui/lib/cascader/enum`：`MenuMode.single`、`multiple`。
- `choerodon-ui/lib/dropdown/enum`：`Placements.bottomLeft`、`bottomCenter`、`bottomRight`、`topLeft`、`topCenter`、`topRight`。
- `choerodon-ui/lib/form/enum`：`FormLayout.horizontal`、`inline`、`vertical`；`FormItemValidateStatus.success`、`warning`、`error`、`validating`。
- `choerodon-ui/lib/table/enum`：`TableAutoHeightType.maxHeight`、`minHeight`。
- `choerodon-ui/lib/tabs/enum`：`TabsType.line`、`card`、`editable-card`、`second-level`；`TabsPosition.top`、`bottom`、`left`、`right`。
- `choerodon-ui/lib/trigger/enum`：`Action.click/focus/hover/contextMenu`、`ShowAction.click/focus/mouseEnter/contextMenu`、`HideAction.click/blur/mouseLeave`。
- `choerodon-ui/lib/tree/enum`：`TreeEvent.check`、`select`；`choerodon-ui/lib/transfer/enum`：`TransferDirection.left/right/up/down`。

## 事实边界
本文件只记录常见组件选型中可直接影响实现和审查的事实。

如果这里没有覆盖某个组件事实，不要编造 props、events、defaults 或协议。应视为未确认，并要求提供用户输入、官方资料或项目证据。

## Tabs 与 TabPane
Choerodon Pro Tabs 使用 `Tabs` 聚合组件承载页签子组件。`TabPane` 不作为 `choerodon-ui/pro` 的独立命名导出使用；不要写 `import { Tabs, TabPane } from 'choerodon-ui/pro'`，该写法在按需构建中会解析到不存在的 `choerodon-ui/pro/lib/tab-pane`。

默认正向写法：

```tsx
import { Tabs } from 'choerodon-ui/pro';

<Tabs defaultActiveKey="lines">
  <Tabs.TabPane tab="采购申请明细" key="lines">
    {/* table or detail content */}
  </Tabs.TabPane>
</Tabs>
```

若目标项目已有健康相似页面使用本地别名，可在记录 `componentApiProvenance` 后采用：

```tsx
import { Tabs } from 'choerodon-ui/pro';

const TabPane = Tabs.TabPane;
```

`Tabs.TabPane` 属于静态子组件 API，必须在 Component Import Contract / `componentApiProvenance` 中记录 exportShape 为 `static-member` 或项目等价证据。不得用 `const { TabPane } = Tabs as any`、薄 wrapper 或未确认的项目旧 wrapper 掩盖来源。

## 组件决策清单
选择组件时先输出或内部确认以下结论：
- 推荐组件：具体到项目自定义组件、HZERO 封装、Pro 组件、基础组件或原生元素。
- 数据模型：DataSet field、query field、Table column、Form field、局部只读展示或自管状态。
- 适用理由：数据量、是否对象回填、是否需要分页/弹窗、是否需要上传协议、是否参与提交/查询/校验。
- 不推荐项：至少说明一个容易误用的替代项及原因，例如 Select vs Lov、Upload vs Attachment、基础 Form/Table vs Pro Form/Table、本地 state vs DataSet。
- 事实缺口：组件 API、import 路径、选项来源、返回结构、生命周期、权限或上传协议。

代码生成前的硬门槛：
- 字段组件参与 Form/Table/DataSet 行为时，优先通过 `name` 或列 `name/editor` 绑定，不重复保存本地 `value/onChange`。
- `Select`、`Lov`、`Attachment`、`Upload`、`Modal/Drawer` 的协议类 props 必须来自已确认事实。
- 组件 props、全局 configure props 和 DataSet 字段元数据必须按宿主归位；不得把 Lov/Table/Form/Attachment/Modal 的组件属性默认展开到 DataSet `fields/queryFields` 中。若某组件属性确实支持 field-level 配置，必须有目标版本类型声明、官方资料或项目源码证据，并记录 `componentApiProvenance`。
- 仅视觉或 Figma 候选不能确认组件 API；只能作为候选组件和待确认项。
- 基础 `choerodon-ui` 组件必须有明确理由；不能因为 API 熟悉或示例简单就替代 Pro 组件。

## 选择类组件
团队偏好：业务组件优先使用 `choerodon-ui/pro`。只有在纯展示/布局/反馈场景，或项目证据表明 Pro 没有合适组件时，才考虑基础 `choerodon-ui`。

- `SelectBox`：适用于选项较少、可平铺展示的场景。
- `Select`：适用于普通枚举或多选下拉；字段 `lookupCode` 可驱动值列表选项。
- `Lov`：适用于弹窗式大数据量值选择；production confirmed 需要后端值集接口以及已确认的字段配置，例如 `lovCode`。默认 mock/demo 或候选实现可先保留 `Lov` 形态，用 `generatedCandidate/mockOnly` 参数承接，不能退化为普通输入。
- `TreeSelect`：树节点选择。
- `Cascader`：层级路径/级联选择。
- `AutoComplete`：既需要自由输入又需要建议提示时的文本输入。

不要把无来源 `lovCode` 或 `lookupCode` 声明为 confirmed。若只缺平台 code，默认 mock/demo 下生成 `generatedCandidate/mockOnly` 参数并进入 replacement；只有无法判断字段是自由文本、值集、对象选择或 value shape 时，才列为阻塞待确认项。

后端 `@LovValue`、平台“值集”或 TDS 中的 `lovCode` 术语不能被 Implementation 静默等同为前端 `lookupCode` 或 `lovCode`。Design 必须按前端组件语义在 `LOV Lookup Binding Contract` 中写清 `semantic`、`codeType`、`code`、来源和转换原因：状态、类型、用途、来源、渠道等普通枚举/值集下拉可落为 `Select + lookupCode`；申请人、员工、部门、组织、供应商、客户、物料、物料类别等主数据对象选择默认落为 `Lov + FieldType.object + lovCode + bind`。如果设计表格、Contract Check 或编码候选表已明确 `codeType=lovCode`，DataSet 示例和实现不得自行改成 `lookupCode`；若发现同一字段在映射表与 DataSet 示例中 `lovCode/lookupCode` 不一致，必须标记 `conflict` 并回 Design/Contract Check 对账。

主数据字段不得用无关业务值集 `lookupCode` 冒充对象选择。典型反例包括 `applicantId/deptId/itemCategoryId/itemId` 使用 `lookupCode: 'HSPD.PRM.URGENCY'`、`lookupCode: 'HSPD.PRM.PURCHASE_TYPE'` 等状态/类型值集；这同时违反字段语义、组件类型和编码来源，不能作为 mock/demo 或 production 候选完成态。

选型决策矩阵：
- 少量扁平选项：`SelectBox` + `options` 或 `lookupCode`
- 普通枚举/值集：`Select` + `lookupCode` 或 `options`
- 无弹窗表格的可搜索下拉：`Select`
- 输入联想：`AutoComplete`
- 复杂对象或大数据量选择：`Lov`
- 需要回填 code/name 等关联字段的业务对象选择：`Lov` + DataSet object field + 已确认 returned-field mapping
- 树节点值：`TreeSelect`
- 层级路径数组：`Cascader`
- 弹窗树表对象：树形 `Lov`

建模说明：
- `Select` 通常使用 `lookupCode`、`options`、`textField`、`valueField` 或 `cascadeMap`。
- `lookupCode` 只适用于普通枚举/值集下拉或已确认的 lookup wrapper；不得挂到主数据 `*Id` 提交字段上替代 `Lov`。如果字段语义是主数据但只有后端 `@LovValue` 或平台编码线索，先生成 object LOV 候选和 replacement，不要把编码改写成 unrelated lookup。
- 新生成 `Lov` 字段必须使用 DataSet object field，配合 `lovCode`、`textField`、`valueField` 以及用于额外返回字段的 `bind`。confirmed 值和映射必须来自项目证据或用户提供的契约；默认 mock/demo 候选实现可用 generatedCandidate 映射并进入 replacement。
- 对于自然语言描述的对象选择且需要回填关联字段的场景，使用 `Lov` + DataSet object field；项目证据出现之前，`lovCode`、返回对象字段、业务字段名和 `bind` 映射可保留为 generatedCandidate/mockOnly 候选，不得声明 confirmed 或 production-ready。不要把 `xxxId` 直接配置成 `FieldType.string + lovCode + textField/valueField`；这是新生成 LOV 的反例，不作为兼容推荐。
- 运行时映射事实：`lovCode + FieldType.object` 才进入 Lov object 值模式；`lovCode + FieldType.string/number` 会走 Select primitive 值模式；省略 `type` 依赖 `auto` 推断不是新生成代码合格形态，必须显式写 `FieldType.object`。
- 当需要回填多个字段时，不要默认把客户/供应商类业务对象选择推荐成 `Select`。只有在选项小而固定、不需要弹窗表格或分页、只需单一简单值且值/展示来源已确认时，才使用 `Select`。
- `TreeSelect` 的 options DataSet 应用 `idField + parentField` 或 `childrenField` 建模树数据。
- `Cascader` 返回路径结构：单选是 `[a, b, c]`，多选是 `[[a, b, c], [a, b, d]]`。
- 字段级 `cascadeMap` 用于选项过滤。主从查询依赖应使用 DataSet `children + cascadeParams`。

Lov 细节：
- Lov 依赖后端 define/query 能力；不要假设一定存在 `lovCode`。
- 有用的全局/项目配置可能包括 Lov define/query 请求配置、批量 define 配置、table/modal props、queryBar props、`lovNoCache` 和 auto-select-single 行为。
- `noCache` 是 Lov 组件行为属性，`lovNoCache` 是全局配置能力；它们都不是 DataSet 通用属性，也不是 `fields/queryFields` 默认生成项。新生成代码不得在 DataSet 字段配置中写 `noCache: false` 这类冗余默认值；只有项目 confirmed 证据或明确需求要求关闭 Lov 缓存时，才允许在 Lov 组件或已确认配置入口设置 `noCache: true` / `lovNoCache`，并记录来源。
- 自定义 `lovDefineUrl` / `lovQueryUrl`、全局 define/query axios config 和批量 define 配置必须来自项目配置、用户契约或后端文档；不得从 `lovCode`、页面名或服务简码反推生成真实 URL。
- `modalProps` 和 `tableProps` 在已确认时可以覆盖 Lov 弹窗/表格行为。
- `viewMode` 可能是 modal、drawer 或 popup。
- 树形 Lov 可以由后端树配置或显式表格树模式驱动，但精确字段必须确认。
- 对象展示/回填依赖返回对象结构与 `textField`、`valueField`、`bind` 匹配。
- `combo` 只改变 Lov 输入交互，不改变字段建模底座；仍应使用 object LOV 容器，并按已确认的 `textField/valueField/bind` 处理复合输入对象和提交字段。

Lov 参数与示例边界：
- 基础示例必须保持 `{ name: 'xxxObj', type: FieldType.object, lovCode, textField, valueField }` + `<Lov name="xxxObj" />` + `{ name: 'xxxId', bind: 'xxxObj.<valueField>' }` / `{ name: 'xxxName', bind: 'xxxObj.<textField>' }` 的闭环。
- 当后端/API 字段是 `xxxId + xxxName`、`xxxCode + xxxMeaning` 或同类提交/展示字段时，不要把提交字段本身改成 object。应新增独立 Lov object 容器，再用 `bind` 回填原业务字段；例如：
  ```typescript
  { name: 'applicantObj', type: FieldType.object, lovCode: 'HPFM.USER_NAME', textField: 'realName', valueField: 'id' },
  { name: 'applicantId', type: FieldType.string, bind: 'applicantObj.id' },
  { name: 'applicantName', type: FieldType.string, bind: 'applicantObj.realName' },
  ```
  其中 `lovCode`、`textField`、`valueField` 必须来自项目证据、后端契约或用户确认；缺证据时可作为 `generatedCandidate` / replacement 输出，但仍保持 object + bind 结构，不退化为 `applicantId: FieldType.object` 或 `applicantId: FieldType.string + lovCode`。
- 静态 `lovPara` 只适合后端契约明确给出的固定过滤条件；动态参数使用 `dynamicProps: { lovPara: ({ record }) => ({ confirmedParam: record.get('confirmedField') }) }`，参数名、依赖字段和空值行为必须来自 UI Contract / FDS/TDS/API / 项目 confirmed evidence。
- 级联 LOV 例如“物料按物料类别过滤”时，子 LOV 的 `lovPara` 应从已回填的 submit 字段读取；若父字段未选择时的查询行为未确认，必须记录为 missing / replacement，不得静默传空字符串伪造可用。
- `lovPara` 审查触发条件包括：子 LOV 依赖父字段，员工/申请人/部门依赖组织、租户、公司或岗位，供应商/客户依赖业务类型或组织范围，查询区 LOV 与明细行 LOV 参数来源不同，同一 `lovCode` 在不同页面/区域过滤条件不同。命中后必须补齐 `paramName`、`paramSourceField`、`sourceTiming`、`emptyValueBehavior`、`cascadeClearPolicy`、`confirmedSource`；缺任一生产参数时，不得声明 LOV 契约闭合或 production-ready。
- 缺 confirmed 参数契约时，可以保留 object LOV + `bind` 的候选能力，但不得输出 `lovPara: { xxx: '' }`、不得从 label/字段名推导参数名、不得用页面 state 或未绑定字段冒充参数来源；必须把 `lovParaContract=missing/partial` 写入 replacement / handoff risk。
- 自定义 define/query URL 示例只能作为组件能力说明；生成代码不得直接套用教程里的 `/test_define/...`、`/test_query/...` 或 mock host。
- 批量 define 示例属于全局性能配置，只有项目全局配置入口和后端批量接口已确认时才写入；单页面业务代码不得临时新增全局 `configure` 来掩盖 LOV 契约缺口。
- `lovQueryBatchAxiosConfig` 是 Lov 批量查询显示值的全局能力，响应结构、key 规则和返回 record shape 必须由项目或后端确认；不得为解决回显问题在页面内临时新增全局批量查询配置。
- `combo` 示例中的 `__dirty` 只说明复合输入对象需要重建；生成代码若使用 combo，必须明确构造对象、回填字段和提交/持久化策略，否则不要启用 combo。

## Upload 与 Attachment
- HZERO + Choerodon 标准业务附件的业务契约、bucket/storage/template、只读展示、权限、mock/demo 和 production replacement 归 `front-hzero-attachment`。本节只保留 Choerodon 组件事实和基础选型提示。
- 标准业务附件默认使用 Choerodon Pro `Attachment` 或目标项目已确认的 Attachment wrapper；常规为 `choerodon-ui/pro` 命名导入，若目标版本运行证据显示桶入口循环依赖或 `ReferenceError: Attachment is not defined`，可按 `front-hzero-attachment` 使用 `choerodon-ui/pro/lib/attachment` 默认导入并记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed`。附件上传、列表展示、预览、下载、删除、全部下载、历史记录和 Attachment 内部分片能力优先交给 Attachment 全局配置或项目 wrapper 承载。需求明确为 HZERO `ChunkUploader` 时转 `front-hzero-common-components`，不得当作 Attachment。
- HZERO `components/Attachment` / `hzero-front/lib/components/Attachment` 的默认导出在常见 HZERO 工程中是附件配置对象而不是 React component；合法场景通常是 `import hzeroAttachmentConfig from 'components/Attachment'` 后传给 `components/RichTextEditor` / `NewRichTextEditor` 等 HZERO 富文本组件。不得把该 config object 作为 JSX 组件；`<Attachment />` 会触发 React #130 `element type invalid / got object`。只有项目证据证明该路径是 confirmed wrapper 且 exportShape 为 React component 时才允许 JSX 渲染。
- `Attachment`：业务附件上传/展示组件，通常依赖全局配置来处理上传服务、action、回调、文件列表获取、UUID 创建、预览、全部下载、分片上传和历史记录。
- 当项目版本和既有 DataSet 用法确认这种建模方式时，`Attachment` 可以通过 attachment field 绑定到 DataSet。
- `Upload` / `FileUpload`：更底层或更灵活的上传控件；只有在确认 Attachment 或项目 Attachment wrapper 不适合作为业务标准方案后才使用，并必须记录原因和证据。
- 不得用普通 `Button`、手写 request、静态 `<ul>` 文件列表、自拼文件 URL、隐藏/禁用入口或占位附件区冒充真实附件预览/下载/删除能力；缺组件模式或文件协议时按 `front-hzero-attachment` 标为 missing/blocked 并补附件契约。

不要编造 bucket、template、UUID 来源、上传 URL、分片协议、预览 URL 或下载 URL。

Attachment 决策矩阵：
- 标准业务附件：`Attachment` 或项目 Attachment wrapper
- DataSet 表单附件：attachment field + `Attachment` / 项目 wrapper，精确字段类型和值结构需根据项目用法或 reference 确认
- 拖拽式业务附件：`Attachment.Dragger`
- Attachment 分片上传：`Attachment` + 已确认的全局附件配置与后端协议；HZERO `ChunkUploader` 分片上传：转 `front-hzero-common-components`
- 自管业务逻辑的简单上传按钮/列表：Pro `Upload`，仅当 Attachment 不适用的原因已确认
- Pro 模型之外的基础包上传：核心 `Upload`，仅当项目证据确认 Pro `Attachment` / Pro `Upload` 都不适合时使用

Attachment 事实：
- Attachment 字段值常常是附件 UUID 字符串，而不是文件对象数组；但精确值结构和生命周期必须根据项目协议确认。
- Attachment 的 component import contract 必须记录 `importPath` 与 `exportShape`；`choerodon-ui/pro` 命名导入 `Attachment` 是默认候选，目标版本证据证明桶入口不安全时 `choerodon-ui/pro/lib/attachment` 默认导入是允许候选。`hzeroAttachmentConfig`、namespace/config object/default object 只能作为配置对象传给已确认组件 API，不能直接进入 JSX。
- 字段可以建模 `accept`、`max`、`template`、`required`。
- 常见组件 props 包括 `accept`、`bucketName`、`bucketDirectory`、`storageCode`、`template`、`multiple`、`directory`、`withCredentials`、`listType`、`viewMode`、`sortable`、`fileKey`、`fileSize`、`useChunk`、`chunkSize`、`chunkThreads`、`count`、`max`、`showHistory`、`downloadAll`、`showSize`、`previewTarget`、`isPublic`、`buttons`、`uploadImmediately`、`removeImmediately`、`removeConfirm`、`downloadAllMode`、`enableDeleteAll`。
- 分片上传通常还需要全局 attachment hooks，例如上传 action、分片预检、成功后合并/回载行为、预览/下载 URL、文件大小、UUID、删除/排序回调。
- 仅设置 `useChunk` 不足以完成分片上传。

## Modal 与 Drawer
- `Modal`：适用于用户无需页面跳转即可完成事务处理，或用于确认对话框。
- 使用 hook/provider 模式时，页面应包裹 `ModalProvider`。
- `Modal.open`、`useModal`、`modal.handleOk`、`modal.handleCancel`、`modal.update` 以及异步 `onOk/onCancel` 都属于文档化用法。
- Drawer 行为依赖 modal/drawer 生命周期和配置默认值；在生成代码前应先确认精确 API。

Modal 与 Drawer 的选择：
- 短表单、确认操作、选择器、轻量编辑或局部配置，优先选 Modal。
- 需要保留列表上下文，同时查看/编辑较大内容时，优先选 Drawer。
- `Modal.open(props)` 会返回一个带 close/open/update 行为的控制器。
- `destroyOnClose` 默认值为 true。
- `drawer` 默认值为 false；drawer 过渡默认是从右侧滑入。
- `onOk`、`onCancel` 或 `onClose` 返回 `false`、resolve `false` 或 reject 都可以阻止关闭。
- Modal/Drawer 中的表单提交应先校验 DataSet；校验失败或请求失败都应阻止关闭。
- 当 `destroyOnClose=false` 时，应使用稳定 key 和显式状态策略。

## 展示与反馈
- `Output`：只读字段展示。
- 当项目用法允许且保持一致时，优先使用 Pro `Tooltip`、`Spin`、`Skeleton`、`Progress`、`Dropdown`、`Pagination`、`Button`、`Typography` 等相关 Pro 组件。
- 基础 `choerodon-ui` 的展示/布局/反馈组件只应在检查过项目先例后，作为非 DataSet 驱动 UI 的兜底方案。
- 当组件需要绑定 DataSet 字段，或参与 Pro Form/Table 行为时，优先使用 Pro 组件。

## 导入偏好
- 业务表单、表格、字段输入、Lov、Attachment、Modal/Drawer、hooks 和 DataSet 通常应从 `choerodon-ui/pro` 导入。
- 仅 DataSet 工具在部分项目中也可能从 `choerodon-ui/dataset` 出现；应遵循项目现有 import 风格。
- 基础 `choerodon-ui` 导入应有明确理由，例如纯展示/布局需求，或确实缺少 Pro 对应组件。

## 需要确认的未定项
- 选择的单/多值基数、值结构、展示字段、取值字段。
- Lov/值集 code 以及后端是否可用。
- Attachment UUID 生命周期、上传/下载/预览协议，以及 bucket/template 配置。
- Modal 生命周期：成功后是否关闭、是否异步提交、是否保留/销毁状态、校验失败后的行为。
- 选择结果返回的是简单值、对象、树节点值还是路径数组。
- 后端是否支持 Lov 视图配置、lookup 值、attachment UUID、分片上传以及预览/下载协议。

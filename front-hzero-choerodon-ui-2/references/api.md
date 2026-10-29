# Choerodon API 参考

## 目录
- 事实边界
- 导入与组件来源
- DataSet
- 字段属性
- Form
- Table
- Lov
- Attachment
- Modal / Drawer
- Configure / ConfigProvider

## 事实边界
本文件只记录高频 Choerodon UI / Pro API 事实，用于具体 props、methods、events 或绑定名判断。

如果这里或同级 reference 没有覆盖某个事实，应视为未确认，并在生成 runnable 代码前从用户输入、官方资料或项目源码核实。

## 导入与组件来源
团队偏好是 Pro-first：
- `choerodon-ui/pro` 用于 DataSet 驱动的业务 UI，包括 Form、Table、字段输入、Lov、Attachment、Modal/Drawer、hooks 以及业务反馈组件。
- 只有当项目代码已经把 DataSet 导入拆分为 `choerodon-ui/dataset`，或任务纯属 DataSet 建模时，才使用 `choerodon-ui/dataset`。
- 基础 `choerodon-ui` 只用于纯展示/布局/反馈，或项目证据表明没有合适的 Pro 组件。

当 Pro 与基础组件看起来都可用时，除非现有项目代码证明相反，否则优先选择 Pro。

## DataSet
高频 props：
- 标识/查询：`name`、`primaryKey`、`autoQuery`、`autoCreate`、`queryFields`、`queryDataSet`、`queryParameter`
- 协议：`queryUrl`、`submitUrl`、`tlsUrl`、`validateUrl`、`exportUrl`、`transport`、`dataKey`、`totalKey`、`countKey`、`dataToJSON`
- 分页/选择：`pageSize`、`paging`、`selection`、`selectionStrategy`、`cacheSelection`、`cacheModified`
- 建模：`fields`、`record`、`children`、`cascadeParams`、`idField`、`parentField`、`childrenField`、`expandField`、`checkField`
- 校验/配置：`validateBeforeQuery`、`forceValidate`、`validationRules`、`modifiedCheck`、`feedback`

高频值：
- 当前/分页/状态：`current`、`currentPage`、`currentIndex`、`totalCount`、`totalPage`、`pageSize`、`status`
- 记录/选择/缓存：`records`、`data`、`created`、`updated`、`destroyed`、`selected`、`currentSelected`、`cachedSelected`、`cachedModified`、`cachedRecords`
- 结构：`fields`、`queryDataSet`、`parent`、`children`、`dirty`、`sortedTreeData`

高频方法：
- 生命周期/查询：`ready()`、`query(page, params, cache)`、`queryMore(page, params)`、`loadData(data, total, cache)`、`appendData(data, parentRecord, index)`
- 提交：`submit()`、`submitRecord(record, strictPageSize)`、`forceSubmit()`
- record 变更：`create(data, index)`、`delete(records, confirmMessage)`、`remove(records, forceRemove)`、`deleteAll(confirmMessage)`、`removeAll(forceRemove)`、`reset()`
- 导航/遍历：`locate(index)`、`page(page)`、`first()`、`last()`、`pre()`、`next()`、`forEach(fn)`、`map(fn)`、`filter(fn)`、`find(fn)`、`findIndex(fn)`
- 选择：`select(recordOrIndex)`、`unSelect(recordOrIndex)`、`selectAll()`、`unSelectAll()`、`batchSelect(recordOrId)`、`batchUnSelect(recordOrId)`、`treeSelect(record)`、`treeUnSelect(record)`、`setAllPageSelection(enabled)`
- 字段/状态/序列化：`validate()`、`getValidationErrors()`、`getField(fieldName)`、`addField(fieldName, fieldProps)`、`toJSONData()`、`toData()`、`bind(ds, name)`、`setQueryParameter(para, value)`、`getQueryParameter(para)`、`setState(key, value)`、`getState(key)`

高频事件：
- 查询/加载：`query`、`beforeLoad`、`load`、`loadFailed`、`beforeAppend`、`append`
- 提交：`submit`、`submitSuccess`、`submitFailed`
- 值/字段/record：`update`、`indexChange`、`fieldChange`、`create`、`remove`、`reset`
- 选择：`select`、`unSelect`、`batchSelect`、`batchUnSelect`、`selectAllPage`、`unSelectAllPage`
- 守卫：`beforeRemove`、`beforeDelete`、`export`、`validate`、`validateSelf`

`query`、`submit`、`export`、`beforeRemove`、`beforeDelete` 等事件在返回 `false` 时可阻止操作。

## 字段属性
高频 props：
- 基础：`name`、`type`、`label`、`labelWidth`、`defaultValue`、`help`、`highlight`、`order`
- 校验：`required`、`pattern`、`maxLength`、`minLength`、`max`、`min`、`maxExcl`、`minExcl`、`step`、`precision`、`validator`、`unique`
- 状态/联动：`readOnly`、`disabled`、`multiple`、`range`、`bind`、`dynamicProps`、`computedProps`
- 选项/对象：`textField`、`valueField`、`trueValue`、`falseValue`、`options`、`optionsProps`、`group`、`lovCode`、`lovPara`、`lookupCode`、`lookupUrl`、`lookupAxiosConfig`、`cascadeMap`
- 转换：`transformRequest`、`transformResponse`

DataSet `fields/queryFields` 只能承载 FieldProps / 字段元数据。Lov/Table/Form/Attachment/Modal 组件 props 或 configure props 不得默认写入字段项；例如 `noCache`、`modalProps`、`tableProps`、`selectionProps`、`queryBarProps`、`labelLayout`、`bucketName`、`storageCode`、`uploadImmediately` 都不属于默认字段配置。确有 field-level 支持时必须记录目标版本类型声明、官方资料或项目源码证据。

已确认字段类型包括 `boolean`、`number`、`string`、`date`、`dateTime`、`time`、`week`、`month`、`quarter`、`year`、`email`、`url`、`intl`、`object`、`attachment`、`json`、`bigNumber`、`secret`。

字段类型清单只表示语义值，不表示代码应直接写字符串。生成代码必须按 enumProvenance 选择形态：空项目、缺参考子模块或 asset/fallback baseline 默认导入 `FieldType` 并写 `type: FieldType.<member>`；只有目标项目健康样例确认 `project-string-confirmed` 时才允许字符串形态。`type: '<fieldType>' as const` 这类任意 DataSet 字段类型字符串加 TS assertion 的写法仍属于裸 enum-like 字符串和类型逃逸，不得作为缺类型报错时的修复方式。

## Form
高频 props：
- 绑定：`dataSet`、`dataIndex`、`record`、`pristine`
- 布局：`layout`、`columns`、`labelWidth`、`labelAlign`、`labelLayout`、`labelTooltip`、`labelWordBreak`、`useColon`、`requiredMarkAlign`、`separateSpacing`、`spacingType`
- 校验/渲染：`showValidation`、`autoValidationLocate`、`fieldHighlightRenderer`
- 不依赖 DataSet 的原生提交：`action`、`method`、`target`、`processParams`
- 事件：`onSubmit`、`onReset`、`onSuccess`、`onError`

`record` 的优先级高于 `dataSet + dataIndex`。Form 下的字段组件可使用 `rowSpan`、`colSpan`、`newLine`、`hidden`、`label`、`name`、`labelWidth` 等布局属性。

## Table
高频 props：
- 数据/列：`dataSet`、`columns`、`groups`、`header`、`footer`、`border`
- 查询：`queryBar`、`queryBarProps`、`queryFields`、`queryFieldsLimit`、`searchCode`
- 动作：`buttons`、`buttonsLimit`
- 选择：`selectionMode`、`alwaysShowRowBox`、`showSelectionTips`、`showCachedTips`、`showAllPageSelectionButton`、`selectionColumnProps`
- 展示/编辑：`mode`、`editMode`、`pagination`、`filter`、`treeFilter`、`keyboard`、`editorNextKeyEnterDown`
- 行/树：`onRow`、`rowHeight`、`defaultRowExpanded`、`expandedRowRenderer`、`expandRowByClick`、`treeLoadData`、`treeAsync`、`treeQueryExpanded`
- 性能/定制：`virtual`、`virtualCell`、`virtualSpin`、`autoHeight`、`customizable`、`customizedCode`、`columnResizable`、`columnHideable`、`columnDraggable`、`rowDraggable`

列属性：
- `name`：绑定 DataSet 字段。
- `editor`：为 `true` 时优先使用内置编辑；只有字段元数据不足时才传入组件。
- `renderer`：自定义展示逻辑；大表中应保持轻量。
- `command`：内置或自定义行操作。

查询渲染：
- DataSet `queryFields` 定义查询模型，并可生成 `queryDataSet`。
- Table `queryFields` 只覆盖查询字段渲染，例如把数字字段渲染替换成特定输入组件。
- 默认查询字段渲染取决于 DataSet field 元数据：`lookupCode`、字符串 `lookupUrl`、`lookupAxiosConfig`、非 object 字段上的 `options` 映射为 `Select`；满足 Select 条件且有 `parentField` 时映射为 `TreeSelect`；`lovCode + FieldType.object` 映射为 `Lov`。`lovCode + FieldType.string/number` 在 Choerodon 运行时会走 Select / 原始值模式，不会得到 object Lov 回填能力。
- 当 Table 使用 filterBar 查询形态时，代码必须按 enumProvenance 写为 `queryBar={TableQueryBarType.filterBar}` 或项目确认的等价 enum 导出；`onQuery`、`onReset`、`onRefresh`、`onBeforeQuery`、`onFieldEnterDown` 等查询条生命周期回调应放在 `queryBarProps` 中，而不是顶层 `Table` props。
- 对于本地 mock 过滤，应把过滤逻辑放进 `queryBarProps.onQuery`，从生成的 `queryDataSet` 读取值，将过滤后的本地行回灌到 DataSet，并在需要阻止默认远程查询时返回 `false`。

## Lov
Lov 用于大数据量值选择，依赖后端值集视图/数据能力。

高频 props：
- popup/table/modal：`modalProps`、`tableProps`、`selectionProps`、`viewMode`
- 行为：`combo`、`noCache`、`showDetailWhenReadonly`
- 常见 DataSet 字段 props：`type: FieldType.object`、`lovCode`、`lovPara`、`textField`、`valueField`、`bind`。新生成 LOV 只能由显式 object 容器字段承载 `lovCode/textField/valueField`；`FieldType.string + lovCode` 会按 Select 原始值模式渲染，是反例；省略 `type` 依赖 `auto` 推断不是生成代码合格形态。string 字段只用于经 `bind` 回填的提交/展示值。

后端字段为 `xxxId + xxxName`、`xxxCode + xxxMeaning` 等提交/展示对时，生成模板必须是独立 object 容器 + 原业务字段 bind，例如 `{ name: 'applicantObj', type: FieldType.object, lovCode, textField: 'realName', valueField: 'id' }`、`{ name: 'applicantId', bind: 'applicantObj.id' }`、`{ name: 'applicantName', bind: 'applicantObj.realName' }`。不要把 `applicantId` 本身改成 object 容器，也不要只写 `applicantObj` 而遗漏同 DataSet 内的 submit/display bind 字段。

`combo`、`noCache`、`showDetailWhenReadonly`、`modalProps`、`tableProps`、`selectionProps` 和 `viewMode` 是 Lov 组件/配置宿主属性，不是 DataSet field/queryField 默认属性。不要为了“补全 Lov 配置”把这些 key 写入 DataSet 字段；`noCache: false` 是冗余默认值，应删除。

有用事实：
- 在适用情况下，`modalProps` 和 `tableProps` 的优先级高于后端 view config。
- 树形 Lov 可依赖后端 `treeFlag`、`idField`、`parentIdField`；当后端无法识别树模式时，可在已确认前提下使用 `tableProps={{ mode: 'tree' }}`。
- `viewMode` 在项目用法已确认时可用于 modal、drawer 或 popup 模式。
- `lovCode` 的组件走向由 `type` 决定：`FieldType.object` 走 Lov object 值模式；`FieldType.string/number` 等具体类型走 Select primitive 值模式；`auto` / 缺 type 不作为新生成代码默认。
- `lovDefineUrl` / `lovQueryUrl` 可来自字段、DataSet 或全局配置，但必须由项目配置、用户契约或后端文档确认；不得根据 `lovCode` 自行编造接口。
- `lovPara` 用于向 Lov 查询传递过滤参数。静态参数、动态参数名和值来源都必须来自已确认契约；动态参数优先通过 DataSet `dynamicProps` 从当前 record/query field/context 读取，不能从字段 label、页面名或相似经验推导。只要 LOV 存在父子级联、组织/租户/公司/岗位范围、查询区与行编辑区参数来源差异、或同一 `lovCode` 在不同页面有不同过滤条件，必须在 `LOV Lookup Binding Contract` 补齐 `paramName`、`paramSourceField`、`sourceTiming`、`emptyValueBehavior`、`cascadeClearPolicy` 和 `confirmedSource`；缺契约时只能生成不带 `lovPara` 的 object LOV 候选并登记 replacement / handoff risk，不得写固定空字符串或猜测参数名。
- `combo` 仍然是 Lov object 结构的输入模式变化。复合输入得到的字符串值必须按已确认的 `textField/valueField/bind` 重建或回填对象/提交字段，不得把 `combo` 当作直接提交 raw string 的理由。

不要编造 `lovCode`、view config 字段、查询 URL、返回对象结构或树 id 字段。

## Attachment
高频 props：
- 上传约束：`accept`、`max`、`multiple`、`directory`、`withCredentials`、`count`
- 存储/协议：`bucketName`、`bucketDirectory`、`storageCode`、`template`、`fileKey`、`fileSize`、`isPublic`
- 展示/行为：`listType`、`viewMode`、`sortable`、`showHistory`、`downloadAll`、`showSize`、`previewTarget`、`buttons`
- 上传时机/删除：`uploadImmediately`、`removeImmediately`、`removeConfirm`、`downloadAllMode`、`enableDeleteAll`
- 分片上传：`useChunk`、`chunkSize`、`chunkThreads`

子组件与实例能力：
- `Attachment.Group`
- `Attachment.Dragger`
- Attachment 实例方法是存在的，但在生成代码前必须确认精确方法名。

当项目版本和既有用法确认这种建模方式时，Attachment 可以通过 attachment field 绑定到 DataSet。字段值通常是附件 UUID 字符串，而不是本地 file-list 对象，但精确值结构和生命周期必须来自项目协议。

不要编造 bucket 名、attachment UUID 生命周期、上传 action、分片预检/合并协议、预览 URL 或下载 URL。

## Modal / Drawer
高频 props：
- 标识/生命周期：`key`、`destroyOnClose`
- 回调：`onOk`、`onCancel`、`onClose`
- drawer：`drawer` 以及已确认的 drawer 相关布局/动画 props

有用事实：
- `destroyOnClose` 默认值为 `true`。
- 当 `destroyOnClose` 为 `false` 时，应指定稳定的 `key`。
- `onOk` / `onCancel` 返回 `false`、resolve `false` 或 reject 都可以阻止关闭。
- `Modal.open()` 在部分 Choerodon UI Pro 版本中会返回带 close/open/update 风格操作的控制器对象；生成代码前必须以目标项目当前源码、类型声明、项目样例或 wrapper 文档确认精确返回值和方法名。不得只凭本参考、其它版本 `.d.ts` 或压缩运行时报错推断可调用 `modal.close()`、`Modal.close(key)` 或私有 close/update API。
- 如果 modal 内容需要 React context，应使用 `ModalProvider` 包裹，并采用 `injectModal` 或 `useModal` 等 provider 模式。

## Configure / ConfigProvider
高频全局配置领域：
- 前缀/图标：`prefixCls`、`proPrefixCls`、`iconfontPrefix`、`icons`
- lookup/select/lov：`lookupUrl`、`lookupAxiosConfig`、`lookupBatchAxiosConfig`、`useLookupBatch`、`lovDefineUrl`、`lovDefineAxiosConfig`、`lovDefineBatchAxiosConfig`、`useLovDefineBatch`、`lovQueryUrl`、`lovQueryAxiosConfig`、`lovQueryBatchAxiosConfig`、`lovTableProps`、`lovModalProps`、`lovAutoSelectSingle`、`lovNoCache`、`lovQueryBar`、`lovQueryBarProps`
- DataSet：`autoCount`、`dataKey`、`totalKey`、`countKey`、`statusKey`、`tlsKey`、`status`、`generatePageQuery`、`feedback`、`transport`、`strictPageSize`、`cacheRecords`、`confirm`
- Form/Field/Table/Modal/Attachment 默认值只有在刻意配置时才会成为项目级行为。

`configure` 用于全局行为，`ConfigProvider` 用于局部作用域行为。`getConfig(key)` 读取的是全局配置，而不是本地 `ConfigProvider` 上下文。

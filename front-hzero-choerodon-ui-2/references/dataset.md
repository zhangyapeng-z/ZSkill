# Choerodon DataSet 参考

## 目录
- 事实边界
- 已确认默认值
- 核心建模
- 查询、提交与 transport
- Record 与字段访问
- 字段属性与选项字段
- 多语、密文、选择缓存和校验
- 需要确认的未定项

## 事实边界
本文件只记录常见 DataSet 工作中可直接影响建模、生成和审查的事实。

如果这里没有覆盖某个事实，不要编造。应视为未确认，并要求提供用户输入、接口契约或项目证据。

## 已确认默认值
- `autoQuery`: 普通查询列表/表格默认 `true`，页面加载后由 DataSet 自动触发首查；存在前置查询条件获取、自定义初始化、路由主键未就绪、F 型布局 List/ListHeader 受控查询、详情/编辑 path-id 加载或其它明确查询时机控制时才设为 `false`，并由页面 `useEffect` / owner action 在条件就绪后主动 `dataSet.query()`。详情页可按主身份参数写成 `Boolean(id)`。
- `autoQueryAfterSubmit`: `true`
- `autoCreate`: `false`
- `selection`: `multiple`
- `pageSize`: `10`
- `paging`: `true`
- `dataToJSON`: `dirty`
- `cacheSelection`: `false`
- `cacheModified`: `false`

不要假设项目层的覆盖配置；应检查 `configure`、本地 DataSet 构造方式或项目包装层。

## 核心建模
- `fields`：业务字段、标签、类型、校验、lookup/lov/options、映射与联动。Table `columns[].name` 默认从主 DataSet `fields` 取字段元数据和列头 label。
- `queryFields`：查询字段属性；它会内部生成 `queryDataSet`，且优先级高于手动传入的 `queryDataSet`。`queryFields` 不替代主 DataSet `fields`，也不为 Table 列提供列头 label。
- `fields` 和 `queryFields` 必须是数组，每个字段写成 `{ name: '<field>', ...props }`。禁止写成 `{ fieldName: { ...props } }` 对象 map；Choerodon DataSet 初始化会对字段集合调用 `forEach`，对象 map 会触发 `forEach is not a function` 并导致页面初始化崩溃。命中 `GCSQ-DATASET-SHAPE-001` / `c7n_dataset_fields_object_shape` 时必须改为数组。
- `fields/queryFields` 字段项只能写 FieldProps / 字段元数据，不得默认混入组件或全局配置宿主的 props。Lov 的 `noCache`、`modalProps`、`tableProps`、`selectionProps`、`combo`、`showDetailWhenReadonly`，Table 的 `queryBar/queryBarProps/buttons/columns`，Form 的 `labelLayout/layout/columns`，Attachment 的 `bucketName/storageCode/uploadImmediately/removeImmediately` 等都不是 DataSet 字段默认项。确有目标版本支持 field-level 配置时，必须有类型声明、官方资料或项目源码证据，并记录 `componentApiProvenance`；`noCache: false` 这类默认冗余值应删除。
- `queryDataSet`：用于复杂查询结构的显式查询 DataSet。
- `queryParameter`：初始查询参数。
- `transport`：自定义 CRUD 请求配置。
- `children`：级联行 DataSet。
- `primaryKey`：常用于级联行查询字段和缓存身份识别。
- `idField + parentField`：扁平树数据。
- `childrenField`：嵌套树数据。
- `cascadeParams`：级联查询参数。

## 生产字段契约与字段使用矩阵
- 生产目标新增页面应建立 `fieldUsageMatrix`，至少覆盖 `field`、`source`、`DataSet fields/queryFields`、`table column`、`form field`、`actionGuard`、`submit payload`、`display only`、`status`。
- 任何 `record.get(name)`、`record.set(name, value)`、`<Column name>`、`<TextField name>`、`<Output name>`、查询字段或 action guard 使用的字段，都应能回溯到 DataSet fields/queryFields、API/DTO 契约或明确的派生字段说明。其中表格展示列 `columns[].name` 应回溯到主 DataSet `fields`；查询控件字段应回溯到 `queryFields/queryDataSet`。同名字段同时用于展示和查询时，需要在两处分别建模。
- 表格列展示 `*Meaning` 时，若按钮、编辑态或流程动作依赖状态，必须同时建模状态 code 字段；不得用 `statusMeaning`、`authorizationStatusMeaning` 等展示字段作为状态机判断依据。
- 列表 DataSet、详情 DataSet 和提交 payload 的同一业务字段命名必须一致；若接口存在字段名映射，应在 transport/adapter 或 Contract Check 中集中说明，不要在页面组件里散落转换。
- 字段只用于展示时应标记 `displayOnly` 或等价说明；不得把 display-only 字段无来源地带入保存 payload。

## 何时优先使用 DataSet
当页面包含结构化业务数据、字段元数据、校验、查询/分页/排序/提交/删除/批量动作、lookup/lov/options、附件、多语字段、联动、树、主从结构、跨页缓存选择或后端协议建模时，应优先使用 DataSet。

本场景常见的 DataSet 枚举/类型事实：
- 高频 DataSet 枚举领域包括字段类型、DataSet 事件/状态、记录状态/缓存类型、排序方向、布尔值、字段 ignore/trim/format、`DataToJSON`、勾选策略和数字舍入。
- 字段、查询和 transport 常量在新增枚举导入前，应先遵循目标项目已有的 import 风格。
- 值集、Lov 和选项字段仍需要确认后端 code 和返回结构；枚举知识不能替代后端协议确认。
- DataSet 配置中出现 `type`、`selection`、`status`、`dataToJSON`、事件名、记录状态、导出模式、字段格式/trim/ignore、`ColumnAlign` 等枚举型配置时，必须建立 `enumProvenance`：优先使用 Evidence enum import map 或项目现有 import 证据；`references/enum-map.md` 只能作为 generatedCandidate / fallback 事实，不能单独标为项目 confirmed；不适用时必须写 not-applicable reason。不能把缺失 enum import 路径时的猜测写成生产代码。

从枚举事实迁入的常见导入与成员：
- `choerodon-ui/dataset/data-set/enum`
  - `FieldType`: `auto`, `boolean`, `number`, `currency`, `string`, `date`, `dateTime`, `week`, `month`, `year`, `time`, `quarter`, `object`, `intl`, `email`, `url`, `color`, `json`, `attachment`, `secret`, `reactNode`, `bigNumber`.
  - `DataSetEvents`: `query`, `beforeLoad`, `load`, `loadFailed`, `submit`, `submitSuccess`, `submitFailed`, `select`, `unSelect`, `batchSelect`, `batchUnSelect`, `selectAllPage`, `unSelectAllPage`, `update`, `fieldChange`, `export`, `create`, `beforeRemove`, `remove`, `beforeDelete`, `reset`, `validate`, `validateSelf`.
  - `RecordStatus`: `delete`, `update`, `add`, `sync`; `RecordCachedType`: `selected`, `delete`, `update`, `add`.
  - `DataSetSelection`: `single`, `multiple`; `DataSetStatus`: `loading`, `submitting`, `ready`; `ExportMode`: `server`, `client`.
  - `DataSetExportStatus`: `exporting`, `success`, `progressing`, `start`, `failed`.
  - `SortOrder`: `asc`, `desc`; `BooleanValue`: `trueValue`, `falseValue`.
  - `FieldIgnore`: `always`, `clean`, `never`; `FieldTrim`: `both`, `left`, `right`, `none`; `FieldFormat`: `uppercase`, `lowercase`, `capitalize`.
  - `DataToJSON`: `dirty`, `selected`, `all`, `normal`, `dirty-field`, `dirty-self`, `selected-self`, `all-self`, `normal-self`, `dirty-field-self`.
  - `CheckedStrategy`: `SHOW_ALL`, `SHOW_PARENT`, `SHOW_CHILD`; `ValidationSelfType`: `minLength`, `maxLength`.
  - `DateMode`: `time`, `dateTime`, `week`, `date`, `month`, `quarter`, `year`, `decade`.
  - `DownloadAllMode`: `readOnly`, `always`; `NumberRoundMode`: `round`, `floor`, `ceil`.
- `choerodon-ui/dataset/enum`
  - `ColumnAlign`: `left`, `center`, `right`.
  - `TimeUnit`: `hour = 'h'`, `minute = 'm'`, `second = 's'`, `a = 'a'`.
  - `LovFieldType`: `INT`, `TEXT`, `DATE`, `DATETIME`, `POPUP`, `SELECT`, `HREF`, `PICTURE`, `IMG`, `PERCENT`.

只有当目标项目已经使用枚举导入，组件/API 事实要求，或代码确实能因避免歧义字符串字面量而受益时，才导入这些枚举。不要仅为了文档式常量而新增枚举导入；但一旦同一 feature 选择了枚举写法，就不得在等价配置上继续混用字符串。若项目既有风格使用字符串且 reference 确认该 prop 支持字符串，可以保持字符串，但必须避免拼写不明、布尔误用或与 enum 混写。

DataSet 类型导入示例：
- `DataSet` 运行时组件/类可按项目风格从 `choerodon-ui/pro` 导入。
- `DataSetProps` 类型必须从 DataSet 类型声明路径导入：`import { DataSetProps } from 'choerodon-ui/pro/lib/data-set/DataSet';`
- 不要写 `import { DataSetProps } from 'choerodon-ui/pro';` 或 `import { DataSetProps } from 'choerodon-ui/dataset/data-set/DataSet';`，也不要把 `DataSetProps` 混入 `choerodon-ui/pro/lib/data-set/enum`、`choerodon-ui/dataset/data-set/enum` 或其它 enum re-export 路径。`FieldType`、`DataSetSelection`、`DataToJSON` 等枚举可以按 enumProvenance 使用项目 enum 路径；`DataSetProps` 不是 enum，必须单独从 `choerodon-ui/pro/lib/data-set/DataSet` 导入。错误来源命中 `HZC-DATASET-PROPS-IMPORT-001`，至少 major；导致 TypeScript 编译失败或用 `as any/as unknown` 规避时 blocking。
- `FieldType`、`DataSetSelection`、`DataToJSON`、`DataSetEvents` 等 DataSet enum 不得从 `choerodon-ui/pro` 聚合入口导入；禁止 `import { DataSet, FieldType } from 'choerodon-ui/pro'`。该写法在部分版本运行时 `FieldType` 为 `undefined`，`type: FieldType.string` 会导致页面初始化时报 `Cannot read properties of undefined (reading 'string')`。默认生成统一使用 `choerodon-ui/pro/lib/data-set/enum`；`choerodon-ui/dataset/enum`、`choerodon-ui/dataset/data-set/enum` 等 re-export 路径即使目标工程已有旧样例也不能覆盖内置规则，只能作为历史兼容/冲突证据。若标准坐标不可用，blocked 并回 Choerodon owner 专项确认。

```ts
import { DataSet } from 'choerodon-ui/pro';
import { DataSetProps } from 'choerodon-ui/pro/lib/data-set/DataSet';
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';

const queryDSConfig = (): DataSetProps => ({
  autoQuery: true,
  fields: [{ name: 'name', type: FieldType.string }],
  transport: {
    read: ({ data, params }) => ({
      url: buildUrl('/v1/{organizationId}/example'),
      method: 'GET',
      params: { ...(data || {}), page: params?.page, size: params?.pagesize },
    }),
  },
});

export const createQueryDS = () => new DataSet(queryDSConfig());
```

该示例是 DataSet transport 的生成基线：`read/create/update/destroy/submit` 返回 DataSet 可消费的 request config。不要把它改成调用业务 service 的 Promise，例如 `read: ({ params }) => queryExample(params)`。

推荐标准配置骨架：

```ts
import { DataSet } from 'choerodon-ui/pro';
import { DataSetProps } from 'choerodon-ui/pro/lib/data-set/DataSet';
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';

const createStatusOptionsDataSet = () =>
  new DataSet({
    data: [
      { value: 'DRAFT', meaning: '草稿' },
      { value: 'SUBMITTED', meaning: '已提交' },
    ],
    selection: false,
    paging: false,
  });

export const createListDSConfig = (): DataSetProps => ({
  autoQuery: true,
  primaryKey: 'documentId',
  queryFields: [
    { name: 'documentNumber', type: FieldType.string, label: intl.get(`${preCode}.model.documentNumber`).d('单据编号') },
    {
      name: 'statusCode',
      type: FieldType.string,
      label: intl.get(`${preCode}.model.statusCode`).d('状态'),
      textField: 'meaning',
      valueField: 'value',
      options: createStatusOptionsDataSet(),
    },
  ],
  fields: [
    { name: 'documentId', type: FieldType.string },
    { name: 'documentNumber', type: FieldType.string, label: intl.get(`${preCode}.model.documentNumber`).d('单据编号') },
    { name: 'statusCode', type: FieldType.string },
    { name: 'statusMeaning', type: FieldType.string, label: intl.get(`${preCode}.model.statusMeaning`).d('状态') },
  ],
  dataKey: 'content',
  totalKey: 'totalElements',
  transport: {
    read: ({ data, params }) => ({
      url: buildApiPath('/v1/{organizationId}/documents'),
      method: 'GET',
      params: {
        ...(data || {}),
        page: params?.page,
        size: params?.pagesize,
        sort: params?.sort,
      },
    }),
  },
});

export const createListDataSet = () => new DataSet(createListDSConfig());

export const createDetailDSConfig = (documentId: string): DataSetProps => ({
  autoQuery: Boolean(documentId),
  paging: false,
  primaryKey: 'documentId',
  fields: [
    { name: 'documentId', type: FieldType.string },
    { name: 'documentNumber', type: FieldType.string, label: intl.get(`${preCode}.model.documentNumber`).d('单据编号') },
    { name: 'statusMeaning', type: FieldType.string, label: intl.get(`${preCode}.model.statusMeaning`).d('状态') },
  ],
  transport: {
    read: () => ({
      url: buildApiPath(`/v1/{organizationId}/documents/${documentId}`),
      method: 'GET',
    }),
  },
});

export const createDetailDataSet = (documentId: string) => new DataSet(createDetailDSConfig(documentId));

export const createLineQueryDSConfig = (): DataSetProps => ({
  autoCreate: true,
  fields: [{ name: 'lineKeyword', type: FieldType.string, label: intl.get(`${preCode}.model.lineKeyword`).d('明细关键字') }],
});

export const createLineDataSet = (documentId: string) =>
  new DataSet({
    queryDataSet: new DataSet(createLineQueryDSConfig()),
    primaryKey: 'lineId',
    fields: [
      { name: 'lineId', type: FieldType.string },
      { name: 'lineNumber', type: FieldType.string, label: intl.get(`${preCode}.model.lineNumber`).d('行号') },
      { name: 'itemName', type: FieldType.string, label: intl.get(`${preCode}.model.itemName`).d('物料') },
    ],
    dataKey: 'content',
    totalKey: 'totalElements',
    transport: {
      read: ({ data, params }) => ({
        url: buildApiPath(`/v1/{organizationId}/documents/${documentId}/lines`),
        method: 'GET',
        params: { ...(data || {}), page: params?.page, size: params?.pagesize },
      }),
    },
  });
```

使用该骨架时，必须把字段、URL、`dataKey/totalKey`、主键和 i18n key 替换为 FDS/TDS/API/MDS 或目标项目证据中的真实值。`fields/queryFields` 保持数组；查询条件进入 `data`，分页排序进入 `params`；详情 path id 由工厂闭包承接，不传给 `read({ id })`；显式查询 DataSet 必须实例化为 `new DataSet(create*QueryDSConfig())`。

DataSet 远程响应 shape 必须与消费端配置一致，不得只套用骨架里的 `dataKey: 'content'` / `totalKey: 'totalElements'`。实现或修复 mock/真实接口前，应先确认当前 DataSet 是否声明 `dataKey/totalKey`、是否使用 `transport.adapter`、项目 request adapter 是否会 unwrap envelope，以及同工程可工作页面的 mock 返回形态。若列表 DataSet 未声明 `dataKey/totalKey` 且相似页面直接消费裸数组，mock 列表应返回裸数组；若详情 DataSet/service 直接消费实体，详情、新建、更新和 LOV 应返回裸实体/裸数组。只有消费端明确读取分页对象或 `{ data: ... }` envelope 时，接口才返回这些结构。请求已发出但页面无数据时，优先对照 `mockResponseConsumerShape` 排查 `{ data: [...] }`、分页对象和裸数组/实体之间的错配。

如果列表首查依赖页面先获取的租户上下文、级联默认值、外部 selected row、权限配置、route search 或其它自定义设置，才将列表 DataSet `autoQuery` 改为 `false`，并在页面条件就绪后集中触发 `listDs.query()`；不得只设 `autoQuery=false` 却没有明确的主动查询入口。

对于静态展示、无需提交/校验/联动的简单本地 UI 状态，以及纯布局或视觉组件，可以不使用 DataSet。

## 查询建模
- 简单查询字段：使用 `queryFields`。
- 复杂查询结构、可复用查询表单、独立查询事件/状态，或多个组件共享条件：使用显式 `queryDataSet`。
- `Table.queryFields` 只覆盖查询条中的查询字段渲染，不是查询模型本身。
- `queryDataSet` 是 DataSet 建模能力，应配置在主 DataSet 上，例如 `new DataSet({ queryDataSet: qds, ... })`；不要把 `queryDataSet` 当作 Table 的业务查询 props 传入，除非目标项目存在明确的组件封装证据。
- `queryDataSet` 的值必须是 `DataSet` 实例，不能是返回 `DataSetProps` 的普通配置对象。推荐写法是把配置工厂和实例工厂分开：`createQueryDSConfig(): DataSetProps` 只返回配置，`createQueryDataSet(): DataSet` 返回 `new DataSet(createQueryDSConfig())`，主列表配置写 `queryDataSet: createQueryDataSet()`。兼容写法是 `queryDataSet: new DataSet(createQueryDS())`；不得写 `queryDataSet: createQueryDS()`、`queryDataSet: queryDSConfig` 或 `queryDataSet: { fields: [...] }`。该误用会在 Choerodon 内部初始化 fields/current record 时触发类似 `Cannot read properties of undefined (reading 'add')` 的运行时错误。
- 查询 DataSet 命名应能区分配置与实例：返回 `DataSetProps` 的工厂推荐命名为 `create*DSConfig()`；返回实例的工厂推荐命名为 `create*DataSet()` 并显式写返回类型 `DataSet`。若项目既有风格已经大量使用 `create*DS()` 表示配置对象，可以不强制重命名，但调用点必须包一层 `new DataSet(...)`；Review 发现新代码命名含混时，应按 `generatedCandidate/major` 要求补类型或命名说明。
- Table 查询条应通过 `dataSet` 上的 `queryFields/queryDataSet` 与 `queryBar` 工作；不要用 Table 层 `onQuery/onReset` 作为 DataSet 查询主链路的兜底实现。若必须自定义 QueryBar，应使用自定义 `queryBar` 组件并通过传入的 `queryDataSet/dataSet` 调用 DataSet 方法。
- `queryDataSet.current`、`queryParameter`、级联参数以及临时 `params` 都可能参与最终查询参数合并。
- 查询执行前默认会校验 query DataSet。

输出查询建模结论时应包含：
- 使用的是 `queryFields` 还是 `queryDataSet`
- `queryDataSet` 是推荐的 `create*DataSet(): DataSet` 实例工厂、兼容的 `new DataSet(create*DS())`，还是误传配置对象
- `Table.queryFields` 是否仅用于覆盖渲染
- 查询触发方式：Table queryBar、DynamicFilterBar、按钮或自定义 Form
- `transport.read` 如何接收/合并参数
- 尚未确认的后端查询协议

## 提交与查询
- `query(page, params, cache)` 用于查询数据。
- `read(page, params, ...)` / `query(page, params, ...)` 的第一个参数是页码，不是业务查询对象；业务参数不得以对象字面量形式传给第一个参数。
- `submit()` 会在远程提交前先校验，校验失败时可能返回 `false`。
- `submit()` 会抛出请求异常；应使用 `try/catch` 或 promise `.catch` 处理。
- `forceSubmit()` 会跳过校验。
- `dataToJSON` 控制提交序列化方式。默认值是 `dirty`；在选择 `normal`、`dirty-field`、self/cascade 模式或自定义序列化前应先确认。

Transport 事实：
- `transport` 项可以是 Axios 配置、URL 字符串或函数。
- 常见 key：`create`、`read`、`update`、`destroy`、`validate`、`submit`、`tls`、`exports`、`adapter`。
- 查询协议放在 `transport.read`。
- 当后端支持统一提交时，create/update/destroy 的统一提交应放在 `transport.submit`。
- 远程唯一性校验通过字段 `unique` 配合 `transport.validate` 实现。
- `dataToJSON` 支持 `dirty`、`dirty-field`、`selected`、`all`、`normal` 以及 `*-self` 变体。
- `dirty` 包含级联变更；`*-self` 变体不包含级联数据。
- `dirty-field` 会保留变更字段，以及主键、唯一字段和标记为 never ignore 的字段。

在建模 transport 前，应确认：
- 后端是拆分 create/update/destroy，还是使用统一 submit
- 提交粒度：dirty/all/selected/self 变体中的哪一种
- 若使用 `unique`，校验 URL 和响应结构是什么
- 子 DataSet 是否需要与父数据一起提交

生产 CRUD / submit 额外约束：
- 列表页必须有可解释的 `transport.read`、项目 request adapter 或上层封装证据；单纯在组件 effect 中调用 service 后 `loadData()` 不能替代列表查询契约。
- DataSet 管理的查询、分页和 CRUD 请求必须收敛在 DataSet `transport`，`transport.read/create/update/destroy/submit` 默认返回 `{ url, method, params/data }` 等 request config；不要在 DataSet 文件中 import 或调用业务 service。即使 service 内部只是封装同一个 `request(buildUrl(...))`，也不得写 `transport.read: ({ params }) => queryRequisitionLines(id, params)` 这类二次委托。
- `transport.read` 回调中的 `data` 与 `params` 语义必须分清：`queryParameter`、`queryDataSet.current`、级联参数、`setQueryParameter` 写入的业务查询条件和详情辅助条件进入 `data`；`params` 只承载 DataSet 查询调用、分页、排序等运行参数。构造 GET query 时通常应合并 `{ ...(data || {}), page/size/sort from params }`；构造详情 path id 时不得从 `params.xxxId` 读取由 `queryParameter` 设置的业务 id。若实现把 `queryParameter.requisitionHeaderId`、`headerId`、`parentId` 等从 `params` 取值，会拼出 `/resource/undefined` 或让筛选条件丢失，按 `GCSQ-DATASET-READ-001` / `GCSQ-ADAPTER-001` 处理。
- DataSet 和 service 允许共享纯 helper，例如 URL builder、query normalizer、payload builder、response adapter；helper 不得发起请求，也不得隐藏业务 action 语义。
- 详情页可用 `loadData()` 装载已经由 service/DataSet transport 查询到的详情结果，但生产目标必须仍有详情 read 契约来源；只有 mock request 已提供详情数据或只读静态数据场景才可把 `loadData()` 作为唯一数据入口。
- 详情/编辑页的 path 主身份参数必须来自 route params，并优先传入 `create*DetailDS(id, auxiliaryQuery)` 这类 DataSet 配置工厂闭包；`transport.read` 直接使用闭包中的 id 拼接详情 URL，`autoQuery` 默认写成 `Boolean(id)`。`navigationToken`、`returnTo`、`source`、详情内子 Tab 等 search 参数只能作为辅助状态进入闭包或 query，不得替代 path id。
- 禁止用 `useEffect(() => detailDs.read({ id, navigationToken }), ...)`、`detailDs.read({ talentCandidateId, navigationToken })`、`detailDs.read({ requisitionHeaderId })` 等形式向详情 read 传业务对象。该对象会被 Choerodon 当作 page 参数处理，`transport.read({ data })` 仍可能拿到空 data，常见后果是 `/resource//detail`、`/resource/undefined/detail` 或 mock 路由无法匹配。
- 若确需手动触发详情刷新，应调用 `detailDs.query()` / `detailDs.read()` 的空参或页码语义，并让当前 id 由 DataSet 工厂闭包、`queryParameter`、`setQueryParameter` 或项目 confirmed wrapper 管理；不得把必填 path id 临时塞进 `read` 第一个参数。
- 单记录详情 DataSet、头详情 DataSet 或不分页的明细读取若直接消费普通对象或数组，必须显式 `paging: false`，或通过 `dataKey/totalKey` / `transformResponse` / response adapter 映射为当前 DataSet 可消费结构。`pageSize: -1` 不等于关闭分页；`paging` 仍为 `true` 时，接口或 mock 必须返回与 `dataKey/totalKey` 对齐的分页 shape。详情接口返回普通对象但 DataSet 仍保留分页模式、或明细接口返回数组却缺 `paging: false` / adapter，导致接口有数据但 Form/Table 不显示时，按 `GCSQ-ADAPTER-001` 处理。
- 可编辑详情、主从页面和 inline table 若存在保存、删除、提交、撤回等动作，必须明确使用 DataSet `create/update/destroy/submit`、`transport.submit`、或 Design 确认的 service action。页面层手工拼 header/lines payload 只能作为已确认 service action 的薄适配，不应成为隐藏协议。
- 主从提交必须说明 header/line 主键、外键、保存粒度、删除语义、`dataToJSON` 策略、是否级联提交、保存后如何刷新 header id / line id / objectVersionNumber / 状态。
- action 函数若会改变状态或删除数据，必须在函数入口二次校验状态与权限适用性；不能只依赖按钮 disabled/hidden。

Mock/demo transport 额外约束：
- 禁止在 `transport.read.url` 中使用 `data:` URL，例如 `data:application/json...`；这类 URL 可能在项目 Ajax/XHR 封装中触发 Invalid URL。
- 可运行 mock 必须使用 HZERO 本地 devServer middleware 暴露的 HTTP mock API；若只能使用内存数组、`src/utils/mock.ts` 或 `service/mock + loadData`，当前实现必须 blocked 并清理，Table query/reset/pagination 不得作为交付验收。
- DataSet 返回结构必须与 `dataKey/totalKey` 对齐。若 response 使用 `{ content, totalElements }`，DataSet 应显式配置 `dataKey: 'content'`、`totalKey: 'totalElements'`；若使用 `{ rows, total }`、`{ list, total }` 或数组，也应明确记录。raw response 已对齐时，可以不写 `transformResponse`。
- 详情 mock 返回普通 header 对象时，详情 DataSet 默认应 `paging: false`；若保留分页模式，则 mock 必须返回 `rows/content + total/totalElements` 等分页结构并配置相应 key。不要用 `pageSize: -1` 代替 `paging: false`，也不要让详情普通对象与分页 DataSet 隐式碰运气。
- `transformResponse` / adapter 是可选的归一化方式；只有 response shape、分页字段、查询过滤、详情组合或 runtime store 初始化需要它时才写。若使用它，不应只处理 JSON string；应兼容已解析 object、array、`content`、`rows`、`list`，并在解析失败时进入同一 mock store fallback，而不是直接清空数据。返回值必须保持为当前 DataSet/request adapter 可消费的对象或数组；除非项目 request adapter 有源码证据要求字符串，否则不得对已解析对象再 `JSON.stringify`，也不得把已对齐的 `content/totalElements` 二次改写成不匹配的 shape。详情明细表无数据时排障顺序必须先证明行 DataSet read 已触发；若没有 Network/DataSet query 证据，先修 `autoQuery` / `lineDs.query()`，不得用扩大 `transformResponse` 兼容范围掩盖未查询问题。
- mock API + runtime store 模式中，`transport.read` 成功路径、service/action request、动作后 query 必须最终从同一 runtime store 当前态生成响应。
- 详细规则见 `references/patterns/dataset-mock-transport.md`。

DataSet-first 复盘护栏：
- 看到 Table 上出现 `queryDataSet/onQuery/onReset` 组合时，应优先判定为实现风险，检查是否应迁回 DataSet `queryDataSet`、`queryFields`、`transport.read` 或自定义 `queryBar`。
- 仅使用 `service/mock + loadData` 不等于 `mock-request`；如果用户要求页面数据走 mock request，必须让 DataSet transport 或项目 request 发出 HZERO devServer mock API 请求。
- `transport.read: () => service.query()`、`transport.submit: () => service.save()` 这类 DataSet 调业务 service 的写法默认判为 legacy/anti-pattern；不要为了确认是否可用额外探索前端工程，相似页面只可作为兼容风险证据。
- 仅让 DataSet 请求静态 JSON 不等于标准 mock request 链路；如果页面存在保存、删除、提交、撤回、取消等运行态动作，后续 query 必须读取 runtime store 当前态，不能每次返回原始 seed。
- 静态代码中配置了 `queryBar` 不代表筛选区运行态可见；必须结合 DataSet 查询字段、queryDataSet 绑定和运行态验证判断。

## Record 与字段访问
- 使用 `record.get(name)` 读取字段值。
- 使用 `record.set(name, value)` 更新字段值。
- 使用 `record.init(name, value)` 初始化干净值。
- `toData()` 用于普通数据，`toJSONData()` 用于提交结构数据。
- 除非有源码证据证明合适，否则避免直接读取或修改 `record.data[fieldName]`。

高价值方法：
- query/load/submit：`ready`、`query`、`queryMore`、`submit`、`submitRecord`、`forceSubmit`、`loadData`、`appendData`、`setQueryParameter`、`getQueryParameter`
- record 变更：`create`、`delete`、`remove`、`deleteAll`、`removeAll`
- selection：`select`、`unSelect`、`selectAll`、`unSelectAll`、`batchSelect`、`batchUnSelect`、`treeSelect`、`treeUnSelect`、`setAllPageSelection`
- 字段/状态/序列化：`validate`、`getValidationErrors`、`getField`、`addField`、`toJSONData`、`toData`、`bind`、`setState`、`getState`、`modifiedCheck`

常见事件：
- 值/查询/加载：`update`、`query`、`beforeLoad`、`load`、`loadFailed`
- 提交：`submit`、`submitSuccess`、`submitFailed`
- 选择：`select`、`unSelect`、`batchSelect`、`batchUnSelect`、`selectAllPage`、`unSelectAllPage`
- record/field：`indexChange`、`fieldChange`、`create`、`remove`、`reset`
- 删除/导出/校验：`beforeRemove`、`beforeDelete`、`export`、`validate`、`validateSelf`

当 API 支持时，返回 `false` 的事件可以阻止操作，例如 `query`、`submit`、`export`、`beforeRemove` 和 `beforeDelete`。

## 字段属性
常见字段属性：
- 基础：`name`、`type`、`label`、`labelWidth`、`defaultValue`、`help`、`highlight`、`order`
- 校验：`required`、`pattern`、`maxLength`、`minLength`、`max`、`min`、`maxExcl`、`minExcl`、`step`、`precision`、`validator`、`defaultValidationMessages`
- 状态/联动：`readOnly`、`disabled`、`multiple`、`range`、`unique`、`bind`、`dynamicProps`、`computedProps`
- 选项/展示：`textField`、`valueField`、`trueValue`、`falseValue`、`options`、`optionsProps`、`group`、`lovCode`、`lovPara`、`lookupCode`、`lookupUrl`
- 请求/转换：`transformRequest`、`transformResponse`

已确认字段类型包括 `boolean`、`number`、`string`、`date`、`dateTime`、`time`、`week`、`month`、`quarter`、`year`、`email`、`url`、`intl`、`object`、`attachment`、`json`、`bigNumber` 和 `secret`。

当组件映射会影响实现时，不要仅凭类型去猜默认编辑器；应通过项目用法确认，或只作为建模建议输出。

## 字段文案与 i18n
- HZERO 页面中的 DataSet `fields`、`queryFields`、行表字段和查询字段，凡是用户可见的 `label`、`help`、校验提示、placeholder/emptyText 等正式业务文案，默认必须使用项目国际化写法，而不是直接写中文或英文字符串。
- 新增页面已有 `preCode` / `promptCode` / `i18nCode` 候选时，字段 label 应生成 ``intl.get(`${preCode}.model.<field>`).d('<中文兜底>')`` 或项目已确认的等价写法。例如 ``{ name: 'requisitionNum', type: FieldType.string, label: intl.get(`${preCode}.model.requisitionNum`).d('申请编号') }``。
- DataSet `label` 必须拿到已经解析后的用户可见文案。禁止新生成 `intlLabel(...)`、`intlPrefix(...)`、局部 `t(...)`、`label: `${preCode}.field.xxx``、`label: '<namespace>.field.xxx'`、`label: { key, defaultValue }` 或类似结构，把 i18n key / 描述对象交给 Choerodon 组件二次解析；组件不会自动把这些 key 翻译，运行时会直接显示 `talent-new.moka-talent-pool.field.positionApplied` 这类编码。
- 只有目标项目 confirmed golden-baseline 明确要求统一 i18n helper，且该 helper 返回的是 `intl.get(...).d(...)` 的解析结果而不是 key/对象时，才可继承；新生成页面默认不得创建这类 helper。
- 若字段契约中给出的是后端字段名 `requisitionNum`，但项目或用户已确认 i18n key 使用业务标准名 `requisitionNumber`，以确认后的 key 为准；不能为了“看起来更规范”擅自改字段名或 key。字段名、展示名和 i18n key 的映射必须进入 Field Usage Matrix / i18nCoverage。
- 空子模块、无参考页面或 `asset-baseline` 场景不能降级成硬编码 label。缺项目样例时仍按 `generated-code-conventions.md` 生成 `generatedCandidate` i18n key；缺服务简码或功能英文名导致 key 无法生成时，只能标记 `i18nCoverage=missing/partial` 和 replacement，不能把硬编码 label 当作生产闭合。
- `type: 'intl'` / `IntlField` 用于编辑多语言业务内容，不等于字段 label 已国际化。字段 label 本身仍必须走页面 i18n key。
- mock/demo 可使用 `.d()` fallback 渲染候选文案，但业务 key 必须进入 platform locale ledger 并标记 pending，或进入 production replacement；不得把 fallback-only 当成 `i18nCoverage=pass`。

## 选项 / 状态字段
- 表单下拉字段（包括启用/禁用这类状态字段）应先在 DataSet `fields` 中建模，再通过 Pro Form 字段组件使用 `name` 绑定渲染。
- 优先使用已确认的项目值来源：项目有值集/lookup 契约时使用 `lookupCode`；只有在固定选项值被明确确认时才使用字段 `options`。
- Design / Contract Check / MDS / 平台资产已确认 `lookupCode` 时，实现必须保留并消费该 `lookupCode`；不得因为 DataSet 示例里存在本地 `options` 骨架、或 mock/demo 更容易运行，就把字段改成静态 options 常量。mock/demo 若需要本地候选支撑运行，只能作为额外 fallback/replacement 记录，不能替代字段上的 confirmed `lookupCode`。
- `Select` / 下拉字段的选项数据必须是 Choerodon 可消费的集合形态：字段 `options` 应为本地 `DataSet`、项目 confirmed 的可消费数组选项或项目 wrapper 已确认的数据源；不得把普通对象、分页响应对象、Promise、接口 raw response 或 JSX 片段作为 `options`。缺值集服务证据的 mock/demo 环境中，不要直接写 `lookupCode` 冒充可运行值集；应优先使用 `new DataSet({ data: [...], selection: false, paging: false })` 承接固定候选，并在字段上显式声明 `textField` / `valueField`，同时记录 `localOptionsReplacement=required`、候选 code、提交值类型和生产替换项。这里的 `selection: false, paging: false` 只约束内层本地 options DataSet，不改变外层 ListDS / QueryDS / DetailDS 的默认查询策略；普通查询列表外层 DataSet 仍优先 `autoQuery: true`。`paging: false` 是本地静态候选的必填项；否则 DataSet 默认分页会按分页响应读取静态数组，可能在组件内部触发 `forEach is not a function`。
- 本地 `DataSet` options 的构造器必须来自顶层静态 `import { DataSet } from 'choerodon-ui/pro'`。不要在字段配置中写 `options: new (require('choerodon-ui/pro').DataSet)(...)`；这种动态 require 不是项目 import 风格证据，会削弱 TypeScript 检查和构建优化，生成代码应统一改为 `options: new DataSet(...)`。
- 普通数组 `options: [{ value, meaning }]` 只有在目标项目 wrapper 或 Choerodon 版本证据确认 Select 会把数组项转换为可 `get()` 的 Record 时才允许；无证据的新生成 DataSet fields/queryFields 默认不得直接传普通数组。若手测或压缩栈出现 `t.get is not a function`，应优先排查 DataSet field/queryField 的 `options` 传了普通数组或数组元素被组件按 Record 读取；修复方向是改为本地 `DataSet` 或项目 confirmed 选项模型，并补 `textField/valueField`。
- 使用 `lookupCode` 时必须确认运行态值集接口可用、返回值为组件可迭代选项集合，且字段 `textField/valueField` 或平台默认映射与提交值一致。若手测或压缩栈出现 `forEach is not a function`，应优先排查 `lookupCode` 返回对象、`options` 非数组/DataSet、本地 `options: new DataSet({ data })` 缺 `paging: false`、`queryFields[].options` 非集合、以及 mock adapter 返回 `{ content, totalElements }` 但未映射为选项集合。
- 不要仅凭常见经验推断“启用”“禁用”等标签对应的提交值。应确认真实持久化值、值类型、默认值以及该字段是否必填。
- 在后端确认接受该字段名和值格式之前，不要把状态字段加入提交载荷。
- 如果同一状态同时参与查询或表格展示，应确认它属于 `queryFields`、主 `fields`、表格列，还是三者都需要。
- 当字段已由 DataSet 表示时，避免再用本地 React `value/onChange` 重复保存下拉状态。
- 字段名为 `*Id` 且语义是人员、员工、申请人、部门、组织、服务站、办事处、分公司、客户、供应商、物料、物料类别等主数据时，默认是 Lov 候选；字段名为 `*Code` 且语义是状态、类型、用途、来源、渠道等业务枚举时，默认是 lookup/value set 候选。缺少 confirmed code 时列入 `generatedCandidate/missing`，不得无说明退化为自由文本。
- 主数据 Lov 候选只允许缺参数，不允许改组件语义。缺 `lovCode/textField/valueField/bind` 时生成 object Lov 候选和 replacement；不得把 `applicantId/deptId/itemCategoryId/itemId` 等字段写成 `lookupCode`，也不得用紧急程度、采购类型、状态等值集编码占位。若后端 TDS 只提供 `@LovValue` / 平台值集术语，Design 先在 `LOV Lookup Binding Contract` 中明确前端 `codeType`，Implementation 不自行转换。
- Lov object 容器字段和后端提交字段必须分离建模：API 暴露 `applicantId/applicantName` 时，DataSet 生成 `applicantObj` 承载 `lovCode/textField/valueField`，再用 `bind: 'applicantObj.id'`、`bind: 'applicantObj.realName'` 回填 `applicantId/applicantName`。不要把 `applicantId` 直接作为 object 容器，也不要只生成 object Lov 而没有同数组内的 `bind` 字段；后者会导致选择 Lov 后业务提交/展示字段不自动回填。
- 已确认或 generatedCandidate 的主数据 `lovCode` 不能被静态 `options DataSet` 替代。`generatedCandidate` 只表示编码、返回字段、参数或运行验证仍待确认；实现仍应生成 object LOV + bind 候选并进入 replacement，而不是把申请人、部门、物料类别、物料等对象选择降级为本地枚举。
- `*Meaning`、`*Name` 一般是展示字段；若需要由 Lov 回填，应确认 `textField/valueField`、映射字段和返回结构。

## 字段组件选择
- `FieldType.date` / `FieldType.dateTime` 编辑态应使用 DatePicker/DateTimePicker 或项目确认的等价 DataSet 绑定组件，不应作为普通 TextField。
- `FieldType.number` / `FieldType.currency` / 比例字段应使用数字/金额输入语义，并确认 precision、min/max、step、舍入和格式化规则。
- `FieldType.email` / `url` 等格式字段应保留字段级校验，不要在页面层用普通 string 覆盖。
- `attachmentUuid`、`fileUuid`、`bucket`、`storageCode` 等附件字段不应以普通 TextField 作为生产编辑入口；应进入 Attachment/Upload 契约，或只读展示并列入 replacement。
- Lov/lookup 字段编辑态应使用 Lov/Select 或项目 wrapper；只有确认业务字段是自由文本时才使用 TextField。

## 多语与密文字段
- 项目需要按语言分别编辑时，多语言文本应使用字段 `type: 'intl'` 和 `IntlField`。
- DataSet 支持 `tlsUrl` 和 `transport.tls`；`transport.tls` 接收 `{ record, name }`。
- 默认多语言数据 key 记录在 `__tls`。
- 敏感字段可使用字段 `type: 'secret'` 和 `SecretField`，但脱敏、空值更新语义、加密方式和后端协议都属于项目契约，必须确认。

## 选择与缓存
- `cacheSelection` 会在分页间保留已选记录，需要 `primaryKey` 或唯一字段。
- `cacheModified` 会在分页间保留已改记录，需要 `primaryKey` 或唯一字段。
- 跨页全选需要同时关注 selected/unSelected/cached records 以及后端支持情况。
- 树选择会受到 `selectionStrategy` 影响。

## 校验
- 字段级校验尽量放在 `fields` 中。
- DataSet 级校验可使用 `validationRules`。
- `validate()` 会校验 DataSet 和记录；`forceValidate` 会影响是否连 sync 记录一起校验。
- 动态 disabled、hidden、readonly 和 required 行为应优先使用 `computedProps` 或 `dynamicProps`。

## 需要确认的未定项
- 接口 URL、HTTP method、请求参数、响应结构、分页字段。
- 字段清单、标签、必填规则、唯一键/主键、提交粒度。
- `lovCode`、`lookupCode`、Attachment UUID/bucket/protocol。
- 对于选项/状态字段：真实字段名、值来源、选项标签、提交值、值类型、默认值、必填规则，以及后端是否接受该字段参与提交。
- 项目级 `configure` 是否覆盖了 DataSet 默认值。
- 对于 intl/secret 字段：语言 key、tls 协议、脱敏规则和更新语义。

# HZERO 国际化、权限与请求模式

## 目录
- 适用范围
- 国际化
- 权限
- 请求
- Service 和 Model
- 输出检查清单
- 临时契约跟进

## 适用范围
用于 HZERO 企业页面中的页面文案、按钮权限、表格列权限、service/model 分层、request 参数、loading 和 notification。

这些模式在未从目标项目确认前都不可直接运行。不要编造 i18n code、permission code、route path、request URL、method 名、DTO 结构或 model namespace。

示例中的尖括号占位只表示缺失事实，不要复制到用户回答、注释或生成文件中。缺少的 i18n、permission、request、model 事实，应转成自然语言待确认项。

## 国际化
- 所有用户可见文案优先使用项目国际化规范。
- 常见写法：

```ts
intl.get('<confirmed.code>').d('<fallback text>');
```

- 项目使用 hzero-front 国际化集合时，类组件或页面导出通常使用 `formatterCollections({ code: ['<confirmed.module>'] })`。
- i18n code 前缀应与相邻页面或已确认模块 code 对齐。
- 若 `generated-code-conventions.md` 已提供足够基础事实（服务简码、功能英文名/页面目录、字段清单、页面范围），新增页面可以生成 `generatedCandidate` i18n namespace/key，并在实现中直接使用该候选编码；不要额外追加 `.mock`、`demo` 或 `TEMP` 前后缀，除非用户明确要求隔离为 mock-only 命名空间。
- code namespace 缺少生成基础事实或与项目既有模块冲突时，列为待确认，不要临时编造。
- 过渡/诊断/演示边界文案（例如“当前为 demo/mock”“未接生产接口”“待替换提示”）不属于生产业务文案，可不绑定 i18n；但必须集中标识为过渡文案，并在生产替换清单中注明生产前删除、隐藏、替换为正式 notification 国际化，或改为开发态/调试态展示。默认不得渲染到业务用户可见 UI，也不要混入正式业务标题、字段 label、按钮、表格列、Alert、Tooltip、Empty/Result、Modal.info 或 notification。
- 页面需要展示演示环境或示例数据边界时，必须由产品/测试确认，并使用正式、用户可理解的 i18n 文案；不得暴露 `mock/demo`、`generatedCandidate`、`待替换`、`未接生产接口`、`request helper 待确认`、`SecurityToken 待确认`、`Figma 未确认` 等内部词。
- 新增模块只登记 `platform-locale-keys.json` 不代表 i18n 闭合；页面实现必须实际消费 locale key，且平台状态必须逐 key 区分 pending/confirmed。检查范围包括 Header title、按钮、查询字段、DataSet label、Table header、Form label、Modal/Drawer 标题、确认文案、notification、校验文案、分组标题、Tab、空态和错误提示。
- DataSet `fields/queryFields` 中的 `label` 若暂时使用 fallback 文案，必须能映射到 generatedCandidate i18n key 或进入替换清单；不得让字段 label 长期停留为散落硬编码。
- 大量硬编码中文与平台 key 清单或 legacy locale 文件并存时，输出 `i18nCoverage=partial/missing`；不得仅因 key 已登记，或 `.d()` fallback 可显示，就声明生产规范闭合。

## 权限
- 按钮、表单域和表格列权限必须与 route、menu、action 语义对齐。
- HZERO/C7N 页面权限按钮固定入口、Provider 入参和旧组件禁用规则由 `front-hzero-permission-button` 负责；本文只说明权限码和 request/model 待确认表达。
- 权限码数组结构、字段名和 Provider 入参字段必须按 `front-hzero-permission-button` 和目标项目源码确认，例如常见按钮权限条目包含：

```ts
const permissionList = [
  {
    code: `${path}.button.<confirmedAction>`,
    type: 'button',
    meaning: '<confirmed meaning>',
  },
];
```

- 按 `front-hzero-permission-button` 记录固定按钮入口、必填 props、权限码字段和 Button props 透传边界。`FormItem`、`Fields`、`TablePermission` 等非按钮权限组件按各自场景确认。
- 开发期新增路由可以按项目约定先配置 `authorized: true` 作为候选访问边界，但不得用它掩盖菜单权限、子模块加载或路由配置问题；交付/Handoff 必须提醒在平台菜单管理和权限资源中维护正式 route/menu/permission。
- 若 `generated-code-conventions.md` 已提供 route path、action 清单和项目权限编码规则，新增页面可以生成 `generatedCandidate` permission code，并在 demo/候选实现中直接使用该候选编码；不要额外追加 `.mock`、`demo` 或 `TEMP` 前后缀，除非用户明确要求 mock-only 权限空间。
- Button Contract 判定为 required 的动作即使缺 confirmed 权限码，也应按 `front-hzero-permission-button` 使用固定 `ButtonPermission` 消费 `generatedCandidate` 权限码；缺码不是改用普通 `Button` 或旧权限组件的理由。生成候选后必须在设计、任务、Handoff 或 production replacement/平台登记清单中保留候选状态。
- 未从菜单/权限契约、相邻页面约定或编码规范确认 action 清单前，不要编造 `create`、`edit`、`delete`、`export` 等权限 action。
- 同一模块必须采用同一权限 namespace 和 action 风格。推荐由最终 route path 点号化后追加 `.button.<action>`，除非目标项目同模块已有更高优先级约定；不得在同一模块混用 `module.feature.create` 与 `module.feature.button.create`。
- 查看、详情、编辑、保存、删除、导入、导出、提交、撤回、作废、复制、创建下游单据、审批/工作流等动作不得互相复用权限 code。`meaning` 必须表达真实页面和动作，例如 `服务请求单-撤回`，不能用“工作流动作”覆盖详情/查看。
- 取消、返回、关闭弹层、清空本地筛选等纯前端动作通常可标记 `permissionRequirement=not-applicable`，并写明 reason；不得为了填充 `permissionList` 而复用 `view/detail` 权限。
- 明细行新增、删除、导入、导出、上传、预览、下载等行级或子表动作也需要进入 Button Contract。required 时按 `front-hzero-permission-button` 使用固定 `ButtonPermission`；缺 confirmed code 但 route/action/编码规则足够时生成 `generatedCandidate`。
- 列表与详情中的同一业务动作应使用同一 action 语义，除非产品/权限平台明确拆分。例如列表编辑和详情保存可以是不同动作，但需要 Button Contract 说明；列表查看和详情取消不应共用同一权限判断。

HZERO 权限组件族可能包括：
- `Button`
- `FormItem`
- `Fields`
- `TablePermission`

手册中的权限编码约定：
- 页面 UI 权限 code 通常是最终 route path 转点号命名空间后追加 `组件类别 + action/含义`。
- 组件类别示例：`button`、`table`、`formItem`、`fields`。
- 示例：route path `/sample/purchase-request` 对应 `sample.purchase-request.button.create`、`sample.purchase-request.button.edit`、`sample.purchase-request.table.orderSeq`、`sample.purchase-request.fields.edit`；不要生成 `/sample/purchase-request/button.create`。
- `meaning` 应表达页面菜单名称和权限含义，例如 `银行定义-保存`。
- API 权限集和页面 UI 权限集是两类不同契约，不要混用。

权限控制行为：
- `check-permissions` 返回权限是否通过以及 `controllerType`。
- 未分配权限时，UI 组件可能隐藏。
- 已分配权限且菜单权限集控制类型为禁用时，UI 组件可能展示但禁用。
- `TablePermission` 控制表格列，默认行为是隐藏。
- 表格中的文字权限按钮可能需要项目样式类，例如 `hzero-permission-text-btn`，用于避免禁用态省略号仍可点击的问题；添加前需确认项目版本和样式。
- 旧权限按钮迁移、`funcType` / `ButtonColor` 等旧 props、`codeList` / `permissionList` 入参错配统一按 `front-hzero-permission-button` 处理。

## 请求
HZERO request 常见写法：

```ts
request(url, options, customOptions);
```

常见 `options` 字段：
- `method`
- `headers`
- `query`
- `body`
- `responseType`

常见 `customOptions` 字段：
- `beforeCatch`

输出具体代码前，先确认项目实际 request 封装。接口协议应集中在 service 或 DataSet transport，不要散落在点击事件里。

手册中的 request 事实：
- 生成具体代码时，`method` 推荐大写。
- `responseType` 常见支持 `text`、`json`、`blob`，默认 `json`。
- `query` 用于 query string 参数。
- `body` 用于请求 payload。
- `customOptions.beforeCatch` 在捕获错误前触发。

## Service 和 Model
- service 文件负责 HTTP URL、method、参数和响应契约。
- 使用 dva/model 的项目中，model 负责 effect 编排、状态更新和 loading 集成。
- namespace、effect 名、reducer 和 loading selector 应跟随相邻页面风格。
- 只有在项目源码确认后，才使用项目特有 helper，常见包括：
  - 项目特有 response adapter
  - `filterNullValueObject`
  - `parseParameters`
  - `parseParameter`
- 标准 HZERO 无冲突路径的 `getResponse` 属于内置响应处理基线；项目明确覆盖、冲突或非 HZERO 工程才回响应处理合同，不得把标准 import path 作为用户待确认项。
- 不要编造 endpoint、分页结构、响应字段或 loading effect 名。

## 输出检查清单
- 已确认的 i18n namespace 和 fallback 文案。
- 已确认的 route path 和 permission path。
- 已确认的 request URL、method、参数、响应结构和错误处理。
- 使用 model 时，已确认 model namespace/effects。
- 所有缺少文档、源码或用户契约支撑的内容都列为待确认项。

## 临时契约跟进
- 用户允许临时 permission code 或 i18n namespace/key 时，应集中管理并标记为非生产契约。
- 最终交付必须包含生产替换清单：临时 permission code 或 i18n key、真实契约确认人/来源、影响按钮/页面/文案、替换文件位置。
- 不要让临时权限或 i18n 值悄悄散落到组件 props 中而没有后续跟进。
- `generatedCandidate` 与 mock-only 不同：前者是按明确编码规范生成、等待平台登记/确认的候选编码，实现中不应自动加 `.mock`；后者只在用户明确要求 mock-only 或缺少生成基础事实时使用，并必须进入替换清单。

# HZERO + Choerodon Production Compliance Gate

用途：防止自动生成的 HZERO + Choerodon 页面“能演示 / 能构建”，但被误判为符合生产规范。本文是跨 Design、Task、Implementation、Review、Verification、Handoff 的一票否决门禁；不替代 mock-request、子模块、DataSet、UI Contract 或生产替换规则，而是把这些规则汇总成可机械检查的生产符合性结论。

执行载体：目标包含生产符合性、production-ready 判定或 Handoff 生产验收时，Design 必须生成或更新 `frontend/design/frontend-compliance-manifest.md`，使用 `front-hzero-enterprise-process-control` 的 frontend compliance manifest 模板。Task、Implementation、Review、Verification 和 Handoff 必须继承同一清单。若当前明确只是 code-generation/mock demo，缺少清单不阻塞 runnable demo，但必须降级并记录 replacement / handoff risk；不得输出 production-ready。

## 目录
- Scope
- Compliance States
- Required Checks
- Stage Output Requirements
- Review / Verification / Handoff Gate

## Scope

命中以下任一场景必须执行本门禁：

- 新建或改造 `packages/<module>` HZEROJS 子模块。
- 新增 HZERO + Choerodon Pro 页面、DataSet、service、route、权限按钮、i18n 或 mock/demo 数据链路。
- 新增或改造 LOV/lookup、附件、导入导出、头行主从、状态动作、表格操作列或生产替换链路。
- 用户要求“是否符合 HZERO / Choerodon UI 规范”“能否生产交付”“为什么没按规范生成”。
- Review / 用户手测发现代码使用 mock/local-filter、本地枚举、普通 Button、缺 locale、缺父工程注册或根依赖/lockfile 变更需要归因。

## Compliance States

所有阶段必须显式区分以下状态，禁止混用：

| state | 含义 | 可进入下一阶段 |
| --- | --- | --- |
| `production-compliant` | 真实 API / request helper、route/menu/permission/i18n/LOV/lookup、子模块注册、验证证据均闭合 | 可进入 Handoff，仍需 Review/Verify 通过 |
| `production-candidate` | 代码结构按生产范式生成，但存在 generatedCandidate 或平台资产待登记 | 可进入 Review/Verify；不得声明 production-ready |
| `mock-demo-compliant` | requestable mock 数据链路、替换清单、权限/i18n 候选和验证边界闭合；Network/DataSet 证明走 mock request | 可进入 demo Review/Verify；不得声明生产符合 |
| `non-compliant` | 缺父工程注册、权限绕过、i18n 缺失、生产请求伪造、普通按钮/本地 options 等非生产能力冒充交付、无来源/未授权全局依赖漂移或关键门禁缺失；不得包含 local-filter、inline mock、模块内存数组或组件内 seed/filter 成功路径 | 阻塞进入 Review/Verify/Handoff，除非用户有条件接受降级交付 |

状态分级不得把“尚未 production replacement”误写成 `non-compliant`。若页面仍为 `queryMode=mock-request`，但 mock request 是可请求 devServer middleware、父工程 mock plugin 源码接线已闭合、required validator 通过、未使用 local-filter / inline mock / 内存 seed 成功路径，且 production replacement checklist 覆盖真实 API、字段形态和平台资产缺口，则最高状态应为 `mock-demo-compliant`，不是 `non-compliant`。若代码已按生产形态使用标准组件/helper，但只缺平台编码、权限资产、locale 资产、LOV/lookup code、附件 bucket/storage/template 或运行态证据，且这些缺口不影响当前 mock demo 路径，应写 `production-candidate` 或 `mock-demo-compliant + replacement`。只有发现当前成功路径本身绕过生产范式、伪造生产请求、缺父工程 required 接线、使用 local-filter/inline mock、无来源全局依赖漂移，或把缺口冒充为 production-ready / usable=true 时，才写 `non-compliant`。

`queryMode=mock-request` 不能与 `productionCompliance.complianceState=production-compliant` 同时出现。`backendApiReadiness.status=closed + runtimeAvailability=verified` 不能把 Mock demo 自动提升为 production-compliant，也不能触发 production replacement slice；它只作为后续独立联调测试的后端证据。CTS 仅完成代码或运行可达性未验证时必须记录 `waiting-backend-integration`。完成独立真实 API 集成和后续稳定化前，Handoff 只能是 `conditional` 或 `blocked`，并用 `productionReplacementTrigger=pending` 表示 advisory 尚未闭合。

## Required Checks

### 1. Query Mode and API Boundary

- 新生成页面的目标 `queryMode` 只能是 `production-transport`、`mock-request`、`partial`、`blocked` 或 `not-applicable` 之一；`local-filter`、inline mock、模块内存数组、组件内 seed/filter、前端本地 service、seed import、无 `transport.read` 的 `loadData` 不得作为 queryMode、降级分支、降级实现或待替换保留项。
- 发现 `local-filter`、模块内存数组、组件内 seed/filter、前端本地 service、seed import、`src/utils/mock.ts`、纯内存 `mock.ts` 或无 `transport.read` 的 `loadData` 成功路径时，当前页面必须判为 `blocked/non-compliant` 并进入 cleanup/rework；即使用户明确要求内存演示，也不得生成或保留这些形态，不得进入 `mock-demo-compliant`、`conditional` 或 `usable=true`。
- `mock-request` 必须有 HZERO 本地 devServer middleware mock API、DataSet `transport.read` / 项目 request adapter / 非 DataSet service-action request 证据，以及生产替换项；DataSet 页面不得用 transport 调业务 service 充当证据。
- `mock-request` 不得读取或使用 `_smock`、`smock`、`sproxy` 或历史 `*.mock.js` 作为字段来源、seed、主接入点或交付方案；标准生成链路只允许记录这些目录/文件存在这一 legacy signal。只有用户明确要求 legacy mock 迁移、审计或解释时才允许只读，并必须标记 `legacyMockEvidenceOnly=true`。新生成 mock/demo 请求必须使用独立 mock namespace：`/_mock/<module>/v1/{organizationId}/...`，其中 organizationId 来自 HZERO 运行时租户上下文。`<unconfirmed-gateway-prefix>/...` 默认视为真实网关/后端服务入口，不得作为 mock/demo 前缀；`/api/v1/demo-org`、裸 `/api/v1`、硬编码 `demo-org`、`/_smock` 或 `/mock` alias 不得声明 `mock-demo-compliant` 或 `usable=true`。
- `mock-request` 的 service/DataSet baseUrl 与 devServer middleware 监听 path 必须同源同路径。若 service 使用 `<unconfirmed-gateway-prefix>/<service>/v1/{organizationId}/...` 但 middleware 监听 `/api/v1/demo-org/...`，或请求被项目 request helper 拼到远端 `API_HOST`，则 `queryMode` 最高为 `blocked/conditional`，不得写 `mock-demo-compliant`。
- Target Placement 是父工程托管子模块的 HZERO 微前端项目，mock handler/plugin 应归属子模块 `packages/<module>/dev-mock/`，同时必须由父工程实际启动配置显式注册，例如父工程 `config/config.ts` 顶层 `plugins` 直接注册子模块 plugin，或注册父工程聚合 plugin 后引用子模块 handler/plugin。`package-start` / 子包独立启动默认适用，必须通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父工程同一 plugin；子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得注册同一 plugin。除非用户或目标工程文档明确禁止 package-start，否则不得写 `not-applicable`。`config/packages-config.js` / `hzeroMicro.packages` 的 package 条目 `plugins` 字段不是 Umi plugin 注册入口。缺父工程顶层 plugin 显式注册，或缺默认 package-start 继承时，不得声明 mock request 可用。
- `production-transport` 必须使用已确认的 HZERO/project request helper、serviceRequestContract、tenantContext、response shape 和错误处理；不得 silent fallback 到 mock/local。
- FSS/API 文档、`external-assets/api-list.json`、`external-assets/apis/*.json` 或 Swagger/OpenAPI 只能证明 `apiContractStatus=documented/partial`；不能单独证明真实接口可达、网关/API_HOST 可用、租户/权限已配置或 response shape 已运行匹配。缺真实前端可调用契约或运行验证计划时，不得把 `queryMode`、compliance state 或 handoff 写成 `production-transport completed / production-compliant / production-ready`。
- `production-transport` 的真实 URL 必须区分 `resourcePath=/v1/{organizationId}/...` 和 `servicePrefix=/<servicePrefix>`；只确认 `/v1/...`、把服务编码推导前缀当 confirmed、误用 `<unconfirmed-gateway-prefix>` 或依赖不存在的 common 包时，不得声明 production-compliant。存在业务包本地 `src/utils/servicePrefix.ts` 时，`src/utils/index.ts` 必须重导出该 helper，DataSet transport、store 和 service 请求入口必须实际消费 `build<Feature>ServiceUrl()` / `get<Feature>ApiPrefix()` 等集中 helper；继续从 `constants.ts` 或 `@/utils` 使用任意只拼 `/v1/{organizationId}` 的 resourcePath 前缀常量属于 servicePrefix bypass，不能声明 mock-demo-compliant 或 production-compliant。mock/demo 双链路默认应走当前 dev server origin + `/_mock/<module>`，裸 `/_mock/<module>` 只作为 middleware mount，不得作为默认 service prefix 交给会拼 `API_HOST` 的 request helper；只有 `<MODULE>_USE_MOCK=false` 精确字符串才能切真实 servicePrefix。
- `HZC-PROD-MOCK-STORE-001`：生产目标或 mock/demo 交付代码中出现页面可直接访问的 `runtimeStore` / 模块级内存数组、`window.location.origin + '/mock-data'`、原生 `fetch` 静态 seed、前端内存分页/保存/删除/提交/撤回/作废、`src/utils/mock.ts` 或纯内存 `mock.ts` 等任一成功路径时，按 blocking；必须清除或改为 devServer middleware 背后的 mock handler/runtime，不能作为降级实现保留。
- `mock-request` 必须通过 HZERO 本地 devServer mock API 访问当前态。有状态动作必须由 mock API 背后的同一个 dev-only runtime store 维护；动作函数直接读写页面内存、详情直接查本地数组、动作后 query 回到旧数据，至少 major；导致保存/删除/状态流转刷新后丢失时 blocking。
- 真实生产 service 文件不得把 mock/demo helper 与生产 request helper 混写在同一成功路径。需要保留 mock 时必须有 `queryMode` 分支、替换清单和 handoff 限制；默认不得自动 fallback 到 mock。

### 1.1 DataSet, Field and Status Contract

- `HZC-DATASET-CRUD-001`：生产目标的列表页 DataSet 必须有可解释的 `transport.read`；详情、主从、可编辑表单若存在保存/删除/提交等动作，必须有 DataSet `read/create/update/destroy/submit` 契约或经 Design 确认的 service action 契约。DataSet 管理的请求默认必须在 `transport` 中返回 request config，不得 import 或调用业务 service；相似页面中的 DataSet 调 service 写法只能标 legacy/anti-pattern。仅 `useEffect + queryDetail + loadData` 或页面层手工组装 payload 不能证明生产数据契约闭合。
- 主从/头行页面必须输出 header/line 的主键、关联键、保存粒度、删除语义、`dataToJSON` 策略和后端是否支持级联提交。缺失时最高 `production-candidate`；实现与契约不一致时 major/blocking。
- 生产符合性结论必须把上述内容落入 Compliance Manifest 的 `DataSet And Field Usage Matrix` 和 `Master Detail Data Contract`。`DataSet And Field Usage Matrix` 必须记录 `canonicalField/runtimeFieldPolicy/adapterAliasPolicy/forbiddenRuntimeAliases`；空子模块、无参考页面或 asset baseline 场景默认 canonical-only，旧字段别名只能在集中 service/request adapter 中出现。若当前流程目标只是生成 mock/demo 或 code-generation 结果，缺少清单不必阻塞代码生成，但必须降级为 `production-candidate / mock-demo-compliant / non-compliant`，不得声明 `production-compliant` 或 `production-ready`。
- `HZC-FIELD-USAGE-001`：任何 `record.get('<field>')`、`record.set('<field>')`、表格列、表单字段、查询字段、actionGuard、renderer 展示字段或提交 payload 使用的字段，都必须在 DataSet fields、queryFields、接口契约或字段使用矩阵中可追溯。`storedField` 与 `renderedField/displayField` 不一致时必须有 `labelSource`；`*Meaning/*Name/displayField` 作为 Output/Table/renderer 展示字段但无 label 来源，至少 major；核心状态/主数据字段无 label 或仍声明 production-ready 时 blocking。状态门禁字段缺失至少 major；导致按钮误显/误禁或提交错误时 blocking。
- `HZC-DATETIME-RENDER-001`：DataSet `FieldType.dateTime/date/time/week/month/year` 字段进入 Table renderer、Output renderer、详情 JSX 或其它自定义展示时，必须证明展示值是 string/ReactNode：组件默认展示、项目 confirmed date renderer、`dateTimeRenderContract`，或显式 `value.format(format)` 等格式化。不得直接返回 `value`、`record.get(dateField)`、moment-like 对象、普通对象或数组对象作为 React child。已出现 React #31、列表/详情崩溃，或仍声明 usable=true / production-ready 时 blocking。
- `GCSQ-CONTRACT-FIDELITY-001`：Implementation / Review 必须从 changed files 反查字段、按钮文案、行操作、状态常量/guard 和用户可见文案，并与 Field Usage Matrix、Status Action Matrix、Action Entry Matrix、Button Semantic Matrix 做 contract diff。页面、DataSet、Table、Form、actionGuard 或 submit payload 使用 `forbiddenRuntimeAliases`，按钮/行操作文案与 `sourceText` 不一致且无 `copyOverrideSource`，状态 code/meaning 与 `statusEnumMap` 漂移，或 required 行操作缺失时，生产符合性不得 pass。
- 状态驱动动作必须有 `code + meaning` 字段契约。`*Meaning` 只用于展示，不得作为状态机判断字段；列表和详情状态码字段命名不一致时必须在 Contract Check 写明映射。
- `HZC-STATUS-MACHINE-001`：提交、撤回、作废、删除、复制、创建下游单据、审批等状态动作在生产符合性结论中必须有状态机矩阵：可见条件、可点击条件、action 函数入口二次校验、mock/API handler 当前态校验、成功目标状态、失败处理和来源。代码生成阶段至少必须生成按钮态、action 入口和 mock/API handler 三处同源状态 guard；完整矩阵缺失只限制 production-ready，不允许生成无条件敏感动作。只在 UI 显隐处判断、不在 action 入口校验，至少 major；误放行敏感动作时 blocking。

### 2. Parent Registration and Submodule Runtime

新建或接入子模块必须识别并检查目标工程实际生效的父工程注册入口。常见候选包括：

- 根 `config/config.ts` 引用的 `config/packages-config.js` / `packages-config.ts`。
- `.hzerorc.js` / `.hzerorc.json` / CI 或脚本读取的 legacy registry。
- workspace / package manager 对 `packages/<module>` 的识别文件。

规则：

- 必须基于工程证据判断哪些注册入口是 active registry；不确定时写 `parentRegistrationStatus=partial/blocked`，不得只注册一个猜测文件后声明完成。
- active registry 中缺任一必要注册，或注册只出现在 SDD 产物而未落到目标工程，生产符合性最高为 `non-compliant`。
- 父工程注册只能新增当前模块项；不得顺手重排、注释、取消注释或修改无关模块。
- `config/packages-config.js` / `packages-config.ts` 这类父工程 package registry 默认只新增最小模块项 `{ name: '<module>' }`。不得为了“更完整”默认追加 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 或其它字段；这些字段只有在 active registry schema、同类 confirmed baseline、平台配置资料或用户确认明确要求时才允许，并必须记录 `extraFieldSource`。`registerRegex` 的默认事实源是子模块 `config/config.ts` 中的 `hzeroMicro.microConfig.registerRegex`，不得重复塞进 packages-config 条目来替代子模块配置。
- `registerRegex` 必须收敛到确认 route prefix，例如 `^\/<module>(?:\/.*)?$`；裸字符串、过宽 catch-all 或与 route path 不匹配时，最高只能 `production-candidate`，导致加载不可判定时 `non-compliant`。

### 3. Permission Coverage

先判断按钮级权限是否适用，再判断组件实现方式。不得仅因为页面使用普通 `Button` 就强行改成权限按钮，也不得从按钮文案静默生成权限码。

- 每个用户可触发业务动作都必须有 Button Contract：动作、位置、权限适用性、权限码来源、enabled/disabled 条件和来源证据。
- 每个用户可触发动作还必须进入动作入口矩阵：`actionId`、`actionExistsSource`、`chosenEntryLocation`、`uiArea`、`pageModes`、`entryStatus`。动作存在于 FDS/TDS/API/status-flow 不等于 Header 可见，入口位置必须单独确认。
- 每个按钮还必须进入按钮语义矩阵：`buttonId`、文案、`uiArea`、`semanticKind`、`navigationTarget`、`businessMutation`、`statusActionRef`。按钮语义不得只按文案合并；页面 Header / 页面级按钮、业务状态动作、Table toolbar `buttons`、行操作列和弹层 footer 必须分区记录。
- 页面工具栏和表格工具栏必须分区落到对应消费组件：`uiArea=page-toolbar` 的按钮默认由页面 `Header` children 消费，不得放入 `Table.buttons`；`uiArea=table-toolbar` 的按钮默认由对应 `Table.buttons` 或项目 confirmed 等价封装消费。把页面工具栏按钮下沉到 `Table.buttons`，把表格工具栏新建/保存/删除/导出上提到 Header，或在 Table 上方自建独立按钮区域替代 `Table.buttons` 且无 UI Contract / 项目证据，按 `HZC-TOOLBAR-SURFACE-001` 至少 major；导致 required 操作不可达、权限位置漂移或误报 production-ready 时 blocking。只看到“明细表”或“页面有 Table”不自动触发表格工具栏，必须有表格工具栏按钮来源。
- 已由 FDS/TDS/UI Contract/Button Semantic Matrix 明确为 `semanticKind=navigation` 的返回、关闭、页面级取消只能执行跳转、关闭或本地 UI 清理，`businessMutation` 必须为 `none`，并填写 `navigationTarget`。不得绑定取消单据、作废、撤回、删除等业务状态 API。
- 取消单据、撤回审批、作废、删除等必须是 `semanticKind=business-state-action`，必须引用 `statusActionRef`，并与同名导航按钮拆成不同 action/buttonId。若上游已明确 Header 取消/返回是导航，实现却改成业务取消单据，或把未确认/不允许 Header 入口的业务状态动作上提复用为页面取消，按 production-ready blocking；若上游只写“取消”且入口或语义未确认，先回 Design/Task 补 Action Entry Matrix / Button Semantic Matrix，不直接归因为实现缺陷。
- `permissionRequirement=required` 只能来自 FDS/TDS/MDS/FSS、菜单/权限资产、目标工程同类页面基线、用户确认或平台规范明确要求；页面级按钮、表格工具栏按钮、行操作按钮、详情 Header 按钮、明细行新增/删除/编辑、导入、导出、上传、预览、提交、撤回、作废、复制等命中 required 时必须通过 `front-hzero-permission-button` 并消费 confirmed/generatedCandidate 权限码。
- required 动作缺 confirmed 权限码时，不得降级为普通 `Button`。若 route path、action 清单和项目权限编码规则足够，Design 必须生成 `generatedCandidate permissionCode`，Task/Implementation 继续按 `front-hzero-permission-button` 使用固定 `ButtonPermission`，并把候选状态写入生产替换/平台登记清单。仅缺权限码、`permissionList` 候选值或平台登记证据时，不得跳过权限组件、隐藏 required 动作或生成权限合同占位；默认权限载荷必须是 `permissionList` 对象数组，不能改成字符串数组或 `codeList`；只有固定组件来源、Provider 契约或动作来源无法判定时才阻塞。
- required 动作只有在 action 清单、route/menu 命名空间或项目权限编码规则不足时才标记 `missing/blocked` 并回到设计/用户确认；不得凭按钮文案编造 `create/edit/delete/export` 等 action，也不得为了绕过缺码而改普通按钮。
- `permissionRequirement=not-applicable` 必须写 reason，例如 FDS/TDS 明确无需按钮级权限、目标工程同位置同动作稳定使用普通按钮、纯前端展示/重置/关闭等非权限业务动作，或本轮为 `deliveryTarget=non-runnable-artifact` 且不进入业务动作交付；此时普通 `Button` 不应被单独判为权限缺陷。
- `permissionRequirement=unknown/missing` 时必须先判断是否能按候选编码规则转成 `generatedCandidate`：route path、action 清单和项目权限编码规则足够时，Design 直接生成候选权限码并使用权限组件；仍缺这些基础事实时才保持 `missing/blocked` 并回到设计/用户确认。涉及提交、删除、导出、上传、审批、敏感信息或平台权限资产已存在时，未知权限仍使用普通 `Button` 至少 major，误报 production-ready 时 blocking。
- 同一 required 业务动作的权限 code 必须命名一致；例如列表编辑和详情保存不得无依据分别使用 `.edit` 与 `.update`。不一致至少 `production-candidate`，导致平台权限资产拆裂时 `non-compliant`。
- 查看、编辑、保存、删除、导入、导出、提交、撤回、作废不得互相复用 required 权限码。
- `HZC-PERM-ACTION-001`：同一模块必须采用同一权限命名空间，优先使用 route path 点号化后追加 `.button.<action>`，例如 `srf.service-request.button.submit`。同一模块混用 `module.feature.create` 与 `module.feature.button.create`，或详情/取消/审批等动作复用无关权限码，至少 major；导致平台权限资产无法登记或错误控制时 blocking。
- 取消、返回、关闭本地弹层等纯前端导航动作可以是 `permissionRequirement=not-applicable`，但必须写 reason；不得为了“有 permissionList”而复用 `view`、`detail` 或其他业务权限。
- 明细行新增、删除、导入、导出、上传、预览、下载也是 Button Contract 范围。required 时必须通过 `front-hzero-permission-button`，并独立于头按钮权限判断。

### 4. I18n Asset Coverage

- 新增 HZERO 页面必须先按规则消费 `intl.get(fullKey).d(defaultValue)` 或 confirmed 等价 i18n 入口；平台 prompt/locale 是否已维护只影响资产覆盖和 production-ready，不得反向导致代码硬编码文案。
- 使用 `intl.get().d()` 或 `formatterCollections` 的新增 HZERO 模块默认把业务 key 登记到 `platform-locale-keys.json` / Compliance Manifest，由 HZERO `/hpfm/prompt` 维护线上译文；不得为了满足静态校验生成目标工程未加载的本地 locale 文件。不得生成或维护目标工程本地 locale 资产。
- 平台多语言清单必须覆盖页面标题、按钮、查询字段、表格列、表单字段、确认文案、通知文案、校验文案、Tab/Modal/Drawer 标题和空态，并逐 key 记录 `defaultMessage`、`platformStatus=pending/confirmed`、平台来源和确认依据。
- Implementation / Review / Verify 必须做 i18n key 对账：从本轮新增或修改的 TS/TSX/DataSet/service 相关文件收集业务 `intl.get('<key>').d(...)`、同文件静态 const 或可追溯 imported static const 的 ``intl.get(`${preCode}.xxx`).d(...)`` key 和 `formatterCollections({ code })` namespace；再与 `platform-locale-keys.json` / Compliance Manifest、项目已确认公共 namespace或平台多语言资产 比对。未登记业务 key 必须补为 pending；已有 `/hpfm/prompt`、平台导出或用户确认的逐 key 证据时才可标记 confirmed。
- `hzero.common.*`、项目确认的公共 locale namespace 和已确认完全由平台菜单/提示维护的 key 可作为外部资产，但必须记录来源；不能把未知公共 key 当作已覆盖。
- 仅依赖 `.d()` fallback、平台 key 仍为 pending、`formatterCollections({ code })` 指向未确认 namespace，或 key 对账后仍存在未登记业务 key 时，代码消费形态可以合规，但生产 i18n 覆盖不能闭合；若目标是 mock/demo，可继续交付，但必须进入 replacement/handoff risk；若目标是 production-ready，则阻塞到平台 key 全部 confirmed 或存在 confirmed 公共 locale 来源。
- generatedCandidate i18n key 可进入 demo/候选实现，但必须进入生产替换/登记清单；不得声明 i18n 契约已闭合。
- `HZC-I18N-COVERAGE-001`：平台 key 清单存在但页面仍大量硬编码用户可见文案，或使用 `intl.get().d()` 但 key 未登记、仍为 pending 且被声明为生产闭合，按 `i18nCoverage=partial/missing`。DataSet label、Table header、Header title、按钮、Modal.confirm、notification、分组标题、Tab/Drawer/空态、记录表字段 label 均在检查范围内；误报生产 i18n 闭合时 blocking。

### 5. Value Set / LOV / Local Options

- 真实 `lookupCode` / `lovCode` 必须来自 FDS/TDS/MDS/FSS、平台资产、相似页面 confirmed 证据或 generatedCandidate 编码规则。
- 前端本地 options DataSet 只能用于 mock/demo 或明确 not-applicable 的纯前端枚举；生产页面必须有替换项或真实值集/LOV 契约。
- 本地 options 被用作查询条件、状态、性别、学历、渠道等业务枚举且未进入替换清单时，最高 `non-compliant`。
- 已确认 `lookupCode/lovCode` 的字段不得被本地 options 覆盖或替换；PRM 这类 `authorizationStatus/purchaseType/urgency` 已有平台值集时，静态 options 是实现偏离，`applicantId/deptId/itemCategoryId/itemId` 等主数据字段即使只有 generatedCandidate，也必须保留 LOV 候选和 replacement，不能静默按普通本地枚举交付。
- `HZC-LOV-LOOKUP-001`：字段名为 `*Id` 且 label/语义指向申请人、员工、部门、组织、服务站、办事处、分公司、客户、供应商、物料、物料类别等主数据时，默认是 LOV 候选；不得静默实现为普通 string/TextField 并声明 production-compliant。字段名为 `*Code` 且语义为状态、类型、用途、来源、渠道等业务枚举时，默认是 lookup/value set 候选。
- 缺 confirmed `lovCode/lookupCode` 时，应生成 `generatedCandidate` 或列入待确认/替换清单；只有字段被确认是自由文本输入时才可作为普通 string。
- `lovCode` 只确认编码，不确认绑定。新生成 LOV 字段必须以独立且显式的 `FieldType.object` 容器承载 `lovCode/textField/valueField`，并通过 `bind` 回填提交字段和展示字段；`*Id: FieldType.string + lovCode + textField/valueField` 会按 Select primitive 值模式运行，是反例，不得声明为 LOV 契约闭合或 production-compliant；省略 `type` 依赖 `auto` 推断也不是合格生成形态。每个 LOV 字段还必须在 Compliance Manifest 的 `LOV Lookup Binding Contract` 写明 `valueField`、`textField`、`bind`、展示字段、提交字段、`lovPara` 参数名、来源字段、来源时机、空值行为、级联清理策略和确认来源；缺失时不能声明 LOV 契约闭合。父子级联、组织/租户/公司/岗位范围、查询区与表格编辑区参数来源不同、同一 `lovCode` 多处过滤条件不同等场景，必须触发 `lovParaContract` 审查；缺 confirmed 参数契约时只允许候选实现并进入 replacement / handoff risk。
- 同一 `fields` 或 `queryFields` 区域内还必须保持 DataSet binding graph 完整性：字段 `name` 不重复，object LOV 容器名不复用为业务/查询 leaf 名，所有 literal `bind` 仅形成 `container -> leaf` 单向边，且不存在直接或间接环。`GCSQ-LOOKUP-005` 失败时不得声明 LOV 契约闭合、mock-demo-compliant、usable 或 production-compliant；必须先重构容器/叶子命名和 bind 方向，再重新运行 C7N validator。
- mock/demo 可以用 generatedCandidate `lovCode/lookupCode`、local mock options 或 mock-only meaning 字段支撑演示，但必须在 replacement 中标记；不得把主数据/枚举字段改成普通文本后声明 `mock-demo-compliant`。详情只读使用 `Form + Output` 时，必须展示 `displayField/*Name/*Meaning` 或明确 display contract 缺失，不能用 raw `*Id/*Code` 冒充业务展示。
- 编辑态组件必须与字段语义匹配：日期/日期时间不得用普通 TextField 替代 DatePicker/DateTimePicker；金额/数量/比例不得用普通 TextField 替代 Number/Currency 语义；附件 UUID 不得用普通 TextField 冒充附件能力。`HZC-COMPONENT-TYPE-001` 命中至少 major，导致能力不可用时 blocking。

### 6. Global Dependency and Lockfile Attribution

生成页面或子模块时，禁止无任务来源修改根 `package.json`、lockfile、全局依赖版本、resolutions 或无关包版本。根依赖/lockfile 变更必须先做来源归因，不得把用户手动的组件库基线调整归因到模块生成质量。

- `none`：根依赖/lockfile/resolutions 无变更。
- `approved`：Design/Task/File Mapping 显式列入，或用户明确要求/确认依赖升级；必须记录确认来源、影响范围和验证范围。
- `user-owned`：变更已由用户手动产生，或用户说明这是独立组件库/工程基线调整；不归因到本轮模块生成，但 Handoff 仍需记录来源和全站影响风险。
- `unapproved`：本轮生成或自动安装副作用引入，且没有设计/任务/用户确认来源；Review 至少 major，影响全站构建或引入无关包版本变化时 blocking。
- `unknown`：无法判断来源或未检查；不得进入 `production-ready`，必须补证据或回到人工确认。
- `not-applicable`：目标不涉及可运行前端工程或无根依赖文件可检查，并有 reason。

lockfile 只允许反映已确认依赖变更；不得作为自动安装副作用混入业务生成提交。若根依赖变更是用户手动基线调整，Review 只记录 `dependencyDrift=user-owned/approved` 和风险范围，不作为当前业务模块本身的生产规范缺陷。

### 7. Production Replacement and Handoff Limit

- 任何 mock/demo、generatedCandidate permission/i18n/lookup/lov、本地 options 或未验证 route，都必须进入 production replacement checklist；local-filter、inline mock、模块内存数组、组件内 seed/filter 或 `service/mock + loadData` 不进入可保留 replacement 项，只能进入 blocking cleanup/rework。导入/导出只接受 HZERO 标准组件或项目 confirmed wrapper 代码形态，参数缺口必须以 mock/generatedCandidate 候选值先支撑标准组件实现，并在 Contract Check / Verification / Handoff 标明来源未确认；权限按钮、附件、LOV/lookup、renderer/helper 等标准能力也遵循同一口径，缺参数生成候选值继续接标准组件/helper。已由 owner reference 固化的标准组件/helper 坐标按 builtin-standard 继承，缺相似页面、缺本地样例或缺项目 wrapper 不得阻塞；只有依赖/版本/编译证据明确否定标准组件/helper 可用且没有 confirmed wrapper，或字段/value/bind 结构无法形成候选时，才进入一级 gate 阻塞；禁用导入导出、普通按钮替代 required 权限、非标准入口、占位附件、隐藏入口或 no-op 关键动作不得作为可接受实现。
- replacement checklist 缺少 `API/transport`、`route/menu`、`permission`、`i18n`、`lookup/lov/local-options`、`mock-store-query-mode`、`validation-guard`、`status-machine`、`import-export-contract`、`field-usage-matrix` 任一适用类别时，不得写 `production-compliant`。
- `HZC-IMPORT-EXPORT-001`：头导入、行导入、头导出、行导出必须作为独立契约检查 template/import code、endpoint、权限、父 ID、查询/选中行参数、tenantContext 和刷新目标。行导入/导出默认不得复用头模板或头权限；父记录未保存且缺临时行导入/导出契约时，行入口必须 hidden/disabled + reason。
- 未运行页面运行态验证时，`usable=unknown`；未运行 build/compile 时，`buildable=unknown`；未运行真实 API Network 时，`production-transport` 不得标 completed。

## Stage Requirements

### Design

Design / Contract Check 必须输出：

```text
complianceManifestPath: # Design / Task 阶段字段；最终 stage-result 写入 artifacts.complianceManifest
hzeroChoerodonComplianceTarget: production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable
queryMode:
parentRegistrationCandidates:
parentRegistrationStatus:
serviceRequestContractStatus:
runtimeDataEntryStatus:
permissionCoveragePlan:
buttonPermissionRequirement:
actionEntryMatrixStatus:
actionEntryMatrix:
  - actionId:
    label:
    actionExistsSource:
    statusActionRef:
    allowedEntryLocations:
    chosenEntryLocation:
    uiArea:
    pageModes:
    entryStatus:
    implementationPolicy:
buttonSemanticMatrixStatus:
buttonSemanticMatrix:
  - buttonId:
    label:
    sourceText:
    copyPolicy:
    copyOverrideSource:
    uiArea:
    semanticKind:
    navigationTarget:
    businessMutation:
    statusActionRef:
    designStatus:
i18nCoveragePlan:
listQueryContractStatus:
fieldUsageMatrixStatus:
fieldUsageRuntimePolicy:
masterDetailDataContractStatus:
statusActionMatrixStatus:
statusEnumMapStatus:
lovLookupCoveragePlan:
componentApiProvenancePlan:
modalLifecycleContractPlan:
componentTypeCoveragePlan:
hzeroCommonComponentContractStatus:
attachmentContractStatus:
importExportContractStatus:
rowActionContractStatus:
routeRedirectGateStatus:
generatedCodeStaticGatePlan:
contractFidelityCheckPlan:
globalDependencyChangePolicy: forbidden-unless-mapped
productionReplacementRequired:
```

若目标是生产实现但上述任一项缺失，只能 `blocked-by-contract / needs-user`，不得进入 production-ready implementation。若目标是 mock/demo 或 code-generation，缺失项应进入 Compliance Manifest、production replacement draft 或 handoff risk；缺少这些资产不阻塞可演示代码生成，但不得隐式升级为生产闭合。

### Task Breakdown

每个 implementation task 必须继承：

```text
complianceManifestPath: # 继承 Design 的同名字段；最终 stage-result 写入 artifacts.complianceManifest
productionComplianceTarget:
queryMode:
parentRegistrationStatus:
serviceRequestContract:
runtimeDataEntryContract:
permissionCoverage:
i18nCoverage:
listQueryContract:
fieldUsageMatrix:
masterDetailDataContract:
statusActionMatrix:
actionEntryMatrix:
buttonSemanticMatrix:
lovLookupCoverage:
componentApiProvenance:
modalLifecycleContract:
componentTypeCoverage:
hzeroCommonComponentContract:
attachmentContract:
importExportContract:
rowActionContract:
routeRedirectGate:
generatedCodeStaticGate:
contractFidelityCheck:
globalDependencyPolicy:
handoffLimit:
```

生产符合性任务验收必须拒收：缺 Compliance Manifest、缺 active registry 注册、动作入口矩阵缺失、按钮语义矩阵缺失、未确认业务状态动作进入 Header、上游已确认导航取消却实现为业务取消单据、required 权限按钮未通过 `front-hzero-permission-button`、FDS/TDS/UI Contract 要求搜索框/关键字/模糊查询但 `listQueryContract` 未 pass、实现显式 `queryBarProps.fuzzyQuery=false` 或把字段映射误写成 `queryBarProps.fuzzyQueryField/fuzzyQueryFields`、详情明细表/子表存在筛选条件却无来源地用外置 Form 替代 Table filterBar 查询形态、local-filter、inline mock、本地内存 seed/filter、`src/utils/mock.ts` 或 `service/mock + loadData` 成功路径、字段使用矩阵缺 actionGuard/submit/renderer 字段来源、`*Meaning/*Name/displayField` 展示字段缺 labelSource、状态动作缺状态机矩阵、主数据/枚举字段退化为普通 string 且无自由文本来源、LOV/lookup 组件被退化为普通 TextField、HZERO 通用组件版本/import 缺失或误归类、附件未通过 `front-hzero-attachment`、头/行导入导出契约混用、头部/页面级导入导出按钮继承行操作 `type='text'` 或样式不一致且无 confirmed 来源、表格多动作操作列未按项目策略处理、操作列 helper payload / 行按钮 type 漂移、无来源/未授权 lockfile 漂移。若任务目标只是 code-generation/mock demo，local-filter / inline mock 类缺口仍必须阻断并清理；其它非阻断缺口进入 generatedCandidate、replacement 或 handoff risk，不得给出 production-ready。

LOV/lookup 缺 `lovCode/lookupCode`、`bind/textField/valueField`、`lovPara` 参数名/来源字段/空值行为/级联清理策略，附件缺 bucket/storageCode/template，导入导出缺 templateCode/endpoint 参数，权限缺候选 code，i18n 平台 key 仍为 pending，或 HZERO 通用组件缺业务参数时，不得单独阻塞流程；必须先保持标准组件/helper 形态并生成 `generatedCandidate/mockOnly/placeholderParameter`，进入 replacement / handoff risk。缺相似页面、缺项目 wrapper 或缺本地组件样例也不得阻塞。只有目标工程依赖/版本/编译证据明确否定标准组件可导入或可实例化且没有 confirmed wrapper、字段或值结构无法形成候选、或实现会变成普通控件、disabled/no-op、local-filter、inline mock 成功路径时，才回到一级 gate 阻塞。

### Implementation

实现完成前必须执行本门禁自查。命中 `non-compliant` 时：

- 结果不得写 `production runnable` 或 `符合 HZERO/Choerodon 规范`。
- 必须写 `design-deviation-report` 或 `unverified/non-compliant items`。
- 若问题在当前任务范围可修复，应直接修复；若缺契约或越界，返回 Design/Task/用户确认。
- 只有目标包含生产符合性或 production-ready 判定时，才必须输出 `productionComplianceAudit` 并逐项引用 Compliance Manifest gate；没有 manifest 或未逐项消费时，Implementation 结果只能是 `partial / blocked-by-contract`。若目标只是 code-generation/mock demo，可输出 `productionComplianceAudit=not-applicable + reason`，并把缺口写入 replacement / handoff risk。

### Review

Review 必须把本门禁作为 findings-first 必查项。严重级别建议：

| 问题 | 默认严重级别 |
| --- | --- |
| 缺 active 父工程注册导致模块不可达 | blocking |
| mock/local-filter、inline mock、本地内存 seed/filter、`src/utils/mock.ts`、`/_local + transformResponse/loadData 调 service` 或 `service/mock + loadData` 出现在成功路径，或被声明为 production-compliant/mock-demo-compliant/usable=true | blocking |
| `_smock/smock/sproxy` 被作为 mock-request 主接入点，或 mock path 未按 `/_mock` 隔离命名空间与本地 devServer 通道确认后仍声明 mock-demo-compliant/usable=true | major / blocking |
| mock/demo 使用 `<unconfirmed-gateway-prefix>`、`/api/v1/demo-org`、硬编码 `demo-org` 或 service/middleware path 分裂，仍声明 mock-demo-compliant/usable=true | major / blocking |
| 父工程托管子模块只在子模块 package 配置注册 mock plugin，父工程 `config/config.ts` 顶层 `plugins` 未显式挂载子模块 plugin 或聚合 plugin；或把 mock plugin 写入子模块 `config/config.ts` 顶层 `plugins`、`config/config.dev.ts`、`packages-config` package 条目 `plugins` 字段；或 plugin 直接 `api.addBeforeMiddlewares(registerMock)` / 直接传 middleware 导致 Umi 插件启动失败 | major / blocking |
| Button Contract 缺权限适用性判定，或 required 权限按钮未通过 `front-hzero-permission-button` | major / blocking |
| Action Entry Matrix / Button Semantic Matrix 缺失；未确认业务状态动作进入 Header；或上游已明确页面导航取消/返回，实际实现却调用取消单据/作废/撤回/删除 | production-ready blocking；入口或语义未确认时回 Design/Task 补矩阵 |
| Contract fidelity diff 未执行，或发现 canonical 字段被页面层改名、旧字段别名进入 DataSet/Table/Form/guard/payload、按钮/行操作文案近义改写无来源、状态 code/meaning 漂移、required 行操作缺失 | major / blocking；导致 guard/payload/验收文案错误或仍声明 production-ready 时 blocking |
| DataSet 日期/时间字段、moment-like 对象或普通对象直接作为 Table renderer / Output renderer / JSX child 渲染 | major / blocking；已出现 React #31、页面崩溃或仍声明 usable=true/production-ready 时 blocking |
| required 明细行操作未通过 `front-hzero-permission-button` | major；涉及删除/审批时 blocking |
| locale namespace 缺失或大量 fallback-only | major |
| 权限 action 命名不一致导致资产拆裂 | major |
| 无来源/未授权根依赖/lockfile 漂移 | major / blocking |
| 本地 options / lookup / lov 未进入替换清单 | major |
| LOV 缺 `bind/textField/valueField/lovPara` 参数闭环但声明契约闭合 | major / blocking |
| 主从页缺 Master Detail Data Contract 仍手工 `loadData + payload` 声明生产闭合 | major / blocking |
| 附件未通过 `front-hzero-attachment`，或 bucket/storage/template 为 generatedCandidate 却声明附件能力完成 | major / blocking |
| Required 导入导出只接入口组件，缺模板/endpoint/参数/刷新目标契约，或头部/页面级导入导出按钮继承行操作 `type='text'` / 风格不一致且无 confirmed 来源 | major / blocking |
| Choerodon Pro Table 多动作操作列无 `front-hzero-renderer` 内置 `c7nOperatorRender` / `operatorRender` 或已记录 `project-override` helper | major |
| 已使用 `c7nOperatorRender` / `operatorRender`，但 operators 未过滤、item shape 不符合 `{ key, ele, len, title }`、缺 `title` 或 `title` 与按钮文案不同源、行按钮不是 `type="text"`、`limit` 内可见按钮被截断，或继承 Header/Toolbar 样式且无 project-override | major |

Review 结论不得因“只是 demo/mock”放行生产符合性；只能有条件进入 demo 验证或 Handoff，并写清降级状态。

### Verification

Verification 必须输出 `productionComplianceVerification` 和 `complianceManifestVerification`：

```text
queryMode verified / not-run:
active parent registries checked:
permission smoke checked:
i18n asset checked:
field usage matrix checked:
detail region coverage checked:
list query contract checked:
status action matrix checked:
action entry matrix checked:
lov/lookup and component type checked:
modal lifecycle checked:
import/export contract checked:
dependency drift checked:
runtime/manual route checked:
network evidence:
result: production-compliant / production-candidate / mock-demo-compliant / non-compliant
complianceManifestVerification:
  manifestPath:
  serviceRequestContract:
  runtimeDataEntryContract:
  listQueryContract:
  fieldUsageMatrix:
  detailRegionCoverage:
  masterDetailDataContract:
  statusActionMatrix:
  actionEntryMatrix:
  buttonSemanticMatrix:
  buttonPermissionContract:
  i18nCoverage:
  lovLookupBindingContract:
  componentApiProvenance:
  modalLifecycleContract:
  componentTypeContract:
  hzeroCommonComponentContract:
  attachmentContract:
  importExportContract:
  rowActionContract:
  routeRedirectGate:
  generatedCodeStaticGate:
  missingOrBlockedGates:
```

仅命令通过不能证明生产符合；缺页面运行态、Network、route registry 或权限/i18n 证据时，最高 `production-candidate` 或 `mock-demo-compliant`。

### Handoff

Handoff 必须汇总 `productionCompliance`，逐项 gate 嵌入 `productionCompliance.manifest`：

```text
productionCompliance:
  complianceState:
  manifest:
    serviceRequestContract: pass / partial / missing / blocked / not-applicable
    runtimeDataEntryContract: pass / partial / missing / conflict / blocked / not-applicable
    listQueryContract: pass / partial / missing / conflict / blocked / not-applicable
    fieldUsageMatrix: pass / partial / missing / blocked / not-applicable
    detailRegionCoverage: pass / partial / missing / blocked / not-applicable
    masterDetailDataContract: pass / partial / missing / blocked / not-applicable
    statusActionMatrix: pass / partial / missing / blocked / not-applicable
    actionEntryMatrix: pass / partial / missing / blocked / not-applicable
    buttonSemanticMatrix: pass / partial / missing / blocked / not-applicable
    buttonPermissionContract: pass / partial / missing / blocked / not-applicable
    i18nCoverage: pass / partial / missing / blocked / not-applicable
    lovLookupBindingContract: pass / partial / missing / blocked / not-applicable
    componentApiProvenance: pass / partial / missing / blocked / not-applicable
    modalLifecycleContract: pass / partial / missing / blocked / not-applicable
    componentTypeContract: pass / partial / missing / blocked / not-applicable
    hzeroCommonComponentContract: pass / partial / missing / blocked / not-applicable
    attachmentContract: pass / partial / missing / blocked / not-applicable
    importExportContract: pass / partial / missing / blocked / not-applicable
    rowActionContract: pass / partial / missing / blocked / not-applicable
    routeRedirectGate: pass / failed / blocked / not-applicable
    generatedCodeStaticGate: pass / partial / missing / failed / blocked / not-applicable
    missingOrBlockedGates:
  activeParentRegistries: pass / partial / missing / blocked / not-applicable
  permissionCoverage: pass / partial / missing / blocked / not-applicable
  i18nCoverage: pass / partial / missing / blocked / not-applicable
  listQueryContract: pass / partial / missing / conflict / blocked / not-applicable
  fieldUsageMatrix: pass / partial / missing / blocked / not-applicable
  detailRegionCoverage: pass / partial / missing / blocked / not-applicable
  statusActionMatrix: pass / partial / missing / blocked / not-applicable
  actionEntryMatrix: pass / partial / missing / blocked / not-applicable
  buttonSemanticMatrix: pass / partial / missing / blocked / not-applicable
  lovLookupCoverage: pass / partial / missing / blocked / not-applicable
  componentApiProvenance: pass / partial / missing / blocked / not-applicable
  modalLifecycleContract: pass / partial / missing / blocked / not-applicable
  componentTypeCoverage: pass / partial / missing / blocked / not-applicable
  hzeroCommonComponentContract: pass / partial / missing / blocked / not-applicable
  attachmentContract: pass / partial / missing / blocked / not-applicable
  importExportContract: pass / partial / missing / blocked / not-applicable
  dependencyDrift: none / approved / user-owned / unapproved / unknown / not-applicable
  failedChecks:
  handoffLimit:
mock:
  queryMode:
artifacts:
  complianceManifest:
```

若目标是 `production-ready`，必须同时满足：`productionCompliance.complianceState=production-compliant`、`failedChecks=[]`、`dependencyDrift=none/approved/user-owned/not-applicable`、`activeParentRegistries=pass/not-applicable`、`permissionCoverage=pass/not-applicable`、`i18nCoverage=pass/not-applicable`、`listQueryContract=pass/not-applicable`、`fieldUsageMatrix=pass/not-applicable`、`detailRegionCoverage=pass/not-applicable`、`statusActionMatrix=pass/not-applicable`、`lovLookupCoverage=pass/not-applicable`、`componentApiProvenance=pass/not-applicable`、`modalLifecycleContract=pass/not-applicable`、`componentTypeCoverage=pass/not-applicable`、`hzeroCommonComponentContract=pass/not-applicable`、`attachmentContract=pass/not-applicable`、`importExportContract=pass/not-applicable`，且 `runtimeDataEntryContract=confirmed/pass/not-applicable`，且 `artifacts.complianceManifest` 存在或明确 not-applicable，`productionCompliance.manifest` 中全部生产适用 gate 为 `pass/not-applicable`、`missingOrBlockedGates=[]`，其中适用详情/编辑/主从页 required 区域时 `detailRegionCoverage=pass`，适用页面按钮或业务动作时 `actionEntryMatrix=pass` 且 `buttonSemanticMatrix=pass`，适用新生成 HZEROJS 子模块 route config 时 `routeRedirectGate=pass/not-applicable`；FDS/TDS/Figma/用户确认要求搜索框、关键字或模糊查询时，`listQueryContract` 不得为 `not-applicable`；新增/改造详情、编辑、主从页且存在 required 或生产验收区域时，`detailRegionCoverage` 不得为 `not-applicable`。usable=true 只要求当前演示路径和 required gate 闭合；production-only、optional 或非本轮范围缺口可以 partial/missing，但必须写入 replacement/blocker 且不能声明 production-compliant。`dependencyDrift=unknown` 表示未检查，不得进入 production-ready；`dependencyDrift=unapproved` 表示无来源/未授权漂移，不得归为生产符合。

## Output Requirement

凡命中本门禁，阶段结果、Review finding、Verification report 或 Handoff 必须包含：

| 字段 | 说明 |
| --- | --- |
| complianceGateId | `HZC-*` 稳定编号 |
| complianceState | 四态之一；`production-compliant / production-candidate / mock-demo-compliant / non-compliant` |
| complianceManifestPath | `frontend/design/frontend-compliance-manifest.md`；Design/Task 使用本字段，最终 stage-result/Handoff 写入 `artifacts.complianceManifest`；code-generation/mock demo 可为 `not-applicable + reason` |
| complianceManifest | 逐项 gate 结果；最终 stage-result/Handoff 写入 `productionCompliance.manifest`，生产 ready 时全部适用项必须 pass/not-applicable |
| activeParentRegistries | active 父工程注册检查结论 |
| permissionCoverage | Button Contract 权限适用性和 required 权限按钮/权限码覆盖结论 |
| i18nCoverage | locale/i18n 资产覆盖结论 |
| listQueryContract | 列表 queryBar/filterBar、顶部 fuzzy search、fuzzyQueryFields、queryFieldsLimit、查询/重置/刷新行为覆盖结论；required fuzzy search 缺失、`queryBarProps.fuzzyQuery=false` 或 `queryBarProps.fuzzyQueryField/fuzzyQueryFields` 不得 production-ready |
| fieldUsageMatrix | DataSet/API/表格/表单/actionGuard/submit/renderer 字段来源，以及 storedField/renderedField/displayField/labelSource 覆盖结论 |
| detailRegionCoverage | 详情/编辑/主从页 Header/基本信息 required 字段、Form owner DataSet/record、required Tabs、明细筛选、详情动作和保存后 route 主键覆盖结论；required / 当前演示路径 / production-ready 适用时不得为 not-applicable；production-only、optional 或非本轮范围缺口可 partial 并进入 replacement/blocker |
| runtimeDataEntryContract | DataSet transport、页面 service action 和 mock/API handler 的唯一入口覆盖结论；confirmed hybrid 仅允许 shared helper/request adapter，不允许 DataSet transport 委托业务 service |
| statusActionMatrix | 状态动作可见、可点、函数入口 guard、目标状态和失败处理覆盖结论 |
| actionEntryMatrix | 动作存在来源、入口位置、页面模式、确认状态和实现策略覆盖结论 |
| buttonSemanticMatrix | 按钮区域、文案、语义类型、导航目标、业务变更和状态动作引用覆盖结论 |
| lovLookupCoverage | `*Id` 主数据 LOV、`*Code` 枚举 lookup/value set 覆盖结论 |
| componentApiProvenance | JSX 组件、权限按钮、组件静态 API、renderer/helper、附件和导入导出组件的 importPath/exportShape/apiEvidence 覆盖结论 |
| modalLifecycleContract | `Modal.open` / Drawer / 业务弹层自定义关闭、保存后关闭和 update 行为的 closeApiSource / closeApiEvidence 覆盖结论 |
| componentTypeCoverage | 日期、金额、附件、LOV/lookup 等字段组件类型覆盖结论 |
| hzeroCommonComponentContract | ChunkUploader、NewRichTextEditor、RichTextViewer 的版本、import、参数、绑定、运行验证和误归类拒收结论 |
| importExportContract | 头/行导入导出、模板、权限、父 ID、参数和刷新目标覆盖结论 |
| dependencyDrift | 根依赖/lockfile 归因结论；unknown/unapproved 不得 production-ready |
| failedChecks | 未通过项 |
| evidence | 文件/行号/命令/Network/设计任务来源 |
| severity | blocking / major / minor / info |
| requiredFixStage | Design / Task Breakdown / Implementation / Verification / Handoff |
| handoffLimit | production-ready / conditional / blocked |

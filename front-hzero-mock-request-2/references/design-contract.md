# Frontend Mock DevServer Contract

本文只描述 Frontend Design / Contract Check 阶段的前端 mock 契约。Task、Implementation、Review、Verification 和 Handoff 的运行时验收继承 `runtime-gate.md`。

## 阅读路由
- 判断是否可进入 mock-request 读 `Core Rule`。
- 确认 devServer、Umi/HZERO 插件和 middleware 归属读 `HZERO DevServer Boundary`。
- 输出 Mock API Contract 字段时读后续 contract 字段和验收要求。
- 运行时验收不在本文闭合，转 `runtime-gate.md`。

## Core Rule
- 默认 mock/demo 存在 generatedCandidate 主数据 LOV 时，Design 额外生成只读 `frontend/design/lov-candidate-contracts.json`。每个候选必须记录 `contractStatus=generatedCandidate`、`runtimeScope=mockOnly`、`*Obj/*Lov` objectField、value/text 与 ID/name bind、consumer、sourceRefs、`requestIsolation=field-level-candidate-only`、current-origin define/query endpoint、fixture fields 和 production replacement；`questionGate.required=false`。`consumers[]` 的最小合法结构为 `{"controlId":"detail-dept","objectField":"deptObj"}`，其中 `objectField` 必须与所属候选顶层字段完全一致，禁止只写 `controlId`。该 manifest 通过 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_lov_candidate_contract.py --manifest <path> --out <feature-root>/evidence/design-gates/lov-candidate-contract.json`，且 manifest/result hash 与 `contractFreezeId` 已进入 Design canonical closeout 后才允许进入 Task；不得用旧 composite status、`validated-pending` 或平台全局 LOV URL。
- 前端 mock 标准实现统一为 HZERO 本地开发服务器上的 HTTP mock API。
- mock API 必须通过内置 HZERO / Webpack / Umi devServer middleware/plugin 链路注册；标准父工程托管子模块直接按父工程 `config/config.ts` 顶层 plugin 注册生成，package-start 通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父工程同一 plugin 闭合。`config/config.dev.ts` 不得重复注册 `../dev-mock/<module>-dev-mock-plugin`。不得为 mock 绕过 `hzero-build`、微前端注册、父工程配置或项目既有启动脚本。
- Design / Contract Check 阶段的 mock-request 是固定快路径，不做工程 mock 机制选型。只要当前目标是标准 HZERO/Umi 可运行数据页面，无论用户是否同时提出真实 API 或 production-ready 诉求，都必须直接输出 `queryMode=mock-request`、`mockApiMode=hzero-dev-server-middleware`、`mockHandlerFile=dev-mock/<module>-dev-mock.js`、`mockPluginFile=packages/<package>/dev-mock/<module>-dev-mock-plugin.js` 和 `mockApiMount=/_mock/<module>`；真实 API 诉求只进入后续独立集成 advisory。目标工程存在 `_smock`、`smock/sproxy`、`.smockrc*`、`*.mock.js` 或其它历史 mock 机制时直接跳过，不触发 question/block，不作为方案候选；不得输出 `mockApiMode=project-smock`、`mockHandlerFile=_smock/*.mock.js`、`mockApiMount=/_smock`，也不得把 `.hzerorc/.smockrc/smock` 或其它工程历史 mock 机制写成 `parentRootMockPluginRegistration`。Contract Check closeout 必须自检这些禁止字段；命中时必须在本阶段内立即改写为标准 devServer middleware 合同，只把旧值记录为 `legacyMockEvidenceOnly=true` 的偏差说明，未改写前不得返回 `Frontend Design 已完成`、`confirmed` 或 `auto-confirmed-for-demo`。
- 业务页面、Choerodon DataSet 和 service 必须通过正常 HTTP 请求访问 mock API；页面交互逻辑应与后续真实 API 接入保持一致。
- mock API 仅用于本地开发和 demo 验证，不代表生产契约；使用 mock API 的顶层交付状态最高为 `conditional` 且必须写 `deliveryTarget=mock-demo`，切换真实 API 并验证通过后才可声明 `production-ready`。
- 非默认历史 mock 场景必须显式脱离 `mock-request`：只有用户明确要求 legacy mock 审计、迁移、解释或沿用，或目标工程已确认不是标准 HZERO/Umi 且无法写入内置 devServer middleware/plugin 链路时，才允许记录 `legacyMockEvidenceOnly=true`、`nonStandardMockMode=legacy-requested/project-equivalent/blocked` 或进入对应 question/block。该场景不得写 `queryMode=mock-request`、`mockDemoDecisionStatus=default-mock-demo`、`mockApiMode=hzero-dev-server-middleware` 或 `mock-demo-compliant`，也不得生成默认 mock demo runnable 任务；默认 mock-request 合同仍必须使用 `dev-mock` 链路。
- 参考子模块、相似页面或项目 evidence 只能证明可复用工程习惯，例如 request helper、DataSet/service 写法和目录结构；不能证明当前 feature 的生产契约或真实远端请求已闭合，也不能作为是否生成 mock plugin 的前提。无参考模块、参考资产缺失/不可读、`hzerojs-asset-baseline` 或 asset baseline 不影响内置 mock-request 生成。进入 Frontend Design 的可运行数据页面固定采用 `mockDemoDecisionStatus=default-mock-demo`、`runtimeDataPathDecision=requestable-demo-mock`、`queryMode=mock-request`、`mockApiMode=hzero-dev-server-middleware`。`default-mock-demo` 必须在 Design/Contract Check 阶段直接解析为 devServer middleware/plugin 方案，不允许保留抽象 mock/demo 分支；真实 API、production-ready 或拒绝 Mock 的诉求只进入后续独立集成与稳定化 advisory。只有目标明确不是标准 HZERO/Umi 托管形态且无法按内置链路写入，或当前 Mock 必需契约/写入范围存在冲突时，才回 question gate。
- Design/Contract Check 阶段必须为 `default-mock-demo` 写清 `mockHandlerFile`、`mockPluginFile`、`parentRootMockPluginRegistration`、`parentMockPluginRegistrationEvidence=standard-generated` 或 `parent aggregator standard-generated`、`packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`、`mockPluginTemplateCompliance`、`mockPluginSelfCheck=planned`、`mockPrefixOriginPolicy=current-dev-server-origin`、父工程 `config/config.ts` 顶层 plugin 注册或父工程聚合注册。任一关键字段缺失时必须自动 backfill；只有写入范围被禁止、dirty/conflict/只读锁、用户显式要求偏离内置链路或目标明确不是标准 HZERO/Umi 托管形态时，才 block/question，不能用 accepted-for-demo 放行。
- 标准 HZERO/Umi 项目不需要额外证明 devServer middleware 扩展点；Contract Check 可写 `devServerExtensionPoint=standard-hzero-umi-plugin`、`devServerExtensionEvidence=internal-standard-chain`。不得因为未深度探索父工程 mock 先例而阻塞 runnable mock 实现。
- 不得生成或接受 service 直接导入/返回本地 mock 数据、`src/utils/mock.ts`、模块内存数组、组件内 seed/filter、`service/mock + loadData`、local-filter、独立 `fetch` mock 或其它绕过 devServer middleware/plugin 的本地演示路线；发现时必须记录为 cleanup/rework blocker，不得作为演示分支、降级 fallback 或交付目标。
- 标准 mock-request 生成链路默认不得读取 `_smock`、`smock`、`sproxy`、`.smockrc*`、`*.mock.js`、`mockjs` 或历史 mock 脚本，避免把旧机制误当 follow-project 范式或样例数据来源。只有用户明确要求“迁移/审计/解释旧 mock 机制”时才允许只读这些文件，并必须输出 `legacyMockEvidenceOnly=true`；读取结果只能进入 legacy 说明或反模式证据，不得作为 `mock-request` 的字段来源、数据 seed、主接入点、交付方案或 HZERO mock 合同。Design 和 Task 不得为了判断“工程现有 mock 机制”而扫描这些文件；最多记录路径存在这一 legacy signal。
- mock handler 可以生成合理的 `demoGeneratedValue` 作为展示值和交互演示值，例如人名、部门、地址、单号、金额、日期等；这不是业务事实来源，也不得写成 FDS/TDS/MDS/API 示例来源。字段名、字段类型、必填性、枚举 code、状态流转、接口 resource path、payload/response shape 必须来自 FDS/TDS/MDS/API、Frontend Design、目标 DataSet/service 消费证据或明确 generatedCandidate 契约；demo 值只能填充这些已确认或候选字段。缺少真实业务样例时优先继续 demo，不因缺样例阻塞；必须在 Contract Check / Handoff / Production Replacement 中记录 `mockValueSource=demoGeneratedValue`、`businessFactSource=not-claimed` 和生产替换说明。
- `demoGeneratedValue` 只允许存在于 devServer mock handler、dev-only runtime store 或 mock API 响应中；不得作为 create/edit/copy 表单业务输入字段默认值、不得污染 submit payload、不得进入 production constants，也不得支撑 production-ready、真实 API readiness、权限/LOV/附件等生产契约闭合。新建页默认业务输入字段仍应为空或来自 UI Contract 明确默认值来源。
- mock/demo 请求必须使用隔离命名空间，默认挂载到 `/_mock/<module>/v1/{organizationId}/...`。`<module>` 使用已确认的业务模块或子模块短名；`{organizationId}` 必须来自 HZERO 运行时 `getCurrentOrganizationId()` 或等价租户上下文，不得使用 `demo-org`、`tenantId=0` 等硬编码占位。mock handler 必须按动态 organizationId 匹配列表、parents/LOV、export、详情和 action 路由；不得把任一分支写成固定租户路径（如 `/v1/0/...`、`/v1/58/...` 或 `/v1/demo-org/...`），也不得用 `organizationId` / `tenantId` / `orgId` 与固定字面量比较来返回 400。
- mock-request 身份必须显式建模，不得从包名、目录名或菜单名自动推导 mock namespace。Contract Check 必须同时记录 `packageDir`、`packageName`、`moduleKey/mockNamespace`、`mockApiMount` 和 `businessApiPath`；例如 `packageDir=packages/boogoo-front-prm`、`packageName=boogoo-front-prm`、`mockNamespace=prm`、`mockApiMount=/_mock/prm`。包名与 mock namespace 不一致是合法场景，但必须进入 validator 参数和后续 Review/Verify 对账；不得把 `boogoo-front-prm` 自动扩展成 `/_mock/boogoo-front-prm`。
- `<unconfirmed-gateway-prefix>/...` 在 HZERO 项目中默认按真实网关/后端服务入口处理，不得作为新生成 mock/demo 的请求前缀或 middleware mount；`/api/v1/demo-org/...`、裸 `/api/v1/...`、`/_smock`、`/mock`、`smock/sproxy` 均不得作为 `mock-request` 标准路径。历史代码命中这些路径时必须标记为 `legacy/invalid mock boundary`，不能声明 `mock-demo-compliant`。
- mock service/DataSet URL 与 middleware 监听必须同源同路径：同一个 `mockApiMount`、同一个 organizationId 参数位置、同一 resource path。mock 分支 servicePrefix 必须由业务包本地 `servicePrefix.ts` 生成当前 dev server origin + `/_mock/<module>` 语义；推荐使用 `front-hzero-enterprise-process-control` 的 `service-prefix.ts.template` 模板内本地 SSR guard helper，例如 `typeof window === 'undefined' ? '' : window.location.origin`。不得 import 或复用目标工程的 `getCurrentOrigin()`、`currentOrigin`、公共 origin helper 或其它项目 wrapper。middleware 必须监听等价模式，如 `/^\/_mock\/<module>\/v1\/[^/]+\/.../`。若 service 和 middleware 一个走 `<unconfirmed-gateway-prefix>`、一个监听 `/api/v1`，或一个使用真实 `API_HOST`、一个挂在本地 devServer，则 `requestWrapperMockConflict=blocked`。
- 详情、明细、状态动作和记录级导航的 mock 合同必须声明 not-found 行为：通过 `find* / lookup* / get*` 未找到 header、parent record 或目标记录时，handler 必须返回 `404 + JSON error body` 或合同确认的等价错误 shape；不得先调用 `enrich* / clone / lineList / child query / status guard`，不得返回 `200 + {}`、`200 + []`，也不得让 devServer 抛 `Cannot read properties of undefined/null`。头行场景中明细查询依赖 header 存在，父 header 不存在时必须 not-found，不能把明细空数组当成功结果。
- mock response shape 必须先对账消费端，再决定返回结构。Contract Check 必须读取目标 DataSet `transport.read`、`dataKey/totalKey`、`transport.adapter`、项目 request adapter、service action 消费代码或同工程可工作 mock 样例，记录 `mockResponseConsumerShape` 和每个 endpoint 的 `pageResponseShape/detailResponseShape/lovResponseShape/actionResponseShape`。若目标 DataSet 未声明 `dataKey/totalKey` 且项目可工作样例直接消费裸数组，列表 mock 必须返回裸数组；若详情 service/DataSet 直接消费实体，详情、新建、更新和 LOV 必须返回裸实体或裸数组。只有消费端明确配置 `dataKey='content'` / `totalKey='totalElements'`、项目 adapter 会读取分页对象，或生产候选契约要求分页对象时，才返回 `content / totalElements / size / number`；只有消费端明确 unwrap `data` 或真实接口契约确认 envelope 时，才允许返回 `{ data: ... }`。不得为了“看起来统一”给列表、详情、LOV、create/update/action 额外包一层 `data`，也不得把分页对象强加给裸数组 DataSet。
- 列表 mock 分页在消费端确认为分页对象时，固定按 Spring Data / Choerodon DataSet 的 0-based `page/size` 协议建模：请求 `page=0` 表示第一页，缺省 page 也必须是 0，handler 计算应为 `start = page * size`，响应返回 `content / totalElements / size / number`。不得用 `Number(query.page || 1)`、`Number(query.page ?? 1)` 或 fallback 1，也不得读取 `currentPage/pageSize`。`totalElements > 0` 但 `content=[]` 不能直接归因于缺 seed，必须检查是否使用了 `(page - 1) * size` 等 1-based 公式、默认 page=1、排序或筛选条件。
- mock 实现前仍必须读取目标项目实际使用的 `utils/request` 或 DataSet request adapter，确认 mock URL 是否会被拼接远端 `API_HOST`。若项目 request helper 会把 `/_mock` 拼到远端，mock service/DataSet transport 必须使用明确的 `dev-only-mock-http-adapter` 或由模板内本地 SSR guard helper 生成的当前 origin 绝对 URL，并保证该 adapter 只在 `queryMode=mock-request` 中使用，不得污染 production transport。
- mock 与真实 API 的 service 代码优先共用同一个项目 `request` helper 和同一个 `requestApi/buildUrl` 派生路径；差异只允许收敛到 `get<Module>ApiPrefix()`。若项目 request helper 对绝对 current-origin mock URL 支持明确，则 mock 分支仍走同一 request helper；若项目 request helper 不支持绝对 URL、会把 `/_mock` 拼到远端 `API_HOST`，或无法验证本地 devServer origin 命中，则必须在 Design/Task 明确拆 `dev-only-mock-http-adapter`。该 adapter 只允许服务 `queryMode=mock-request`，必须写入 production replacement / Handoff，不得污染 production transport。不得生成 `mockRequest` / `hzeroRequest` 两套长期请求实现，也不得让 mock 分支散落 URL 拼接或另一套 body/query 处理。mock 开关必须使用当前模块的静态 env 属性名，并严格生成 `process.env.<MODULE>_USE_MOCK !== 'false'`；不得生成 `process.env[envName]`、`process.env.<MODULE>_USE_MOCK === 'true'`、`!= 'false'` 或其它动态 key / 等价表达式。若项目没有公共 prefix helper，Design 应引用 `production-switch.md#Prefix Switch Pattern` 和 `front-hzero-enterprise-process-control` 的 `service-prefix.ts.template` 模板作为实现形态，并把模板来源写入 serviceRequestContract。
- `queryMode` 只表达设计/任务/验证阶段当前走 mock-request 还是 production-transport，不是业务源码的运行时字段。Design 不得把它写入 Mock API Contract 的 query/body、DataSet `queryParameter/transport`、service params、URL builder 或 mock handler，也不得要求 Implementation 生成 `queryMode === 'mock-request' ? mock : real` 作为请求主开关；源码必须使用模块静态 env switch。所有业务请求入口，包括 DataSet read/create/update/submit、form 保存、详情/action service 和导出，都必须从同一个 mock/real helper 派生 URL，不得直接使用 real-only service prefix 常量或 `get<Module>ServicePrefix()` 绕过 mock 分支。
- 若项目 request / DataSet adapter 没有任何可确认的本地 mock 通道，devServer middleware 不能拦截已经被拼成远端绝对 URL 的请求。Design 只能选择两类处理：一是明确拆 `dev-only-mock-http-adapter`，仅在 `queryMode=mock-request` 的 service/DataSet transport 内使用当前 dev server origin 请求本地 `/_mock/<module>/...`，且不得被 production transport 引用；二是输出 `requestBypassPrefix=none`、`requestWrapperMockConflict=blocked`、`handoffStatus=blocked`，无可运行目标时补 `blockedReason=non-runnable-target`。不得为了 mock 页面交付修改全局 request / DataSet adapter，不得用 `<unconfirmed-gateway-prefix>` 伪装真实接口、未证实的 `/api/v1` alias、独立 `smock/sproxy`、修改生产 API path、页面直连散落 `fetch`，或把远端 `API_HOST` 请求当作本地 mock。

## HZERO DevServer Boundary
- 接入前必须先识别目标工程的启动链路：package scripts、`hzero-start` / `hzero-build`、Umi 配置、`config/config.ts`、父工程 devServer 扩展点、微包 `packages-config`。
- mock middleware 只接入本地开发 devServer，不修改生产构建、微包产物、`remoteEntry`、`microConfig`、`PACKAGE_PUBLIC_URL`、public path 或部署配置。
- Webpack DevServer API 必须按项目版本和封装方式选择：webpack-dev-server v4/v5 常见为 `setupMiddlewares`，v3 常见为 `before` / `onBeforeSetupMiddleware`，Umi/HZERO 封装项目优先使用项目已有 config/devServer/mock 扩展入口。
- Umi/HZERO 项目若 `config.dev.ts` 的 `devServer.before` 未被实际启动链路消费，应优先使用 Umi 插件 `api.addBeforeMiddlewares` 注册 mock middleware；推荐文件形态为子模块自有 `packages/<module>/dev-mock/<module>-dev-mock.js` + `packages/<module>/dev-mock/<module>-dev-mock-plugin.js`。`dev-mock` 目录与子模块 `config` 目录平级；不存在时直接新建。原先规划在 `config` 目录下的 mock handler/plugin 也必须迁入 `dev-mock` 目录；父工程托管子模块必须由父工程注册并通过 `extendParentConfig` 继承，`config/config.dev.ts` 不得注册同一 mock plugin。
- `packages/<module>/mock` 是 Umi 内置 mock 扫描保留目录；`umi dev` 会按当前 `cwd` 自动加载 `mock/**/*.[jt]s` 并把导出对象归一化为路由 mock config。devServer middleware、Umi plugin、runtime store 或带 `__mockMount` 元数据的函数不得放入该目录；否则 package-start 时即使已继承父工程 plugin，也会被扫描器当普通 mock 配置展开，触发 `mock value of __mockMount should be function or object, but got string` 或等价启动失败。该目录只允许放标准 `"GET /path": handler` 形态的 Umi route mock config；标准 HZERO mock-request 不使用它。
- 子模块标准 plugin/handler 形态必须稳定：`<module>-dev-mock.js` 直接 `module.exports = <module>DevMockMiddleware` 导出 middleware 函数；`<module>-dev-mock-plugin.js` 必须来自 `front-hzero-enterprise-process-control` 的 submodule dev mock plugin 模板 的占位符替换结果，并直接 `require('./<module>-dev-mock')`。`api.addBeforeMiddlewares` 必须传入回调并返回 middleware 数组，例如 `api.addBeforeMiddlewares(() => [middleware])`；不得生成旧 `api.addBeforeMiddleware` fallback。生成物必须带启动自检：导出类型校验、`__mockMount` 与 `/_mock/<module>/` 一致性校验、重复注册跳过/告警、注册日志，以及缺失 Umi 扩展点时抛出明确错误。不得生成 `api.addBeforeMiddlewares(registerMock)`、`api.addBeforeMiddlewares(middleware)`、`require('./<module>-dev-mock')(api.app)`、`api.addBeforeMiddlewares(() => { require(...)(api.app); })`、解构不存在的命名导出，或只判断 `api.addBeforeMiddlewares` 属性存在而不判断函数类型。
- 必须区分目标落点是否为父工程管理的微前端子模块。只要页面落在父工程托管的 `packages/<module>`，mock handler/plugin 应归属子模块本身；父工程必须在 `config/config.ts` 顶层 `plugins` 用 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 显式注册该子模块 plugin，或用 `require.resolve('./dev-mock-plugin')` 注册父工程聚合 plugin 再由聚合 plugin 引用子模块 handler/plugin。不得写裸字符串 `./packages/<package>/dev-mock/<module>-dev-mock-plugin.js`、`packages/<package>/dev-mock/<module>-dev-mock-plugin` 或其它依赖当前 cwd 的相对路径；HZERO 子模块 build 会从 `packages/<package>` 作为 cwd 解析 Umi plugin，裸路径会找错目录。独立非父工程项目无 parent config 时，写 `parentMockPlugin=not-applicable` 并使用项目等价根配置入口。
- 必须区分 HZERO 子模块注册和 Umi 插件注册：`config/packages-config.js` / `hzeroMicro.packages` 只用于注册子模块包，默认最小条目为 `{ name: '<module>' }`。不得无来源在 package 条目中新增 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段；其中 `plugins` 不能用于注册 dev mock plugin，`registerRegex` 默认属于子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`。Umi plugin 必须进入父工程 `config/config.ts` 的顶层 `plugins` 数组，或由该数组注册父工程聚合 plugin。
- 必须区分父工程启动和子模块独立启动：父工程 `config/config.ts` 顶层 `plugins` 覆盖 `parent-root-start`，记录 `parentRootMockPluginRegistration=parent config/config.ts plugins -> submodule plugin / parent config/config.ts plugins -> aggregator`；HZEROJS Umi `packages/<module>` 子模块默认支持 `package-start` / 子包独立 `start`，还必须确认 package-start 能拿到同一个 dev mock plugin。标准链路是子模块 `config/config.ts` 使用 `extendParentConfig`，且父工程已经用 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 或聚合 plugin 注册当前 mock；记录 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`。`config/config.ts` 不得新增仅服务 mock 的顶层 plugin，`config/config.dev.ts` 不得注册同一 plugin；若项目明确不是父工程托管/继承模式，必须按 `standalone-project-equivalent-root-config` 另行记录，不得混入标准父工程托管路径。子模块 `config/config.ts` 默认是路由、微前端和构建配置事实源，其 `extendParentConfig` 继承父 plugins 只能作为 package-start 插件来源证据，不能表述为子模块注册 plugin。
- mock 数据归属同样在子模块 `dev-mock` 目录。数据量较多、包含多接口 seed、状态流转或头行明细 store 时，应拆为 `dev-mock/<module>-dev-mock-data.js`、`dev-mock/<module>-dev-mock-store.js` 或等价小模块，由 handler 引用；只有 1-2 条简单 seed 或极少量静态返回时，允许内联在 handler 中，不强制拆分。
- 默认不得为 mock 新增运行时或开发依赖。POST/PUT 请求体优先复用项目已有 JSON parser；若无现成 parser，则在 mock 模块内使用轻量 `readJsonBody` 工具。
- Contract Check 必须规划 mock plugin 自检机制，覆盖父工程/子模块 dev 配置重复加载、middleware 导出形态、mock mount 一致性、body parser 来源和缺失扩展点失败信息；缺少该规划时不得声明 mock plugin 模板合规。
- devServer middleware 必须拦截已确认 mock mount（例如 `/_mock/<module>/v1/{organizationId}/...`）并保证浏览器 Network 命中当前 dev server origin。mock 合同不得依赖启动独立 `smock/sproxy` 进程、不得要求业务页面请求远端 `API_HOST`，也不得把 `_smock` 文件注册为运行时入口。

父工程聚合 plugin 示例（允许）：

```js
// parent config/dev-mock-plugin.js
export default function devMockPlugin(api) {
  api.addBeforeMiddlewares(() => {
    const featureMockMiddleware = require('../packages/<module>/dev-mock/<module>-dev-mock');

    return [featureMockMiddleware];
  });
}
```

多个子模块同时需要 mock 时，父工程聚合 plugin 可以返回多个来自不同子模块的 middleware；不得把子模块业务 mock store/handler 搬到父工程聚合文件中。

```ts
// parent config/config.ts
plugins: [require.resolve('hzero-front'), require.resolve('./dev-mock-plugin')]
```

该形态只允许父工程聚合/转发；业务 mock handler、runtime store 和 resource path 仍应归属对应子模块。

父工程直接注册单个子模块 plugin 时，必须从父工程 `config/config.ts` 所在目录用 `require.resolve` 解析到子模块 `dev-mock` 目录：

```ts
// parent config/config.ts
plugins: [
  require.resolve('hzero-front'),
  require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin'),
]
```

该写法会在配置加载时生成绝对路径，兼容父工程 dev server 和 `hzero-build` 以子模块目录作为 cwd 的构建链路。

## State Transition Contract
- 涉及保存、提交、废弃、撤销、删除、复制、撤回等状态流转时，mock API 必须通过同一个 dev-only runtime store 维护当前态。
- 列表、详情、明细和动作后的刷新必须从同一个 runtime store 读取当前态。
- 状态守卫应在 mock route/store 中执行，并与页面按钮显隐/禁用规则一致。

## Contract Check Required Section

Contract Check 必须单列 `Mock API Contract`：

| 检查项 | 结论规则 |
| --- | --- |
| mock API 标准实现 | 固定为 HZERO 本地 devServer middleware 暴露的 HTTP mock API |
| default mock 收敛 | `mockDemoDecisionStatus=default-mock-demo` 必须同时写 `queryMode=mock-request`、`mockApiMode=hzero-dev-server-middleware` 和完整 plugin 注册计划；缺失时 Design 阻塞 |
| devServer 扩展点 | 标准 HZERO/Umi 目标写 `standard-hzero-umi-plugin`；只做最小路径/写入范围/冲突检查，不因缺相似模块或父工程 mock 先例阻塞 |
| legacy mock 证据 | 标准生成链路不读取 `_smock/smock/sproxy/*.mock.js`；仅用户明确要求 legacy 迁移/审计时只读，并标记 `legacyMockEvidenceOnly=true`；不得作为字段、seed 或交付方案 |
| request / adapter 边界 | 不做深度探索时默认使用 current-origin mock prefix 或 dev-only mock HTTP adapter；新生成 mock 的 middleware mount 为 `/_mock/<module>`，service prefix helper 必须返回当前 dev server origin + `/_mock/<module>`，不得交给可能拼远端 `API_HOST` 的裸 prefix |
| service 请求形态 | 优先共用项目 `request` helper 和统一 `requestApi/buildUrl`；若项目 request helper 不支持 current-origin mock URL 或会拼远端 `API_HOST`，必须拆 `dev-only-mock-http-adapter` 并仅限 `queryMode=mock-request`；不得拆 `mockRequest` / `hzeroRequest` 两套长期实现；mock env 开关必须是静态 `process.env.<MODULE>_USE_MOCK` 形态 |
| 无本地 mock 通道处理 | 不存在可确认本地 mock 通道时，只能拆 dev-only mock HTTP adapter 并验证隔离性，或阻塞 runnable mock；devServer middleware 不能拦截远端绝对 URL |
| mock API path | middleware 必须使用独立 mock namespace，如 `/_mock/<module>/v1/{organizationId}/...`，service/DataSet 实际请求必须命中当前 dev server origin + 该 namespace，并保留业务 resource path |
| organizationId 动态匹配 | service/DataSet 使用运行时租户时，mock handler 的列表、parents/LOV、export、详情和 action 分支必须动态解析同一 `{organizationId}` path 段；禁止数字租户、`demo-org` 等固定租户 path 字符串/正则，禁止 `organizationId` / `tenantId` / `orgId` 与固定字面量比较形成硬拒绝 |
| mock 身份模型 | 必须显式记录 `packageDir`、`packageName`、`moduleKey/mockNamespace`、`mockApiMount`、`businessApiPath`；包名与 mock namespace 不一致时必须按显式 namespace 生成 handler/plugin/prefix/validator 参数，不得从 package name 推导 |
| API_HOST 边界 | mock 请求必须命中当前 dev server origin；若落到远端 `API_HOST`，mock 合同失败 |
| middleware 挂载 | Umi 项目优先 `api.addBeforeMiddlewares` 插件；父工程托管子模块必须由父工程 `config/config.ts` 用 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 显式注册子模块 plugin，或用 `require.resolve('./dev-mock-plugin')` 注册父工程聚合 plugin；不得只依赖未被父工程挂载的子模块 plugin、裸相对路径或 `config.dev.ts devServer.before` |
| Design 必填 plugin 字段 | `mockHandlerFile`、`mockPluginFile`、`parentRootMockPluginRegistration`、`parentMockPluginRegistrationEvidence`、`packageStartMockPluginSource`、`invalidMockPluginRegistrationSites`、`mockPluginTemplateCompliance`、`mockPluginSelfCheck=planned`、`mockPrefixOriginPolicy=current-dev-server-origin` |
| mock 响应值来源 | 字段 shape / 枚举 code / 状态流转必须来自契约；展示值允许 `demoGeneratedValue`，但必须标记为非业务事实，进入 Handoff / replacement；不得用作 create/edit 默认业务输入 |
| plugin 自检机制 | 模板生成物必须校验 middleware 导出函数、`__mockMount`、重复注册保护和 Umi 扩展点；POST/PUT/DELETE body 读取必须说明复用 parser 或 `readJsonBody` |
| service/middleware 一致性 | service/DataSet baseUrl 与 middleware 监听 path 必须同源同路径；禁止 service `<unconfirmed-gateway-prefix>`、middleware `/api/v1/demo-org` 这类分裂 |
| lookup / not-found guard | 详情、明细、状态动作和记录级导航必须先判断 `find* / lookup* / get*` 结果，再进入 `enrich* / clone / lineList / child query / status guard`；缺失记录返回 `404 + JSON error body` 或合同等价错误 shape；头行明细缺父 header 不得返回成功空数组 |
| response shape 消费契约 | 必须先记录消费端证据：DataSet `dataKey/totalKey`、`transport.adapter`、项目 request adapter、service action 消费代码或同工程可工作样例；列表、详情、LOV、新建、更新和 action mock 返回结构必须与消费端一致 |
| 分页结构 | 只有消费端明确要求分页对象时，列表才返回 `content / totalElements / size / number`；消费端直接消费裸数组时必须返回裸数组，禁止额外 `{ data: [...] }` envelope |
| 分页语义 | 固定使用 0-based `page/size`，缺省 page=0；`page=0&size=10`、未传 page 都必须能返回首屏数据，禁止 `(page - 1) * size`、fallback 1 和 `currentPage/pageSize` 双协议 |
| 接入边界 | 仅允许本地 devServer；不得改变生产构建、微前端注册、remoteEntry、microConfig、public path 或部署配置 |
| 业务请求链路 | 页面、DataSet、service 必须通过 HTTP 请求访问 mock API |
| 状态流转 | 有运行态动作时必须使用同一个 dev-only runtime store |
| 依赖策略 | 默认零新增依赖；不得默认安装 `body-parser`、`msw`、`json-server`、`mockjs`、`faker` |
| 交付上限 | `queryMode=mock-request` 时最高 `handoffStatus=conditional` + `deliveryTarget=mock-demo`，不得声明 `production-ready` |

## Output Fields

```text
queryMode: mock-request / production-transport / blocked / not-applicable
packageDir: packages/<package> / not-applicable
packageName: <package.json name> / not-applicable
moduleKey: <mock namespace> / not-applicable
mockNamespace: <mock namespace> / not-applicable
mockApiMode: hzero-dev-server-middleware / not-applicable
devServerExtensionPoint: standard-hzero-umi-plugin / project-equivalent / blocked / not-applicable
devServerExtensionEvidence: internal-standard-chain / package script / Umi config / webpack devServer / HZERO wrapper / blocked / not-applicable
legacyMockEvidenceOnly: true / false / not-applicable
requestWrapperMockConflict: pass / blocked / not-applicable
requestBypassPrefix: current-dev-server-origin + /_mock/<module> / dev-only-mock-http-adapter-current-origin / none / unknown / not-applicable
requestBypassRemediation: existing-bypass / dev-only-mock-http-adapter / blocked / not-applicable
businessApiPath: /v1/{organizationId}/... / not-applicable
mockApiMount: /_mock/<module>/v1/{organizationId}/... / not-applicable
mockHandlerFile: dev-mock/<module>-dev-mock.js / not-applicable
mockPluginFile: packages/<module>/dev-mock/<module>-dev-mock-plugin.js / config/dev-mock-plugin.js aggregator / not-applicable
parentRootMockPluginRegistration: parent config/config.ts plugins -> submodule plugin / parent config/config.ts plugins -> aggregator / missing / not-applicable
packageStartMockPluginSource: parent-config-inherited-by-extendParentConfig / standalone-project-equivalent-root-config / missing / not-applicable
invalidMockPluginRegistrationSites: packages/<module>/config/config.dev.ts duplicate plugin / packages-config plugins field / parent-managed packages/<module>/config/config.ts top-level plugins-only / packages/<module>/mock dev-mock files / none
parentMockPluginRegistrationEvidence: standard-generated / parent config/config.ts top-level plugins confirmed / parent aggregator standard-generated / parent aggregator confirmed / invalid-packages-config / not-applicable
mockPluginTemplateCompliance: submodule-dev-mock-plugin-template / parent-aggregator-template / non-template-invalid / unknown / not-applicable
mockPrefixOriginPolicy: current-dev-server-origin / bare-prefix-invalid / remote-api-host-invalid / unknown / not-applicable
middlewareRegistration: api.addBeforeMiddlewares / project-equivalent / confirmed-devServer.before / unknown / not-applicable
mockPluginSelfCheck: planned / export-shape-pass+mount-pass+duplicate-guard-pass / failed / not-run / not-applicable
startupEntry: parent-root-start / package-start / parent-root-start+package-start / unknown / not-applicable
serviceMiddlewarePathConsistency: pass / failed / unknown / not-applicable
pageResponseShape: content / totalElements / size / number / not-applicable
mockResponseConsumerShape: bare-array / bare-object / page-response / data-envelope / project-adapter / unknown / not-applicable
detailResponseShape: bare-object / data-envelope / project-adapter / not-applicable
lovResponseShape: bare-array / page-response / data-envelope / project-adapter / not-applicable
mockRuntimeStoreRequired: true / false / not-applicable
mockEntityLookupGuard: pass / planned / missing / not-applicable
mockNotFoundResponseShape: 404-json / contract-equivalent / missing / not-applicable
detailLineMissingHeaderBehavior: explicit-not-found / empty-success-invalid / runtime-error / not-applicable
affectedStateActions: save / submit / abandon / withdraw / delete / copy / none / not-applicable
dependencyPolicy: zero-new-dependency / project-existing-parser / blocked
mockResponseValuePolicy: contract-shape-with-demoGeneratedValue / contract-example-values / placeholder-values / not-applicable
mockValueSourceLedger: fieldShapeSource + enumSource + demoValueSource + businessFactSource + handoffReplacementRequired
productionBuildImpact: none / risk / blocked
deliveryCeiling: conditional-mock-demo / production-ready / blocked / not-applicable
```

## Design Decisions
- Design 只冻结 mock API 的内置 devServer 接入点、挂载路径、父工程注册计划、plugin 模板合规、mock prefix origin 策略、状态流转需求、依赖策略和交付上限；不得把缺父工程历史证据作为 `generatedCandidate` 或降级理由。
- 不再在设计期维护 mock 方案优先级，不输出旧 mock 工具能力字段。
- `mock-request` 不等于 `production-ready`；存在 mock API 时必须进入 Production Replacement Draft，记录真实 API、request/response field shape、权限、LOV、lookup、附件、导入导出等生产契约替换项。

## Handoff To Process Control
后续任务验收、Network / HTTP smoke 证据、Review finding 和 mock-demo `reachable/usable` 闭合判定必须继承 `runtime-gate.md`。

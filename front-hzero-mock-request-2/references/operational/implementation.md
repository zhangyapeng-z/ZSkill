# Mock Request - 实现与工程证据

## 阅读路由
- Mock Request 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## Core Rules
- `frontend/design/lov-candidate-contracts.json` 存在时视为冻结只读输入。仅对 manifest 列出的候选字段配置 field-level `lovDefineUrl/lovQueryUrl`，并在 `dev-mock` 实现 define/query handler 与 consumer-aligned fixture；不得全局覆盖 HZERO LOV、修改 candidate code/objectField、改为普通 string/options，或让 contract-fidelity 自报 N/A。
- mock-request validator 与 contract-fidelity validator 必须传入同一 `--lov-candidate-manifest`。manifest 不存在时不激活该分支，不影响无 LOV 的普通 mock-request。
- mock/demo 请求必须使用隔离命名空间：`/_mock/<module>/v1/{organizationId}/...`；`{organizationId}` 来自 HZERO 运行时租户上下文，不得硬编码。
- mock handler 必须先按 `submodule-dev-mock.js.template` 保留 `parseMockRequestPath(pathname)`，业务分支统一从该 helper 返回的 `organizationId` 和 `resourceSegments` 派生；列表、parents/LOV、export、详情和 action 分支都必须动态解析同一个 `{organizationId}` path 段。不得用数字租户、`demo-org` 等固定租户 path 字符串/正则，也不得用 `organizationId` / `tenantId` / `orgId` 与固定字面量比较来拒绝当前运行租户。
- Implementation 写完 mock handler 后必须先做 `dynamicTenantPathImplementationCheck`：检查新增/修改的 `dev-mock/*-dev-mock.js` 是否保留模板 helper、所有 `/v1/{organizationId}/...` 业务分支是否基于 `resourceSegments` / 动态正则参数分发、parents/LOV/export/action 是否没有固定租户分支。该检查失败且文件在写入范围内时必须同轮修复，再运行 `mockRequestValidator`；不得把这类问题留给 Review / Verification 才发现。
- mock API 必须通过目标工程既有 HZERO / Webpack / Umi devServer 扩展点注册；不得改生产构建、微前端注册、remoteEntry、microConfig 或 public path。
- 子模块 mock handler、plugin、数据和 runtime store 统一放在与 `config` 平级的 `dev-mock` 目录；不存在时直接新建。原先生成到 `config` 或 Umi 保留 `mock` 目录下的 `*dev-mock*.js` 必须迁入 `dev-mock`。父工程托管子模块的 mock plugin 由父工程注册，并由子模块 `config/config.ts` 通过 `extendParentConfig` 继承；`config/config.dev.ts` 不得注册同一 plugin。
- `mock` 目录只允许存放 Umi 标准 route mock config，不得放 devServer middleware、Umi plugin 或带 `__mockMount` 元数据的函数。子模块 package-start 时 Umi 会以子模块为 `cwd` 自动扫描 `mock/**/*.[jt]s`；文件放错目录时，继承父工程 plugin 仍会正常发生，但扫描器会额外 require 这些文件并按 mock config 展开，导致 `__mockMount` 字符串进入 normalizeConfig 并启动失败。
- 父工程托管子模块的父工程入口必须在 `config/config.ts` 顶层 `plugins` 用 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 直接注册子模块 plugin，或用 `require.resolve('./dev-mock-plugin')` 注册父工程聚合 plugin；不得写裸字符串 `./packages/<package>/dev-mock/<module>-dev-mock-plugin.js`。HZERO 子模块 build 会从子模块目录作为 cwd 解析 Umi plugin，裸路径会在构建时找错目录。
- mock 数据量较多、包含多接口 seed、状态流转或头行明细 store 时，应拆为 `dev-mock/<module>-dev-mock-data.js`、`dev-mock/<module>-dev-mock-store.js` 或等价小模块；只有 1-2 条简单数据时允许内联在 handler 中，不强制拆分。
- 拆分 data/store 后，handler 必须显式 `require/import` 并让列表、详情、保存、状态动作和刷新接口从同一 data/store 读取或写回；不得只创建 data/store 文件但接口仍读局部空数组或另一套 seed。
- mock response shape 必须先对账目标 DataSet/service 消费端。Implementation 修改 handler 前必须确认 `dataKey/totalKey`、`transport.adapter`、项目 request adapter、service action unwrap 逻辑或同工程可工作 mock 样例，并记录 `mockResponseConsumerShape`。消费端直接消费裸数组/裸实体时，列表、详情、LOV、新建、更新和 action mock 必须返回裸数组/裸实体；不得额外包 `{ data: ... }`。只有消费端明确需要分页对象或 envelope 时，才返回 `content / totalElements / size / number` 或 `{ data: ... }`。
- 列表页 DataSet 出现 `paging: true`、未显式 `paging: false` 且请求参数包含 `page/size`，或绑定 Table 的主 DataSet 由 `transport.read` 分页查询时，默认按分页消费端处理，除非项目 request adapter / 同工程样例明确证明该 DataSet 直接消费裸数组。有效闭环只能是：mock/API 原始响应已经提供消费端可读的 `content / totalElements / size / number`，或由 DataSet `dataKey/totalKey`、项目 response adapter 等既有消费链路归一化到同一 shape；这些链路已经正常工作时不得为了“兼容/保险”新增 `transformResponse`。只有 raw shape、`dataKey/totalKey` 和项目 adapter 均不能闭合，且有消费证据说明需要局部归一化时，才允许新增最小 `transformResponse`。不得只因为 Network 里有 `{ data: [...] }` 或 `rows/list` 就声明列表可用；若表格空白但 HTTP 有数据，必须先打印实际响应、DataSet 消费链路和 Table 绑定 DataSet，再修 response shape / adapter。
- 列表分页在消费端确认为分页对象时固定按 0-based `page/size` 处理：`page=0` 是第一页，缺省 page 也是 0，`start = page * size`，响应返回 `content / totalElements / size / number`。不得用 `Number(query.page || 1)`、`Number(query.page ?? 1)` 或 fallback 1，也不得读取 `currentPage/pageSize`。`totalElements > 0` 但 `content=[]` 时优先排查 page 默认值、分页公式、排序和筛选，不要直接判定为缺数据。
- 头行明细、详情集合和其它 child collection 的分页参数只能来自 query/searchParams 中的 `page/size` 或等价分页字段；路径段只允许作为组织、父记录 id、资源名或动作名。不得把 `resourceSegments[0]`、`segments[1]` 等 path segment 传给 `createPage` 的 `page/size` 参数，否则 `/headers/1001/lines` 会把 `1001` 当页码并返回空 `content`。
- service/DataSet baseUrl 与 middleware 监听 path 必须同源同路径。浏览器 Network 必须命中当前 dev server origin，不能落到远端 `API_HOST`。
- prefix helper 必须区分 mock mount 与请求前缀：middleware mount 是 `/_mock/<module>`，但 mock service/DataSet 的 prefix helper 必须返回当前 dev server origin + `/_mock/<module>`；不得把裸 `/_mock/<module>` 作为默认 service prefix 交给会拼 `API_HOST` 的 HZERO/project request。
- handler `__mockMount` 和 plugin 自检 mount literal 必须统一使用 canonical `/_mock/<mockNamespace>/`，带尾斜杠且逐字一致；`/_mock/<module>` 与 `/_mock/<module>/` 混用必须判定 `mockPluginSelfCheck=failed`。
- mock 与真实 API 的 service 代码优先共用项目 `request` helper 和同一个 `requestApi/buildUrl` 派生路径；差异只能收敛到 `get<Module>ApiPrefix()`。
- 生成业务包 `src/utils/servicePrefix.ts` 时必须读取 `front-hzero-enterprise-process-control` 的 `service-prefix.ts.template` 模板并只替换占位符；不得 import 或复用目标工程 origin helper；模板内本地 SSR guard helper 是允许且推荐的生成形态，不得自由改写 mock mount、origin 或 env switch。
- 若项目 request helper 不支持 absolute current-origin mock URL，或会把 `/_mock` 拼到远端 `API_HOST`，必须使用仅服务 `queryMode=mock-request` 的 `dev-only-mock-http-adapter` 并写入 replacement / Handoff；不得污染 production transport。
- 不得生成 `mockRequest` / `hzeroRequest` 两套长期请求实现，不得让 mock 分支散落 URL 拼接或另一套 body/query 处理。
- `queryMode` 是 SDD / `frontend-stage-result` 的保留流程状态，不是业务源码运行时字段。生成代码不得在 `src/**/*.{ts,tsx,js,jsx}` 中定义、读取或透传 `queryMode`，尤其不得把它放入 DataSet `queryParameter/transport`、service `query/params`、request body、`URLSearchParams` 或手工 URL；mock handler 也不得依赖该参数决定响应。不得生成 `queryMode === 'mock-request' ? ... : ...` 来决定请求前缀。Implementation 必须使用模板里的模块 env switch，并让 DataSet transport、form submit、详情/action service、导出等业务请求入口统一走 `build<Feature>ServiceUrl()`、`get<Feature>ApiPrefix()` 或项目等价 helper；不得直接 import/use real-only service prefix 常量或 `get<Feature>ServicePrefix()` 拼 URL。
- mock 开关必须严格按 Contract Check / Task 的 `switchEnvVar` 静态 env 属性名生成，必须出现原表达式 `process.env.<switchEnvVar> !== 'false'`；不得根据 package、namespace 二次猜测，不得生成 `process.env[envName]`、`process.env.<switchEnvVar> === 'true'`、`process.env.<switchEnvVar> != 'false'` 或其它动态 key / 反向默认值 / 等价包装写法。
- 默认 mock；只有 `switchEnvVar` 精确等于字符串 `'false'` 时切真实。`undefined`、`true`、`1`、空字符串都继续走 mock；不得生成 `const <FEATURE>_USE_MOCK = process.env.<switchEnvVar> === 'true'` 这类未配置时默认走真实 API 的变量。
- 有状态动作必须请求 mock API，并由同一个 dev-only runtime store 维护当前态；mock handler 必须读取当前状态并校验迁移。
- 详情、明细、状态动作和记录级导航必须先 guard `find* / lookup* / get*` 结果，再进入 `enrich*`、字段读取、`lineList`、child query 或状态机；缺失 header / parent / target 返回 `404 + JSON error body` 或合同等价错误 shape。不得生成 `enrichHeader(findHeader(...))`、无判空的 `return enrichHeader(header)`、判空前访问 `header.lineList/header.xxx`，也不得把头行明细缺父 header 返回成功空数组。
- `queryMode=mock-request` 最高只能支撑 `handoffStatus=conditional` 且 `deliveryTarget=mock-demo`，不能声明 `production-ready`。切真实 API 并验证通过后才可参与 production-ready 汇合。

## Handoff And Ownership
- production replacement 或交付摘要必须记录 mock-only 项、真实 API 切换 owner、验证状态和不能声明 production-ready 的原因。
- 本 skill 是 HZERO 前端 mock-request 的规则事实源；其它 agent、skill、template 只保留阶段入口和摘要，不复制完整规则。

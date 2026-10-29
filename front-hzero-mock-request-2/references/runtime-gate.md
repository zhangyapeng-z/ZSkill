# Mock Request Runtime Gate

用于把 HZERO 本地 devServer middleware 暴露的 HTTP mock API 固化为 Task Breakdown、Implementation、Review、Verification 和 Handoff 的运行时验收门禁。Design / Contract Check 的精简合同在 `design-contract.md`。

## 阅读路由
- 判断 mock/demo 是否可进入实现前，先读 `适用边界` 和 `核心原则`。
- 拆任务时读 `Task Breakdown 门禁`；实现汇报时读 `Implementation 门禁`。
- 审查、验证和 Handoff 分别读 `Review 门禁`、`Verification 门禁` 和 `Handoff / 汇合门禁`。

## 适用边界
- 仅当功能进入 mock/demo 实现、`queryMode=mock-request`，或 Handoff 试图声明 mock-demo `reachable/usable` 已闭合时适用。
- 本门禁不提供 mock 方案选择；前端 mock 标准实现只有一种：HZERO 本地开发服务器上的 HTTP mock API。
- 使用 mock API 的顶层交付状态最高为 `conditional` 且必须写 `deliveryTarget=mock-demo`。切换真实 API 并验证通过后，才可参与 `production-ready` 汇合。
- 标准 mock-request 生成、任务拆分和实现链路默认不得读取 `_smock`、`smock`、`sproxy`、历史 `*.mock.js`、`mockjs`。只有用户明确要求 legacy mock 迁移、审计或解释时才允许只读，并必须标记 `legacyMockEvidenceOnly=true`；读取结果不得作为字段来源、mock seed、`mock-request` 主接入点或交付方案。

## 核心原则
- mock API 必须通过目标工程既有 HZERO / Webpack / Umi devServer 扩展点注册。
- 业务页面、Choerodon DataSet 和 service 必须通过正常 HTTP 请求访问 mock API。
- mock/demo 请求必须使用隔离命名空间，middleware mount 默认为 `/_mock/<module>/v1/{organizationId}/...`；service/DataSet 实际请求必须命中当前 dev server origin + 该 namespace。`<unconfirmed-gateway-prefix>/...` 视为真实网关/后端服务入口，不得作为新生成 mock/demo 前缀；`/api/v1/demo-org/...`、裸 `/api/v1/...`、`/_smock`、`/mock`、`smock/sproxy` 均不得作为 `mock-request` 标准路径。
- mock-request 身份必须显式建模：`packageDir`、`packageName`、`moduleKey/mockNamespace`、`mockApiMount` 和 `businessApiPath` 必须来自 Design / Task 合同。包目录、package name 与 mock namespace 不一致时，以显式 `mockNamespace` 为 handler/plugin 文件名、`/_mock/<namespace>` 和 validator 检查依据；不得从 `packages/<package>`、`package.json name`、路由或菜单名自动推导 mock namespace。
- `{organizationId}` 必须来自 HZERO 运行时 `getCurrentOrganizationId()` 或等价租户上下文；不得硬编码 `demo-org`、`tenantId=0` 或其它固定租户占位。
- mock handler 必须按动态租户路径解析所有业务 route：`/v1/{organizationId}/<resource>`、`parents/LOV`、`export`、详情和 action 分支都不得写成数字租户、`demo-org` 等固定租户路径，也不得用 `organizationId` / `tenantId` / `orgId` 与固定字面量比较来硬拒绝当前运行租户。handler 可读取并记录 `organizationId`，但不能把 mock 可用性收窄到任一固定租户。
- service/DataSet baseUrl 与 middleware 监听 path 必须同源同路径：同一个当前 dev server origin、同一个 `mockApiMount`、同一 organizationId path 段、同一 resource path。若 service 使用裸 `/_mock/<module>` 且项目 request helper 会拼远端 `API_HOST`、或使用 `<unconfirmed-gateway-prefix>/<service>/v1/{organizationId}/...`，middleware 却监听 `/api/v1/demo-org/...`，或 service 请求远端 `API_HOST` 而 middleware 挂在本地 devServer，必须判定 `serviceMiddlewarePathConsistency=failed`、`requestWrapperMockConflict=blocked`。
- mock response shape 必须与消费端一致。Task / Implementation / Review 必须读取目标 DataSet `dataKey/totalKey`、`transport.adapter`、项目 request adapter、service action 消费代码或同工程可工作 mock 样例，记录 `mockResponseConsumerShape`。消费端直接消费裸数组/裸实体时，列表、详情、LOV、新建、更新和 action mock 不得额外返回 `{ data: ... }`；消费端声明 `dataKey='content'` / `totalKey='totalElements'`、项目 adapter 或生产候选契约确认分页对象时，列表才返回 `content / totalElements / size / number`。请求发出成功不代表页面可用，response shape 与 DataSet 消费不一致时不得写 `usable=true`。
- 列表页 DataSet 若 `paging: true`、未显式 `paging: false` 且请求携带 `page/size`，或主 Table DataSet 的 `transport.read` 按分页查询运行，默认判定为分页消费端；只有项目 adapter / 同工程工作样例证明可直接消费裸数组时才可例外。分页消费端的成功路径必须能解释为 raw page response、`dataKey/totalKey`、项目 adapter，或确有必要时的最小 `transformResponse` 中的一条归一化链路，最终供 DataSet 消费的结构必须包含行集合与总数。raw response / `dataKey/totalKey` / 项目 adapter 已能正常消费时，不得新增 `transformResponse`；不得为了兼容多种猜测 shape 而覆盖已对齐字段。HTTP 200 且 body 有 `{ data: [...] }`、`rows` 或 `list` 但 Table 无记录时，优先按 `GCSQ-MOCK-005` / `GCSQ-ADAPTER-001` 处理，不得只扩大 seed 或声明 mock 可用。
- mock 实现默认使用当前 dev server origin 的 mock prefix 或 dev-only mock HTTP adapter，避免裸 `/_mock` 被项目 request wrapper / DataSet adapter 拼接到远端 `API_HOST`。不要求为 mock 生成深度探索 request wrapper；只要无法证明裸 prefix 安全，就直接使用 current-origin adapter。不得修改全局 request / DataSet adapter，不得改用 `<unconfirmed-gateway-prefix>`、`/api/v1`、`_smock`、`smock/sproxy`、页面散落 `fetch` 或远端 `API_HOST`。
- 外部 runtime acceptance 或用户手工 Network 证据中的实际请求必须命中当前 dev server origin。若请求落到远端 `API_HOST`，或需要启动独立 `smock/sproxy` 进程才能响应，则 `mockApiRequestVerified=false`，不得写 `reachable=true` 或 `usable=true`。
- mock middleware 只允许影响本地 devServer，不得修改生产构建、微前端注册、`remoteEntry`、`microConfig`、`PACKAGE_PUBLIC_URL`、public path 或部署配置。
- `packages/<module>/mock` 不得作为标准 HZERO mock-request 文件目录。Umi 内置 dev mock 插件会在当前 `cwd` 下扫描 `mock/**/*.[jt]s` 并把导出值当作路由 mock config 归一化；父工程启动时可能因为根目录没有 `mock` 而不触发，子模块 package-start 则会扫描子模块 `mock` 目录。把 middleware/plugin/store 放在该目录会造成“插件通道已继承且已注册，但 mock 扫描链路额外报错”的双链路问题。命中 `mock value of __mockMount should be function or object, but got string` 时，优先检查是否把 `*dev-mock*.js` 放在 Umi 保留 `mock` 目录，而不是误判为父配置未继承。
- 必须区分目标落点是否为父工程管理的微前端子模块。只要 Target Placement 是 `packages/<module>` 这类父工程托管子模块，mock handler 和 mock plugin 的归属就是子模块本身，例如 `packages/<module>/dev-mock/<module>-dev-mock.js` 与 `packages/<module>/dev-mock/<module>-dev-mock-plugin.js`；`dev-mock` 目录与子模块 `config` 目录平级，不存在时直接新建。父工程 `config/config.ts` 顶层 `plugins` 必须用 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 显式注册该子模块 plugin，或用 `require.resolve('./dev-mock-plugin')` 注册一个父工程聚合 plugin 再由聚合 plugin 引用子模块 handler/plugin。不得使用裸字符串 `./packages/<package>/dev-mock/<module>-dev-mock-plugin.js`、`packages/<package>/dev-mock/<module>-dev-mock-plugin` 或其它依赖当前 cwd 的相对路径；HZERO 子模块 build 会从 `packages/<package>` cwd 解析 Umi plugin，裸路径会找错目录。仅在子模块自己的 `config/config.ts` 注册、但父工程没有任何显式挂载时，mock-request 不成立。
- `config/packages-config.js` / `hzeroMicro.packages` 是子模块包注册入口，不是 Umi plugin 注册入口。父工程托管子模块默认只能新增/维护最小 `{ name: '<module>' }` 条目；不得无来源添加 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段。需要 mock plugin 时，不得把 `plugins: [require.resolve(...dev-mock-plugin)]` 塞进 package 条目；该写法不符合 Umi 顶层 `plugins` 规范，必须判定为 `invalidMockPluginRegistrationSites=packages-config plugins field`。`registerRegex` 默认属于子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`，不得用 package 条目字段兜底。
- 父工程和子模块独立运行路径的静态接线必须分别闭合：父工程 `config/config.ts` 顶层 `plugins` 覆盖 `parent-root-start`；HZEROJS Umi `packages/<module>` 子模块默认按 `startupEntry=parent-root-start+package-start` 处理，package-start 继承条件也必须能拿到同一个 dev mock plugin。标准父工程托管链路拆成两个字段记录：`parentRootMockPluginRegistration=parent config/config.ts plugins -> submodule plugin / parent config/config.ts plugins -> aggregator`；`packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`，表示子模块 `config/config.ts` 只通过 `extendParentConfig` 继承父配置，不表示子模块注册 plugin。子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得重复注册同一 plugin。若未继承父插件，`packageStartMockPluginSource=missing`，不得用 `config.dev.ts` 注册兜底；只有目标明确不是父工程托管/继承模式时，才按 `standalone-project-equivalent-root-config` 另行记录。
- Umi/HZERO 项目若 `config.dev.ts devServer.before` 未被启动链路消费，必须通过 Umi 插件 `api.addBeforeMiddlewares` 注册 middleware。父工程托管子模块推荐由子模块 plugin 实现 `api.addBeforeMiddlewares` 并维护子模块 mock store/handler；父工程只做注册/聚合，不承载业务 mock 逻辑。独立非父工程项目无 parent config 时，记录 `parentMockPlugin=not-applicable` 并使用项目等价根配置入口。
- 子模块标准 plugin/handler 形态必须稳定：`<module>-dev-mock.js` 直接 `module.exports = <module>DevMockMiddleware` 导出 middleware 函数；`<module>-dev-mock-plugin.js` 必须来自 `front-hzero-enterprise-process-control` 的 submodule dev mock plugin 模板 的占位符替换结果，并直接 `require('./<module>-dev-mock')`。`api.addBeforeMiddlewares` 必须传入回调并返回 middleware 数组，例如 `api.addBeforeMiddlewares(() => [middleware])`；不得生成旧 `api.addBeforeMiddleware` fallback。模板生成物必须带启动自检：导出类型校验、`__mockMount` 与 `/_mock/<module>/` 一致性校验、重复注册跳过/告警、注册日志，以及缺失 Umi 扩展点时抛出明确错误。handler 模板生成物还必须保留 `parseMockRequestPath(pathname)`，业务 route 从 `organizationId/resourceSegments` 动态分发，Implementation 阶段必须先用该 helper 实现列表、parents/LOV、export、详情和 action 分支。标准 middleware mount 的 canonical 值固定为 `/_mock/<mockNamespace>/`，带尾斜杠；plugin 自检常量与 handler 暴露的 `__mockMount` 必须逐字一致，不得通过 trim、尾斜杠归一或运行时容错掩盖差异。不得生成 `api.addBeforeMiddlewares(registerMock)`、`api.addBeforeMiddlewares(middleware)`、`require('./<module>-dev-mock')(api.app)`、`api.addBeforeMiddlewares(() => { require(...)(api.app); })`、解构不存在的命名导出，或只判断 `api.addBeforeMiddlewares` 属性存在而不判断函数类型。
- 保存、提交、废弃、撤销、删除、复制、撤回等状态流转必须请求 mock API，并由同一个 dev-only runtime store 维护当前态。
- 有状态动作的 mock handler 必须从 runtime store 读取当前记录状态并校验状态迁移，再写回目标状态；不得只根据前端传入的 action、旧 status 或 id 无条件改状态。前端按钮态/action guard 是第一层保护，mock handler 是第二层服务端语义保护，两者都必须存在。
- mock/demo 若提供记录级详情导航 API，即同一详情 Modal / Drawer / 当前页详情内按当前业务主记录切换到另一条业务主记录，必须复用同一个 runtime store 和同一套列表查询/筛选归一化规则。导航范围可以是当前筛选结果、全量候选或后端确认的固定集合，但必须在任务和验证中声明；当前记录不在筛选快照内时必须有明确 fallback 或错误 shape，不得静默返回 `{}` 后让前端误判为边界。方向、目标 id、筛选快照和 ID 类型必须规范化，`id` 默认按字符串比较；方向参数如存在大小写或别名兼容，必须集中处理并记录。
- runtime store 的 header/line 结构、分页返回、详情读取、save 级联回写和状态动作写法可直接参考 `mock-runtime-store-example.md`；允许项目差异，但不允许拆成列表、详情、动作三套事实源。mock 数据和 store 文件统一放在子模块 `dev-mock` 目录；数据量较多、包含多接口 seed、状态流转或头行明细 store 时拆为 `dev-mock/<module>-dev-mock-data.js`、`dev-mock/<module>-dev-mock-store.js` 或等价小模块，只有 1-2 条简单数据时允许内联在 handler 中。
- 拆出 `dev-mock/<module>-dev-mock-data.js` 或 `dev-mock/<module>-dev-mock-store.js` 后，handler 必须显式 `require/import` 这些文件，并让列表、详情、保存、状态动作和刷新接口都从同一 data/store 读取或写回；不得只创建 data/store 文件但 route 继续返回空数组、局部 seed 或另一套内存变量。若响应中 `totalElements > 0` 但当前页 `content=[]`，优先排查分页计算，不得直接归因为“没建数据”。
- 详情、明细、状态动作和记录级导航 handler 必须先判断 `find* / lookup* / get*` 的结果，再调用 `enrich*`、读取字段、读取 `lineList`、执行 child query 或执行状态机校验。缺失 header、parent record 或目标记录必须返回 `404 + JSON error body` 或合同确认的等价错误 shape；不得出现 `enrichHeader(findHeader(...))`、`const header = findHeader(...); return enrichHeader(header);` 无判空、判空前访问 `header.lineList/header.xxx`，或让 devServer 抛 `Cannot read properties of undefined/null`。头行明细查询缺父 header 时必须 not-found，不得返回成功空明细。
- 列表 mock 在消费端确认为分页对象时，固定按 Spring Data / Choerodon DataSet 的 0-based `page/size` 协议处理分页：`page=0` 必须从索引 0 开始；缺省 page 必须是 0，`start = page * size`，响应 `number` 回传当前 0-based page。不得用 `(page - 1) * size`、`Number(query.page || 1)`、`Number(query.page ?? 1)` 或三元 fallback 1，也不得读取 `currentPage/pageSize` 建立双协议。头行明细、详情集合和其它 child collection 也必须从 query/searchParams 读取 `page/size`；路径段只允许表达 organizationId、父 id、资源名或动作名，不得把 `resourceSegments[0]`、`segments[1]` 等 path segment 当作 page/size 传入分页 helper。
- 默认不得为 mock 新增运行时或开发依赖；POST/PUT 请求体优先复用项目已有 JSON parser，缺失时使用 mock 模块内轻量 `readJsonBody` 工具。
- 自检机制必须覆盖“有时正常、有时失败”的常见分叉：父工程和子模块 dev 配置同时加载时不得重复挂载同一个 mock；当子模块 `extendParentConfig` 已继承父 plugins 时，`config.dev.ts` 再注册同一 plugin 属于重复接线；父工程启动要有父工程注册证据，package-start 要有 `extendParentConfig` 继承来源证据；POST/PUT/DELETE handler 读取 body 前必须能解释 body parser 来源，若未复用项目 parser，则使用 mock 模块内 `readJsonBody`。

允许的父工程聚合 plugin 示例：

```js
// parent config/dev-mock-plugin.js
export default function devMockPlugin(api) {
  api.addBeforeMiddlewares(() => {
    const featureMockMiddleware = require('../packages/<module>/dev-mock/<module>-dev-mock');

    return [featureMockMiddleware];
  });
}
```

多个子模块同时需要 mock 时，父工程聚合 plugin 可以返回多个来自不同子模块的 middleware。父工程 `config/config.ts` 必须显式注册该聚合 plugin；聚合 plugin 只做集成转发，业务 mock handler/runtime store 仍在子模块。

父工程直接注册单个子模块 plugin 时必须使用 `require.resolve`：

```ts
// parent config/config.ts
plugins: [
  require.resolve('hzero-front'),
  require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin'),
]
```

父工程聚合 plugin 也必须用 `require.resolve('./dev-mock-plugin')` 注册。`require.resolve` 会在配置加载时生成绝对路径，避免 Umi/HZERO build 以子模块目录作为 cwd 时把 plugin 相对路径解析到 `packages/<package>/packages/...`。

状态动作 mock handler 参考模式：

```js
function withdraw(req, res, id) {
  const current = store.findById(id);

  if (!current) {
    return sendJson(res, 404, { message: '数据不存在' });
  }
  if (current.status !== 'SUBMITTED') {
    return sendJson(res, 400, { message: '当前状态不允许撤回' });
  }

  current.status = 'WITHDRAWN';
  store.save(current);
  return sendJson(res, 200, current);
}
```

该示例只表达生成形态：真实状态值、目标状态、错误 shape 和 HTTP status 必须来自 FDS/TDS/API 契约或标为 generatedCandidate；不得把示例状态码当 confirmed 业务契约。

## Task Breakdown 门禁
mock demo 实现任务必须写清：
- 身份模型：`packageDir`、`packageName`、`moduleKey/mockNamespace`、`mockApiMount`、`businessApiPath`。单 package 验证必须把 validator 命令写成显式 `--package-dir packages/<package> --mock-namespace <namespace>` 或等价参数；不得用无 `--package-dir` 的全量扫描结果代表目标包通过。
- 内置 HZERO / Webpack / Umi devServer middleware/plugin 接入文件；标准父工程托管子模块默认是父工程 `config/config.ts` 顶层 plugin 注册 + package-start 通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父 plugin。
- mock API 挂载路径、route 列表、method、query/body、response shape；挂载路径必须记录 `businessApiPath` 和 `mockApiMount`，例如 `businessApiPath=/v1/{organizationId}/...`、`mockApiMount=/_mock/<module>/v1/{organizationId}/...`。
- response shape 消费证据：必须列出目标 DataSet/service 如何消费接口结果，包括 `dataKey/totalKey`、`transport.adapter`、项目 request adapter、service action unwrap 逻辑或同工程可工作 mock 样例；任务不得只写“返回 DataSet 可消费结构”而不说明是裸数组、裸对象、分页对象还是 `{ data: ... }` envelope。
- 分页列表证据：若目标主 DataSet `paging: true` 或请求包含 `page/size`，必须记录 `pagingConsumerEvidence`，说明最终行集合字段、总数字段、page 语义、既有 `dataKey/totalKey` / adapter 是否已闭合，以及是否确需新增 `transformResponse`；不得只以“mock 返回 data 有值”作为可渲染证据。
- request wrapper / `API_HOST` 边界：任务必须把请求前缀字段记录为模板内本地 SSR guard helper 生成的当前 dev server origin + `/_mock/<module>`；不得把裸 `/_mock/<module>` 写成可交给 request wrapper 的 service prefix，不得 import 或复用目标工程 `getCurrentOrigin()` / `currentOrigin` / origin helper，也不得通过 `<unconfirmed-gateway-prefix>` 或未经证实的 `/api/v1` alias 规避。
- 无免拼口时的处理：任务必须直接拆分 `dev-only-mock-http-adapter` 和隔离性验证；不得让 Implementation 自行改 request wrapper 或散落新增 HTTP 调用。
- 目标落点与插件挂载：任务必须明确 `targetPlacement=parent-managed-package/standalone-app` 和 `startupEntry=parent-root-start/package-start/parent-root-start+package-start`。父工程托管子模块默认记录 `startupEntry=parent-root-start+package-start`，必须明确子模块 mock handler/plugin 文件、父工程 `config/config.ts` 用 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 直接注册该子模块 plugin 或用 `require.resolve('./dev-mock-plugin')` 注册父工程聚合 plugin，以及 package-start 通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父 plugin；不得因为缺父工程历史 mock 证据或相似模块而省略，也不得用子模块 `config/config.dev.ts` 注册同一 plugin 兜底。
- mock handler 文件和插件挂载：任务必须明确 mock store/handler 文件、子模块 plugin 文件、父工程注册文件、`api.addBeforeMiddlewares` 注册位置，或写明项目已有等价入口。
- mock-request 三项必填验收：父工程托管子模块必须在任务中列出父工程 `config/config.ts` 顶层 `plugins` 注册子模块 plugin 或父工程聚合 plugin 的文件映射，并记录 `parentRootMockPluginRegistration`；子模块暴露 plugin 必须按 `front-hzero-enterprise-process-control` 的 submodule dev mock plugin 模板形态生成，并列出占位符替换；service/DataSet 的 mock prefix 必须按 `service-prefix.ts.template` 生成，通过模板内本地 SSR guard helper 拼接当前 origin 与 `/_mock/<module>`，不得只写裸 `/_mock/<module>` 后交给可能拼远端 `API_HOST` 的 request wrapper，也不得 import 或复用目标工程 `getCurrentOrigin()` / `currentOrigin` / origin helper。父工程托管子模块还必须把 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig` 写入任务验收，并提供子模块 `config/config.ts` 使用 `extendParentConfig` 且父工程已注册同一 plugin 的源码证据。
- pre-review required validator：Task Breakdown 必须把 `mockRequestValidator` 写入当前 mock-request implementation task 的 required validators，并列出单 package 命令目标。能在任务阶段判断的错误必须直接拒收：`queryMode` 不得出现在生成的业务源码、DataSet/service query、request body、URL 或运行时主开关中；业务请求入口不得直接使用 real-only service prefix；DataSet/form/action/export 必须共用 mock/real URL helper。缺这些拒收项时，`Can Enter Implementation` 为否或只能拆 backfill task；不得把这类问题留到 Review/Verify 才发现。
- 分页接口必须返回 DataSet 可消费结构：`content / totalElements / size / number`。
- 分页验收必须覆盖 `page=0&size=10` 和未传 `page` 的首屏查询；`currentPage/pageSize` 必须被静态规则拒绝。当 seed/store 有数据时，`content` 不得因 1-based 公式或默认 page=1 为空；`totalElements > 0` 且 `content=[]` 时必须检查 page 默认值、`start = page * size`、排序和筛选条件。
- 头行明细和详情集合分页验收必须覆盖无分页参数的 `/parents/{id}/lines` 或等价 child collection URL；当父记录存在且有明细时，`content` 不得因父 id、资源名或其它 path segment 被误当分页页码而为空。
- 页面、DataSet、service 通过 HTTP 请求访问 mock API 的实现要求。
- 有状态动作时的 runtime store 文件、状态机、动作后刷新验收。
- 有状态动作时必须列出每个 action 的最小 guard：状态字段、允许源状态、目标状态、失败提示、handler 文件和 action service；生产完整矩阵缺失时写 `generatedCandidate / replacement`，但 Implementation 不得生成无条件动作。
- 有头行、详情和状态动作的 mock 页面必须说明列表查询、详情读取、保存回写和动作刷新如何共享同一个 runtime store；形态可按 `mock-runtime-store-example.md` 继承或等价实现。
- 有详情、明细、状态动作或记录级导航时，任务必须列出 lookup guard 和 not-found 验收：每个 `find* / lookup* / get*` 后先判空，缺失 header / parent record / target record 返回 `404 + JSON error body` 或合同等价错误 shape，再执行 enrich、明细读取、状态机或响应组装。头行明细查询必须写明缺父 header 的 `detailLineMissingHeaderBehavior=explicit-not-found`。
- 有记录级详情导航 API 时，任务必须说明导航候选集合、筛选快照字段、当前 id 来源、direction/target 参数、边界返回 shape、当前项不在候选集合时的 fallback 或错误处理，以及导航响应如何驱动详情 Header、基本信息、Tabs、子表和附件刷新。若该交互不是业务主记录切换，而是分页、轮播、步骤向导、Tab/区块切换或附件/图片预览翻页，必须写 `detailRecordNavigation=not-applicable + reason`。
- 不修改生产构建、微前端注册、`remoteEntry`、`microConfig`、public path 或部署配置。
- demo 运行态证据方式：外部 runtime acceptance 或用户手工浏览器 Network / HTTP smoke 必须记录 URL、method、query/body 和 response；Verification/Implementation 不启动服务或浏览器来生成该证据。
- 如可访问本资产脚本，Implementation 完成 mock-request 接线后必须运行一次 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_mock_request.py --root <frontend-root> --package-dir packages/<package> --mock-namespace <namespace> --mock-env-var <switchEnvVar>` 或等价本仓库路径，并记录 `mockRequestValidator`、`validatorCommand`、`validatorTarget`、`mockNamespace`、`mockEnvVar`、`validatorCheckedFiles` 和 `validatorChangedFilesHash`。`switchEnvVar` 从 Contract Check 读取，不得根据 package 或 namespace 二次猜测；合同未提供时才回退为 `<namespace>_USE_MOCK`。validator 只接受显式 `--package-dir`，不提供包名推导或全量扫描入口。该脚本用于机械拦截缺 `config/config.ts` 父配置继承、`config.dev.ts` 重复/错误注册 mock plugin、缺父工程 plugin 注册、plugin/handler mount literal 不一致、裸 `/_mock/<module>` prefix、service 绕 helper 直拼 URL、动态 `process.env[...]` mock 开关、0-based 分页漂移、以及 child collection 分页误用 path segment。无法运行时必须在 Implementation 写 `mockRequestValidator=not-run + reason`，并按本节人工逐项静态检查；manualStaticEquivalentCheck 不能替代外部 HTTP/Network smoke 证据。
- 父工程托管子模块的 mock plugin 注册任务关闭必须有源码级证据，不能只引用任务台账、文件存在或 validator 计划态。实现结果必须对账 `task-breakdown.md` 中的 required file mapping：父工程 `config/config.ts` 或已确认的父工程聚合 plugin 注册文件、子模块 `dev-mock/<module>-dev-mock-plugin.js`、子模块 `dev-mock/<module>-dev-mock.js`，以及 package-start 的 `config/config.ts extendParentConfig` 继承来源证据；`config/config.dev.ts` 或子模块 `config/config.ts` 顶层 `plugins` 注册同一 mock plugin 不能作为关闭证据。若父工程 `config/config.ts` 是 required file，本轮 `changedFiles` 未包含它，必须读取实际源码并记录 `alreadySatisfiedEvidence=exact require.resolve(...) present`；否则当前集成任务只能是 `partial-needs-rework / blocked-needs-rework / blocked`，不得以“子包已注册 / packages-config 已注册 / validator scoped passed”关闭。

## Implementation 门禁
实现结果必须声明：

```text
queryMode: mock-request / production-transport / blocked
packageDir: packages/<package> / not-applicable
packageName: <package.json name> / not-applicable
moduleKey: <mock namespace> / not-applicable
mockNamespace: <mock namespace> / not-applicable
mockApiMode: hzero-dev-server-middleware / not-applicable
devServerExtensionPoint: standard-hzero-umi-plugin / project-equivalent / blocked / not-applicable
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
mockPluginSelfCheck: export-shape-pass+mount-pass+duplicate-guard-pass / failed / not-run / not-applicable
dynamicTenantPathImplementationCheck: pass / failed / not-applicable
startupEntry: parent-root-start / package-start / parent-root-start+package-start / unknown / not-applicable
parentMockPluginSourceEvidence: changed-parent-config / already-satisfied-exact-source / parent-aggregator-source / missing / invalid-packages-config / not-applicable
serviceMiddlewarePathConsistency: pass / failed / unknown / not-applicable
pageResponseShape: content / totalElements / size / number / not-applicable
mockResponseConsumerShape: bare-array / bare-object / page-response / data-envelope / project-adapter / unknown / not-applicable
detailResponseShape: bare-object / data-envelope / project-adapter / not-applicable
lovResponseShape: bare-array / page-response / data-envelope / project-adapter / not-applicable
mockRequestEvidence: DataSet transport.read / project request adapter / non-DataSet service-action request / not-run
mockRuntimeStoreRequired: true / false / not-applicable
mockEntityLookupGuard: pass / failed / not-run / not-applicable
mockNotFoundResponseShape: 404-json / contract-equivalent / missing / not-applicable
detailLineMissingHeaderBehavior: explicit-not-found / empty-success-invalid / runtime-error / not-applicable
detailRecordNavigation: required / not-applicable
detailRecordNavigationScope: current-filter-result / all-candidates / fixed-set / unknown / not-applicable
detailRecordNavigationFallback: fallback-to-all-candidates / explicit-not-found / explicit-boundary / blocked / not-applicable
stateTransitionActions: save / submit / abandon / withdraw / delete / copy / none / not-applicable
stateTransitionGuard: ui-action-handler / ui-action-only / handler-only / missing / not-applicable
productionBuildImpact: none / risk / blocked
dependencyPolicy: zero-new-dependency / project-existing-parser / blocked
```

`mockPluginSelfCheck=planned` 只允许出现在 Design / Task Breakdown 的规划态；Implementation、Verification、Review 和 Handoff 必须写实际结果：`export-shape-pass+mount-pass+duplicate-guard-pass`、`failed`、`not-run` 或 `not-applicable`。

Implementation 不得以页面有数据显示作为完成证据；若没有 HTTP mock API 请求链路，只能输出 `handoffStatus=blocked`，或在存在可生成 mock-demo 目标但运行态未验证时输出 `handoffStatus=conditional`、`deliveryTarget=mock-demo`、`reachable/usable=unknown`。

`queryMode=mock-request` 的 Implementation 必须反查任务文件映射和实际 changedFiles：缺 `mockHandlerFile`、`mockPluginFile`、父工程 `config/config.ts` 顶层 plugin 注册或父工程聚合注册、默认 package-start 的 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig` 证据、当前 origin prefix helper / adapter 任一项时，不得补写为完成态；只能先回 Task Breakdown 补 integration task，或在明确 L1/本轮授权且写入范围允许时同步补齐并记录 `changedFilesSource=integrationTaskId/targetFiles`。若 task 没有授权 `dev-only-mock-http-adapter`，Implementation 不得为绕过 `API_HOST` 临时散落 `fetch/axios`。

Implementation 结果必须记录 `mockRequestValidator.status=passed/failed/not-run/not-applicable`，并同步 `validatorCommand`、`validatorTarget`、`packageDir`、`mockNamespace`、`mockEnvVar`、`validatorCheckedFiles`、`validatorChangedFilesHash`、`issueCount`、`issuesSummary` 和 `notRunReason`。若脚本或等价静态检查发现 `mock_config_parent_inheritance_missing`、`mock_config_dev_plugin_registration_forbidden_parent_managed`、`mock_config_dev_plugin_duplicate_inherited_parent`、`mock_parent_plugin_registration_missing`、`mock_service_prefix_current_origin_missing`、`mock_service_prefix_bare_mount_return`、`mock_request_direct_real_service_prefix`、`mock_service_direct_mount_path`、`mock_dynamic_env_key`、`mock_handler_entity_lookup_guard_missing`、`mock_handler_child_pagination_uses_path_arg` 或 `mock_handler_organization_id_fixed_tenant`，当前任务不得进入 `mock-completed`、`usable=true`、`Implementation Complete` 或 `Done`。当 validator 因包名、mock namespace 或 env key 推导不一致而失败时，必须按 Contract Check 改用 `--package-dir` + `--mock-namespace` + `--mock-env-var <switchEnvVar>` 复跑；不得把“脚本推导不适配”作为放行理由。若最终仍为 `failed/not-run/missing`，即使人工静态核对通过，也只能输出 `conditional` 或 `blocked`，且仍需外部 HTTP/Network smoke 证据才能证明可用性。`mockRequestValidator=passed` 也不能单独关闭父工程集成任务；必须同时有 `parentMockPluginSourceEvidence=changed-parent-config / already-satisfied-exact-source / parent-aggregator-source`，否则 task-status 必须保持返工或阻塞。

Review 阶段默认不重复运行 validator；它只消费 Implementation 的 `mockRequestValidator` 结果、`validatorTarget`、`validatorCheckedFiles`、`validatorChangedFilesHash` 和当前 diff，不启动 dev server、build 或 HTTP smoke。Review 只读取当前 diff / changedFiles 中的 mock plugin / servicePrefix / service 关键文件，并输出 `validatorReuseStatus=reused/stale/missing/failed/not-run`、`reviewMockStaticCheck=pass/failed/not-applicable`、`checkedMockFiles=[...]`。若 validator 缺失、failed/not-run 无等价人工检查、hash 与当前 changedFiles 不匹配，或 diff 检查命中 `mock-parent-plugin-missing`、`mock-config-parent-inheritance-missing`、`mock-config-dev-plugin-duplicate`、`mock-prefix-bare`、`mock-service-helper-bypass`、`mock-dynamic-env-key` 任一码，则输出 blocking finding 并回 Implementation。

Verification 阶段优先复用未过期的 `mockRequestValidator=pass`。只有缺少 validator 结果、结果为 failed/not-run、`validatorChangedFilesHash` 与当前 changedFiles 不匹配，或验证目标要求关闭该阻塞项时，才重跑 validator。无论是否复用 validator，声明 mock-demo `reachable/usable=true` 仍必须消费外部 Network / HTTP smoke 证据，证明请求命中当前 dev server origin；Verification 不启动服务或浏览器来补该证据。

## Review 门禁
以下情况必须形成 finding：
- mock API 未通过内置 HZERO / Webpack / Umi devServer middleware/plugin 链路注册。
- Target Placement 是父工程托管子模块时，只在子模块 `packages/<module>/dev-mock/*dev-mock-plugin.js` 注册 mock middleware，父工程 `config/config.ts` 未挂载等价 plugin。
- 在 `config/packages-config.js` / `hzeroMicro.packages` 的模块条目中无来源新增 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段；或新增 `plugins` 字段来注册 mock plugin，而父工程 `config/config.ts` 顶层 `plugins` 未挂载该 plugin 或聚合 plugin。
- 父工程托管场景下，子模块 `packages/<module>/config/config.ts` 新增仅服务 mock 的顶层 `plugins` 注册，或 `config/config.dev.ts` 重复注册同一 mock plugin。
- 父工程托管子模块声明 `mock-completed`、`usable=true` 或 `mockApiRequestVerified=true`，但缺少父工程 `config/config.ts` 顶层 `plugins` 标准注册或父工程聚合注册。
- 生成的 `*dev-mock-plugin.js` 未按模板直接 require middleware 并用 `api.addBeforeMiddlewares(() => [middleware])` 注册，或使用 `registerMock`、命名导出错配、直接传 middleware 等非模板形态。
- 生成的 `*dev-mock-plugin.js` 缺少模板自检能力，或启动时不能证明 middleware 导出形态、mock mount、重复注册保护和 Umi 扩展点可用性。
- 将 `_smock`、`smock`、`sproxy` 或历史 `*.mock.js` 作为主 mock 接入点，或把这些痕迹当作可 follow-project 的 mock 规范。
- 新生成 mock/demo service 或 DataSet 使用 `<unconfirmed-gateway-prefix>/...`，把 mock 伪装成真实网关/后端入口。
- service 或 middleware 出现 `/api/v1/demo-org`、硬编码 `demo-org`、固定租户占位，或未使用运行时 organizationId。
- mock handler 由 Implementation 新建或重写，但未从 `submodule-dev-mock.js.template` 保留 `parseMockRequestPath(pathname)`，或业务 route 没有基于 `organizationId/resourceSegments` 统一分发，导致实现阶段无法证明动态租户路径已闭合。
- mock handler 使用数字租户、`demo-org` 等固定租户 path 字符串/正则，或用 `organizationId` / `tenantId` / `orgId` 与固定字面量比较来拒绝当前租户；parents/LOV、export、详情和 action 分支也必须与列表一样使用动态 organizationId。
- service/DataSet baseUrl 与 middleware 监听 path 不一致，例如 service `<unconfirmed-gateway-prefix>/<module>/v1/{organizationId}/...`、middleware `/api/v1/demo-org/...`。
- 未确认项目 request / adapter 对 `/_mock` 的处理，导致请求落到远端 `API_HOST`。
- servicePrefix、DataSet transport 或 service helper 只返回裸 `/_mock/<module>`，没有拼接当前 dev server origin；当项目 request wrapper 可能追加远端 `API_HOST` 时必须判定为阻塞。
- 为了让 mock 命中本地服务而使用未经证实的 alias，例如把 `/v1/{organizationId}/...` 改成 `/api/v1/...`、`<unconfirmed-gateway-prefix>/...`、`/_smock/...`、`/mock/...`。
- Umi 插件链路应使用 `api.addBeforeMiddlewares` 但实现依赖未生效的 `config.dev.ts devServer.before`。
- `api.addBeforeMiddlewares` 直接接收 middleware 函数或 `registerMock`，没有使用 `() => [middleware]`；或 handler 使用命名导出但 plugin 按默认导出 require，导致启动时报错或 middleware 未注册。
- mock response shape 与消费端不一致，例如 DataSet 直接消费裸数组却返回 `{ data: [...] }`、详情直接消费实体却返回 `{ data: entity }`、LOV 直接消费数组却返回 envelope，或消费端需要 `dataKey/totalKey` 分页对象但 handler 返回裸数组，导致请求有数据但页面不展示。
- 分页消费端明确要求 `content / totalElements / size / number` 时，分页接口返回结构缺少这些字段，或对 `page` 使用 `(page - 1) * size` 等 1-based 公式导致 `page=0` 空页，导致 DataSet 不能稳定消费。
- 头行明细、详情集合或其它 child collection 把父 id、资源名或其它 path segment 当作分页参数传给分页 helper，导致存在明细时 `content=[]`。
- 拆出 `dev-mock/<module>-dev-mock-data.js` / `dev-mock/<module>-dev-mock-store.js` 后 handler 未引用，或列表、详情、动作接口没有从同一 data/store 读取/写回。
- mock 请求会被项目 request helper 拼到远端 `API_HOST`，或浏览器 Network 实际命中远端 host。
- 为 mock 改造生产构建、微前端注册、`remoteEntry`、`microConfig`、public path 或部署配置。
- 页面、DataSet 或 service 绕过 HTTP 请求自行维护 mock 数据成功路径。
- 保存、提交、废弃、撤销、删除、复制、撤回等动作没有请求 mock API。
- 保存、提交、废弃、撤销、删除、复制、撤回等 mock handler 不读取 runtime store 当前态、不校验允许源状态或无条件写目标状态。
- 列表、详情、明细和动作函数读写两套数据源，动作后刷新不能保持当前态。
- 详情、明细、状态动作或记录级导航中未判空就把 `find* / lookup* / get*` 结果传给 `enrich*`、读取 `header.lineList/header.xxx`、执行 child query 或状态机；缺失记录导致 500/devServer 抛异常，或头行明细缺父 header 时返回成功空数组。
- 记录级详情导航 API 的候选集合、筛选快照或当前 id 归一化与列表/详情 runtime store 不一致；当前记录不在筛选结果时静默返回空对象；边界、not-found 和成功响应 shape 混淆；或前端收到成功响应后仍无法刷新详情主记录。
- 为 mock 新增 `body-parser`、`msw`、`json-server`、`mockjs`、`faker` 等依赖，且没有项目既有统一约定或用户确认。
- `queryMode=mock-request` 被声明为 `production-ready`。

## Verification 门禁
声明 mock-demo `reachable/usable=true` 时必须记录：

| 字段 | 要求 |
| --- | --- |
| mockApiRequestVerified | 浏览器 Network 或 HTTP smoke 已验证 |
| networkMockApiUrl | 实际请求的 mock API URL |
| networkMockApiOrigin | 必须是当前 dev server origin，不得是远端 `API_HOST` |
| networkMockApiPath | 必须匹配确认后的 mock mount，如 `/_mock/<module>/v1/{organizationId}/...`；并记录对应 `businessApiPath=/v1/{organizationId}/...` |
| networkMockApiMethod | GET/POST/PUT/DELETE 等 |
| networkMockApiBodyOrQuery | 查询、分页、筛选或动作 body |
| pageResponseShape | 记录消费端确认的返回结构：`bare-array`、`page-response(content/totalElements/size/number)`、`data-envelope` 或 `project-adapter`；必须与 DataSet/service 消费证据一致 |
| middlewareRegistration | Umi 插件 `api.addBeforeMiddlewares` 或项目等价入口已生效 |
| mockPluginSelfCheck | 插件启动自检通过：middleware 导出函数、`__mockMount` 匹配、重复注册保护生效、缺失扩展点会明确失败 |
| startupEntry / targetPlacement | 父工程托管子模块或独立应用已识别；父工程托管子模块必须验证父工程 plugin 已注册并生效 |
| parentRootMockPluginRegistration | 父工程托管 HZEROJS Umi 子模块默认必须闭合父工程启动接线：父工程 `config/config.ts` 顶层 `plugins` 直接注册子模块 plugin，或注册父工程聚合 plugin |
| packageStartMockPluginSource | 父工程托管 HZEROJS Umi 子模块默认必须闭合 package-start：记录 `parent-config-inherited-by-extendParentConfig`（子模块 `config/config.ts` 通过 `extendParentConfig` 继承父工程已注册 plugin）；除非用户或目标工程文档明确禁止 package-start，否则不得写 `not-applicable` |
| serviceMiddlewarePathConsistency | service/DataSet baseUrl 与 middleware 监听 path 一致 |
| legacyMockToolBypass | `_smock/smock/sproxy` 未作为运行时入口；若使用则 failed |
| requestEntryEvidence | DataSet `transport.read`、项目 request adapter 或非 DataSet / 明确 service-action owner 的 service request 触发证据；不得用 DataSet transport 调业务 service 充当证据 |
| detailRecordNavigationVerified | 适用时，HTTP smoke 或浏览器 Network 覆盖当前记录切换到另一条业务主记录并切回，记录 currentId、targetId 或 direction、筛选快照、响应记录 id、边界返回 shape；不适用时写 not-applicable + reason |
| stateTransitionVerified | 有状态动作时，保存/提交/废弃/撤销/删除后刷新仍为当前态 |
| runtimeStoreConsistency | 列表、详情、明细和动作后刷新来自同一个 runtime store |
| lookupNotFoundVerified | 详情、明细、状态动作或记录级导航适用时，HTTP smoke 或浏览器 Network 覆盖不存在 header/parent/target id，并返回 404 JSON 或合同等价错误 shape；正常存在 id 仍返回详情和明细 |
| stateTransitionGuard | 有状态动作时，UI 按钮态、action 入口和 mock handler 均存在同源状态 guard |
| productionBuildImpact | 已确认未改生产构建、微前端注册和部署配置，或写明未验证 |

只跑 lint、typecheck 或 build 不足以证明 `mock-request`。缺外部浏览器或 HTTP smoke 证据时，`mockApiRequestVerified=false`，不得声明 `reachable=true` 或 `usable=true`。

## Handoff 门禁
Handoff / frontend-stage-result / Lite 汇合判定中，只要当前功能属于 mock demo 或 `mock.queryMode=mock-request`，且试图声明 `reachable/usable=true`，必须同时满足：

- `queryMode=mock-request`。
- `mockApiMode=hzero-dev-server-middleware`。
- `mockApiRequestVerified=true`。
- Verification Report 已记录 `networkMockApiUrl`、`networkMockApiMethod`、`networkMockApiBodyOrQuery`。
- Verification Report 已记录 `networkMockApiOrigin` 为当前 dev server origin，`networkMockApiPath` 与已确认 mock mount 一致，且可追溯到业务 API path。
- Verification Report 已记录 `pageResponseShape`、middleware registration、startupEntry 和 serviceMiddlewarePathConsistency；插件链路可用性可以用 Node middleware/plugin smoke test 证明。
- Verification Report 已记录 `mockResponseConsumerShape`，且外部 HTTP/Network 响应结构与 DataSet/service 消费证据一致；只证明接口返回 200 或有 JSON 不能证明 DataSet 已可渲染。
- Verification Report 已确认未依赖 `_smock/smock/sproxy` 作为运行时入口。
- Verification Report 已记录 DataSet / request adapter / 非 DataSet service-action request 触发证据。
- 有状态动作时，`stateTransitionVerified=true` 且 `runtimeStoreConsistency=pass`。
- 有状态动作时，`stateTransitionGuard=ui-action-handler`；若仅按钮禁用或仅 action guard 生效，只能输出 `conditional` 并写 `usable=unknown/false`。
- production replacement checklist 已覆盖真实 API、request/response field shape 和相关生产契约替换项。

缺少任一项时，Handoff 只能输出 `conditional` 或 `blocked`；无可运行目标时写 `progressionDecision.blockedReason=non-runnable-target`。缺口必须写入 `blockers`、`unverifiedItems`、`frontend-stage-result-fields.mock.mockApiRequestVerified=false` 和 `progressionDecision`。

父工程托管子模块下，`parentMockPluginSourceEvidence / parentMockPluginSourceVerification` 是源码级接线证据，不等同于 `config/packages-config.js` 包注册、子模块 `config/config.dev.ts`、task-status 勾选或 validator scoped pass。缺失时应优先回 Implementation 补父工程 `config/config.ts` 顶层 plugin 或父工程聚合 plugin 证据；若父工程不可写/不可读或本轮只交付静态候选，则降级为 `conditional`，写 `reachable/usable=unknown`、`mockApiRequestVerified=false` 和手动/后续接线项。只有已确认该目标无可运行入口或接线冲突无法形成 mock demo 时，才写 `blocked`。

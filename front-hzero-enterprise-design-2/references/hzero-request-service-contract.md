# HZERO Request / Service Contract

用途：统一 HZERO 前端 service、Choerodon DataSet transport 和 mock-to-production replacement 中的请求封装、API_HOST、服务前缀和原生 HTTP 使用边界，避免绕过 HZERO request 或手写不完整 base URL。

## 阅读路由
- 生产请求、servicePrefix、API_HOST 和 request helper 边界读 `默认规则`。
- mock/demo 与真实 API 快速切换读 `Mock / Production Prefix Switch`。
- 原生 HTTP 或 native fetch/axios 需求读原生 HTTP 相关小节。
- Design / Contract Check 输出字段以本文字段名为准。

## 默认规则

- HZERO 业务页面和 service 的生产请求默认使用目标工程已确认的 request helper，常见为 `import request from 'utils/request'`。
- HZEROJS / hzero-front 标准工程中，若工程探索未发现项目级自定义 request wrapper、native HTTP 要求或相互冲突的请求封装，`requestHelper` 必须按 HZERO baseline 自动闭合为 `symbol=request`、`importPath=utils/request`、`evidence=HZERO baseline + target project no-conflict scan`。不得向用户询问“request helper 的真实符号与导入路径”。只有发现多个项目 wrapper、目标工程明确禁用 `utils/request`、或需要原生 HTTP / 外部直连时，才进入 question 或标记 conflict。
- 当前 HZERO request helper 默认视为已内置 `API_HOST` 拼接；业务 service URL 默认不要再手动拼 `API_HOST`，除非目标工程现有代码或 request 封装证据证明必须显式拼接。
- service URL 应使用已确认服务前缀，例如 `HZERO_PLATFORM`、`HZERO_IAM` 或业务服务环境 key，并通过 `getEnvConfig()` / 项目等价 env helper 获取。
- MDS/API/Swagger 中的 `/v1/{organizationId}/...` 只代表业务资源路径，不等于前端可请求 URL。生产 URL 必须由 `servicePrefix + resourcePath` 组成，例如 `/<servicePrefix>/v1/{organizationId}/...`；不得从 `/v1/...` 反推服务前缀，也不得只保留 `/v1/...` 后声明 production transport。
- `servicePrefix` 来源优先级：先读取项目公共配置或 env helper（如 `@common/utils/config`、`src/utils/config`、`src/config/servicePrefix`、`getEnvConfig` 等目标工程实际存在项）；再读取同项目相似 service 写法归纳服务前缀；再使用 FDS/TDS/MDS 中明确服务编码生成候选（如 `HSPD` -> `/hspd`）。候选只能写 `generatedCandidate`，未被项目证据或用户确认前不得升级为 confirmed。
- 不得假设存在 `packages/<project>-common` 或任意特定公共包。目标工程没有公共配置时，可在当前业务包内生成本地 `src/utils/servicePrefix.ts` 作为 demo/production replacement 过渡工具；后续若平台要求统一配置，再迁移到公共配置。
- 运行时代码读取 `API_HOST`、`HZERO_*`、业务服务前缀、`BASE_PATH` 或 public URL 时，必须使用 `getEnvConfig` 或项目已确认 env helper；不得使用未确认的 `process.env`、`window` 全局变量或硬编码 host。
- DataSet `transport` 可以直接返回项目 request helper 所需的 `url/method/params/data` 配置；若需要函数式 transport，也必须走项目 request helper 或已确认 DataSet request adapter。
- HZERO 标准工程无冲突时，非 DataSet service action 的统一成功/失败处理自动使用 `getResponse`（`import { getResponse } from 'utils/utils'`）。这不是用户确认项；接口特有 body、分页和 adapter 仍必须来自 backend API readiness 或已确认 API 契约。
- DataSet read 默认使用 DataSet-native 响应消费，不能因为 `getResponse` 是内置标准就把所有列表请求包一层。`dataKey/totalKey`、data envelope 或 project adapter 由逐接口 `responseHandlingContract` 决定。

## Mock / Production Prefix Switch

mock/demo 页面可以默认生成可切换请求前缀，但必须把 mock namespace 和真实 servicePrefix 分清。若需要在业务包生成本地 `src/utils/servicePrefix.ts`，Design / Task / Implementation 必须引用 `front-hzero-enterprise-process-control` 的 `service-prefix.ts.template` 模板，只替换占位符后落盘；不得自由重写 origin helper、mock mount 或 env switch。

```ts-template
const REAL_SERVICE_PREFIX = '/<servicePrefix>';
const MOCK_PREFIX = '/_mock/<module>';

export const getRealServicePrefix = () => REAL_SERVICE_PREFIX;
export const getMockOrigin = () =>
  typeof window === 'undefined' ? '' : window.location.origin;
export const getMockPrefix = () => `${getMockOrigin()}${MOCK_PREFIX}`;
export const getRequestPrefix = () =>
  process.env.<MODULE>_USE_MOCK !== 'false' ? getMockPrefix() : getRealServicePrefix();
```

- 默认必须走 mock，保证 demo 有数据；只有显式环境变量字符串 `'false'` 才切真实 API。`undefined`、`true`、`1` 或其它值都继续走 mock。
- 环境变量名必须带业务模块前缀，例如 `<MODULE>_USE_MOCK`；不得使用全局 `USE_MOCK` 影响多个模块，除非项目已有统一规范。
- mock mount 固定使用 `/_mock/<module>` 并命中当前 dev server origin；业务包本地 prefix helper 的 mock 分支必须通过模板内本地 SSR guard helper 返回当前 dev server origin + `/_mock/<module>` 语义，不得只返回裸 `/_mock/<module>` 再交给会拼 `API_HOST` 的 HZERO/project request，也不得 import 或复用目标工程 `getCurrentOrigin()`、`currentOrigin` 或其它 origin helper。真实前缀使用已确认或候选 `/<servicePrefix>`，交给 HZERO/project request helper 拼接 `API_HOST`。不得用 `<unconfirmed-gateway-prefix>` 作为 mock 前缀，也不得把 `/_mock` 当成真实 servicePrefix。
- mock mount 的 `/_mock/<module>` 必须在落盘源码中作为字面量出现；不得生成 `` `/_mock/${MODULE_CODE}` ``、`` `/_mock/${mockNamespace}` `` 或其它运行时拼接 mount 的形态。mock namespace 来自 Design / Task 合同，替换发生在生成阶段。
- DataSet 列表、详情、保存、删除、提交、撤回、复制等动作必须从同一个 `baseUrl` 派生，避免列表走 mock、详情或 action 走真实接口。
- mock/demo 实现可以同步生成真实 API 候选分支，便于后续切换，但必须满足：至少已有 `resourcePath`、method、payload/response 基础事实或后端服务编码候选；真实分支默认不启用，只能通过 `<MODULE>_USE_MOCK=false` 精确切换；状态为 `generatedCandidate / partial` 的真实分支必须进入 Production Replacement Draft，不得支撑 production-ready。
- 保存、删除、提交、撤回、作废、复制等 action 的 mock 分支和真实候选分支必须共用同一组 service 函数、状态 guard、payload builder 和 response adapter；差异只允许在 baseUrl / request prefix / mock runtime handler。不得在按钮 handler 中散落 `if mock then ... else ...` 的两套业务逻辑。
- 当 `servicePrefix` 只是候选时，交付状态最高为 `conditional`；只有真实前缀、response shape、payload、错误结构、权限/租户等契约闭合并验证后，才能声明 `production-ready`。

## Typical Scenarios

| 场景 | 规则 |
| --- | --- |
| 项目已有公共 service 配置 | 复用公共配置，记录 importPath/evidence；不得新造本地 prefix helper。 |
| 没有公共配置，但相似 service 都使用 `/hspd` | 可生成业务包内 `src/utils/servicePrefix.ts`，`REAL_SERVICE_PREFIX='/hspd'` 标记为 `generatedCandidate` 或 `confirmed`（取决于证据质量）。 |
| 后端文档只写 `/v1/{organizationId}/xxx` | `resourcePath` 可确认，`servicePrefix=missing`；不得切 production transport。 |
| FDS/TDS/MDS 写服务编码 `HSPD`，工程无证据 | 可生成候选 `/hspd` 方便 `XXX_USE_MOCK=false` 试连，但 production-ready 阻塞。 |
| 当前项目真实 API 不使用 `<unconfirmed-gateway-prefix>` | `<unconfirmed-gateway-prefix>` 不得作为 mock 或生产候选；必须寻找真实 servicePrefix 或标 missing。 |
| 父工程托管子模块使用 mock | mock plugin/handler 归属子模块，但必须被父工程 `config/config.ts` 顶层 `plugins` 显式注册，或被该数组注册的父工程聚合 plugin 引用；真实 API 切换只改 service prefix，不依赖 mock plugin。 |

## 原生 HTTP 例外

原生 `axios`、`fetch`、`XMLHttpRequest` 不是绝对禁止，但不能作为 HZERO service 默认方案。

- 只有业务需求文档、技术设计或用户输入明确要求原生 HTTP、第三方直连、二进制流特殊处理、跨域外部系统或不经过 HZERO request 的场景，才允许进入原生 HTTP 候选；目标项目既有原生 HTTP 代码只能作为实现参考证据，不能单独作为授权来源。
- 如果需求文档明确提到原生 `axios/fetch/XMLHttpRequest`、外部直连或绕过 HZERO request，但用户尚未确认，Design 阶段应通过 question 工具确认是否允许原生 HTTP，并记录确认来源。
- 如果需求文档没有写原生 HTTP，不要为了“确认是否能用 axios/fetch”去问用户；默认使用 HZERO request / 项目 request adapter。
- 原生 HTTP 一旦确认，必须记录为什么不能使用 HZERO request、token/header/error/tenant/API_HOST/CSRF 如何处理、验证方式和残余风险；否则不得进入 production-ready。

## 禁止项

- 非 mock / production transport 中直接 `import axios from 'axios'`、`axios(...)`、`fetch(...)` 或 `new XMLHttpRequest()`，但没有 explicit native-http 确认来源。
- 新建 `getRequestBase()`、`buildRequestBase()`、`resolveRequestBase()`、`getApiBase()`、`getBaseUrl()` 等本地 base URL resolver 来替代项目 request/env/helper 契约。
- 在本地 base resolver 中只替换路径占位符或模板参数，例如 `{organizationId}`、`{tenantId}`、`{id}`、`{code}`、`:id`、`${id}`，但不处理已确认服务前缀、request helper、envSource、tenantContext、权限/安全头和路径参数来源。
- HZERO request 已内置 `API_HOST` 时仍手动拼 `${API_HOST}${servicePrefix}`，导致重复 host 或跨环境错误。
- 真实 API 请求 URL 缺少已确认服务前缀，只保留 `/v1/...` 或业务相对路径，却声明 production transport 已闭合。
- 用硬编码 host、`process.env.API_HOST`、`window.API_HOST` 或未确认 env key 拼 production API URL。

## Contract Check Schema

```text
serviceRequestContract:
  requestMode: hzero-request / project-request-wrapper / dataset-transport / native-http-explicit / mock-request / not-applicable / missing
  requestHelper:
    symbol: request / <project-request> / DataSet transport adapter / not-applicable / missing
    importPath: utils/request / <confirmed import path> / not-applicable / missing
    evidence: file path + line / HZERO baseline + target project no-conflict scan / not-applicable / missing
  baseUrlStrategy: request-adds-api-host / explicit-api-host-required / current-origin-static-mock / project-proxy / not-applicable / missing
  envSource:
    symbol: getEnvConfig / <project-env-helper> / not-applicable / missing
    importPath: utils/iocUtils / <confirmed import path> / not-applicable / missing
    keys: [HZERO_PLATFORM / HZERO_IAM / business service key / API_HOST / BASE_PATH]
    evidence: file path + line / deployment handoff / missing
  resourcePath: /v1/{organizationId}/... / not-applicable / missing
  servicePrefix: HZERO_PLATFORM / HZERO_IAM / business service key / literal prefix such as /hspd / full external origin / generatedCandidate / not-applicable / missing
  servicePrefixSourcePriority: common-config / similar-service / backend-service-code / user-confirmed / missing / not-applicable
  servicePrefixHelperFile: packages/<module>/src/utils/servicePrefix.ts / existing-common-config / not-applicable / missing
  switchEnvVar: <MODULE>_USE_MOCK / not-applicable / missing
  mockDefaultPolicy: default-mock-explicit-false-to-production / production-only / not-applicable
  responseHandlingContract:
    mode: hzero-get-response / dataset-native / dataset-data-key-total-key / data-envelope / project-adapter / not-applicable / missing
    evidence: backendApiReadiness.apis[].responseHandlingEvidence / API contract source / missing
    rule: non-DataSet service action uses hzero-get-response by baseline; DataSet read remains dataset-native unless documented otherwise
  nativeHttp:
    allowed: yes / no / not-applicable
    confirmationSource: requirement-doc / user-question / not-applicable / missing
    reason: external-system / binary-stream / special-cors / third-party-sdk / other / not-applicable
  status: confirmed / partial / generatedCandidate / missing / conflict / not-applicable
```

缺少 `serviceRequestContract` 时，前端可调用契约不得标为 `confirmed`，production-ready 不得通过。仅缺 request helper 符号/导入路径但目标为 HZEROJS / hzero-front 标准工程且无冲突证据时，不得阻塞或提问，应使用 baseline `request from 'utils/request'` 并把证据写为 `HZERO baseline + no-conflict scan`。

仅缺 `getResponse` 标准 import 或其基础通知行为时，目标为 HZEROJS / hzero-front 标准工程且无冲突证据时，同样不得阻塞或提问；直接写 `responseHandlingContract.mode=hzero-get-response`。DataSet read 的实际 data envelope、`dataKey/totalKey` 或项目 adapter 不属于该自动闭合范围，必须由逐 API response handling evidence 确认。

## Runtime Handoff

Task、Implementation、Review、Verification 和 mock-to-production replacement 必须继承 serviceRequestContract；运行期 request helper、baseUrlStrategy 和 servicePrefix 检查集中在 `front-hzero-enterprise-process-control` 的 data-service runtime gates。

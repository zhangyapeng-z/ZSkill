# HZERO Core Utils 证据

## 来源边界
本资产基于 HZERO front core `src/utils/utils` 目录的工具形态沉淀。目标项目中是否可直接导入，必须由 `tsconfig.json` 的 `compilerOptions.paths`、实际文件存在和 export 共同确认；不要只凭本资产编造 import。

常见 alias：
- `utils/utils`：聚合导出用户、文件、分页、token、common、time、url、routers、collections、system、momentHelp、promise、aes 等工具。
- `utils/iocUtils`：`getEnvConfig`、`getDvaApp` 等 IOC / 环境配置工具候选。

业务代码中需要读取运行时环境变量时，优先使用：

```ts
import { getEnvConfig } from 'utils/iocUtils';

const { API_HOST } = getEnvConfig();
```

如果目标项目存在更细粒度的 env key，也可以使用 `getEnvConfig('<CONFIRMED_KEY>')`，但 key 必须来自项目配置、部署值、现有源码、平台 handoff 或明确文档。

生产 service 请求默认使用目标工程 HZERO/project request helper。当前 HZERO request helper 默认视为已内置 `API_HOST` 拼接；业务 service 通常拼已确认服务前缀（例如 `HZERO_PLATFORM` 或业务服务 key）和 API path，不要再手动拼 `${API_HOST}`，除非项目现有 request 封装证据证明必须显式拼接。

## 常见工具分组

| 分组 | 常见 export | 适用场景 | 边界 |
| --- | --- | --- | --- |
| env / IOC | `getEnvConfig` | 读取 `API_HOST`、`HZERO_FILE`、`ACCESS_TOKEN_NAME`、`configureParams` 等运行时环境配置 | import 固定从 `utils/iocUtils`；env key 不得编造 |
| token | `getAccessToken`、`setAccessToken`、`removeAccessToken`、`getRefreshToken`、`setTokenExpires`、`extractAccessTokenFromHash`、`extractRefreshTokenFromHash`、`extractErrorInfomationFromSearch` | 文件下载、外部系统跳转、请求 header/token 适配、登录回跳参数解析 | 只用于已确认 token 策略；真实 token key 可能来自 `ACCESS_TOKEN_NAME`，不要在页面里自造 token key |
| storage | `setSession`、`getSession`、`setLocal`、`getLocal`、`useSessionStorageState`、`removeAllCookie` | 运行态偏好、临时状态、会话缓存 | 不存放未确认的敏感业务数据；SSR/无 window 环境需降级 |
| file | `getAttachmentUrl`、`_getAttachmentUrl` | 基于文件服务、bucket、directory、storageCode 生成附件下载/预览 URL | bucket、directory、storageCode、redirectDownload 和租户级路径必须来自附件协议；会拼接 access token 和 `H-Request-Id` |
| user / tenant | `getCurrentUser`、`getCurrentTenant`、`getCurrentOrganizationId`、`isTenantRoleLevel`、`getCurrentRole`、`getCurrentLanguage`、`getMenuId` | 租户路径、角色级别、语言、菜单上下文 | 依赖全局 dva store；本地 mock/未登录环境可能返回空对象或报缺用户上下文 |
| route | `gotoPage`、`getRoutes`、`getMicroModuleInfoList`、`getMicroModuleInfo`、`isSpecialRouter` | 页面跳转、子模块存在性判断、特殊路由识别 | 不能替代 route/menu 配置确认；openTab/Tab 行为仍按路由资产确认 |
| common response | `filterNullValueObject`、`getRequestId`、`getResponse`、`listenDownloadError` | 清理查询参数、生成请求 ID、统一失败响应、监听下载错误 | `getResponse` 是 HZERO service action 默认响应处理并会触发通知；逐接口 body/page 映射必须来自 backend readiness/API 契约 |
| request params | `parseParameter`、`parseParameters`、`generateUrlWithGetParam`、`getUrlParam` | 普通 Table 查询参数、排序、分页和 URL 参数拼接 | `parseParameter(s)` 会把页码转成从 0 开始，排序 `ascend/descend` 转 `asc/desc`；不要用于 DataSet 已处理分页的场景 |
| pagination | `createPagination`、`addItemToPagination`、`delItemToPagination`、`addItemsToPagination`、`delItemsToPagination` | HZERO 普通 Table 分页和本地增删行后分页修正 | Choerodon DataSet 分页优先走 DataSet/transport；不要混用两套分页状态 |
| table/edit | `tableScrollWidth`、`getEditTableForm`、`getEditTableData` | 普通 Table 横向滚动宽度、行内编辑表格校验取数 | Choerodon Pro Table 不默认套用普通 HZERO edit-table helper |
| time | `getDateFormat`、`getDateTimeFormat`、`getTimeFormat`、`getTimeZone`、`getCurrentTimeZoneDate` | 按当前用户设置格式化日期、时间、时区 | 依赖当前用户信息；未加载用户时要有兜底 |
| url | `isUrl`、`generateUrlWithGetParam`、`getUrlParam` | 外部链接判断、拼接 GET 参数 | 参数仍需过滤和编码；安全跳转需确认来源和 token/origin 策略 |
| system | `getSystemName` | 根据 `hzero-boot` 配置和语言获取系统名 | 依赖 `getConfig('systemNameConfig')`；不能编造系统名配置 |
| tree / collections | `mapTree`、`getPlainNode` | 树结构转化、路由树拍平 | children 字段名、parent 语义和 `exact` 规则需与目标项目路由/树结构一致 |
| promise wait | `waitUserInfoLoad`、`waitMenuDataLoad`、`dataObsMap` | 等待用户信息或菜单数据加载完成后再执行依赖逻辑 | 不要用轮询/超时替代已存在 wait 工具；缺少导出时回到项目证据 |
| crypto | `encryptPwd`、`RSAUtil`、`decryptedSignedData`、`AESEncrypt`、`MD5Encrypt`、`publicKeyProps` | 密码或后端明确要求的字段加密、SQL 加密字段 transform | 只能用于已有加密契约；publicKey/secretKey/aesOptions/fields 必须来自后端/平台契约，不能自行设计加密方案 |

## 使用规则
- 先确认 alias 和 export：读取目标项目 `tsconfig.json` / `paths`，再确认目标文件实际导出。
- HZERO 页面/service/runtime 代码读取运行时 env 时，不硬编码 `API_HOST`、`BASE_PATH`、public URL，也不随意用 `process.env` 或 `window` 变量绕过 `getEnvConfig`。
- 生产 service 默认不直接使用原生 `axios`、`fetch` 或 `XMLHttpRequest`；只有需求文档或用户确认明确要求原生 HTTP 时才可使用，并需说明 token/header/error/API_HOST/tenant 处理策略。目标项目既有原生 HTTP 代码只能作为实现参考，不能单独授权。
- 不新建 `getRequestBase()`、`buildRequestBase()`、`resolveRequestBase()`、`getApiBase()`、`getBaseUrl()` 等本地 base URL resolver 来替代 HZERO request、`getEnvConfig` 和项目 helper。
- 附件下载/预览优先复用 `getAttachmentUrl` 类工具；但 `bucketName`、`bucketDirectory`、`storageCode`、租户级/平台级路径和 `redirectDownload` 必须由附件协议确认。`getAttachmentUrl` 会基于 `HZERO_FILE`、当前 token、租户角色级别和 `H-Request-Id` 拼接 URL；未登录或 mock 环境不能宣称下载生产可用。
- 租户路径优先使用 `getCurrentOrganizationId` / `isTenantRoleLevel` 等既有工具；不要手写当前用户 store 路径或硬编码 tenantId。hzero-front 中 `getCurrentOrganizationId()` 实际返回当前租户 `getCurrentTenant().tenantId`；`getUserOrganizationId()` / `currentUser.organizationId` 是用户所属租户，不随当前租户切换变化，不能默认用于租户级 API path variable。
- 项目等价租户 helper 必须是目标工程或 HZERO 已存在的导出符号，并有 import path、symbol、文件行号证据；不要在业务页面或 service 中新建 `getOrganizationId()`、`getTenantId()`、`resolveOrganizationId()`、`resolveTenantId()` 来包装默认值。
- `DEFAULT_ORGANIZATION_ID`、`DEFAULT_TENANT_ID`、`MOCK_ORGANIZATION_ID`、`MOCK_TENANT_ID`、env/config 默认租户值不能作为 production transport 的租户级 path variable。
- 平台版本 API 路径优先使用 `getPlatformVersionApi(api)` 或项目已有 helper；它会在租户级角色下拼接当前租户 ID，不能手写 `/v1/${tenantId}` 后再叠加该 helper。
- 普通 HZERO Table 可复用 `createPagination` 和本地增删分页 helper；Choerodon DataSet 页面不要同时维护 HZERO pagination 与 DataSet pagination。
- 查询参数清理可复用 `filterNullValueObject`；避免把空字符串、null、undefined 和空数组传给后端或 mock 请求。
- 普通 HZERO Table 的查询参数可参考 `parseParameter(s)`：`page.current` 会转为 `page=current-1`，`page.pageSize` 转 `size`，排序转为 `field,asc|desc`；Choerodon DataSet transport 已处理分页时不要重复 parse。
- 标准 HZERO 无冲突路径中，非 DataSet 的 service action 默认使用 `getResponse`；不把其 import、通知副作用或基础成功/失败流程作为用户确认项。逐接口 body/page 映射仍必须由 `backendApiReadiness.apis[].responseHandling`、`responseShape` 和 `responseHandlingEvidence` 闭合，不能凭 `getResponse` 的存在推断业务响应字段。
- Choerodon DataSet 的 read/transport 默认保持 DataSet-native 响应消费；只有接口契约要求 `dataKey/totalKey` 或项目 adapter 时才配置相应映射，不得为了统一而把 `getResponse` 套到所有列表请求。
- 路由跳转可参考 `gotoPage`，但菜单路由、Tab/openTab、direct URL 和子模块加载规则仍由 HZERO route 资产确认。
- 行内编辑普通 Table 可使用 `getEditTableData` 做表单校验和取数；它依赖记录上的 `$form`、`_status` 和 children 结构。Choerodon Pro Table / DataSet 行编辑不默认使用该 helper。
- 日期/时间格式应优先消费 `getDateFormat`、`getDateTimeFormat`、`getTimeFormat` 和 `getTimeZone`；不要把默认格式硬编码进业务列和表单，除非目标项目已有固定规范。
- 需要等待用户或菜单加载完成的逻辑，应优先查找 `waitUserInfoLoad`、`waitMenuDataLoad` 或项目等价机制；不得在组件中随意写无限轮询。
- 字段加密、密码加密或 `publicKeyProps.transformRequest` 只能在后端契约明确要求时使用；加密字段、是否 RSA、签名 nonce/timestamp/signature 规则必须由接口契约确认。

## 禁止项
- 未确认 alias/export 就写 `import { xxx } from 'utils/utils'`。
- 把 core utils 中的内部相对路径，如 `../iocUtils`，复制到业务页面 import；业务侧应使用项目 alias，如 `utils/iocUtils`。
- HZERO request 已处理 API_HOST 时仍手动拼 `${API_HOST}`，或用本地 base resolver 只替换 `{organizationId}`、`{tenantId}`、`{id}`、`{code}`、`:id`、`${id}` 等路径占位符后声称生产请求已闭合。
- 未经显式确认在 production service 中直接使用 `axios/fetch/XMLHttpRequest`。
- 用 core utils 的存在证明业务契约存在，例如 bucket、templateCode、permission code、接口 URL、菜单 path 或字段 shape。
- 在本地 mock/demo 中把 `getCurrentUser`、`getAccessToken` 等真实登录态工具当作必然可用；未登录试点环境要说明限制或降级。
- 在 Choerodon DataSet 页面里同时使用 DataSet 分页和 `createPagination` / `parseParameters` 双重分页。
- 在页面组件内直接写 `localStorage` token key、`window.dvaApp._store` 用户路径或 `window._access_token`；应使用项目工具并说明运行态依赖。
- 未确认 publicKey/secretKey/加密字段就接入 `encryptPwd`、`RSAUtil`、`decryptedSignedData` 或 `publicKeyProps`。

# HZERO Runtime Core Utils

## Environment / IOC
HZERO front core 中常见 `getEnvConfig` 工具用于读取运行时环境配置。业务代码 import 使用项目 alias：

```ts
import { getEnvConfig } from 'utils/iocUtils';

const { API_HOST } = getEnvConfig();
```

规则：
- 使用前确认目标项目 `utils/iocUtils` alias、文件和 export 存在。
- 运行时代码读取 `API_HOST`、`BASE_PATH`、public URL、网关地址、`ACCESS_TOKEN_NAME`、`HZERO_FILE`、`configureParams` 等配置时优先使用 `getEnvConfig()` 或项目确认的单 key API。
- HZERO request helper 默认视为已内置 `API_HOST` 拼接；业务 service 默认不要手动拼 `API_HOST`，除非项目 request 封装或相邻 service 证据证明必须显式拼接。
- env key 必须来自项目配置、部署 values、现有源码、平台 handoff 或明确文档；不得编造。
- 不要硬编码环境值，也不要用未确认的 `process.env` 或 `window` 变量绕过项目 env 读取方式。
- 区分 build-time placeholder 和 runtime env；业务运行时代码不要把构建占位当作 confirmed runtime value。
- 文件下载/预览 URL 需要 `HZERO_FILE`、`configureParams.uploadRedirectDownload`、token、租户路径和 `H-Request-Id` 时，优先复用 `getAttachmentUrl` / `_getAttachmentUrl`，不要手拼文件服务 URL。

## Token / User Context
core utils 中常见 token 和用户上下文工具包括 `getAccessToken`、`setAccessToken`、`removeAccessToken`、`getRefreshToken`、`setTokenExpires`、`getCurrentUser`、`getCurrentOrganizationId`、`getPlatformVersionApi`、`isTenantRoleLevel`。

规则：
- token、租户、角色、语言、菜单上下文依赖全局运行时和 dva store；未登录、本地 mock 或页面局部试点环境可能不可用。
- 全局 request/header、外部系统跳转、文件下载等场景使用这些工具前，必须确认目标项目 token/origin/tenant 策略。
- 不要在页面里自造 token key、tenantId 或 store 路径；优先复用项目工具并说明不可用时的降级边界。
- 不要在 production service 中新建本地 request base resolver 或未经确认改用原生 `axios/fetch/XMLHttpRequest` 绕过项目 request helper。
- `getAccessToken` 可能从 URL query/hash 或 `ACCESS_TOKEN_NAME` 指定的 localStorage key 读取 token；不要硬编码 `access_token` 或 HZERO 内部 token key。
- `getPlatformVersionApi(api)` 会按租户角色决定是否拼当前租户 ID；不要先手写租户前缀再调用该 helper。
- 运行态读取 `window.dvaApp._store` 的工具只能在 HZERO 应用上下文中使用；独立 storybook、单测、local mock 页面需要 fallback 或标记不可用。

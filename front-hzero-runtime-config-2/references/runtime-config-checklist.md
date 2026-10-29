# 运行时配置检查清单

## 判断顺序
先整理 `RuntimeConfigPacket`：配置入口、作用域、runtime export 是否确认、项目版本证据、扩展点可用性、跨模块污染风险和验证方式。

1. 判断需求属于构建期配置、运行时配置、全局 request/response 适配、跨系统导航 hook 还是普通页面业务逻辑。
2. 判断作用域是父工程全局、子模块局部还是单页面局部。
3. 判断配置入口：`app.tsx`、`routes-config.tsx`、`config/`、局部 wrapper。
4. 判断是否有全局污染风险、请求副作用或跨系统导航副作用。

## 检查点
- 全局初始化是否更适合 `appInit`，且目标项目 runtime valid keys 是否已确认支持。
- layout/header/extra 等扩展是否走正式扩展点。
- Choerodon 配置是否需要局部 `ConfigProvider` 而不是全局 `configure`。
- 子模块配置是否需要 `extendParentConfig`，以及当前文件是否允许使用该能力。
- 普通页面业务逻辑是否误放进运行时入口。
- 全局 request/response 拦截是否只处理认证、租户、统一错误、通用响应处理等跨切面逻辑。
- token、origin、租户、语言、退出和 session 过期策略是否有项目契约。
- HZERO 页面、service、runtime、request、集成或导航代码读取运行时环境变量时，是否使用 `import { getEnvConfig } from 'utils/iocUtils';`，并且 env key 已从项目配置、部署值、现有代码或 handoff 确认。

## 场景化判断
### 项目级初始化
- 登录态、租户、全局字典、运行时基础能力等跨切面初始化优先考虑项目级初始化入口。
- 项目级初始化入口必须来自目标项目已确认 runtime export；未确认 `appInit` 支持时，不输出可运行 `appInit` 代码。
- 单页面查询、表单默认值或按钮逻辑不应放进项目级初始化。
- 初始化依赖的接口、缓存和失败策略不明确时列为待确认。

### 路由配置与页面注册
- 静态路由、覆盖路由、标题和权限相关配置优先放在路由配置体系中。
- 路由覆盖需要确认优先级、菜单路径和子模块加载关系。
- 不用临时路径或 `authorized: true` 掩盖路由/权限错误。

### 子模块配置继承
- 子模块配置按需使用 `extendParentConfig`，但不要在 `config/config.${UMI_ENV}.ts` 中使用，避免循环引用。
- 使用前必须确认项目 HZEROJS 版本、配置文件位置和已有配置继承方式。
- 如果只是页面局部诉求，不应通过配置继承扩大影响范围。

### Layout / Header / Float 扩展
- 全局 header、layout extra、悬浮组件优先使用已确认扩展点。
- 扩展内容应保持跨页面独立，不依赖某个业务页面的渲染顺序。
- 是否仅在部分模块或部分角色出现，需要先确认作用域与权限。

### Choerodon UI 配置
- 父工程全局一致的配置才考虑全局配置。
- 子模块或页面局部诉求优先考虑局部 wrapper 或 `ConfigProvider`。
- 配置是否影响其他模块、弹窗、表单或表格交互需要列为风险。

### 普通页面业务逻辑
- 页面查询初始化、表单联动、按钮状态和局部数据加载应留在页面、service/model 或 DataSet 中。
- 不把单页面协议写进全局 request、runtime hook 或 layout wrapper。
- 如果需求只是局部改动，优先给出局部实现边界。

### Request / Header 全局适配
- 全局拦截器只处理已确认的跨切面逻辑，如认证、租户、统一错误和通用响应处理。
- 单页面接口协议差异应放在 service/model/DataSet transport 或页面局部 adapter。
- 请求头、token、租户字段、响应结构和影响模块不明确时列为待确认。
- 不把单页面业务协议写成全局副作用。

### 环境变量读取
- 运行时代码需要 `API_HOST`、`BASE_PATH`、public URL、网关地址或部署期 host 等环境变量时，优先使用 `getEnvConfig`。
- 固定 import：`import { getEnvConfig } from 'utils/iocUtils';`。
- HZERO request helper 默认视为已内置 `API_HOST` 拼接；业务 service 默认不手动拼 `API_HOST`，除非项目 request 封装或相邻 service 证据证明必须显式拼接。
- env key 必须来自目标项目 `config/`、部署 values、现有源码、平台 handoff 或明确文档；缺少证据时列为待确认，不要编造。
- 不要在 HZERO 页面/service/runtime 代码里硬编码环境值，或随意用 `process.env.<KEY>`、`window.<KEY>` 替代项目 env 读取方式。
- 区分 build-time placeholder 和 runtime env。构建配置可以保留部署占位，业务运行时代码读取已确认 runtime env 时使用 `getEnvConfig`。
- dev 静态 mock JSON 通常使用当前 dev server origin；不要为了 mock 静态资源默认读取 `getEnvConfig('API_HOST')`，除非项目已有静态资源 host 约定。

### 跨系统导航 Hook
- 先确认项目是否支持 route hook、openTab helper、menu data helper 或自定义 navigation wrapper。
- 只有跨页面或平台级需求才考虑全局导航 hook；单页面跳转优先放在页面/路由层。
- title、route path、query/state、tab 唯一性、token/origin 和 session 过期行为不明确时列为待确认。

## 常见风险
- 把普通页面逻辑放进 `app.tsx`。
- 风险：未确认 runtime valid keys 时默认输出 `export async function appInit()`。
- 子模块随意调用全局 `configure`。
- 把 HZERO 配置写到 `.umirc`。
- 在 `config/config.${UMI_ENV}.ts` 中使用 `extendParentConfig` 导致循环引用。
- 在 `innerLayoutWrapper` 中写依赖执行顺序的业务逻辑。
- 将构建期配置、运行时配置和页面逻辑混在一起。
- 用全局拦截器处理单页面特殊协议。
- 未确认 token/origin 策略就输出跨系统导航或 request/header 适配代码。
- 硬编码 `API_HOST` / `BASE_PATH` / public URL，或用未确认的 `process.env` / `window` 变量绕过 `getEnvConfig`。
- 编造 env key，或把 build-time placeholder 当作 runtime confirmed value。

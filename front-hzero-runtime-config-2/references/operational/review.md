# 运行时配置 - 审查与反模式

## 阅读路由
- 运行时配置 Review、自查、反模式、finding 或合规判断时读取。

## 反模式
- 把 HZEROJS 配置写到 `.umirc`。
- 默认输出 `export async function appInit()` 作为可运行答案。
- 把普通页面业务逻辑放进 `app.tsx`。
- 把单页面接口适配放进全局 request/response 拦截器。
- 未确认 token/origin、租户、语言或退出策略时输出跨系统导航或请求适配代码。
- 子模块随意调用全局 `configure`。
- 在 `innerLayoutWrapper` 中写依赖执行顺序的逻辑。

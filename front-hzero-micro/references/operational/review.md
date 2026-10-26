# 微前端 - 审查与反模式

## 阅读路由
- 微前端 Review、自查、反模式、finding 或合规判断时读取。

## 反模式
- 默认用 `\\/.*` 让子模块首屏加载。
- 未确认构建产物就判断组件不存在。
- 用直接 import/require 替代已确认的 `MfComponent` 或 `getComponent` 机制。
- 用 iframe 或 qiankun 承载可通过 HZERO federation 共享的内部组件。
- 未区分外部独立应用、qiankun 微应用和 HZERO 子模块。
- 编造远程包地址或 exposed code。
- 将 `PACKAGE_PUBLIC_URL`、构建产物目录、`microConfig` 地址、`window.mfRemotes` 地址、`registerRegex` 和远程访问路径混为同一个事实。

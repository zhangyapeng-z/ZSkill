# HZERO 微前端证据包 Schema

## 证据包使用边界
本文件只保留远程加载和跨模块组件排查所需的证据结构，用于约束输出中的已确认项、待确认项和验证边界。

## MicroFrontendPacket
用于 remoteEntry、chunkError、子模块白屏、跨模块组件和运行时远程加载问题。

必查字段：
- `PACKAGE_PUBLIC_URL`：静态资源根路径来源。
- `packages/microConfig.json`：远程元数据文件是否存在、是否含目标包。
- `window.mfRemotes`：运行时远程地址是否包含目标包。
- remoteEntry URL：实际访问 URL，必须来自 microConfig、mfRemotes、部署说明或 Network 失败请求。
- 构建产物路径：目标包构建输出中是否存在 `remoteEntry.js` 和页面 chunk。
- 远程访问路径：目标环境可访问路径和静态资源服务路径。
- Network 失败请求：浏览器 Network 中失败的真实 URL 和状态。
- exposes/消费 API：跨模块组件的 exposed key 和加载方式是否已确认。

输出要求：
- `PACKAGE_PUBLIC_URL`、构建产物路径、microConfig、`window.mfRemotes`、remoteEntry URL、远程访问路径和 Network 失败请求必须分别确认，不得相互推导。
- 不依据包名、路由名、菜单名或环境名编造远程地址。

## RouteAccessPacket 交界
如果白屏或 remoteEntry 问题由菜单点击触发，还应补齐：
- 实际 URL、route path、menu path。
- 子模块注册、registerRegex、父子模块加载状态。
- permission/menu 是否已确认。

# 微前端排查检查清单

## 排查顺序
先整理 `MicroFrontendPacket`：`PACKAGE_PUBLIC_URL`、`packages/microConfig.json`、`window.mfRemotes`、remoteEntry URL、构建产物路径、远程访问路径、Network 失败请求、exposes/消费 API。每一项都应标注已确认或待确认。

1. 判断问题属于 public url、构建产物路径、远程元数据、运行时 `mfRemotes`、远程访问路径、路由匹配、qiankun 外部微应用还是运行时加载。
2. 检查 `PACKAGE_PUBLIC_URL` 是否能定位 `packages/microConfig.json`。
3. 检查 `window.mfRemotes` 是否包含目标包。
4. 检查 `remoteEntry.js` 的实际访问 URL 是否来自已确认来源，并确认是否可访问。
5. 检查 `mfExposes` 是否暴露了目标组件。
6. 检查 `registerRegex` 是否匹配路由前缀且优先级正确。

## 检查点
- 父模块 / 子模块 / 远程依赖包边界是否明确。
- 远程元数据与构建产物是否一致。
- `PACKAGE_PUBLIC_URL`、构建产物路径、`microConfig`、`window.mfRemotes`、远程访问路径是否分别有证据确认。
- route prefix 和 `registerRegex` 是否一致。
- 暴露组件是否通过正式微前端机制共享。
- qiankun、iframe、HZERO federation 子模块是否已区分清楚。

## 场景化排查
### remoteEntry 404
- 先确认 `PACKAGE_PUBLIC_URL` 指向的静态资源根路径是否能访问。
- 再确认 `packages/microConfig.json` 中目标包信息是否存在且路径与部署产物一致。
- 检查目标包构建产物中是否存在 `remoteEntry.js`。
- 对比构建产物路径、远程访问路径、`microConfig` 地址、`window.mfRemotes` 地址和 Network 失败请求，缺一项就列为待确认。
- 结论按 `MicroFrontendPacket` 分层输出，避免把 public url、远程访问路径和 runtime remotes 混成同一个事实。
- 不直接猜测远程地址、部署目录、Nginx 路径或 CDN 规则。

### 子模块路由白屏
- 先区分是子模块未注册、remoteEntry 未加载、路由未匹配还是运行时报错。
- 检查目标路由前缀是否命中有效 `registerRegex`。
- 检查父工程是否能在运行时拿到目标包的 remote 信息。
- 如果只有特定菜单白屏，还需要联动路由和菜单权限排查。

### registerRegex 过宽或过窄
- 优先收敛到明确业务路由前缀，不默认使用宽泛 `\/.*`。
- 只有首屏必须加载或有未迁移 legacy 依赖时，才说明可能需要宽泛加载。
- 检查 `microServices.registerRegex`、`packages.registerRegex`、`microConfig.registerRegex` 之间是否存在覆盖关系；有效优先级需要以项目源码和运行时配置确认为准。
- 变更后需要验证首屏加载包数量和目标页面命中情况。

### 跨模块组件共享
- 先确认目标能力是否通过 `mfExposes` 暴露。
- 页面消费优先使用已确认的联邦组件加载机制。
- 暴露组件的包名、exposed key 和入参协议不明确时列为待确认。
- 不用直接 import 替代微前端共享机制。

### qiankun 外部微应用
- 先确认是否是真正独立应用接入，而不是 HZERO federation 子模块或内部共享组件。
- 明确生命周期、路由前缀、样式隔离、鉴权、远程访问路径和父子应用通信协议。
- 父子应用通信协议不明确时列为待确认，不编造 message type、payload 或 token 传递。
- 不把 qiankun 与 HZERO module federation 机制混成同一方案。

### 部署后可访问但运行时报错
- 检查远程包版本、依赖共享和运行时环境是否与父工程匹配。
- 区分资源 404、chunk 加载失败和组件执行异常。
- 需要结合浏览器 Console、Network 和构建产物确认，不凭症状下结论。

## 常见风险
- 默认用 `\/.*` 让子模块首屏加载。
- 未确认构建产物就判断组件不存在。
- 编造远程包地址或 exposed code。
- 依据包名、路由名、菜单名或环境名推导 `remoteEntry.js` 地址。
- 混淆 public url、构建产物路径、`microConfig`、`mfRemotes`、`registerRegex` 和远程访问路径。
- 把菜单权限、路由 404 和微前端加载失败混为一类。
- 未验证运行时 `window.mfRemotes` 就修改构建配置。
- 用 qiankun 或 iframe 承载可通过 HZERO federation 共享的内部组件。
- 未区分外部独立应用、qiankun 微应用和 HZERO 子模块。

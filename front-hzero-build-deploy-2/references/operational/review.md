# 构建与产物加载 - 审查与反模式

## 阅读路由
- 构建与产物加载 Review、自查、反模式、finding 或合规判断时读取。

## 反模式
- 不确认项目脚本就直接要求运行某个 yarn 命令。
- HZEROJS Umi 子模块最终编译未使用唯一命令 `npm run build:ms -- <module>`，改成 yarn、pnpm、其它 build 命令，或省略 `-- <module>`。
- 路由或微前端元数据变更后，只依赖 HMR 或普通刷新，不重建子模块、不刷新 microConfig、缺外部 dev server restart / hard reload 证据就声明运行态已生效。
- 把所有 chunkError 都归因于前端代码错误，而不检查 public URL 和远程产物。
- 未确认远程访问路径就编造 `PACKAGE_PUBLIC_URL`。
- 混淆 public url、构建产物路径、`microConfig`、`mfRemotes`、Network 失败请求和远程访问路径。
- 依据包名、路由名、菜单名或环境名推导 `remoteEntry.js` 地址。
- 忽略增量构建依赖 git 变更记录这一前提。

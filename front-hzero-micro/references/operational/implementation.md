# 微前端 - 实现与工程证据

## 阅读路由
- 微前端 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## 本地资源
按需查本目录资源；不要外显内部路径。
- 远程加载、白屏、remoteEntry、chunkError 和跨模块组件排查：优先使用 `references/schema-packets.md` 中的 `MicroFrontendPacket`。
- 微前端加载链路检查清单：`references/micro-frontend-checklist.md`。
- remoteEntry、chunk、registerRegex、mfExposes 和跨模块组件模式：`references/patterns.md`。
- 需要稳定诊断输出时使用模板：`templates/micro-diagnosis.md`。

## 工作流程
1. 识别问题属于 public url、构建产物路径、远程元数据、运行时 `mfRemotes`、route prefix 匹配、远程访问路径、qiankun 外部微应用，还是暴露组件加载。
2. 检查 `PACKAGE_PUBLIC_URL` 是否能定位 `packages/microConfig.json`。
3. 检查运行时 `window.mfRemotes` 是否包含目标包。
4. 检查目标包`构建产物`是否存在 `remoteEntry.js`，并确认`远程访问路径`与产物路径一致。
5. 检查 `registerRegex` 是否过宽、过窄或优先级被覆盖。
6. 涉及 qiankun 时，先确认是否是真正独立应用接入；不要把 qiankun 与 HZERO module federation 子模块混成同一方案。
7. remoteEntry、chunkError、子模块白屏、qiankun 或跨模块组件问题按 `MicroFrontendPacket` 输出分层证据；如果由菜单访问触发，同时补 route/menu/registerRegex 交界信息。
8. 输出排查清单和最小配置建议；remoteEntry/chunk 白屏或加载失败必须原样包含 `PACKAGE_PUBLIC_URL`、`microConfig`、`packages/microConfig.json`、`window.mfRemotes`、`remoteEntry`、`构建产物`、`远程访问路径`。

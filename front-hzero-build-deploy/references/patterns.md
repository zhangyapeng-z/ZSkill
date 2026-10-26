# HZERO 构建与部署模式

## 适用范围
本参考用于 HZERO 前端构建/启动诊断、构建阶段识别、子模块或微包编译问题、微包产物、增量构建以及远程模块加载问题。

在目标项目的 package scripts 或 HZERO tooling 确认前，不要假定某个命令一定存在。这里的命令都应视为待验证候选，而不是通用事实。

输出前先形成 `BuildStagePacket`：阶段分类、包管理器和执行目录、scripts/tooling、目标模块/包名、构建参数/环境变量、产物路径和验证结论。remoteEntry 或 chunkError 还需补齐 `MicroFrontendPacket` 的 public URL、microConfig、mfRemotes、remoteEntry URL、远程访问路径和 Network 失败请求。

## 候选 HZERO 信息命令
常见 HZERO tooling 可能支持：

```bash
npx umi hzero-info
npx umi hzero-info --show-micro-packages
```

只有在确认项目使用兼容的 umi/HZERO tooling 后，才用它们检查项目 HZERO 元数据和微包列表。

## 候选构建命令
常见 HZERO tooling 可能支持：

```bash
npx umi hzero-build --only-build-parent
npx umi hzero-build --only-build-micro
npx umi hzero-build --only-build-micro --all-packages
```

在推荐或执行前，应先确认 scripts、环境变量、包管理器和 CI 约定。

对于通用子模块或微包编译请求，先确认目标包名、workspace/包管理器、执行目录、可用 scripts，以及项目是支持单包编译还是只支持全部微包一起编译。HZEROJS Umi 子模块最终编译不进入包管理器或其它 build 命令选择，直接适用下方固定命令。

HZEROJS Umi 子模块交付验收的唯一最终编译命令为：

```bash
npm run build:ms -- <module>
```

适用前提：目标是 HZEROJS Umi 子模块，执行目录为父工程/根工程。`--` 是 npm 参数分隔符，必须保留，用于把 `<module>` 传入 `build:ms` 脚本；`<module>` 写当前处理的子模块名，不带 `packages/`。该命令不根据 yarn、pnpm、lockfile、README、CI、`packageManager` 或用户环境改写。目标子模块名未明确时停止并补目标信息；根 `package.json` 缺少 `build:ms` script 时记录 `missing-required-build-ms-script` 并回工程接线补齐，不得选择替代命令。hzero-cli 或非 Umi 子模块不适用本固定命令，按各自项目证据处理。

如果根级 `hzero-build` 进入交互式模块选择，不要直接记为构建失败。先查项目脚本是否已提供非交互封装，例如 `build:all`、`build:ms-all`、`--all-packages`。验证自动化场景优先使用这些非交互命令。

## Workspace 微包链接模式
新建 HZERO 子模块/微包时，先确认项目 scripts、resolver 或相邻模块是否要求根 `package.json` 的 `workspace:*` 依赖；有工程证据时再同步补齐。不能仅因创建了 `packages/<pkg>`、workspace 配置和 `config/packages-config.*` 就默认新增根依赖。

当 HZERO 构建日志出现 `Cannot find module '<pkg>/package.json'`、`require.resolve('<pkg>/package.json')` 失败或类似微包名解析错误时，先将其归类为 workspace / 依赖链接候选问题，而不是直接归因为业务代码。优先核对可用证据：
- `packages/*` 或等价 workspace 配置是否包含目标包
- 项目 scripts 或 resolver 是否要求根 `package.json` 声明目标微包的 `workspace:*` 依赖
- 依赖已安装时，`node_modules/<pkg>` 是否已生成 link
- lockfile 或 `.pnpm-workspace-state.json` 是否提供适用的 workspace / link 状态证据

确认是安装或 link 问题后，仅在独立构建诊断或用户明确允许修复依赖环境时，才按项目约定补根依赖、重新安装或刷新 lockfile / link；普通 Verification 只记录 `blocked-by-missing-dependencies` 和用户手工补跑步骤。若 `build:ms -- <module>` 已经通过，但后续单独 `require.resolve('<module>/package.json')` 失败，应保留构建通过事实，把它记录为 `workspaceResolverStatus=failed-but-build-passed`，优先核对执行目录、package name、项目所需根 `workspace:*` 依赖和 link 状态，而不是生成页面业务代码修复。

## 远程模块部署
当已部署模块加载失败时，按以下顺序检查：
- 已确认的 `PACKAGE_PUBLIC_URL`
- 目标包已确认的构建产物路径
- 已生成的 `packages/microConfig.json`
- micro config 中的目标包入口和远程地址
- 运行时 `window.mfRemotes` 中的目标包地址
- 浏览器 Network 失败 URL 和 Console 报错
- 已部署 `remoteEntry.js` 的访问结果

要区分是资源缺失、public path 错误、micro config 过期、运行时 remotes 过期、远程访问路径不匹配，还是组件运行时错误。不要根据包名、路由名、菜单名或环境名去推断远程 URL。

## 增量构建
常见的增量构建相关概念可能包括：
- `SKIP_NO_CHANGE_MODULE`
- `PARENT_SRC_FILES_REG`
- `PACKAGE_SRC_FILES_REG`
- `BUILD_DIST_PATH`

在诊断前应先确认项目确实使用这些变量。很多场景下，增量构建依赖准确的源码变更检测和 git 历史。

## Dev Server / HMR 边界
- HZERO `dev server` 和 HMR 只是开发便利手段，不能替代 build/compile 验证。
- 修改 `config.ts`、routes、`hzeroMicro`、微包注册、exposes、public path 或其他编译期元数据后，运行态验收需要用户手工重启 dev server 或由独立 runtime acceptance 执行；默认 Verification / 前端流程不自动重启服务，也不要依赖 HMR 让这些变更生效。
- 前端 mock 标准实现若需要接入本地 HTTP mock API，只能通过目标工程既有 HZERO / Webpack / Umi devServer 扩展点注册 middleware。mock middleware 仅限本地开发和 demo 验证，不得为 mock 改造生产构建、微前端注册、`remoteEntry`、`microConfig`、`PACKAGE_PUBLIC_URL`、public path 或部署配置；缺少明确扩展点时应阻塞并补工程证据，不自动改造构建体系。
- 简单页面、文案、样式、mock 数据或本地组件改动，不应自动触发完整子模块 build/compile。优先做针对性验证：lint/typecheck、已确认的本地 scripts，或记录外部 browser/HMR 证据缺口。只有在涉及编译期元数据、routes/config、微前端 entry/exposes、public path、依赖、共享组件或发布/产物信心时，才升级到子模块 build/compile。
- 轻量验证决策表：text/style/static display -> lint/typecheck 或外部 HMR/browser evidence；mock JSON/DataSet query -> 外部 Network + query/refresh evidence；detail/routing -> route params + detail data 静态/外部 evidence；service/helper -> typecheck + affected page 静态检查；routes/config/micro/build metadata -> build/compile candidate + 外部 restart evidence；shared components/dependencies -> typecheck + affected pages，必要时再 build/compile 以获得发布信心。
- 如果热更新报 `hzero-entry.ts`、`_hzero_layout`、`window.hzeroMfCodeExposes` 或 `Object.keys(undefined/null)`，先检查是否是 HZERO 微前端 entry/layout 元数据在 HMR 后暂时缺失。先让用户检查 `window.hzeroMfCodeExposes` 以及 `window.hzeroMfCodeExposes && window.hzeroMfCodeExposes._hzero_layout`，不要先归因到业务页面代码。
- public/static mock JSON 变更可能需要刷新浏览器缓存或重启 dev server，具体取决于 tooling；但除非涉及构建产物或远程加载，否则不应诊断成已部署 remoteEntry 问题。
- 输出必须区分 开发态 和 产物态：dev server 恢复不代表具备交付可用性；当需要交付信心时，仍应建议补做相关 build/compile 检查。

## 输出检查清单
- 已确认的构建阶段：local start、parent build、submodule/micro package compile、artifact deploy、runtime load。
- 已确认的项目 scripts/tooling。
- 已确认的 public URL、artifact path、deployment access path、micro config address、runtime remotes address 以及 Network failed URL。
- 已确认的微包元数据。
- 候选命令必须明确标注为已确认或待确认。

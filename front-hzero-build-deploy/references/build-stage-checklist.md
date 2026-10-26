# 前端构建与产物加载分阶段检查清单

## 阶段分类
先整理 `BuildStagePacket`：阶段分类、包管理器和执行目录、scripts/tooling、目标模块/包名、构建参数/环境变量、产物路径、验证结论。命令和产物证据不足时必须标注待确认。

- 本地开发启动
- 父模块构建
- 子模块/子包编译
- public url
- 构建产物路径
- 远程元数据
- 远程访问
- 运行时 `mfRemotes`
- 运行时加载
- 增量构建

## 检查顺序
1. 先确认项目 scripts 和执行目录。HZEROJS Umi 业务子模块交付验收的唯一编译候选和补跑入口为父工程/根工程执行 `npm run build:ms -- <module>`；`--` 用于把 `<module>` 传给 npm script，不得使用 yarn、pnpm、其它脚本或 build 类等价命令替换。目标模块未明确时停止并补目标信息；根 scripts 缺少 `build:ms` 时记录 `missing-required-build-ms-script` 并回工程接线补齐。只有依赖就绪且本轮验证目标明确要求编译产物、production-ready 或完整验收时才运行；默认 mock/demo 只记录候选和未验证影响。`packages/<module>/package.json` 里的 `transpile` 是发布/转译模板能力，Verification 不得把它当作直接验证入口。
   - 若本轮修改子模块 routes、`config/config.ts`、`registerRegex`、父工程 packages 注册或微前端元数据，确认 `scripts/refreshMicroConfig.js` 或项目等价命令是否存在。依赖就绪且本轮实际运行 `npm run build:ms -- <module>` 时，build 后按项目证据执行或记录 `node scripts/refreshMicroConfig.js`；dev server restart 和 hard reload 只作为外部 runtime acceptance / 用户手工证据状态记录，Verification 或默认前端流程不得自动执行。目标工程依赖未安装时只记录为安装依赖后的补跑链路，不作为当前强制验证要求。
   - 实际运行 `npm run build:ms -- <module>` 后必须检查 `packages/<module>/lib`、`dist`、`.umi`、`.umi-production` 是否残留在业务子模块工作区。`lib/` 只能作为构建/转译副产物处理，不能作为页面源码、DataSet/service 证据、Handoff 资产或提交内容；出现时记录 `artifact-found-cleaned` / `artifact-found-untracked` / `invalid`。
2. 再区分是父模块构建失败、子模块/子包编译失败、产物缺失、路径错误还是运行时加载问题。
3. 新建子模块/微包时先检查前置配置是否完整：`packages/<pkg>/package.json`、workspace 配置、`config/packages-config.*`，以及项目 scripts、resolver 或相邻模块是否要求根 `package.json` 声明该微包的 `workspace:*` 依赖。
4. 若报 `Cannot find module '<pkg>/package.json'`、微包名解析失败或 `require.resolve('<pkg>/package.json')` 失败，先归类为 workspace / 依赖链接候选问题，再核对可用证据：workspace 配置是否包含目标包、项目 scripts 或 resolver 是否要求根 `package.json` 声明该微包 `workspace:*` 依赖、`node_modules/<pkg>` link 是否存在，以及 lockfile 或 `.pnpm-workspace-state.json` 等包管理器状态证据（适用时）。这些证据未闭合前，不得直接归因为业务代码失败。仅在独立构建诊断或用户明确允许修复依赖环境时，才执行项目约定的安装、lockfile 或 workspace link 刷新操作；普通 Verification 只记录 `blocked-by-missing-dependencies` 和用户手工补跑步骤。
5. 根级 `hzero-build` 若出现交互式模块选择，先区分是等待选择还是实际报错；优先查找项目内非交互脚本或参数（如 `build:all`、`--all-packages`）用于验证。
5. 远程加载问题分别检查 `PACKAGE_PUBLIC_URL`、构建产物路径、`packages/microConfig.json`、`window.mfRemotes`、Network 失败请求、`remoteEntry.js` 和远程访问路径。
6. 增量构建问题检查 git 变更记录和相关环境变量。
7. 输出时区分开发态验证和产物态验证；dev server/HMR 不能替代 build/compile。
8. 新增可视页面验收按 `frontend-verification-levels.md` 分级记录；build 未运行时必须声明不能确认产物态可交付，browser 未运行时必须声明不能确认页面可演示。

## 常见风险
- 没确认项目命令就要求运行固定命令。
- HZEROJS Umi 子模块最终编译改用 yarn、pnpm、其它 build 命令，或输出 `npm run build:ms` 但遗漏 `-- <module>`。
- 直接执行包内 `transpile` 或把 `build:ms` 生成的 `packages/<module>/lib/` 当成业务交付源码。
- 把 chunkError 全归因于代码问题。
- 未确认远程访问路径就猜测 `PACKAGE_PUBLIC_URL`。
- 依据包名、路由名、菜单名或环境名推导 `remoteEntry.js` 地址。
- 混淆 public url、构建产物路径、`microConfig`、`mfRemotes`、Network 失败请求和远程访问路径。
- 只跑 lint/typecheck 就把新增页面写成交付可用。
- 修改 routes/config/registerRegex 后只依赖 HMR 或普通刷新，不重建子模块、不刷新 microConfig、缺外部 dev server restart / hard reload 证据，却声明 route 已在运行态生效。

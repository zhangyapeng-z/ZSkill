# 构建与产物加载 - 实现与工程证据

## 阅读路由
- 构建与产物加载 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## 本地资源
按需查本目录资源；不要外显内部路径。
- 构建、启动、产物和交付验收判断：先用 `references/schema-packets.md` 中的 `BuildStagePacket`，远程加载交界再结合 `MicroFrontendPacket`。
- 构建阶段检查清单：`references/build-stage-checklist.md`。
- 前端验证与交付状态分级：`references/frontend-verification-levels.md`。
- 常见构建、增量和 remoteEntry/chunkError 模式：`references/patterns.md`。
- 需要稳定诊断输出时使用模板：`templates/build-diagnosis.md`。

## 工作流程
1. 先判断问题阶段：本地开发服务/HMR、父模块构建、子模块/子包编译、远程元数据、远程访问或运行时加载。
2. 确认项目脚本，不编造命令行为；HZEROJS Umi 子模块交付验收固定以 `npm run build:ms -- <module>` 作为最终编译命令，`--` 用于把当前子模块名传给 npm script，不得使用 yarn、pnpm 或其它 build 命令替换。根 scripts 缺少 `build:ms` 时回工程接线补齐。修改子模块 routes/config/registerRegex/父工程 packages 注册后，还必须确认是否存在 `scripts/refreshMicroConfig.js` 或项目等价命令；确认存在时把 `node scripts/refreshMicroConfig.js` 纳入验证链路。
3. 本地开发类问题检查目标子模块启动脚本、执行目录、端口、父子模块加载关系和 HMR/browser 验证方式。
4. 构建/编译类问题检查 `npx umi hzero-info`、子模块列表、目标包名、执行目录和构建命令参数。
5. 新建 HZERO 子模块/微包时，先确认项目 scripts、resolver 或相邻模块是否要求根 `package.json` 的 `dependencies` 声明对应 `workspace:*` 依赖；有证据时同步补齐，不得仅凭子模块目录存在就默认新增根依赖。
6. 若报 `Cannot find module '<pkg>/package.json'` 或类似模块解析错误，先归类为 workspace / 依赖链接候选问题，核对 workspace 声明、项目 scripts 或 resolver 所需的根 `workspace:*` 依赖、`node_modules/<pkg>` link，以及 lockfile 或 `.pnpm-workspace-state.json` 等适用的包管理器状态证据。证据未闭合前不得先改业务代码。确认是安装/链接问题后，只有独立构建诊断或用户明确允许时才修复安装、lockfile 或 link 状态；普通 Verification 只记录环境前置和手工补跑步骤。
7. 根级 `hzero-build` 若进入交互式模块选择，优先寻找并验证项目内已存在的非交互命令（如 `--all-packages`、`--only-build-micro`、`build:all`）；不能把交互式卡住误判为构建失败。
8. 远程加载类问题分别检查 `PACKAGE_PUBLIC_URL`、构建产物路径、`packages/microConfig.json`、`window.mfRemotes`、`remoteEntry.js` 和远程访问路径。
9. 增量构建类问题检查 `SKIP_NO_CHANGE_MODULE`、`PARENT_SRC_FILES_REG`、`PACKAGE_SRC_FILES_REG`、git 变更记录和 `BUILD_DIST_PATH`。
10. 构建、启动、增量构建或产物态验证按 `BuildStagePacket` 输出阶段、命令证据、产物证据和验证状态。
11. 输出最小排查命令、确认信息和验证方式。

# HZERO 前端构建与产物加载证据包 Schema

## 证据包使用边界
本文件用于约束构建、启动和产物态验证输出。候选命令、产物路径和远程地址必须来自项目证据或明确标注为待确认。

## BuildStagePacket
用于构建、启动、子模块编译、增量构建和产物态验证。

必查字段：
- 阶段分类：本地开发服务/HMR、父模块构建、子模块/微包编译、构建产物、运行时加载或增量构建。
- 包管理器和执行目录：通用构建诊断可来自项目 scripts、lockfile 或用户确认；HZEROJS Umi 子模块最终编译不进入包管理器选择，唯一候选和补跑入口为父工程/根工程执行 `npm run build:ms -- <module>`。目标子模块名未明确时保持 missing；根 scripts 缺少 `build:ms` 时记录 `missing-required-build-ms-script`，不得选择 yarn、pnpm 或其它 build 命令。只有依赖就绪且本轮验证目标明确要求编译产物、production-ready 或完整验收时才运行。
- scripts/tooling：已确认命令和候选命令分开记录。
- tsconfig paths：目标工程或子模块 `compilerOptions.baseUrl`、`paths`、`include`、`exclude` 对类型检查、alias 解析和子模块覆盖范围的影响。
- 目标模块/包名：父工程、子模块、微包或共享包。
- 构建参数/环境变量：如 public path、增量构建变量或 HZERO tooling 参数。
- 产物路径：构建输出目录、`packages/microConfig.json`、`remoteEntry.js`、chunk。
- 验证结论：dev server/HMR、lint/typecheck、build/compile、Network/browser 中哪些已验证，哪些未验证。

输出要求：
- 候选命令必须标注“待确认”或“项目证据不足”，不能写成已确认命令。
- HZEROJS Umi 子模块已确认命令必须且只能为 `npm run build:ms -- <module>`；`--` 是 npm 参数分隔符，不得省略。不得改用 yarn、pnpm、其它脚本或 build 类等价命令；根 scripts 缺少 `build:ms` 时记录缺口并回工程接线补齐。
- dev server/HMR 只能证明开发态可用，不能替代 build/compile 或交付验收判断。
- 根 tsconfig 的 `include` / `exclude` 会影响 tsc 覆盖范围；例如 exclude `packages` 时，不得宣称根 tsc 覆盖子模块，必须读取子模块 tsconfig 或列为未验证。

## MicroFrontendPacket 交界
当构建产物问题表现为 remoteEntry、chunkError 或运行时白屏时，还必须区分：
- `PACKAGE_PUBLIC_URL`、构建产物路径、microConfig、`window.mfRemotes`。
- remoteEntry URL、远程访问路径和 Network 失败请求。
- 资源缺失、public path 错误、远程元数据过期、访问路径不匹配和组件运行时报错。

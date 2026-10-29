# 构建与产物加载 - 设计与契约

## 阅读路由
- 构建与产物加载 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 事实确认契约
- 仅依赖自身说明和本地 `references/` 给出安全流程、硬规则、输出结构和不确定性处理。
- 本地 references 是模式和候选事实，不等同于目标项目契约。
- 输出具体构建命令、环境变量、远程地址或排障结论前，必须先从项目 scripts、配置、实际日志或明确文档确认；确认不了就列为待确认项。
- HZEROJS Umi 子模块的最终编译命令固定输出 `npm run build:ms -- <module>`，不得改成 yarn、pnpm、其它脚本或 build 类等价命令。目标子模块名未明确时保持 missing；根 scripts 缺少 `build:ms` 时记录 `missing-required-build-ms-script` 并回工程接线补齐。路由或微前端元数据变更后，`node scripts/refreshMicroConfig.js` 只有在脚本文件或项目文档确认时才写成已确认命令；否则只能作为候选检查项。
- 本地开发服务命令只能作为用户手工自测或独立 runtime acceptance 的候选，必须来自目标模块或父工程 scripts；dev server/HMR 证据只能证明开发态可运行，不能替代 build/compile 或交付验收判断。未获用户明确要求发包、交付验收或构建产物验证前，不主动运行 `pnpm` / `npm` / `yarn` 开头的 `transpile` 类命令。
- 本地开发服务/HMR 输出必须包含 `dev server`、`HMR`、`开发态`、外部 `服务已运行` 或 `复用现有 URL` 证据状态、`产物态`、`build` 或 `compile`、`未验证`、`建议补跑`、`不得宣称交付可用`、`不能替代`。
- 子模块 routes/config/registerRegex/父工程 packages 注册变更后的输出必须包含：子模块 build/compile、microConfig refresh 状态，以及 dev server restart、browser hard reload 的外部 runtime acceptance / 用户手工证据状态。缺外部运行态证据时，不能声明路由变更已在运行态生效。
- 构建/编译命令证据不足时，输出必须包含 `候选命令`、`待确认`、`项目证据`，不得把示例命令写成已确认命令。
- 处理 `remoteEntry.js`、chunk 或远程模块访问失败时，必须区分 public url、构建产物路径、`microConfig`、运行时 `window.mfRemotes`、Network 失败请求和远程访问路径；访问地址和路径必须确认。
- `remoteEntry.js` 的实际访问 URL 只能来自已确认的 `microConfig`、运行时 `window.mfRemotes`、产物说明或浏览器 Network 失败请求；不得依据包名、路由名、菜单名或环境名推导。

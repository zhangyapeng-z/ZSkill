# HZERO 运行时配置证据包 Schema

## 证据包使用边界
本文件用于约束 runtime config、layout 扩展和局部配置的证据边界。不要把目标项目未确认的 runtime key 写成可运行代码。

## RuntimeConfigPacket
用于 `app.tsx`、`routes-config.tsx`、layout/header/workbench 扩展、局部 wrapper 和 Choerodon 配置作用域。

必查字段：
- 配置入口：`app.tsx`、`routes-config.tsx`、`config/`、layout extension、局部 wrapper 或页面代码。
- tsconfig paths：`compilerOptions.baseUrl` / `paths` 对 runtime、layout、`hzero-boot`、`components/*`、`utils/*` 等 import alias 的影响。
- 作用域：父工程全局、子模块局部、页面局部、角色/租户局部。
- runtime export 是否确认：如 `appInit` 是否是目标项目 runtime valid key。
- 环境变量读取：是否需要 `API_HOST`、`BASE_PATH`、public URL、网关地址或部署期 host；运行时代码应使用 `import { getEnvConfig } from 'utils/iocUtils';` 和已确认 env key。
- 项目版本证据：模板、现有源码、生成的 runtime valid keys 或项目文档。
- 扩展点可用性：header/layout/workbench/user menu/plugin extension 是否存在。
- 跨模块污染风险：全局 request、全局 `configure`、layout wrapper 或运行时 hook 是否影响其他模块。
- 验证方式继承 route/runtime 外部证据边界：普通 Verification 只覆盖 lint/typecheck、构建候选和手工检查记录；dev server restart、HMR/browser 状态只记录外部 runtime acceptance 或用户手工证据。

输出要求：
- 未确认 runtime valid key 前，不输出可运行 `export async function appInit()`。
- 普通页面业务逻辑应回到页面、service/model、DataSet 或局部 wrapper。
- `paths` 只能确认 import alias 候选，不能确认 runtime export key、layout 扩展点或全局配置可用性。
- 不硬编码运行时环境值；不编造 env key；不把 build-time placeholder 当作 runtime confirmed value。需要读取已确认运行时环境变量时，使用 `getEnvConfig`，import 路径为 `utils/iocUtils`。

# 运行时配置 - 实现与工程证据

## 阅读路由
- 运行时配置 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## 本地资源
按需查本目录资源；不要外显内部路径。
- runtime config、layout/header/workbench 扩展和局部配置：优先使用 `references/schema-packets.md` 中的 `RuntimeConfigPacket`。
- app.tsx、routes-config、runtime export、局部配置和污染风险检查：`references/runtime-config-checklist.md`。
- 运行时配置、Choerodon configure、ConfigProvider 和局部 wrapper 模式：`references/patterns.md`。
- HZERO core utils、`getEnvConfig`、token、租户和运行时环境变量读取边界：`references/core-utils.md`。
- layout/header/workbench/user menu/plugin 扩展：`references/layout-extension.md`。
- 需要稳定运行时配置方案输出时使用模板：`templates/runtime-config-design.md`。
- 需要稳定 layout 扩展方案输出时使用模板：`templates/layout-extension-design.md`。

## 工作流程
1. 判断需求是构建期配置、运行时配置、全局请求/导航适配还是普通页面业务逻辑。
2. 判断作用域是父工程全局、子模块局部，还是单页面局部。
3. 选择目标项目已确认支持的 runtime export、layout/federation extension 或局部 wrapper。
4. 检查是否存在跨模块污染、全局请求副作用或跨系统导航副作用风险。
5. 按 `RuntimeConfigPacket` 输出配置入口、作用域、runtime key 证据、扩展点可用性和污染风险。
6. 输出最小配置片段和验证方式。

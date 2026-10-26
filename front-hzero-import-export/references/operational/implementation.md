# 导入导出 - 实现与工程证据

## Evidence
- 从 Design/Contract Check 读取 mode、standard import、业务参数、权限和 tenantContext。
- `project-wrapper` 必须有当前 wrapper 源码/类型证据，并证明内部使用 `Import` 或 `ExcelExportPro`。
- 不探索 `CommonImport/Route` 或旧 `ExcelExport` 作为复用候选。

## Implementation Rules
1. 导入固定实现 `Import` 抽屉或 confirmed current wrapper。
2. 导出固定实现 `ExcelExportPro` 或 confirmed current wrapper。
3. 参数缺失使用可追溯 generatedCandidate 常量，不得隐藏组件、生成 disabled/no-op 或普通按钮替代。
4. 权限使用组件自己的 `buttonProps.permissionList` / `otherButtonProps.permissionList`，值为 `{ code, type: 'button', meaning }[]`。
5. request、tenant、模板下载、结果反馈、错误明细和关闭刷新必须按冻结合同接线。
6. 页面工具栏与 Table toolbar 按 UI Contract 放置，不额外创建薄 wrapper。
7. 发现存量 `CommonImport/Route`、旧 `ExcelExport` 或旧 wrapper 时，当前 Todo 只能迁移到 canonical 组件；不得保留新旧双分支。

## Output
- changedFiles / changedFilesSource
- component/importPath/wrapperEvidence
- request/permission/tenant wiring
- validators / unverifiedItems / replacementItems

# 导入导出 - Review

## Pass Conditions
- required 导入使用 `Import` / `components/Import` 或 confirmed current wrapper。
- required 导出使用 `ExcelExportPro` / `components/ExcelExportPro` 或 confirmed current wrapper。
- wrapper 内部标准组件、props、权限、request、tenant、文件名和结果反馈证据完整。
- generatedCandidate 参数集中且进入 replacement，没有用户可见占位文案。
- 导入导出入口、权限、请求、结果反馈和刷新行为与 Contract Check 一致。

## Findings
- `CommonImport/Route`、旧 `ExcelExport` 或内部仍使用旧组件的 wrapper：major；新增代码或仍声明 production-ready 时 blocking。
- 普通 Button/Upload/自建 Modal/Drawer/静态链接替代 required 标准组件：major/blocking。
- 缺 templateCode/endpoint 就隐藏入口、disabled/no-op 或只显示 replacement 文案：major。
- 权限数组 shape、tenantContext、query/export 参数、文件名、错误明细或关闭刷新与合同不一致：major；导致功能不可用时 blocking。
- 为单个入口新增薄 wrapper 或保留新旧双分支：major。

Review 只给 finding 和修复范围；不得把旧入口重新确认为项目模式。

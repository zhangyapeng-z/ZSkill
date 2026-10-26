# 导入导出 - 验证与运行态

## 阅读路由
- 导入导出 验证、构建、浏览器检查、运行态判定或输出检查时读取。

## Verification Checklist
- 导入：打开入口、模板下载、文件类型校验、上传、结果反馈、错误明细、关闭/返回后列表刷新。
- 导出：打开入口、列选择、查列请求参数、真正导出请求参数、query/export 参数分流、选中行策略、权限行为、文件格式、同步/异步、成功文件响应和错误反馈。
- 导出验证必须记录两次 Network：第一次取导出列，第二次执行导出；记录 URL、method、query、body/customData/templateCode 和差异原因。
- required 导入/导出若已接标准入口但受权限、后端部署、模板登记或网络环境限制无法跑通，验证结果写 `partial / blocked-by-runtime-contract / not-verified`，并在 Handoff 说明；不得回写成代码层 disabled/no-op。
- 浏览器或代码验证发现导入/导出入口不是 HZERO 标准组件或项目 confirmed wrapper，验证结果必须为 failed；普通按钮、普通上传/下载、静态链接、提示入口或本地状态不是 mock/demo 证据。
- 验证报告必须记录 `ImportExportEntryProof.runtimeStatus`；未打开组件、未触发模板/上传/查列/导出请求或缺 wrapper 证据时，不能写 verified。
- mock/demo 未跑真实文件流时，不得写 production-ready。

# Choerodon 导入 / 导出

用于列表页导出、模板下载、导入上传以及导入结果处理。

## 最小形态
- 导出是一个业务动作，必须已确认 permission、endpoint/protocol、查询参数和文件处理方式。
- 导入是一个业务动作，必须已确认 template、upload endpoint、payload 格式、结果反馈和错误明细流程。
- HZERO 页面在实现前，必须先从设计 handoff 中获得 route/menu/permission 和平台协议。

## 导出流程
- 标准导出入口固定为 `ExcelExportPro` from `components/ExcelExportPro`；confirmed wrapper 必须证明内部仍使用该组件并保留权限、租户、请求、参数和文件处理合同。
- `ExcelExport`、深层导入和内部仍使用旧组件的 wrapper 只形成 migration finding，不进入组件模式候选，也不触发版本选择问题。
- 标准组件已确定不等于 `exportRequestContract` 闭合；仍必须确认查列请求和真正导出请求的 URL/method/参数位置。
- 确认导出触发位置：toolbar、row action、batch action，或 DataSet 内置导出。
- 确认 permission code，以及无权限动作是隐藏、禁用还是直接省略。
- 确认导出使用的是当前查询条件、选中行、全部行，还是服务端异步任务。
- 确认 API endpoint、method、params、响应类型、文件名来源和错误响应格式。
- 确认查列请求与真正导出请求是否同参；使用 `queryParams(type)` 时，必须明确 `query` / `export` 两阶段的参数差异和返回值。
- 确认 `queryColumnProps`、`allBody`、`fakePost`、`queryFormItem` / `queryFormItemExtra`、文件配置和用户选择列进入 query/path/body/customData 的位置。
- 如果使用 DataSet `transport.exports`，应确认项目先例和后端协议；否则导出逻辑应留在 service 边界。

## 导入流程
- 标准导入入口固定为 `Import` from `components/Import`；confirmed wrapper 必须证明内部仍使用该组件并保留权限、模板、上传、结果和刷新合同。
- `CommonImport/Route + openTab`、深层导入和内部仍使用旧入口的 wrapper 只形成 migration finding，不进入组件模式候选。
- 标准入口已确定不等于 `importFlowContract` 闭合；仍必须确认模板、上传、结果反馈、错误明细和关闭/返回刷新流程。
- 确认模板来源：`templateCode`、模板下载 endpoint、静态模板，或平台导入配置。
- 确认 upload endpoint、请求方法、表单字段名、额外参数、tenant/org 上下文以及可接受文件类型。
- 确认结果行为：立即成功/失败、异步任务、进度轮询、错误明细文件，或逐行校验报告。
- 确认导入成功后的列表刷新行为。
- 当导入与模板下载权限不同，分别确认对应 permission code。

## 未闭合参数
- Export endpoint/query/permission：待确认。
- Import template/upload/result/permission：待确认。
- File protocol 与错误处理：待确认。

## 护栏规则
- 不要编造 `templateCode`、export endpoint、upload endpoint、bucket、tenant rule、token/origin 或文件名。
- 除非后端明确确认，否则不要把普通列表 `transport.read` 复用成导出协议。
- 不能只验证第一次“获取导出列”请求成功就认为导出可用；第二次真正导出请求的参数缺失同样属于 blocking 风险。
- 不得自建普通下载按钮替代 HZERO 标准导出组件；参数未确认时按 generatedCandidate / missing 标记承接，但代码形态仍必须是 `ExcelExportPro` 或内部使用它的 confirmed wrapper，不得降级为旧组件、普通按钮、普通下载或提示入口。
- 当后端存在异步校验/结果阶段时，不要把 upload success 直接当成 import success。

## 验证
- Export：验证查询参数、选中行行为（如适用）、权限行为、成功文件响应和错误反馈。
- Import：验证模板下载、文件类型校验、上传、结果反馈、错误明细和列表刷新。
- 最终实现交接仍需 build/compile，或明确标注阻塞/未验证状态。

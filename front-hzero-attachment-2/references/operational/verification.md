# 附件 - 验证与运行态

## 阅读路由
- 附件 验证、构建、浏览器检查、运行态判定或输出检查时读取。

## Verification Checklist
- V0 静态扫描必须覆盖本轮 changed files 或目标 `packageDir` 的 Attachment import/exportShape：如可访问本资产脚本，运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_c7n_component_api_ast_grep.py --root <frontend-root-or-packageDir>` 或等价路径，并记录 `attachmentComponentValidator`、`validatorCommand`、`validatorTarget`、`validatorCheckedFiles`、`result`。命中 `components/Attachment` / `hzero-front/lib/components/Attachment` 配置对象作为 JSX、ambient module shim 掩盖真实 exportShape、配置对象以 `Attachment` 命名传给富文本、或跨库 Attachment/Upload API 污染时，Verification 结果为 failed/blocking，必须回 Implementation 修复；build 通过不能覆盖该失败。
- Attachment V0 报告必须列出命中的 ruleId，至少识别 `hzero_attachment_ambient_module_declaration`、`hzero_attachment_config_object_rendered_as_jsx`、`hzero_attachment_config_import_name_ambiguous`、`hzero_front_hfile_attachment_import_invalid`、`hzero_attachment_visible_contract_placeholder`。
- V0 静态扫描命中 `hzero_attachment_visible_contract_placeholder`，或浏览器页面出现“待接标准附件组件 / attachmentUuid 引用 / replacement / 未实证 / 本轮不模拟上传”等附件占位文案时，Verification 结果为 failed/blocking；这些内容只能记录在 handoff/replacement，不能显示给业务用户。
- 浏览器 console 或构建运行栈出现 `ReferenceError: Attachment is not defined`，且栈涉及业务 `Attachment*.tsx`、`choerodon-ui/pro/lib/index.js` 或 `choerodon-ui/pro` 桶入口时，优先按 Attachment import 运行态问题处理：检查当前实现是否从 `choerodon-ui/pro` named import 取 `Attachment`，若目标版本存在桶入口循环依赖，必须回 Implementation 改为 `import Attachment from 'choerodon-ui/pro/lib/attachment'` 或 confirmed wrapper，并记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed`。不得把该错误归因成 bucket/storage/template 参数缺失或普通变量漏导入后放行。
- 附件组件渲染，编辑态可上传/删除，只读态可展示/预览/下载。
- Network 或项目 wrapper 证据显示 bucket/storage/template、tenantContext 和 attachment UUID 使用正确。
- 新建、编辑、刷新、保存后附件 UUID 和文件列表不丢失。
- 无权限或只读状态下上传/删除入口不可用，预览/下载策略符合 Button Contract。
- mock/demo 验证报告写明 mock-only UUID、候选 bucket/storage 和 production replacement。

## Handoff Closeout
- 交付摘要必须记录 Attachment Contract 状态、component/importPath/exportShape、attachmentField/valueStructure、bucket/storage/template、preview/download/remove、tenantContext 和 permissionCode。
- generatedCandidate 或 mock-only 项必须记录值、来源缺口、replacement owner、生产阻塞原因、未验证项和后续需要平台/后端/前端确认的协议。

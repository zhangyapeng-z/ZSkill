# 附件 - 审查与反模式

## 阅读路由
- 附件 Review、自查、反模式、finding 或合规判断时读取。

## Review Checklist
至少 major：
- 附件字段退化为普通 TextField、Output raw UUID、静态列表或普通按钮。
- `bucketName` / `storageCode` / template 无来源硬编码，且未标记候选和 replacement。
- Required 上传/预览/下载/删除入口缺权限边界。
- 使用 `Upload/FileUpload` 但没有 Attachment 不适用证据。
- 从 `hzero-front-hfile` 导入 `Attachment`，或把 HFILE 模块包当作标准业务附件 JSX 组件来源。
- 只因为组件能渲染就声明附件生产能力完成。
- 页面可见区域渲染附件合同占位、待接标准附件组件、`bucket/storage 未实证`、`editable-contract-pending`、`replacement`、静态附件列表或“本轮不模拟上传/预览/下载/删除”等内部治理文案。
- 目标版本已有 `choerodon-ui/pro` 桶入口循环依赖证据或浏览器报 `ReferenceError: Attachment is not defined`，但仍继续从 `choerodon-ui/pro` named import 取 `Attachment`，且未记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed`。

blocking：
- 上传、预览、下载、删除核心流程不可用仍声明 production-ready。
- 租户、bucket、权限或文件身份错用导致跨租户/跨业务文件风险。
- `attachmentUuid` 当作 file URL 下载/预览，或普通字符串传输导致附件组不可用。
- 将配置对象、namespace 对象或未证明 exportShape 的默认导入当作 `<Attachment />` / `<Attachment.Dragger />` 渲染，导致 React #130 / element type invalid。
- `ReferenceError: Attachment is not defined` 导致附件区或详情页不可渲染，仍声明 mock-completed、usable=true 或 production-ready。
- 新增 `declare module 'components/Attachment'`、`declare module 'hzero-front/lib/components/Attachment'`、`declare module 'components/*'`、`declare module 'hzero-front/lib/components/*'` 或等价 ambient shim 掩盖 Attachment exportShape / import 来源错误。
- Required 附件能力只落成可见占位组件或内部 replacement 文案，并声明 mock-completed、usable=true、production-ready 或 Implementation Done。

## Validator Rule Mapping
- `hzero_attachment_ambient_module_declaration`：用精确或通配 ambient module 声明掩盖 `components/Attachment` / `hzero-front/lib/components/Attachment` 的真实 exportShape。
- `hzero_attachment_config_object_rendered_as_jsx`：`components/Attachment` / `hzero-front/lib/components/Attachment` 配置对象被当 JSX 组件。
- `hzero_attachment_config_import_name_ambiguous`：富文本配置对象命名为 `Attachment`，容易被误当组件。
- `hzero_front_hfile_attachment_import_invalid`：从 `hzero-front-hfile` 导入标准业务附件 JSX。
- `hzero_attachment_visible_contract_placeholder`：页面可见附件合同占位、replacement 或内部治理文案。

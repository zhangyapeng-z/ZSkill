# 附件 - 实现与工程证据

## 阅读路由
- 附件 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## Component Policy
- 标准业务附件默认使用 Choerodon Pro `Attachment`、`Attachment.Dragger` 或项目已确认 Attachment wrapper；常规入口为 `choerodon-ui/pro` named import，若目标版本证据显示桶入口循环依赖或运行时报 `ReferenceError: Attachment is not defined`，可使用 `choerodon-ui/pro/lib/attachment` 默认导入并记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed`。
- HZERO `components/Attachment` / `hzero-front/lib/components/Attachment` 的默认导出主要是附件配置对象，常见合法用法是 `import hzeroAttachmentConfig from 'components/Attachment'` 后传给 `components/RichTextEditor` / `NewRichTextEditor` 等 HZERO 富文本组件的附件配置入口；它不是标准业务附件 JSX 组件。
- `hzero-front-hfile` 是 HFILE 模块包，不是标准业务附件 JSX 组件来源；不得 `import { Attachment } from 'hzero-front-hfile'` 或通过 namespace/default 方式从该包取 `Attachment` 渲染。
- 禁止把上述配置对象当作 JSX 组件渲染；`<Attachment />` 会触发 React #130 `got: object`。只有项目明确存在同名 confirmed wrapper 且 exportShape 证明为 React component 时才可使用。
- `Upload` / `FileUpload` 只有在 Attachment 不适用且有 UI Contract、项目证据或用户确认时才允许。
- 不得用普通 `Button` + request/download、静态 `<ul>` 文件列表、自拼 `HZERO_FILE` URL、隐藏入口、永久 disabled/no-op 或普通 `Output attachmentUuid` 冒充附件能力。
- mock/demo 可使用 mock-only `attachmentUuid`、本地 devServer 文件列表响应或候选 bucket/storage 参数保持演示可运行，但必须保留 replacement；replacement 只能进入产物、manifest、verification 或 handoff，不得作为页面文案、静态 JSX 或占位组件渲染。

## Implementation Rules
1. 先读取设计/任务中的 Attachment Contract；标准业务附件的 Choerodon Pro `Attachment` / `Attachment.Dragger` 坐标默认按 `builtin-standard / use-standard-import` 继承，目标工程缺相似用法、缺本地 import 样例或缺项目 wrapper 时不得阻塞。仅缺 `bucketName` / `bucketDirectory` / `storageCode` / `template` 等参数时，不返回 Design / Task，也不跳过组件生成，必须生成 `mockOnly/generatedCandidate` 参数常量并接入标准附件组件，同时记录 replacement。只有依赖/版本/编译证据明确否定标准 Attachment 可导入或可实例化且没有 confirmed wrapper，或附件字段/value 结构无法形成候选时，才返回 Design / Task 补齐。不得生成 `AttachmentContractPlaceholder`、`*-attachment-contract-placeholder`、静态 `<div>` 文件列表或“待接标准附件组件 / replacement / 未实证”页面文案。
2. 使用确认的 `Attachment` / `Attachment.Dragger` / project wrapper import；默认从 `choerodon-ui/pro` 命名导入 `Attachment`，或按项目 confirmed wrapper 导入。若运行栈或源码证据显示 `choerodon-ui/pro` 桶入口加载 `attachment` 时发生循环依赖，导致 `ReferenceError: Attachment is not defined`，应改为 `import Attachment from 'choerodon-ui/pro/lib/attachment'`，并在实现摘要、componentApiProvenance 或验证报告记录 `barrelImportStatus=unsafe`、`deepImportStatus=confirmed`。不得用 `import Attachment from 'components/Attachment'`、`import Attachment from 'hzero-front/lib/components/Attachment'` 后直接 `<Attachment />`；不得从 `hzero-front-hfile` 导入 `Attachment` 作为 JSX 组件；若因富文本配置需要 HZERO Attachment 配置路径，应命名为 `hzeroAttachmentConfig` 或等价 config 名并只作为配置对象传入，不进入 JSX；不要自行新建薄 wrapper。
3. DataSet 字段保留附件真实字段语义，通常为 `attachmentUuid` 字符串；不要把附件字段改成普通文本字段。
4. 只读详情使用附件只读组件、附件列表或 wrapper 的 view mode；不要只展示 raw UUID。
5. 新建页如果需要提前生成 UUID，必须有组件或后端协议来源；不能用随机/硬编码 UUID 冒充生产协议。
6. `bucketName` / `bucketDirectory` / `storageCode` / `template` 等候选值可用于 mock/demo，缺失时应主动生成 `mockOnly/generatedCandidate` 常量或组件 props 候选值，继续完成标准组件实例化；候选状态和替换责任必须写入 manifest / Verification / Handoff，不要写成 confirmed。不能模拟的真实上传/预览/下载效果只记录 replacement 和未验证项，不得阻塞标准组件代码生成，也不得落成页面占位。
7. 上传、预览、下载、删除按钮若是 required 业务动作，权限按钮规则归 `front-hzero-permission-button`。
8. 需求实际是 HZERO `ChunkUploader` 时立即转 `front-hzero-common-components`，不得用 Attachment 替代。
9. 实现写入或修改包含业务附件 JSX、`components/Attachment`、`hzero-front/lib/components/Attachment`、`hzero-front-hfile`、`choerodon-ui/pro` `Attachment` 的目标工程文件后，如可访问本资产脚本，必须在目标前端根目录或已确认 `packageDir` 运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_c7n_component_api_ast_grep.py --root <frontend-root-or-packageDir>` 或等价本仓库脚本路径。命中 `hzero_attachment_config_object_rendered_as_jsx`、`hzero_attachment_config_import_name_ambiguous`、`hzero_front_hfile_attachment_import_invalid` 或其它 Attachment/C7N 组件 API finding 时，当前实现必须回修或标记 `partial-needs-rework` / `blocked-needs-rework`，不得进入 Review/Verify；无法运行时必须记录 `attachmentComponentValidator=not-run + reason`，并执行同等人工静态检查。
   - 不得新增或保留 `declare module 'components/Attachment'`、`declare module 'hzero-front/lib/components/Attachment'`、`declare module 'components/*'`、`declare module 'hzero-front/lib/components/*'` 等精确或通配 ambient shim 来让错误 import 通过 TypeScript；命中 `hzero_attachment_ambient_module_declaration` 必须删除 shim，并改用目标版本确认的 Choerodon Attachment import 或 confirmed React component wrapper。
10. 命中 `hzero_attachment_visible_contract_placeholder` 时必须回修：删除可见占位；若只是 bucket/storage/template 等参数缺失，改为生成 mock/generatedCandidate 参数并接入标准附件组件；只有依赖/版本/编译证据明确否定标准 Attachment 可导入或可实例化且没有 confirmed wrapper，或字段/value 结构无法形成候选时，才隐藏入口并记录 replacement 或返回 Design/Task 补契约。不得把“协议占位展示”视为合规实现。

## Storage Parameter Rules
`bucketName`、`bucketDirectory`、`storageCode`、`template`、目录、存储编码等参数的生产值必须有来源：
- Attachment Contract。
- 平台文件/附件配置。
- 后端契约或 MDS/FSS 文件资产。
- 项目同类页面强证据。
- 用户确认。

`bucketName="hzero"`、`bucketName="default"`、`storageCode="default"` 等默认值不是天然生产事实。无来源且 mock/demo 已授权时，按以下顺序处理，不再提问：
- 先生成 `mockOnly/generatedCandidate` 值，例如本地 devServer mock 文件列表、mock-only `attachmentUuid`、候选 bucket/storage/template 常量，并用这些候选值继续实例化标准附件组件。
- 不能模拟真实上传/预览/下载效果时，只在 `constants.ts`、Attachment Contract、Verification 和 Handoff 中保留 replacement / 未验证记录，不生成用户可见的禁用入口或“待替换”文案，也不因此跳过标准组件代码。
- 所有候选和占位都必须写入 production replacement，生产状态保持 `partial/missing`，不得写 confirmed。

无来源时只能作为候选：

```text
bucketNameStatus=generatedCandidate
replacementRequired=true
confirmedSource=missing
productionOwner=platform/backend/frontend
```

有明确来源时，`bucketName="hzero"` 可以保留，不单独构成缺陷。

# HZERO NewRichTextEditor 新版富文本编辑器

## 阅读路由
- 判断组件归属读 `组件归属`。
- 设计和任务拆分读 `Design Gate`、`Contract Fields`。
- 编码读 `Implementation SOP`。
- 审查和验证读 `Review Checklist`、`Verification Checklist`。

## 组件归属
`NewRichTextEditor` 是 HZERO `hzero-front 1.11.38-alpha.8+` 提供的新版富文本编辑器，基于 TinyEditor 封装，底层基于 quill 2.0。它不是 Choerodon rich-text 组件；Choerodon Form/DataSet 只承载字段绑定。

命中词：
- `新版富文本编辑器`
- `NewRichTextEditor`
- `components/NewRichTextEditor`
- `RichTextViewer`
- `TinyEditor`
- `quill2.0`
- `FieldType.object`
- `FieldType.intl`
- `removeButtons`
- `table-up`

标准 import：

```js
import NewRichTextEditor from 'components/NewRichTextEditor';
```

附件配置 import：

```js
import hzeroAttachmentConfig from 'components/Attachment';
```

`hzeroAttachmentConfig` 是 HZERO 附件配置对象，主要用于传给 `components/RichTextEditor` / `NewRichTextEditor` 等富文本组件的附件配置入口；不要把它命名为 `Attachment` 并作为 `<Attachment />` 渲染。标准业务附件列表/上传组件仍按 `front-hzero-attachment` 使用 `choerodon-ui/pro` `Attachment` 或 confirmed wrapper。

预览组件：

```js
const { RichTextViewer } = NewRichTextEditor;
```

## Design Gate
必须确认或标记：
- `component=NewRichTextEditor` / `RichTextViewer`，以及 importPath 或项目 wrapper。
- `hzeroFrontVersion >= 1.11.38-alpha.8` 的证据。
- 使用模式：受控 `value/onChange`、DataSet `name` 绑定、只读预览或多语言富文本。
- 值结构：Delta object；受控 string 仅作为组件转换候选，生产提交结构必须确认。
- DataSet 字段类型：普通富文本优先 `FieldType.object`；多语言富文本使用 `FieldType.intl`。
- 图片/视频/附件上传参数：`bucketName`、`bucketDirectory`、`storageCode`、`privateBucket`、`accept`、上传回调。
- 若使用 `components/Attachment` 配置对象，记录 `attachmentConfigImportPath=components/Attachment`、`attachmentConfigExportShape=config-object` 和配置传入的目标 prop / wrapper API。
- UI/校验：`label`、`placeholder`、`readOnly`、`showValidation`、高度、工具栏、需移除按钮。
- 表格内或类似容器中使用时，必须评估 `removeButtons=['table-up']`，避免 quill table 插件异常。
- 预览使用 `RichTextViewer`，确认 `deltaOps` 来源。

## Contract Fields

```text
newRichTextEditorContract:
  status: confirmed / partial / missing / blocked / not-applicable
  component: NewRichTextEditor / RichTextViewer / project-wrapper / missing
  importPath:
  hzeroFrontVersion:
  bindingMode: controlled / dataset-field / viewer
  valueShape: Delta / Delta.ops / string-candidate / missing
  fieldType: FieldType.object / FieldType.intl / not-applicable / missing
  uploadProtocol: bucketName / bucketDirectory / storageCode / privateBucket / accept / callbacks
  attachmentConfig: importPath / exportShape / targetProp / wrapperApi / not-applicable
  toolbar / removeButtons:
  readOnly / showValidation / placeholder / style:
  intl: enabled / disabled / missing / not-applicable
  viewerDeltaOps:
  runtimeValidation: edit / change / validation / readonly / intl / upload / preview / table-up-disabled
```

## Implementation SOP
1. 使用 `NewRichTextEditor` 或项目 confirmed wrapper；required 新版富文本不得改成普通 textarea、旧版 editor、Choerodon rich-text 或第三方组件。
2. 受控模式必须同时维护 `value` 和 `onChange`；不要只读 ref 内部内容作为唯一业务状态。
3. DataSet 模式使用 `name` 绑定字段；字段类型按设计使用 `FieldType.object` 或 `FieldType.intl`。
4. 多语言富文本启用时，保留 `onIntlChange`、`intlModalProps`、`intlTabPaneProps` 的合同或待确认项。
5. 图片/附件上传参数不得编造；缺 bucket/storage 时写 missing/generatedCandidate，并进入验证或替换清单。
6. 使用 `components/Attachment` 时必须按配置对象命名，例如 `hzeroAttachmentConfig`，并只传给已确认的富文本组件 prop / wrapper API；不得 JSX 渲染。
7. 在 Table 或同类嵌套场景中使用时，默认加入或确认 `removeButtons={['table-up']}`；若保留 table 插入能力，必须有 UI/组件证据。
8. 预览使用 `RichTextViewer`，传入确认来源的 `deltaOps`，不要用 `dangerouslySetInnerHTML` 冒充 Delta 预览。

## Review Checklist
- 是否使用 HZERO `NewRichTextEditor` / `RichTextViewer` 或 confirmed wrapper。
- 是否误归到 Choerodon rich-text、textarea、普通 HTML editor 或第三方 editor。
- `hzero-front 1.11.38-alpha.8+` 是否有证据。
- DataSet 字段类型是否与值结构匹配；Delta 数据不得当普通 string 随意提交，除非 API 契约确认。
- 多语言场景是否使用 `FieldType.intl` 或有明确豁免。
- 图片/附件上传 bucket、directory、storageCode、privateBucket、accept 和 callbacks 是否有来源。
- `components/Attachment` 是否只作为 `hzeroAttachmentConfig` 等配置对象传给富文本组件，而不是作为 `<Attachment />` 渲染。
- 表格内使用是否处理 `table-up` 插件风险。
- 预览是否使用 `RichTextViewer` 和 Delta ops。

## Verification Checklist
- 编辑输入后 `onChange` 或 DataSet 字段更新。
- 必填、只读、校验信息和高度显示符合 UI Contract。
- 多语言按钮、弹窗和不同语言值写回符合设计。
- 图片/附件上传可触发；未跑真实文件服务时写 partial/blocked。
- `RichTextViewer` 能渲染已保存 Delta ops。
- 表格内或复杂容器中使用时，确认插入表格能力已关闭或无异常。

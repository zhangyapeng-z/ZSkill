# HZERO ChunkUploader 分片上传组件

## 阅读路由
- 判断组件归属读 `组件归属`。
- 设计和任务拆分读 `Design Gate`、`Contract Fields`。
- 编码读 `Implementation SOP`。
- 审查和验证读 `Review Checklist`、`Verification Checklist`。

## 组件归属
`ChunkUploader` 是 HZERO `hzero-front@1.6+` 提供的分片上传组件，不是 Choerodon Attachment，也不是普通 Upload fallback。

命中词：
- `分片上传组件`
- `ChunkUploader`
- `components/ChunkUploader`
- `prefixPatch`
- `uploadMode`
- `chunkSize`
- `attachmentUUID`

标准 import：

```js
import ChunkUploader from 'components/ChunkUploader';
```

## Design Gate
必须确认或标记：
- `component=ChunkUploader`，`importPath=components/ChunkUploader` 或项目 wrapper 路径。
- `hzeroFrontVersion >= 1.6` 的证据；缺证据写 `missing/generatedCandidate`。
- `action`、`method`、`prefixPatch`、`paramsData`、`uploadMode`、`bucketName`、`directory`、`storageCode`、`attachmentUUID` 的来源。
- 文件限制：`fileSize`、`chunkSize`、可接受文件类型、单/多文件策略。
- 显示与状态：`text`、`doneText`、`type`、`showUploadList`、`hidden`、`disabled`。
- 回调：`callback` 成功/失败后刷新、写回字段或提示策略。
- 文件服务和租户：tenantContext、bucket/storage 是否来自平台配置、后端契约或相似页面。

## Contract Fields

```text
chunkUploaderContract:
  status: confirmed / partial / missing / blocked / not-applicable
  component: ChunkUploader / project-wrapper / missing
  importPath:
  hzeroFrontVersion:
  action / method:
  prefixPatch:
  paramsData:
  uploadMode: default / oss / generatedCandidate / missing
  bucketName / directory / storageCode:
  attachmentUUID:
  fileSize / chunkSize:
  showUploadList:
  hidden / disabled:
  callbackPolicy:
  tenantContext:
  runtimeValidation: render / select-file / chunk-upload / callback / error / disabled-state
```

## Implementation SOP
1. 使用 `ChunkUploader` 或项目 confirmed wrapper；required 分片上传不得改成 Attachment、Upload、Button + request 或静态占位。
2. `prefixPatch` 默认候选可来自 HZERO 文件服务环境变量，但不能写成 confirmed；手册默认名是 `HZERO_HFLE`，项目中可能有差异。
3. `bucketName` 默认候选可为 `BKT_PUBLIC`，但生产值必须来自平台配置、后端契约或用户确认。
4. `chunkSize` 默认候选为 `5 * 1024 * 1024`，`fileSize` 默认候选为 `1000 * 1024 * 1024`；需求或 bucket 限制优先。
5. `paramsData` 应来自已确认业务上下文；不要在组件内临时拼装无来源租户、配置编码或业务主键。
6. `hidden/disabled` 条件必须来自 UI Contract 或业务状态；不得用永久 disabled/no-op 代替缺契约。
7. 上传后如果需要写回 DataSet 字段或刷新文件列表，必须在 callbackPolicy 中说明。

## Review Checklist
- 是否使用 `ChunkUploader` / confirmed wrapper，而不是 Attachment 或普通 Upload。
- `hzero-front@1.6+` 是否有证据。
- `prefixPatch` 是否误写为 `prefixPath` 或未确认服务前缀。
- `bucketName/directory/storageCode/uploadMode/action/paramsData/attachmentUUID` 是否有来源。
- `chunkSize/fileSize` 是否与需求、bucket 或平台限制冲突。
- `hidden/disabled` 是否可能永久阻断 required 上传能力。
- 是否输出 `HzeroCommonComponentProof` 或等价证明。

## Verification Checklist
- 组件可渲染，选择文件入口可用。
- disabled/hidden 状态符合业务状态。
- 发起上传时请求使用正确 prefix/action、method、paramsData、bucket/storage 和 chunk 参数。
- 成功后 callback 执行，页面字段或列表刷新符合设计。
- 大文件、超限文件、失败重试或错误提示至少有手工或代码验证记录。

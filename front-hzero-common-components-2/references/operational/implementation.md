# HZERO 通用组件 - 实现与工程证据

## 阅读路由
- HZERO 通用组件 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## Implementation Rules
1. 先使用 HZERO 标准组件坐标或已确认 wrapper；目标项目没有相似用法、没有本地 wrapper 或没有组件样例时，不得返回阻塞。只有依赖/版本/编译证据明确否定标准组件可导入或可实例化，且没有 confirmed wrapper 时，才返回 Frontend Design / Contract Check；不得自行改用 Attachment、Upload、基础 Button 或第三方富文本组件。
2. 按 reference 中的组件模式实现，保留 generatedCandidate 参数和 production replacement 项。
3. 组件参与 Form/DataSet 时，优先使用已确认的 `name` / `dataSet` / 字段类型绑定，不重复维护无来源本地状态。
4. 上传、图片、附件、bucket、directory、storageCode、action、prefix 或 private bucket 等协议类参数优先来自合同或项目证据；仅参数缺失时使用 `generatedCandidate/mockOnly/placeholderParameter` 继续接标准组件，并写入 replacement / Handoff risk。参数缺口不得让 required 组件退化为普通 Upload、textarea、disabled/no-op 或页面可见占位。
5. 实现结果必须输出 `HzeroCommonComponentProof`，说明组件、版本、importPath、关键参数、运行状态和未验证项。

```text
HzeroCommonComponentProof:
  component: ChunkUploader / NewRichTextEditor / RichTextViewer / confirmed-project-wrapper / missing
  requirementStatus: required / optional / not-applicable
  importPath:
  hzeroFrontVersion: confirmed / generatedCandidate / missing
  bindingMode: controlled / dataset-field / viewer / upload-button / project-wrapper / not-applicable
  contractStatus: confirmed / generatedCandidate / missing / blocked / not-applicable
  fileProtocolStatus: confirmed / generatedCandidate / missing / blocked / not-applicable
  runtimeStatus: not-run / partial / verified / blocked
  replacementRequired: true / false
```

# HZERO 通用组件 - 审查与反模式

## 阅读路由
- HZERO 通用组件 Review、自查、反模式、finding 或合规判断时读取。

## Review Checklist
- 是否误把 `ChunkUploader` 当成 Attachment，或误把 `NewRichTextEditor` 当成 Choerodon rich-text。
- 是否使用 HZERO 组件或目标项目 confirmed wrapper；普通 Button、普通 Upload、自建 request、第三方 editor 直接替代 required HZERO 组件时至少 major，导致能力不可用或误报 production-ready 时 blocking。
- 是否具备 hzero-front 版本证据；缺版本证据但声明可交付至少 major。
- `HzeroCommonComponentProof` 是否存在，且 component/importPath/version/contract/runtime 可追溯。
- 参数缺失是否用 generatedCandidate/missing/replacement 承接，而不是 disabled/no-op、静态占位或隐藏入口。

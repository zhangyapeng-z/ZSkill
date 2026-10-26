# 附件 - 领域细节

## 阅读路由
- 附件 其它不归入阶段的领域细节、交叉引用或 proof 结构命中时读取。

## Scope
本 skill 只管前端业务附件组件、页面交互和生产替换边界。

不负责：
- 后端 `FileClient`、`uploadAttachment`、`getAttachmentFiles`、签名 URL 等实现；这些归 `hzero-integrate-file-operation`。
- HZERO `ChunkUploader` 分片上传、`NewRichTextEditor` / `RichTextViewer` 图片附件上传；这些归 `front-hzero-common-components`。
- 导入导出框架；这些归 `front-hzero-import-export`。

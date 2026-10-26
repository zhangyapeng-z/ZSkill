# HZERO 通用组件 - 设计与契约

## 阅读路由
- HZERO 通用组件 设计、契约冻结、question gate、事实确认或资源选择时读取。

## Design Gate
设计阶段必须记录：
- `hzeroCommonComponentContract.status`：confirmed / partial / missing / blocked / not-applicable。
- 组件名、组件 importPath、hzero-front 最低版本、目标项目版本证据和相邻页面使用证据；标准组件坐标默认作为 `builtin-standard / use-standard-import`，相邻页面只用于确认 wrapper/override 或发现冲突。
- 组件业务模式：分片上传 / 富文本编辑 / 富文本预览 / DS 绑定 / 受控组件 / 多语言 / 文件上传。
- 参数契约状态：confirmed / generatedCandidate / missing / not-applicable。
- 与 HZERO 页面容器、DataSet/Form、权限、tenantContext、文件服务协议和 verification 的关系。

## Scenario Routing
- 命中 `ChunkUploader`、`components/ChunkUploader`、`分片上传组件`、`prefixPatch`、`uploadMode`、`chunkSize`、`attachmentUUID` 时，读取 `references/chunk-uploader.md`。
- 命中 `NewRichTextEditor`、`components/NewRichTextEditor`、`新版富文本编辑器`、`RichTextViewer`、`TinyEditor`、`quill2.0`、`FieldType.object`、`FieldType.intl`、`table-up` 时，读取 `references/new-rich-text-editor.md`。
- 页面同时涉及附件列表/预览/下载/删除时，继续按 HZERO 文件协议和附件契约补齐文件服务边界；但组件入口归属以当前 HZERO 组件规则为准。

## Source Priority
- 用户确认、FDS/TDS/API、目标项目源码、平台组件手册和 hzero-front 版本证据优先于本规则。
- 本规则只处理 HZERO 通用组件的组件选型、版本门槛、实现顺序、拒收项和验证清单；不生成业务字段、接口、权限码、bucket、目录、存储编码或上传地址的 confirmed 契约。
- 目标工程缺少相似页面、缺项目 wrapper 或缺本地组件样例时，不得把 HZERO 标准组件写成 `missing/blocked`；应写 `componentSource=builtin-standard`、`implementationPolicy=use-standard-import`。只有依赖/版本/编译证据明确否定标准组件可导入或可实例化，且没有 confirmed wrapper 时，才输出 `missing/blocked` 并回 Design / Evidence。缺少 bucket、目录、存储编码、上传地址、private bucket、prefix、action 等业务参数时，输出 `generatedCandidate/mockOnly/placeholderParameter + replacement`，继续保留标准组件或 confirmed wrapper 方案，不得声明 production-ready。
- 不要把 HZERO `ChunkUploader` 自动归入 Attachment；不要把 HZERO `NewRichTextEditor` 自动归入 Choerodon rich-text。Choerodon DataSet/Form 只提供绑定承载，不是组件归属。

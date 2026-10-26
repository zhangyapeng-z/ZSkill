# 附件 - 设计与契约

## 阅读路由
- 附件 设计、契约冻结、question gate、事实确认或资源选择时读取。

## Design Gate
涉及附件能力时，设计或 Contract Check 必须形成 Attachment Contract：
- `attachmentComponentMode`：`Attachment` / `Attachment.Dragger` / project wrapper / fallback。
- `component`、`importPath` 与 `exportShape`：来自项目证据、组件库事实或用户确认；必须能证明导入值是可渲染 React component / static member / confirmed wrapper，而不是配置对象。
- `attachmentField`、`valueStructure`、`attachmentUuidPolicy`：字段名、是否 UUID 字符串、创建/读取/复用/提交策略。
- `bucketName`、`bucketDirectory`、`storageCode`、`template` 或等价存储参数：来源和状态。
- `preview/download/remove/history/downloadAll/chunk` 协议：由全局配置、项目 wrapper、平台配置或后端契约承接。
- `tenantContext` 和 `permissionCode`：上传、预览、下载、删除是否 required 权限；required 按 `front-hzero-permission-button`。
- `readonlyDisplayContract`：只读时显示附件列表/只读组件，不直接 Output raw `attachmentUuid`。

标准业务附件的内置标准坐标默认从 Choerodon Pro Attachment 能力继承，首选 `import { Attachment } from 'choerodon-ui/pro'`，`Attachment.Dragger` 使用该 named export 的 static member。目标工程没有相似页面或 import 证据时，不得把标准 Attachment 能力写成 `missing`、`partial` 或普通 generatedCandidate；应写 `importSource=builtin-standard`、`status=confirmed`、`implementationPolicy=use-standard-import`，并只把 bucket/storage/template、tenantContext、运行验证或业务参数写成 `generatedCandidate/partial/replacement`。若目标版本运行或源码证据显示桶入口 `choerodon-ui/pro` / `choerodon-ui/pro/lib/index.js` 会因循环依赖触发 `ReferenceError: Attachment is not defined`，Design / Contract Check 必须记录 `barrelImportStatus=unsafe`、`deepImportStatus=confirmed`，允许 Implementation 使用 `import Attachment from 'choerodon-ui/pro/lib/attachment'` 作为版本确认后的标准坐标。只有目标工程证据明确证明 Choerodon Attachment 不可用、版本不含 Attachment、深层入口也不可实例化，或存在 confirmed React component wrapper 替代时，才允许改成 `conflict/blocked/project-wrapper` 并回 Design / Evidence。

缺任一关键协议时可以进入默认 mock/demo，但必须标记 `partial/missing/generatedCandidate/mockOnly`，并写入 production replacement；不得声明 production-ready。默认 mock demo 下，不得再单独向用户追问 `bucketName / bucketDirectory / storageCode / template`。仅缺 bucket/storage/template/目录等参数时，必须先生成 `mockOnly/generatedCandidate` 常量并继续规划 confirmed 标准附件组件，不得把参数缺口升级成“组件不生成”。只有缺少可渲染组件来源、附件字段/value 结构或组件无法实例化的必要协议时，才返回 Contract Check / Design 补契约。任何缺口都不得设计或要求页面渲染 `附件能力待接`、`bucket/storage 未实证`、`replacement`、`contract-placeholder` 等用户可见占位。

## Visible Placeholder Boundary
- 附件是 required 标准能力时，默认必须接入 confirmed `Attachment` / `Attachment.Dragger` / project wrapper；缺 bucket/storage/template 这类参数时用 mock/generatedCandidate 候选值继续生成组件，缺组件坐标或组件无法实例化的必要协议时回 Contract Check / Design，不得生成页面占位组件。
- 页面 JSX、列表/详情区块、Modal/Drawer 内容和只读区不得渲染“待接标准附件组件”“仅保留 attachmentUuid 引用”“本轮不模拟上传/预览/下载/删除”“replacement”等内部治理文案。
- `attachmentUuid` 可作为数据字段、hidden payload、组件 value 或 handoff 证据保留；不能以普通 `<div>` / `Output` / 静态列表展示为附件能力替代。
- 若仅标准组件参数未确认，Design 应输出候选参数、`replacementRequired=true` 和生产替换原因，同时允许 Implementation 接入真实可渲染的 mock-only 标准组件；若标准组件坐标或 exportShape 未确认且无法采用内置 `choerodon-ui/pro` 坐标，才输出 `attachmentComponentMode=missing/partial` 和阻塞原因。无论哪种情况都不得交付可见占位。

# HZERO 企业页面契约 Schema

## 契约使用边界
本文件用于约束 HZERO 企业页面交付的契约、证据和待确认项。页面名、业务对象名和相似页面只能提供线索，不能替代新页面契约。

## EnterprisePageContract
用于 HZERO 企业页面新增、修改、审查和 HZERO + Choerodon DataSet 组合页面。

必查字段：
- 子模块路径和页面目录。
- 路由/菜单入口、Tab/openTab 行为和 direct URL 边界。
- 页面容器：`Header + Content`、`PageHeaderWrapper` 或项目封装。
- i18n namespace/key 和 `formatterCollections`。
- 权限码：菜单权限、按钮权限、`front-hzero-permission-button` 固定入口和 Provider 契约。
- 字段清单：字段名、label、类型、必填、展示/查询/提交归属。
- 接口契约：service/model、request 协议或 DataSet transport。
- serviceRequestContract：request helper/import、baseUrlStrategy、envSource、servicePrefix、nativeHttp 是否显式确认；HZERO request 默认内置 API_HOST。
- 上传/导入/导出协议：bucket、UUID、templateCode、endpoint、错误下载、轮询策略。
- Choerodon 边界：DataSet、Pro Form/Table、Lov、Attachment 等交给 Choerodon 规则确认。
- 生产替换清单：临时 mock/demo 契约最终需要替换的权限、字段、接口、i18n、LOV、上传和导入导出项。

输出要求：
- 生产契约缺失时固定进入 Mock demo 候选路径，但不得生成看似 production confirmed 的权限码、service/helper、DataSet transport、上传协议或本地业务 mock；候选值必须标为 `generatedCandidate/mockOnly` 并进入 production replacement。用户拒绝 Mock 或要求真实 API 只形成后续独立集成 advisory；只有当前 Mock 必需契约或 Mock 接线无法闭合时，才输出 `blocked + 待确认项`，不得生成结构骨架或占位页面。
- HZERO owns 工程、路由、权限、i18n 和平台契约；Choerodon owns DataSet 与 Pro 组件细节。

## RouteAccessPacket 交界
页面涉及路由、菜单、Tab 或 direct URL 时，应同步确认：
- 实际 URL、route path、menu path、component。
- authorized、permission/menu、registerRegex。
- remoteEntry/chunk 和父子模块加载状态。

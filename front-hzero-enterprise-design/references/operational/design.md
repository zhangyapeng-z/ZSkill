# 企业前端设计 - 设计与契约

## 阅读路由
- 企业前端设计 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 职责边界
- 编码实现、验证命令、浏览器验收、findings-first review、Handoff 汇总或 Lite 并行汇合不属于本 skill。
- Task Breakdown、Implementation、Review、Verification、Handoff、并发控制、写入范围控制、frontend-stage-result 汇合或 mock 切真实 API replacement slice 归属 `front-hzero-enterprise-process-control`。
- 缺少功能文档或接口列表且只能输出资料清单时，不生成可确认的 Frontend Design。
- 单一 HZERO、Choerodon 或 Figma 事实查询归属对应领域 agent/skill。

## Output Contract
- 设计文档和 Contract Check 必须区分 `confirmed`、`partial`、`generatedCandidate`、`missing`、`conflict` 和 `not-applicable`。
- `contract-check.md` 是契约状态事实源；`frontend-design.md` 引用 Contract Check 结论，不复制完整契约表，除非用户明确要求单文件交付。
- `generatedCandidate` 只表示按规则生成的设计候选，不等于已登记平台契约。
- 接口 URL/method、bucket、templateCode 不得仅凭命名规则生成 confirmed 生产事实。导入导出 required 能力为先生成标准组件时，可按设计/任务规则生成 mock/generatedCandidate `templateCode/importCode/requestUrl/exportRequest/endpoint/queryParams` 候选值，并在 Contract Check / Verification / Handoff 标明来源未确认。
- 生成 `contract-check.md` 前必须按 `contract-asset-discovery.md` 输出 Backend Asset Coverage；未执行兜底搜索时必须写明原因。
- 设计确认前只允许进入待确认或 Task Breakdown 准备，不允许进入 production runnable code。
- 设计文档输出路径默认是 `sdd-workspace/changes/{change-id}/frontend/design/frontend-design.md`。
- Design 阶段默认核心产物是 `frontend-design.md` 和 `contract-check.md`；`frontend-clarifications.md`、`ui-contract.md` 和 `production-replacement-draft.md` 仅按条件生成或内嵌。
- 页面交付、demo-slice 或存在 Feature Root 时，应维护 `sdd-workspace/changes/{change-id}/frontend/index.md` 作为过程入口；该索引只记录路径、状态摘要、当前阶段和开放事项，不复制各产物正文。

## 职责范围
- Frontend Design 阶段需要生成或更新 `sdd-workspace/changes/{change-id}/frontend/design/frontend-design.md`。
- 需要生成或更新 `sdd-workspace/changes/{change-id}/frontend/design/contract-check.md`。
- 需要检查字段、接口、路由、权限、i18n、LOV/lookup、上传、导入、导出、附件、request helper、tenantContext、ID runtime 和 targetPlacement 是否足以进入 Task Breakdown。
- 需要为 route path、routeOpenMode、tabTitle、dws/queryStateKey、permission code、i18n key、lovCode、lookupCode 生成 `generatedCandidate` 并标注来源和确认人。
- 需要按统一前端技术设计模板输出前端技术设计文档、架构设计文档或 UI Contract。

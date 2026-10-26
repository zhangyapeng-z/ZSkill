---
name: front-hzero-attachment
description: 当任务涉及 HZERO + Choerodon 前端附件上传、Attachment、Attachment.Dragger、attachmentUuid、bucketName、bucketDirectory、storageCode、template、附件预览/下载/删除/历史、只读展示、mock/demo 附件候选值或 production replacement 时使用。后端 FileClient 文件身份归 hzero-integrate-file-operation；ChunkUploader 分片上传和 HZERO 新版富文本上传归 front-hzero-common-components。
---

# HZERO 附件前端规范

## Scope
- `front-hzero-attachment` 是 附件 任务的执行入口，不是完整知识库。
- 先用本文件选择 附件 需要的 reference，再按阶段读取细则。
- 附件 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 附件 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 附件 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 附件 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 附件 reference 停止、降级或写入 replacement。

## Reference Routing
- 附件 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 附件 设计/契约/问题门禁：`references/operational/design.md`。
- 附件 实现/修复/工程证据：`references/operational/implementation.md`。
- 附件 审查/反模式/合规：`references/operational/review.md`。
- 附件 验证/构建/运行态/交付收口：`references/operational/verification.md`。
- 附件 其它领域细节：`references/operational/domain.md`。

## Shared Governance
- 附件 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 附件 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 附件 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

# Frontend Compliance Manifest Governance

用途：治理 `frontend-compliance-manifest.md` 的 gate 准入、owner、生命周期和模板边界，避免合规清单继续把所有场景规则复制一遍。

## 阅读路由
- 需要判断某个 gate 是否应该进入 manifest 时读 `Gate Admission`。
- 需要判断 gate 的 owner 和消费阶段时读 `Ownership And Lifecycle`。
- 需要调整模板正文时读 `Template Boundary`。
- 需要判断 gate 合同是否完整时读 `Gate Contract Closure`。

## Gate Admission

只有同时满足以下条件的规则，才允许进入 compliance manifest：

- 它属于生产符合性或 demo 合规性判断，而不是普通流程推进字段。
- 它跨至少两个阶段消费，通常至少会被 Design 和 Review/Verification/Handoff 共同使用。
- 它可以沉淀为稳定 gate，而不是一次性场景说明。
- 它未满足时会影响 `production-compliant / production-candidate / mock-demo-compliant / non-compliant` 中至少一个状态判断。

以下内容不应直接进入 manifest：

- 单个组件 props 说明。
- 单个 API 字段的业务语义解释。
- 某个页面一次性的 UI 设计取舍。
- 只在一个专项 skill 内部有效的局部 SOP。

## Ownership And Lifecycle

manifest 的 gate 必须满足 owner 清晰：

- gate 事实源在 owning reference，例如 mock、route、attachment、import-export、common-components。
- manifest 只负责汇总 gate 状态，不重写 owning reference 的细节。
- Design 负责生成初版 gate 和状态目标。
- Task 负责把 gate 映射到任务验收。
- Implementation 负责消费 gate 并回写偏差。
- Review / Verification / Handoff 负责复核 gate 是否闭合。

如果某个 gate 没有稳定 owner，不应进入 manifest。

## Template Boundary

`frontend-compliance-manifest.md` 模板应该主要承载：

- gate 名称
- 状态
- 证据入口
- requiredFixStage
- 关键字段结构

模板不应长期承载：

- 大段重复的专项规则正文
- 与 owning reference 一字不差的实现细节
- 只对单一场景有效的补充说明

更具体的写法、反模式和判定细则，应继续归属于：

- `hzero-choerodon-production-compliance-gate.md`
- `frontend-ui-runtime-gates.md`
- `generated-code-static-quality-gate.md`
- `hzerojs-submodule-runtime-gate.md`
- 以及对应专项 skill/reference

## Gate Shape

manifest gate 优先复用既有结构：

- `status`
- `blockingReason`
- `requiredFixStage`
- `evidence`

只有某个 gate 无法被通用结构表达时，才使用专门表格或额外字段；此类结构必须能说明为什么不放回 owning reference 或 design contract。

## Gate Contract Closure

gate 进入 manifest 合同前必须能回答：

1. gate 是否真的是生产合规门禁，而不是流程字段。
2. gate 的事实源是否在 owning reference，而不是只写在模板里。
3. `hzero-choerodon-production-compliance-gate.md` 是否已有对应生产合规口径。
4. `schema-checklist.md` 和 `productionCompliance` / `productionCompliance.manifest` 汇合字段是否已有消费边界。
5. 对应 stage agent 是否只保留摘要，未复制整段 gate 细节。
6. 旧 gate 名、旧状态或旧判定口径是否残留。

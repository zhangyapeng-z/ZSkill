# Input Root Multi-Module Discovery

用途：当用户提供目录、workspace、`@` 引用上下文、文档根路径或任意可展开输入根时，约束 Lite / frontend-auto / Explore 在进入设计、任务、编码、Review、Verify 或写操作前，先完成候选模块/功能枚举和执行范围确认。

## 核心原则

- 多模块发现：当用户提供的是目录、workspace、`@` 引用上下文、文档根路径或任意可展开的输入根时，必须先以该输入根为边界枚举全部候选模块/功能；不得因先命中某类文件（如 `tds.md`）就默认只进入其中一个模块。
- 输入根解析：输入根可以来自用户显式路径、`@` 引用、当前会话上下文、已确认的 SDD workspace 或上游交接路径。执行前必须先解析为真实目录，并说明“本次扫描范围为：<resolvedRoot>”。示例：用户提供 `@sdd-workspace` 时，应先解析该引用对应的真实目录，再在该真实目录内枚举候选。
- 候选枚举优先于文档类型筛选：必须先枚举输入根下的一级/二级候选模块、feature root 和可识别文档，再标注每个候选是否包含 FDS/FSD/TDS/MDS/FSS/README/frontend 产物；不得先按 `**/*tds*.md`、`**/*fds*.md` 等单一模式收敛范围。可验证锚点为 `owner=input-root-discovery`、`evidence=resolvedRoot + candidateModules[] + documentStatusMap`、`status=single-candidate | multi-candidate-needs-user | no-candidate-blocked`、`reason=document-type-filter-not-yet-applied`；若 `status=multi-candidate-needs-user`，回退动作只能是整理候选清单并调用 `Input Root Range Confirm`，不得只输出普通文本等待确认。
- 执行范围确认：如果输入根下发现多个候选模块/功能，必须调用 question 工具，使用 `Input Root Range Confirm` 向用户确认执行范围：单个、多个指定项或全部。未确认前只允许只读扫描和候选清单整理；不得只在普通输出中写“需要确认范围”。
- 执行策略确认：当确认范围包含多个候选时，默认建议“并行读取/评估 + shared-scope 串行先行 + feature-scope 并行实现 + handoff-scope 串行收口”。只有 scope partition 已证明无 shared-scope，或 shared contract 已冻结且各 feature lane 写入范围互不交叉时，才允许并行实现；发现父工程配置、全局注册、公共组件/DataSet/service/mock/配置等 shared-scope 改造时，必须先串行处理。可验证锚点为 `owner=input-root-discovery`、`evidence=candidateModules[] + scopePartitionStatus + sharedContractStatus`、`status=range-confirmed-shared-first | range-confirmed-serial-only | range-unconfirmed`、`reason=shared-scope-present | no-shared-scope | user-selected-serial`；回退动作是保持只读扫描、整理候选清单并通过 `Input Root Range Confirm` 确认范围/策略。

## 候选识别

候选模块/功能可以来自以下任一证据：

- 目录结构：输入根下的一级/二级业务目录、`<module>/<feature>` 形态目录、包含 `frontend/` 产物的 feature root。
- 设计文档：`fds.md`、`fsd.md`、`tds.md`、`mds/`、`fss/`、`README.md`、`frontend/design/`、`frontend/index.md`。
- 上游交接：Lite handoff、frontend-stage-result、artifact index、用户明确点名的模块名或功能名。

枚举输出必须区分 `confirmed`、`candidate` 和 `missing`，不得把“有 TDS”作为唯一进入条件；缺少 TDS 但存在 FDS/FSD/FSS/README/frontend 的模块也必须列入候选并说明可推进边界。

## 输出要求

只读扫描完成后，先统一输出：

```text
本次扫描范围：<resolvedRoot>
发现候选：
- <module>/<feature>：文档=<FDS/FSD/TDS/MDS/FSS/README/frontend 状态>；完成度=<ready/partial/missing>；备注=<关键缺口>
建议执行策略：默认并行读取/评估 + shared-scope 串行先行 + feature-scope 并行实现 + handoff-scope 串行收口；原因=<共享风险或独立性判断>
questionGate.template=Input Root Range Confirm；待确认：执行范围=<单个/多个/全部>；执行策略=<shared-first lane model/全部串行/其它>
```

用户未确认范围前，不得调度 Frontend Design、Task、Implementation、Review、Verification、Handoff、后端编码实现或任何写操作。若用户只要求“先分析/先看一下”，可完成只读候选清单和执行建议，但必须明确尚未确认执行范围。

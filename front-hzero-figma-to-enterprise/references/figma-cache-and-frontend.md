# Figma 缓存与 frontend 产物规则

## 阅读路由
- 判断 Figma cache 和 frontend 产物应该写到哪里时读 `目标` 和 `frontend 目录`。
- 设计缓存文件、PageSchema、截图和资源保存策略读 `Figma 缓存策略`、`缓存文件内容`。
- 向 Frontend Design、Task 或 Handoff 交接时读 `交接要求`。
- 防止写错目录、污染目标工程或重复抓取时读 `反模式`。

## 目标
Figma 链接读取后应形成可复用设计证据，避免同一链接或 node 在多轮中重复读取、重复解析和重复消耗上下文。Figma cache、PageSchema、UI Contract seeds 和资源清单必须归入当前 Change Root 下的 `frontend/`，不写入目标前端工程。

## frontend 目录
所有前端执行期、验证期、交付期和 Figma cache 产物统一写入当前 SDD 项目根下的 `sdd-workspace/changes/{change-id}/frontend/`，不写入目标前端工程内部、目标前端工程平级外部目录、子模块内部、`.opencode`、`docs` 或其它内部资料目录。

Frontend Design 阶段需要纳入前后端统一确认的前端设计契约也写入 `sdd-workspace/changes/{change-id}/frontend/`；Figma cache、工程探索 evidence、task-status、verification、review、handoff 和最终前端资产索引同样写入该目录。TDS 主文档仍位于 Change Root 的 `tds.md`。

定位规则：
- Change Root 是 `sdd-workspace/changes/{change-id}/`。
- Frontend Root 是 `sdd-workspace/changes/{change-id}/frontend/`。
- 如果 change-id、模块名、功能名、父工程、已有子模块或新建子模块落点不明确，必须先确认 Change Root、Frontend Root 和目标前端工程目录，再创建或写入 `sdd-workspace/changes/{change-id}/frontend/`。

推荐结构：

```text
sdd-workspace/
  changes/
    {change-id}/
      mds/
      fds.md
      tds.md
      fss/
      frontend/
        index.md
        evidence/
          evidence.md
        design/
          contract-check.md
          frontend-design.md
          frontend-clarifications.md
          ui-readback.md
          ui-contract.md
          production-replacement-draft.md
        tasks/
          task-breakdown.md
          task-status.md
        verification/
          verification-report.md
        review/
          pre-review.md
          final-review.md
        handoff/
          production-replacement-checklist.md
          artifact-index.md
          frontend-handoff.md
        figma-cache/
          <fileKey>/
            <nodeId-normalized>/
              figma-source.json
              page-schema.json
              ui-contract-seeds.json
              assets-manifest.json
              readme.md
```

`{change-id}` 是本轮增量变更的归档键。同一 Change 涉及多个页面或文件时，仍归入同一个 `sdd-workspace/changes/{change-id}/frontend/`，在设计和任务文档里用模块、功能或文件组区分。

## Figma 缓存策略
- Figma 阶段必须先走产物目录读取：定位 `sdd-workspace/changes/{change-id}/frontend/` 后，优先读取 `index.md`、`handoff/artifact-index.md`、`figma-cache/**/readme.md`、`figma-cache/**/page-schema.json`、`figma-cache/**/ui-contract-seeds.json`、`figma-cache/**/ui-contract-seeds.md` 和 `figma-cache/**/assets-manifest.json`，再决定是否需要请求 Figma 链接。
- 读取 Figma URL 后，应优先把原始 Framelink/Figma JSON、解析后的 PageSchema、UI Contract seeds 和资源清单缓存到 `sdd-workspace/changes/{change-id}/frontend/figma-cache/`，并同步 `index.md` 的 figma-cache source、Current Stage 和 Open Items。
- Figma API / Framelink 返回 429 rate limit 时，也必须写回稳定产物：`figma-cache/<fileKey>/<nodeId>/readme.md`、可生成的 `page-schema.json` 降级字段、`frontend/index.md` 的 figma-cache 状态和 Open Items。不得只在对话中说明 429。
- 缓存 key 使用 `fileKey + nodeId`；`nodeId` 需做文件名安全化，例如把 `:` 替换为 `-`。
- 如果用户只要求短答且未授权写文件，可以在对话中输出 PageSchema 摘要，并标记 `Figma 缓存状态：未写入`。
- 进入设计文档、跨轮开发、代码生成或验证闭环时，应写入或更新缓存文件；无法写入时说明原因和后续需要。
- 后续请求引用相同 Figma link/node 时，先检查 `sdd-workspace/changes/{change-id}/frontend/figma-cache/` 是否已有可用缓存；缓存存在且输入 link/node 未变时，优先复用缓存摘要，不重复读取 Figma。
- 如果 Figma link、node id、设计更新时间、用户明确说明设计已变，或缓存缺少必要节点，应重新读取并更新缓存；如果只是缺少局部区域或资源，只补读缺失区域/资源，不从头读取整个节点。
- 缓存命中但没有本轮重新请求 Figma 时，输出状态应为 `cache-only` 或 `confirmed-from-cache`，并说明缓存路径、缓存有效性和仍需补读的区域；不得写成“本轮已读取 Figma”。

## 缓存文件内容
- `figma-source.json`：原始 Framelink/Figma 响应或等价结构化数据。
- `page-schema.json`：由脚本或模型复核后的 PageSchema，必须保留 confirmed / inferred / missing。
- `ui-contract-seeds.json` 或 `ui-contract-seeds.md`：Figma/PageSchema 到 HZERO/Choerodon 组件约束的区域级 seeds。
- `assets-manifest.json`：导出图片、图标、切图、组件资源的来源、文件名和使用位置。
- `readme.md`：读取时间、来源链接、fileKey、nodeId、缓存有效性、待确认事项。

`readme.md` 必须额外记录 Figma 获取状态：

| field | value |
| --- | --- |
| figmaFetchStatus | success / partial / rate-limited-429 / permission-denied / node-not-found / failed / cache-only / not-applicable |
| figmaFetchErrorCode | 429 / 403 / 404 / timeout / unknown / not-applicable |
| figmaFetchErrorMessage |  |
| rawErrorShape | http-status / json-error / tool-exception / stderr-text / empty-with-message / empty-response / unknown / not-applicable |
| rawErrorExcerpt | 原始错误摘要，避免长日志 |
| normalizedReason | rate-limit / permission / not-found / timeout / parse-failed / unknown / not-applicable |
| attemptedCount |  |
| cacheUsable | yes / no |
| fallbackMode | confirmed-from-cache / cache-only / screenshot-only / figma-unverified / not-applicable |
| partialReadNodes |  |
| missingNodes |  |
| retryPlan | 分批目标、建议等待时间、下一次可重试条件 |

当 `figmaFetchStatus=rate-limited-429` 时：
- 429 可来自不同工具格式；只要 HTTP status、error code、异常 message、stderr 或工具输出包含 429 / rate limit / too many requests / quota exceeded 等语义，均归一化为 `rate-limited-429`，并保留 `rawErrorShape/rawErrorExcerpt/normalizedReason`。
- `page-schema.json` 中 `source.fetchStatus` 必须为 `rate-limited-429`。
- 若存在可用缓存，`figmaStatus` 只能为 `confirmed-from-cache` 或 `cache-only`，并写明缓存有效性。
- 若无缓存或缓存不足，`figmaStatus` 必须为 `figma-unverified`，只允许输出 partial/inferred 视觉结论。
- `frontend/index.md` 必须把该 429 写入 `Open Items`，并指向 retryPlan。

当工具返回空失败且无法识别错误语义时：
- `figmaFetchStatus=failed`、`figmaFetchErrorCode=unknown`、`rawErrorShape=empty-response / unknown`、`normalizedReason=unknown`。
- 若无可用缓存，`figmaStatus=figma-unverified`，并把 retryPlan 或需要更精确 selection link 写入 Open Items。
- 不得把空失败写成 `confirmed-from-cache`，除非 readme/page-schema 中已有同 fileKey + nodeId 的可用缓存证据。

## 交接要求
Figma 分析输出应包含：
- Figma 文件路径：`sdd-workspace/changes/{change-id}/frontend/figma-cache/...`
- 缓存状态：新建 / 更新 / 复用 / 未写入
- Figma 获取状态：success / partial / rate-limited-429 / permission-denied / node-not-found / failed / cache-only / not-applicable
- 429 / 读取失败回写路径：readme.md / page-schema.json / frontend/index.md / not-persisted + reason
- PageSchema 文件路径：如已生成则给出相对路径
- UI Contract seeds 文件路径：如已生成则给出相对路径
- 设计输入边界：Figma 确认项、推断项、待确认业务契约
- 后续开发入口：设计文档路径或 enterprise handoff metadata

## 反模式
- 每轮都重新读取同一个 Figma node，却不检查缓存。
- 已有 `figma-cache/page-schema.json` 或 artifact-index 指向可用缓存时，仍直接请求同一 Figma 链接。
- 有 PageSchema 但没有 UI Contract seeds，就把 Figma 映射交给实现阶段。
- 局部缺资源时重新拉取整个大节点，而不是补读缺失区域。
- 只在对话里保留 PageSchema，导致跨轮无法复用。
- 把 Figma 缓存写入 `.opencode` 运行资产。
- 把 Figma 视觉字段当成真实业务字段、接口或权限。

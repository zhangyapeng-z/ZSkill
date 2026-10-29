# 企业前端流程控制 - 设计与契约

## 阅读路由
- 企业前端流程控制 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 职责边界
- Frontend Design 阶段的 `frontend-design.md`、`contract-check.md`、UI Contract、候选编码或目标落位归属 `front-hzero-enterprise-design`。
- 单个组件 API、HZERO 路由事实、Choerodon DataSet 写法或 Figma 解析归属对应领域 agent/skill。

## Output Contract
- 执行、验证、Review 和 Handoff 阶段不得修改 `frontend/design/` 中的设计事实源。并行启动后确需改变 frozen Design/Contract 时，必须返回 `parallel-baseline-invalidated`，由 Lite 受权后创建新 Design revision 和全新并行身份；不得显式回到普通 Frontend Design / Contract Check 继续旧 run。
- 非 Implementation 阶段不得修改目标前端工程业务代码；需要修复时回到 Implementation 或输出 write-scope/question gate。
- `production-ready` 只能在 contract、review、buildable、reachable、usable、write scope、tenantContext、backendApiReadiness 和 productionReplacementTrigger 均满足对应模板条件时输出。
- `conditional` 和 `blocked` 必须带状态来源、未验证项和下一步；输入出现非 canonical 交付状态时按 `invalid-stage-result` 回原 owning stage，不做状态映射。
- `frontend/index.md` 是跨轮恢复和阶段换手入口；`handoff/artifact-index.md` 是最终交付索引。两者冲突时以 canonical sources 修正。
- 用户可见最终输出必须通过 `final-output-quality-gate.md`：发送前删除无意义字符、乱码、错别字、重复字和未解释残留词；验证结论使用固定格式 `验证：<command>，<passed/failed/not-run>。` 或等价矩阵。

## 职责范围
- 需要编排或检查 Explore -> Design -> Task -> Implementation -> Review -> Verification -> Handoff 的前端执行流程。
- 需要处理 Lite 前后端并行、前端内部多 slice 并行、共享文件锁、integration task、状态回写或汇合判定。
- 需要判断已有文件写入范围、`edit` 权限边界、dirty/conflict、只读参考文件转可写或是否需要用户确认。
- 需要生成或校验 `frontend-stage-result`、`task-status.md`、verification report、artifact index、handoff summary 或 production replacement checklist。
- 后端 API readiness 已闭合，需要记录独立联调测试准备、production replacement advisory，或按前端自身证据清理 local-filter / inline mock 违规；不得据此自动把 mock-request / partial 前端切换到 production-transport。

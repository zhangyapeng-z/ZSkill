# 企业前端流程控制 - Verification

## 阅读路由
- 进入 `frontend-verify-agent` 时读取本文件和 `templates/verification-report.md`。
- 页面行为清单读取 `templates/manual-checklist.md`；validator 命令、字段和值域读取 `frontend-validator-rule-index.md` 和对应脚本，不在 Agent 中重复枚举。
- 构建诊断命中时读取 `front-hzero-build-deploy`；领域 validator 只按 changedFiles、Task required validators、Review finding 或用户目标触发。

## 验证分层
- V0：插件内置静态 validator、路径/placement/contract/manifest 对账；修改代码后执行。
- V1：lint/typecheck/tsc，按目标 package 或最小 workspace 范围执行。
- V2：build/compile，页面交付默认必须尝试；优先目标 package 或根工程最小可证明命令。
- V4：已有项目测试命令仅在 Task、Review finding 或用户目标要求时执行；Verification 不自行搜索和扩展单元测试资产。
- Runtime Acceptance：独立于 Verification。Verification 不启动 dev server、不操作浏览器，只消费外部/用户证据或输出手工清单。

## 阶段算法
1. 从 package manager、scripts、workspace 和 Design/Task handoff 发现最小合法命令，不凭经验编造。
2. 检查依赖就绪。缺依赖时运行可行 V0，V1/V2 写 `not-run + blocked-by-missing-dependencies`，`buildable=unknown`，不误报代码失败。
3. 执行 required validators 和目标范围 typecheck/build/compile；真实记录 command、cwd、target、exit status、duration 和证据路径。
4. 修复后只重跑 fingerprint invalidated 的命令，复用未失效 passed 结果；最终只做一次 aggregation。
5. 将页面行为、Network、console、状态流转、滚动和视觉项写入 manual checklist；没有外部 runtime evidence 时保持 `reachable/usable=unknown`。
6. 失败项按 `frontend-validator-fix-routing.md` 输出 direct-fix、owner-needed、design-needed、user-needed 或 blocked；Verification 不修改业务代码。
7. `repair-fast-lane` 只跑 V0 与依赖就绪时的 V1，复用未失效结果；V0/V1 failure、targetFiles 扩大、shared file、contract delta 或 source evidence 缺失时退出 fast lane 并回标准 regular-change。通过只形成 `flowCutoff=after-verification` 的最小结果，不声明 Handoff ready 或 production-ready。

## 风险域索引
- `query-table`、`row-actions`、`master-detail` -> `front-hzero-choerodon-ui`。
- `f-layout`、`customization` -> `front-hzero-enterprise-page`；`performance` -> `front-hzero-build-deploy`。
- route/runtime、mock-request、Attachment、import/export、renderer、PermissionButton、common components 按对应 owner verification reference。
- 未采用参考实现时不运行 reference quality gate；只有 `referenceReuseIntent=adopt` 或实现来源证明实际采用时才消费结果。

## 结果边界
- Verification 只输出命令、validator、buildable/reachable/usable 事实和 repair/backfill 建议，不根据验证事实单独声明最终 `production-ready`。
- build/compile 通过只证明 `buildable=true`；运行态缺失进入 conditional，不反复回 Verification。
- required compile/build 实际失败且可定位时进入修复；环境不可用且允许降级时保留 `not-run + reason`。

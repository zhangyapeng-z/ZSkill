# 前端 Skill 通用治理

## 阅读路由
- 判断任一 `front-hzero-*` skill 的入口结构、输出合同、停止/降级规则或验证收口是否需要统一口径时读取本文件。
- 普通领域任务只需要按领域 skill 的 `SKILL.md` 读取阶段 reference；只有遇到状态、production-ready、mock/demo 或 replacement 判定冲突时才回到本文件。

## Owner
- `front-hzero-enterprise-process-control` 是前端 skill 通用治理 owner。
- 领域证据、模式和拒收项归领域 skill；跨 skill 状态词、输出层级、降级语义和验证收口归本文件。
- 其它 skill 不直接引用本文件内部路径；只引用 `front-hzero-enterprise-process-control` 作为 owner，避免 packaged skill internal path 泄漏。

## Source Priority
- 用户确认、FDS/TDS/API、目标工程源码、运行日志、命中场景的 `front-hzero-*` 专项 skill 和已加载 owner reference 都是证据来源，但适用范围不同，不能混用优先级。
- 业务事实由用户确认、FDS/TDS/API、目标工程源码或运行日志支撑，包括业务字段、接口路径、权限码、租户规则、平台登记值、生产配置和运行状态。通用治理和领域 reference 不凭空产生这些业务事实。
- 规范事实优先由命中场景的 `front-hzero-*` 专项 skill 及其已加载 owner reference 支撑，包括内置标准 import 坐标、固定 helper、标准 UI 形态、禁止形态、validator ruleId 和阶段拒收项。目标工程证据只能补充、确认 project wrapper/override、证明兼容性或证明冲突；目标工程缺相似页面、缺 import 样例或缺 wrapper 证据时，不得把内置规范事实降级为 `partial`、`missing`、`generatedCandidate` 或替换成常见但未确认的工程坐标。
- 可见业务 UI 或 required 标准能力的选择顺序固定为：命中场景的 `front-hzero-*` 专项 skill / HZERO / Choerodon 内置组件规则 -> 项目 confirmed 组件或 wrapper -> 原生 DOM fallback。项目 confirmed wrapper 只有在等价承载标准能力、未命中 legacy/anti-pattern 且不削弱 owner 规则时才可采用；专项 skill 已固化为“必须使用标准组件/helper”的场景，不得再用项目 wrapper 或原生 DOM fallback 替代。
- `generatedCandidate` 只承接业务参数、平台编码、路径、权限码、mock/demo 值、生产配置和运行验证缺口；不得用于表示内置标准坐标、固定 helper 或标准 UI 形态可以被任意替换。
- 领域 skill 与本文件冲突时，保留领域规范事实，回到 process-control 判断状态、replacement、handoff 和 production-ready 口径；若目标工程证据与领域 reference 明确冲突，必须记录 `conflict` 并回 Design/Task/Review 处理，不能静默选择非规范兜底。

## Status Vocabulary
- `confirmed`：有用户、设计、接口、源码、运行日志或目标工程证据支撑。
- `generatedCandidate`：可用于候选实现或 mock/demo，但生产事实未确认。
- `missing`：必需事实缺失，当前阶段不能声称闭合。
- `partial`：部分能力可用，但关键运行、契约或生产替换仍未闭合。
- `blocked`：缺少外部输入、权限、后端、配置或工程条件，当前无法继续验证或实现。
- `not-applicable`：当前任务明确不涉及该能力，并记录原因。
- `passed` / `failed` / `not-run`：只用于命令、检查或验证项结果。

## Output Contract
- 输出必须区分任务场景、已读取资源、已确认工程证据、未确认项和下一步。
- 领域实现或审查必须引用对应领域 reference/template 的 contract、proof、checklist 或 finding，不用通用治理替代领域证据。
- 验证结论必须写明命令、浏览器检查或运行态证据，并标记 passed、failed、blocked 或 not-run。
- Handoff 必须列出 production replacement、owner、剩余契约缺口和运行风险。

## Stop And Degrade
- required 契约缺失且未允许 mock/demo 降级时，停止并回到设计、Contract Check 或流程 gate。
- 运行事实不足时只能标记 generatedCandidate、partial 或 blocked，不得自行宣布 production-ready。
- required HZERO/Choerodon 能力不得降级为普通按钮、本地状态、静态列表、disabled/no-op、常见但未确认的项目坐标或未验证 wrapper，除非命中场景的专项 skill / owner reference 明确允许，或目标工程源码证明存在不削弱 owner 规则的兼容 project wrapper/override。
- mock/demo、业务参数 generatedCandidate 或 runtime 未验证必须保留 verification 记录；内置 Standard Component Coordinates 本身不需要 replacement。
- HZERO/Choerodon 标准 UI 形态、helper 签名和组件入口已经由领域 reference 固化时，`generatedCandidate` 只表示业务参数或运行验证待补；内置 Standard Component Coordinates 直接按规范事实处理，设计/任务/实现/审查不得因目标工程缺证据而标成 `partial/missing` 或回退为裸 JSX、手写 Form、普通 Button、自建 wrapper、兼容 adapter、`command` 函数或其它“等价实现”。缺 import/export 且不是内置标准坐标时修复坐标或阻塞；缺业务参数时仍按标准组件/helper 落代码并记录 verification/handoff 缺口。
- 标准能力参数缺口通用适用于导入、导出、权限按钮、附件、LOV/lookup、renderer/operator helper、HZERO 通用组件等领域：只缺 `templateCode/importCode/requestUrl/exportRequest/endpoint/queryParams`、`permissionCode/permissionList`、`bucketName/storageCode/template`、`lovCode/lookupCode`、renderer item 参数、tenantContext 或运行验证证据时，应生成 `mockOnly/generatedCandidate` 参数、候选常量或候选权限码继续接标准组件/helper；权限载荷默认写成 `permissionList` 对象数组，不因缺 confirmed 权限码改成字符串数组或 `codeList`。不得因此跳过 required 组件、改成普通 Button/Upload/下载链接、输出合同占位、显示 replacement 文案、永久 disabled/no-op 或隐藏 required 入口。只有缺少可渲染组件来源、固定 helper 不存在、组件 exportShape 冲突、关键字段/value 结构缺失或领域 reference 明确不可实例化时，才阻塞或回 Design/Task 补契约。

## Global Delivery Decisions
| decision | owner verdict | process effect |
| --- | --- | --- |
| 默认 Mock demo | 新模块页面开发、mock/demo 页面开发或新增/改造可运行数据页面，在企业前端编排中固定进入 `frontendExecutionMode=demo-slice`，并记录 `runtimeDataPathDecision=requestable-demo-mock`、`queryMode=mock-request`。用户要求真实 API 或 production-ready 也不跳过本阶段，后续转独立联调测试。 | 不重复提问；必须保留 `uncoveredProductionGates`、verification 缺口和 production replacement advisory。 |
| production-ready 输入缺失 | 缺少 FDS/TDS/元数据/前端设计且任务要求 production-ready 时必须阻塞。 | 不得用 mock/demo、generatedCandidate、静态骨架或 code-only 宣称生产闭合。 |
| 主流程确认边界 | 影响当前 Mock demo 的 route/menu、权限码、API 契约、前端工程落点或接受与用户目标冲突的非默认条件性交付，必须回 `hzero-auto-agent-lite`。production-ready/真实 API 目标只记录后续独立集成与稳定化提示，不触发本轮切换。 | 前端子模块只能处理局部确认，不决定全局交付语义。 |
| Missing Contract Confirm | 关键契约缺失且影响当前 Mock demo 的 runnable/handoff 状态时，必须停在 question gate；production-ready、拒绝 Mock 或真实 API 诉求本身只形成后续 advisory。 | 未 resolved 前不得进入当前 Mock runnable 路径；真实传输由独立联调测试承接。 |

## Production Ready Boundary
- `production-ready` 只能由 process-control 口径汇总判断，不能由单个领域 skill 单独宣布。
- 生产就绪至少需要 contract、review、buildable、reachable、usable、write scope、tenantContext、backendApiReadiness 和 productionReplacementTrigger 满足对应模板条件。
- dev server、mock/demo、静态自查或单一 build 成功不能替代 production-ready。

## Admission Boundary
- 只有跨两个以上前端 skill、影响两个以上阶段、需要统一状态或统一 fallback 的规则才进入本文件。
- 单一组件、页面、路由、构建或 mock 细则留在对应领域 skill 的阶段 reference。
- 本文件只定义跨 skill 语义契约；领域 `SKILL.md` 只保留运行期入口和 owner 引用。

# Performance Scenario

## 阅读路由

- Active owner: `front-hzero-build-deploy`.
- 触发词：性能、加载慢、大表、渲染卡顿、bundle、chunk、构建体积、首屏、验证耗时。

## Scope

性能是构建、运行和验证诊断场景，不再作为常规阶段独立 skill。构建命令、dev server、产物加载、chunk、verification level 和性能验证记录归 `front-hzero-build-deploy`；页面结构或组件写法导致的性能风险回到对应 enterprise page / Choerodon UI owner。

## Stage Routing

- Design：仅在用户要求性能目标或页面存在明显大数据/大表风险时记录预算和验证口径。
- Implementation：避免明显重复渲染、无界列表、无来源大依赖和不必要 wrapper。
- Review：检查大表、重复请求、渲染 helper、依赖漂移和 bundle 风险。
- Verification：记录构建、首屏、交互、网络、chunk 加载或用户指定性能命令；未运行必须写 not-run reason。

## Triage Layers

性能排查必须先分层，不得在未确认前直接归因于 bundle 或组件库：

1. 首屏资源加载：HTML、runtime、remoteEntry、首屏 chunk、CSS、字体和静态资源。
2. 远程模块或远程访问路径：`PACKAGE_PUBLIC_URL`、`microConfig`、`mfRemotes`、remoteEntry URL、chunk 404 / timeout。
3. 接口并发与等待时间：首屏接口数量、慢接口、串行等待、重复请求、失败重试。
4. 渲染计算与 DataSet 转换：大表、列数、renderer、computedProps、`toData()` / `toJSONData()`、transformRequest / transformResponse。
5. 多 Tab / 多列表 / inactive tab：隐藏 Tab 是否提前构造 DataSet、发起查询或渲染大表格。

## Evidence Checklist

需要尽量收集或在 not-run reason 中说明缺失：
- 数据量、列数、Tab 数量、首屏接口数量、是否使用 DataSet、是否涉及动态远程模块。
- Network waterfall、关键资源体积、remoteEntry/chunk 请求、失败 URL 和 HTTP 状态。
- 构建产物或分析命令证据；项目没有脚本时只能建议确认 scripts，不编造 `build:analyze`、Lighthouse 或 Treemap 命令。
- 浏览器交互证据：首屏可见时间、Tab 切换、查询/分页、大表滚动、保存/刷新后的卡顿点。
- Verification 未运行真实浏览器或构建时，必须写 `not-run + reason`，不得把 typecheck/build 通过等同性能通过。

## Scenario Checks

### 首屏慢或白屏久
- 区分资源下载、远程包注册、接口阻塞和页面渲染阻塞。
- 检查首屏是否加载不必要子模块、重型页面、inactive tab 或大表。
- 需要 Network waterfall、关键资源体积和首屏接口数量；未确认前不直接归因于 bundle。

### bundle / chunk 体积大
- 先确认项目是否有分析产物或构建分析脚本。
- 检查重复依赖、同步引入重型模块、聚合导入和不必要首屏依赖。
- 优化建议优先拆首屏路径或按需加载，不做无来源大重构。

### DataSet 大数据卡顿
- 检查渲染期是否频繁调用 `dataSet.toData()` / `toJSONData()`。
- 检查大列表 renderer、computedProps、formatter、transformRequest / transformResponse 是否重复计算。
- 优先考虑分页、虚拟滚动、精简 renderer、按需迭代和减少主线程转换；未确认数据量、列数和交互复杂度前，不直接建议替换表格组件。

### 多 Tab / 多列表卡顿
- 检查 inactive tab 是否提前构造 DataSet、发起查询或渲染大表格。
- 优先考虑激活后构造、激活后查询和保留必要缓存。
- 切换 Tab 是否必须保留编辑态、选择态或查询态必须由 UI Contract / 用户确认决定。

### loading 或交互卡顿
- 区分网络响应耗时、服务端处理耗时、主线程计算阻塞和重复 set state / DataSet 变更。
- 检查大范围重渲染、重型 formatter、频繁校验和批量状态变更。
- Spin 动画在 JS 高负载下卡顿时，不要误判为请求未返回。

### 远程资源或微前端加载慢
- 检查 remoteEntry、chunk、microConfig、运行时 mfRemotes、远程访问路径和 registerRegex 对首屏加载的影响。
- 结合 `front-hzero-micro` / `front-hzero-build-deploy` 的构建部署链路确认 public url、产物路径、资源体积或注册策略问题。
- 不把远程加载慢直接归为页面代码问题。

## Rejection Anchors

- 未确认数据规模就建议 `PerformanceTable` 或替换组件库。
- 未区分资源问题、接口问题、远程模块问题和渲染问题。
- 不看 inactive tab 就只优化当前可见表格。
- 在渲染路径上继续增加格式化、`toData()` 或深拷贝转换。
- 编造项目不存在的分析命令、性能指标或构建脚本。
- 只跑 build/typecheck 就声明性能验证通过。

## Owner Source

新增规则只写入本 reference 或 build-deploy owner references。

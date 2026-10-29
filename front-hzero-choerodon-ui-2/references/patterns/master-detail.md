# Choerodon 主从 / 头行

用于 header-line、parent-child、order-lines 和主从页面。

## 最小形态
- Parent DataSet 负责头字段、查询/详情加载以及父级提交边界。
- Child DataSet 负责行字段、行编辑、选择、delete/remove 以及行提交边界。
- 关系必须明确：`children + cascadeParams`、已确认的 parent key、已确认的 child foreign key，或已确认的后端嵌套 payload。

## 建模流程
- 确认后端返回的是嵌套子行、独立的头/详情 endpoint，还是独立的行查询 endpoint。
- 确认 parent primary key、child primary key、child foreign key，以及父级保存前行数据是否允许存在。
- 选择提交策略：
  - parent 提交嵌套 dirty children
  - parent 和 child 分开提交
  - child 行只在 parent 保存后再提交
  - 后端统一处理 header-line 提交
- 如果 child 查询依赖 parent，可用 `children + cascadeParams` 建模，或在 parent load 后显式执行 child DataSet query。
- 如果 child 表需要筛选区，应把查询字段放入 child DataSet 的 `queryFields` 或显式 `queryDataSet`，并让 child DataSet 持有查询关系；Table 只通过 `dataSet + queryBar` 展示筛选入口。
- 如果 FDS/TDS/UI Contract 写明 child 表“列表头按钮区”“表格工具栏”“明细表工具栏按钮区”，默认落到 child Table 的 `buttons` 属性或项目等价封装，而不是 Table 外手写页面 toolbar。
- 如果需要行内编辑，应结合 `table-inline-edit.md`；列应使用 DataSet 字段元数据和已确认的 editor 规则。
- 如果需要弹窗行编辑，应结合 `form-edit.md`；modal submit 更新 child DataSet，或调用已确认的 service。

## Non-runnable 骨架
- Parent 字段、primary key、detail endpoint 和 submit payload：待确认。
- Child 字段、primary key、parent mapping、row edit mode、delete mode 和 submit payload：待确认。
- Cascade/query relation：待确认。
- 保存顺序和刷新行为：待确认。

## 护栏规则
- 不要仅因为 UI 上有头和行，就假定后端一定是嵌套 payload。
- 不要编造 parent/child key，例如 `headerId`、`lineId` 或 `orderId`。
- 当 DataSet 应负责行记录时，不要把本地数组当成唯一事实来源。
- 不要把 child 查询 DataSet 当成 Table prop 传入；不要用 Table `onQuery/onReset` 兜 child 查询主链路，除非项目封装有证据。
- 主从详情页必须区分页面级按钮区、child 表工具栏按钮区和 child 行操作列；三者不能互相替代。
- child 表工具栏按钮（如新建、保存、删除、导出）和行操作列（如编辑、删除）必须在设计/任务的 `Contract Acceptance`、`UI Acceptance`、`Verification Acceptance` 中逐项列出。
- child 表工具栏按钮必须优先使用 Choerodon Pro Table `buttons` 或项目 confirmed wrapper，例如 `['add', ['save', saveConfig], ['delete', deleteConfig], 'export']` 绑定到 child Table。Table 外手写 `<div className="*-toolbar">` 只在项目统一封装或相似页面证据明确要求时允许；否则按 Table 模式偏差处理。按钮位置在表格上方不代表实现方式可以脱离 Table `buttons`。
- 头行/详情页通常由 HZERO `Content` 或页面容器承担主滚动；child 明细表默认自然撑开，不使用 `autoHeight={{ type: TableAutoHeightType.maxHeight, ... }}` 或等价动态 max-height。该配置只适合单一列表页、固定查询区 + 主表格页；放在详情底部明细表时会在滚到底部后因表格高度重算改变页面总高度，导致页面滚动位置反复修正。若确需限制明细表高度，必须使用有来源的稳定容器高度或明确 `height`，并把底部滚动不抖动列入验证。
- 编辑态必须有稳定来源。若 URL 显式表达编辑意图（例如 `editFlag=Y`），详情加载后的状态守卫不得无条件覆盖该意图；应明确合并规则并验证刷新场景。
- 编辑态必须拆分三类状态源：UI 编辑意图（如 `editFlag=Y`）、业务状态守卫（如 `NEW/REJECTED` 可编辑）、异步加载状态（后端/seed 返回的当前记录状态）。不要用一个 `editable` state 同时驱动 DataSet 创建、按钮显隐和业务动作守卫。
- 页面最终编辑 UI 可以按设计采用 `routeEditable && statusEditable` 或其它明确规则，但保存/提交/取消/删除等动作入口必须独立校验业务状态，不能只因为 `editFlag=Y` 放行。
- 异步加载出来的状态必须绑定当前 parent/header id。切换单据、路由参数变化或 Tab 复用组件时，必须清空旧状态，或使用 `loadedHeaderId/loadedRecordId` 防止旧单据状态短暂放行新单据。
- 若状态加载未完成，默认不得放行保存/提交/取消/删除/明细编辑；可以显示 loading、禁用按钮或等待当前记录状态就绪。
- 在 delete/remove 语义和后端协议确认前，不要远程删除 child 行。

## 验证
- 验证 parent load、child load、child 查询条显示与查询、加行、编辑行、删除/移除行、校验、保存顺序、保存失败行为、保存后刷新以及刷新后编辑态保持。
- 验证 child Table 工具栏按钮来自 Table `buttons` / 项目等价封装，且需求要求的新增、保存、删除、导出等按钮逐项可见、可用或有明确禁用原因。
- 验证长详情滚动：小视口、长表单、多明细行、连续新增多行后滚到底部，页面应可达最后一区块且不出现底部来回滚动；若 child Table 使用任何高度/overflow/autoHeight 配置，必须记录滚动容器和高度来源。
- 额外验证编辑态状态源：从列表编辑进入、直接刷新编辑 URL、切换不同 header id、不可编辑状态带 `editFlag=Y`、状态加载中等场景，均不得出现旧状态复用或动作守卫绕过。
- 实现交接前运行最终 build/compile，或基于命令/证据明确标注阻塞。

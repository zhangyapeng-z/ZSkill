# Choerodon DataSet Mock Transport

## 目录
- 目标
- 标准链路
- 实现要求
- 状态流转要求
- Review 阻塞条件
- 验证要求
- 可抽象链路模板

## 目标
约束 Choerodon UI Pro DataSet 页面在 mock/demo 下的可运行数据来源，确保 DataSet、service 和动作按钮通过同一套 HZERO 本地 devServer HTTP mock API 工作。

## 标准链路
```text
业务页面 / DataSet / service
  -> HTTP request
  -> HZERO / Webpack / Umi devServer middleware
  -> mock route handler
  -> dev-only runtime store
  -> HTTP response
```

## 实现要求
- DataSet `transport.read` 必须请求 HZERO 本地 devServer middleware 暴露的 mock API。
- 保存、提交、废弃、撤销、删除、复制、撤回等 action service 必须请求 mock API，不得只在页面或 service 内部改本地变量。
- mock API 的 route、store 和状态机应集中放在目标工程确认的 mock 目录或 devServer 扩展模块下，避免散落在页面组件里。
- runtime store 只服务本地 devServer mock API，不进入生产构建或部署配置。
- response shape 必须先与当前 DataSet/service 消费端对齐，再与后续真实 API 候选 shape 对账。实现前必须确认目标 DataSet 的 `dataKey/totalKey`、`transport.adapter`、项目 request adapter、service action unwrap 逻辑或同工程可工作 mock 样例。消费端直接消费裸数组/裸实体时，mock 列表、详情、LOV、新建、更新和 action 返回裸数组/裸实体；只有消费端明确需要分页对象、项目 adapter 或 envelope 时，才返回 `{ content, totalElements }`、`{ data: ... }` 或项目等价结构。真实 API 候选与当前 mock 消费 shape 不一致时，差异必须进入 production replacement checklist。
- 默认不得新增 `body-parser`、`msw`、`json-server`、`mockjs`、`faker` 等依赖。POST/PUT body 优先复用项目已有 JSON parser，缺失时在 mock 模块内使用轻量 `readJsonBody`。

## 状态流转要求
- store 初始化、列表查询、详情读取、明细读取和动作修改必须读写同一个 runtime store。
- 动作后刷新链路必须可解释为 `action request -> mock route -> mutate runtime store -> DataSet query/detail -> mock route returns current state`。
- delete 后列表刷新不得复现已删记录。
- submit、withdraw、abandon、cancel 后重新 query 列表和详情，状态码和 meaning 必须保持一致。
- UI guard 和 action guard 必须使用同一状态规则；按钮隐藏或禁用后仍可通过 action 成功修改状态时，应在 Review 中标为缺陷。

## Review 阻塞条件
- DataSet `transport.read` 没有请求有效 mock API。
- mock API 请求正常返回，但 response shape 与 DataSet/service 消费端不一致，例如 DataSet 直接消费裸数组却返回 `{ data: [...] }`、详情直接消费实体却返回 `{ data: entity }`、或消费端需要 `dataKey/totalKey` 分页对象但 handler 返回裸数组。
- action service 没有请求 mock API，而是在页面、DataSet 或 service 内部维护第二套数据源。
- mock middleware 没有通过目标工程既有 HZERO / Webpack / Umi devServer 扩展点注册。
- 为 mock 改造生产构建、微前端注册、`remoteEntry`、`microConfig`、public path 或部署配置。
- 列表、详情、明细和动作函数读写不同数据源，导致刷新后状态回退或数据不一致。
- 为 mock 新增依赖但没有项目既有约定或用户确认。
- `queryMode=mock-request` 被声明为 `production-ready`。

## 验证要求
- 打开列表页，确认表格有数据。
- 点击查询、重置、刷新、分页，确认 Network/console 无 `Invalid URL`。
- 记录 mock API 请求 URL、method、query/body、response shape，以及消费端证据（`dataKey/totalKey`、adapter、service unwrap 或可工作样例）。
- 确认列表查询、重置、刷新、分页由 DataSet `transport.read` 或项目 request adapter 触发。
- 点击首行详情，确认详情和明细可通过 mock API 加载。
- 执行 save/copy/delete/submit/withdraw/abandon/cancel 后返回列表或刷新详情，确认数据和状态来自同一个 runtime store。
- 手动刷新列表和详情 route，确认无 runtime error。

## 可抽象链路模板
```text
DataSet transport.read / action service
  -> request('/api/mock/...')
  -> devServer middleware route
  -> ensureRuntimeStoreInitialized()
  -> query/detail/action mutate
  -> normalize response
  -> DataSet / service consumes response
```

实现时可以把多个 route 委托给同一个 store/service 文件；不要让 transport 成功路径与 action 路径分别维护过滤、详情组合或状态流转逻辑。

# Mock / Demo 契约边界

## 适用场景
用于 HZERO 企业页面在缺少生产契约但可按默认策略进入 mock/demo 时，约束临时代码、交付状态和生产替换清单。

## 基本原则
- 前端 mock 标准实现统一为 HZERO 本地开发服务器上的 HTTP mock API。
- mock API 必须通过目标工程既有 HZERO / Webpack / Umi devServer 扩展点注册；业务页面、DataSet 和 service 必须通过正常 HTTP 请求访问 mock API。
- mock/demo 只能证明演示意图，不能替代生产契约；使用 mock API 的顶层交付状态最高为 `conditional` 且必须写 `deliveryTarget=mock-demo`。
- mock middleware 只允许影响本地 devServer，不得修改生产构建、微前端注册、`remoteEntry`、`microConfig`、`PACKAGE_PUBLIC_URL`、public path 或部署配置。
- 默认不得为 mock 新增运行时或开发依赖；POST/PUT 请求体优先复用项目已有 JSON parser，缺失时使用 mock 模块内轻量 `readJsonBody` 工具。
- transitionalCopy 是文档/交付边界，不是默认页面 UI。`mock/demo`、`generatedCandidate`、`待替换`、`未接生产接口`、`request helper 待确认`、`SecurityToken 待确认`、`Figma 未确认` 等内部说明不得出现在业务用户可见的页面正文、Header、Toolbar、表格说明、字段 label、按钮、Modal.info、notification、Alert、Tooltip 或 Empty/Result 中；应放入 Handoff、生产替换清单、验证报告、实现摘要、代码注释或开发态日志。
- 若产品/测试明确要求可见演示标识，只能使用正式业务文案和 i18n，例如“演示环境”“示例数据”，并记录确认来源。
- 若已有明确编码规范可生成 `generatedCandidate`（例如 i18n namespace/key、permission code、lovCode、lookupCode），实现应优先使用候选值本身，不要因为 demo/mock 实现自动追加 `.mock`、`demo` 或 `TEMP` 前后缀；候选状态和待确认项必须进入生产替换清单。
- 如果 `sdd-workspace`、FDS/FSS、BASP/SASP、Swagger 或 API JSON 中已存在正式编码，必须引用为候选证据；若仍使用 mock，说明原因和替换位置。

## 必查资产
- 当前 Change Root：`sdd-workspace/changes/{change-id}/fds.md`、`tds.md`、`mds/**`、`fss/**`。
- 缺项兜底：当前 Change Root 下指定文件或目录不存在、为空、明显过期或无法覆盖关键契约时，按模块名、功能名、接口路径、DTO/entity、权限码、菜单名、值集/LOV/lookup、bucket、templateCode 等关键词在 `sdd-workspace/**` 下自发发现相关后端/通用资产，并把命中路径、未命中项和仍需确认项写入契约检查或生产替换清单。
- 项目相似页面：route、PermissionButton、DataSet/service、i18n、Attachment、Export/Import 模式、devServer 扩展入口。

## 生产替换清单字段
| 类型 | 当前临时值 | 正式契约来源 | 影响文件 | 替换条件 | 状态 |
| --- | --- | --- | --- | --- | --- |
| API | mock API route | FDS/TDS/MDS/FSS/API JSON | service/DataSet/mock route | URL/method/payload 确认 | pending |
| field-shape | mock response shape | DTO/Swagger/API JSON | service/DataSet/adapter | request/response shape 确认 | pending |
| permission | `generatedCandidate` 或待确认权限 | 菜单/权限资源/编码规范 | route/按钮 | 权限码确认 | pending |
| lovCode | `generatedCandidate` 或待确认 LOV | 平台主数据/LOV 资产/编码规范 | constants/DataSet | 正式 LOV 确认 | pending |
| lookupCode | `generatedCandidate` 或待确认值集 | FSS/平台值集/编码规范 | constants/DataSet | 正式值集确认 | pending |
| bucket | 待确认 bucket | 文件服务协议 | Attachment 字段 | bucket 和权限确认 | pending |
| templateCode | 待确认模板 | 导入模板协议 | 导入按钮/service | templateCode 确认 | pending |

## Mock API 数据链路
- 查询模式必须声明为 `mock-request`、`production-transport`、`blocked` 或 `not-applicable`。
- `mock-request` 表示页面、DataSet 或 service 通过 HTTP 请求访问 HZERO 本地 devServer middleware 暴露的 mock API。
- 对需要新增、复制、删除、保存、提交、废弃、撤销、撤回等动作的 demo，mock API 背后必须使用同一个 dev-only runtime store 维护当前态。
- 列表、详情、明细和动作后的刷新必须读取同一个 runtime store；删除后列表刷新不得复现已删记录，提交/废弃/撤销后列表和详情状态必须一致。
- mock route/store 负责数据读写、状态流转和持久化；DataSet 负责字段、查询、校验、加载和提交编排；页面组件不得再维护第二套独立数据源。
- save/copy 必须返回确认的主键字段或 demo 主键候选，供路由跳转和详情 reload 使用；submit/withdraw/abandon/cancel 必须更新状态码和 meaning。
- 新建提交应先 save 再 submit，提交语义必须改变状态或记录提交动作，不能只保存。
- header DataSet 和 line/detail DataSet 必须同时校验；明细为空、字段 shape 不一致或必填 options 缺失时不得提交。

## 状态守卫模板
| 动作 | 可操作状态 | 禁用/隐藏状态 | action guard | UI guard |
| --- | --- | --- | --- | --- |
| save | draft / rejected | submitted / approved / closed / abandoned | required | required |
| submit | draft / rejected | submitted / approved / closed / abandoned | required | required |
| delete | draft | submitted / approved / closed / abandoned | required | required |
| copy | any readable status | none unless business says so | required | optional |
| withdraw | submitted | draft / approved / closed / abandoned | required | required |
| abandon | draft / rejected | submitted / approved / closed / abandoned | required | required |

按钮显隐和动作函数必须使用同一状态判断；隐藏按钮后仍可调用 action 的实现必须视为缺陷。

## Handoff 限制
- 缺外部 browser/manual 或 HTTP smoke 证据：交付状态只能为 `conditional`，并写 `reachable/usable=unknown`、`manualVerificationRequired=true` 和未验证项。
- 未运行 build：不得声明产物态可交付。
- 未落盘生产替换清单：不得进入 Handoff ready。
- mock API 未切真实 API 前，不得声明 `production-ready`。

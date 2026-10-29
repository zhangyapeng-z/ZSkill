# Frontend Manual Checklist

Feature：<feature>
建议路径：`sdd-workspace/changes/{change-id}/frontend/verification/manual-checklist.md` 或并入 `verification-report.md`
状态：not-run / partial / pass / failed

前端服务提示：请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面。

## List Smoke
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 页面首屏有表格 DOM | 表格可见 | not-run | - | not-run |  |
| 首屏有数据行或明确空态 | 数据行/空态可见 | not-run | - | not-run |  |
| 分页可见 | pagination 可见 | not-run | - | not-run |  |
| 有可见行动作时操作列可见且在最后一列 | lock='right'；无可见动作时不显示空操作列 | not-run | - | not-run |  |
| Runtime console / chunk 反查 | 无 fatal console error；若出现压缩 chunk 栈、`forEach is not a function`、React #31/#130 或组件初始化异常，记录 URL、chunk 文件、关键栈帧、反查到的组件/源码文件和已回扫的集合 props | not-run | - | not-run |  |

## Query Behavior
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 模糊查询 | fuzzyQuery 生效 | not-run | - | not-run |  |
| 查询 | 回第一页 | not-run | - | not-run |  |
| 刷新 | 保留当前页 | not-run | - | not-run |  |
| 重置 | 清空条件并回第一页 | not-run | - | not-run |  |

## Detail / Modal / Drawer
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 点击后打开详情/业务弹层 | 非初始挂载；形态匹配 UI Contract；业务弹层通过 Modal.open / confirmed wrapper 打开 | not-run | - | not-run |  |
| Drawer 可调整 | Drawer 使用 resizable=true 或 wrapper 等价默认 | not-run | - | not-run |  |
| 尺寸 | 业务 Modal / Drawer / Overlay 严格按 UI Contract；普通表单 Modal 设计未指定宽度时为 `size=small` 或项目 small 等价值；详情 Drawer / 高密度只读详情按项目默认尺寸或 confirmed baseline，并记录 readabilityRisk | not-run | - | not-run |  |
| 长值展示 | 长文本、邮箱、公司名、职位名、地址等按 `valueOverflowPolicy` 展示；单行省略可查看完整值，长正文不被无来源强制单行截断 | not-run | - | not-run |  |
| 遮罩和层级 | 不穿透 Header/列表 | not-run | - | not-run |  |
| 关闭后列表状态 | 筛选/分页保留且无遮挡 | not-run | - | not-run |  |
| 基本信息 | Form + Output | not-run | - | not-run |  |
| 数组区块 | 表格型详情集合必须使用 Choerodon Pro Table；字段名与 API/MDS `apiField` 对齐；不得使用项目只读表格、原生 DOM 或文本拼接 | not-run | - | not-run |  |

## Create / Edit / Save
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 新建默认值 | 仅保留已确认系统默认；无示例 seed、无历史详情回填 | not-run | - | not-run |  |
| 新建审计字段显隐 | `creationDate/lastUpdateDate/createdBy/lastUpdatedBy/objectVersionNumber` 等后端生成字段未保存前不可见且不占位 | not-run | - | not-run |  |
| 新建派生字段空态 | `requisitionNumber/totalAmount/budgetRate` 等编号/合计/比例字段按 Empty / Derived Field UX Rules 隐藏或展示确认 placeholder，无只读空 Output | not-run | - | not-run |  |
| 可编辑字段 | create/edit/copy 可编辑字段可输入且组件类型正确 | not-run | - | not-run |  |
| 只读字段 | 只读/禁用字段有来源且表现符合 UI Contract | not-run | - | not-run |  |
| 展示字段 label | `*Meaning/*Name/displayField`、状态 Tag、只读 Output 均有可见 label，且符合 Field Usage Matrix 的 labelSource | not-run | - | not-run |  |
| Form label 布局 | 详情/编辑/新建业务 Form 的 label 在页面可见；未无来源使用 `labelLayout=placeholder/none` 隐藏 label | not-run | - | not-run |  |
| 详情审计字段显隐 | 已有主键详情/只读态按 UI Contract 显示后端返回审计字段 | not-run | - | not-run |  |
| 保存成功 | 保存后刷新/回跳符合 saveRedirectPolicy | not-run | - | not-run |  |
| 保存后详情 | 列表、详情、行表读取到同一当前态 | not-run | - | not-run |  |

## Status Actions
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| Header/工具栏/行操作入口位置 | 与 Action Entry Matrix 一致；未确认业务取消、撤回、作废、删除不出现在 Header | not-run | - | not-run |  |
| 提交/撤回/作废/删除按钮态 | 可见性和可点击条件符合 Status Action Matrix | not-run | - | not-run |  |
| 禁用原因与 hover 提示 | 业务按钮置灰时有 disabledReasonSource；删除/提交/撤回/作废等关键动作可通过 Tooltip/title/project wrapper 说明原因 | not-run | - | not-run |  |
| 批量按钮选择态刷新 | 依赖勾选行的按钮在未选中、选中、取消选中、全选、重新加载后实时刷新 disabled/enabled 状态 | not-run | - | not-run |  |
| 导航取消/返回 | 只导航、关闭或清理本地 UI；不调用取消单据、作废、撤回、删除 API | not-run | - | not-run |  |
| 非法状态拦截 | action 入口提示失败，不无条件成功 | not-run | - | not-run |  |
| 动作后刷新 | 列表/详情/行表刷新后仍为当前态 | not-run | - | not-run |  |

## Route Context / Edit Mode
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 列表进入编辑 | routeContext 从编辑 path/pageMode 派生编辑态，字段进入预期编辑态 | not-run | - | not-run |  |
| 刷新编辑 URL | 编辑 path/pageMode 刷新后编辑态符合设计 | not-run | - | not-run |  |
| 新建路由 | 固定 `/create` 不带 query 也进入 create/editable；`/detail/create` 命中即失败并迁移 | not-run | - | not-run |  |
| 保存后跳转 | 按 saveRedirectPolicy 保留或切换编辑 path/pageMode | not-run | - | not-run |  |
| 切换记录 | 切换不同 id / Tab 不复用旧记录编辑态或旧状态守卫 | not-run | - | not-run |  |

## Data / Permission / Attachment
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 数据链路 | mock-request/production-transport 证据明确；local-filter / inline mock 成功路径必须 blocking cleanup，不得写 `reachable=true` 或 `usable=true` | not-run | - | not-run |  |
| mock-request Network | Network 记录 mock request URL、method、query/body | not-run | - | not-run |  |
| mock-request origin | mock seed 请求命中当前前端服务 origin 或项目已证实 dev mock API | not-run | - | not-run |  |
| DataSet transport | 列表查询/重置/刷新/分页由 DataSet `transport.read` 或项目 request adapter 触发；`service/mock + loadData` 不算 mock-request | not-run | - | not-run |  |
| 权限按钮 | 文案、权限码、type、disabled 来源明确 | not-run | - | not-run |  |
| 附件 | 可访问/失败/无附件三态明确 | not-run | - | not-run |  |
| 附件编辑态 | bucket/storage/template 不外露到页面文案；编辑/只读符合 contract | not-run | - | not-run |  |

## Table / Import Export
| 检查项 | expected | actual | evidence | result | issueId |
| --- | --- | --- | --- | --- | --- |
| 明细增删改 | 行新增、删除、保存符合主从 contract | not-run | - | not-run |  |
| 行导出参数 | parentId、queryParams、tenantContext 正确 | not-run | - | not-run |  |
| 导入关闭刷新 | 导入完成或关闭后刷新目标明确 | not-run | - | not-run |  |
| 导出链路 | 使用 `ExcelExportPro` from `components/ExcelExportPro` 或内部使用它的 confirmed wrapper；非旧组件、深层导入或普通下载按钮 | not-run | - | not-run |  |
| 表格企业能力 | `customizedCode/customizable/columnDraggable` 符合设计或有 not-applicable reason | not-run | - | not-run |  |

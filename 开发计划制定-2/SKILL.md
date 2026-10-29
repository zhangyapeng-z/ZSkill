---
id: rd-dev-planning
name: 开发计划制定
description: 基于需求规格与原型设计，制定数据库设计（Oracle + Liquibase groovy，对齐 demo 工程）、API 契约（对齐 crm-demo 前端 transport）与开发任务拆解（含前后端 TS 任务、依赖、工时、里程碑），主交付产物为 Excel 工作簿（dev-plan.xlsx，7 个 Sheet 面向评审排期），同时输出 dev-plan.json 作为数据源与下游代码生成输入
version: 2.4.0
stage: 3
trigger_patterns:
  - 开发计划
  - 任务拆解
  - dev planning
  - 开发排期
  - 数据库设计
  - API设计
  - 生成计划
  - excel
  - xlsx
output_artifact: dev-plan.xlsx
---

# Skill: 开发计划制定 (Development Planning)

## 1. 职责范围

### 核心任务
基于需求规格说明书（`requirement-spec.json`）和原型设计规格（`prototype-spec.json`），完成：
1. **数据库设计**：将需求实体转化为 Oracle 表结构（对齐工作区 `demo/` 工程的 Liquibase groovy 建表风格）
2. **API设计**：详细定义 RESTful API 契约（路径必须与原型 DataSet transport 一致）
3. **任务拆解**：将功能需求拆解为前后端开发任务（前端任务对齐 crm-demo 的 TS 工程组织）
4. **依赖分析**：确定任务间依赖关系和开发顺序
5. **工时估算**：按基准为每个任务估算开发工时

**主交付物为 Excel 工作簿**（`dev-plan.xlsx`，面向评审/排期/人力分配），同时输出 `dev-plan.json`（结构化数据源，Excel 由脚本从 JSON 生成，下游代码生成也读取 JSON）。

> **v2.4.0 变更（hzero-copilot 借鉴增补）**：新增 `templates/tds-template.md` 结构化 TDS 模板与 `tools/gate-guard.py` 段门校验脚本：
> - **技术方案设计（专家团工序 2.1）产出按 TDS 模板结构化**：需求覆盖清单（100% 覆盖后才得开始详细设计）、TECH 五形态（A-QUERY/A-COMMAND/A-SYNC/A-CROSS/A-INFRA）决定必填工件、持久层组件矩阵 + 复杂 SQL 白名单（7 条情形之外一律复用 BaseService/BaseRepository）、数据库硬约束（单表索引≤5、禁物理外键、逻辑关联必须写明目标表.字段、禁 SELECT *）、待确认项（阻塞编码项，每条给默认实现并转 L2 强制确认清单）
> - **段门校验**：主理人在 Part2/Part3 段门与实现段收尾前调用 `tools/gate-guard.py --artifacts-dir <artifacts> --gate <part2|part3|finish>` 做产物存在性与状态对账校验，任一缺失拒绝过段（详见 §5.5）

> **后端技术基线（v2.0.0，对齐工作区 `demo/` 工程）**：数据库一律按 HZERO 官方 demo 的 **Oracle + Liquibase groovy** 风格设计：
> - 建表用 `script/db/*.groovy`，`databaseChangeLog(logicalFilePath: 'script/db/{table}.groovy')`，changeSet id `{yyyy-MM-dd}-{table}`
> - 支持序列的数据库（Oracle）先 `createSequence(sequenceName: '{table}_s', startValue: "1")`
> - 主键 `id bigint(20)` + `autoIncrement: true` + `constraints(primaryKey: true)`
> - 唯一约束用 `addUniqueConstraint(columnNames: "...", tableName: "...", constraintName: "{table}_u1")`，不建外键
> - **Oracle 字符长度放大**：varchar 长度按 `helper.isOracle()` 分支放大（demo 用 `weight = 3` 分支：`type: "varchar(" + 64 * weight + ")"`），grovvy 脚本须含 `helper.isSqlServer()/isOracle()` 权重分支
> - 审计五列 + 租户列见 §4.1 标准字段
>
> **前端技术基线（v2.0.0，对齐工作区 `crm-demo/` 工程）**：前端任务按 UMI3 HZERO 微前端 + TypeScript 组织拆解：
> - 页面任务（`FRONTEND_PAGE`）按 `src/pages/{module}/index.tsx` 组织；DataSet 独立任务（`FRONTEND_DATASET`）产出 `dsConfig.ts` 工厂；服务封装（`FRONTEND_SERVICE`）产出 `services/index.ts` 请求
> - 任务描述中涉及的组件/DataSet 类型引用以 `prototype-spec.json` 的 `tsImports`/`tsType` 为权威来源

### 边界定义
- **负责**：数据库表结构设计（Oracle groovy）、API 接口契约、任务拆解、依赖排序、工时估算、里程碑定义、需求覆盖矩阵、Excel 交付
- **不负责**：需求分析、UI 设计、代码编写、测试用例编写
- **上游**：需求接收（①）+ 原型设计（②）
- **下游**：代码生成（④）

## 2. 输入

### 输入产物
| 产物 | 路径 | 用途 |
|------|------|------|
| 需求规格 | `artifacts/01-requirement/requirement-spec.json` | 提取实体、功能需求（FR）、API 端点、角色权限 |
| 原型设计 | `artifacts/02-prototype/prototype-spec.json` | 提取页面、DataSet transport（API 路径必须一致）、tsImports |

### L1 入口校验
- [ ] 两个上游产物文件均存在
- [ ] JSON 格式合法
- [ ] 上游 `qualityGateStatus` = "PASSED"
- [ ] `requirement-spec.json` 的 `modules[].entities` 或 `functionalRequirements` 非空
- [ ] `prototype-spec.json` 的 `pages` 非空

## 3. 输出

### 产物文件
| 产物 | 路径 | 说明 |
|------|------|------|
| **开发计划 Excel（主交付物）** | `artifacts/03-planning/dev-plan.xlsx` | 7 个 Sheet 的评审用工作簿，由 `tools/generate-excel.py` 从 JSON 生成 |
| 开发计划数据（数据源） | `artifacts/03-planning/dev-plan.json` | 唯一数据源，Excel 与下游代码生成均读它，禁止手工改 Excel |

### 3.1 Excel 工作簿规范（主交付物）

**生成方式**：`python tools/generate-excel.py`（openpyxl，零外部配置），**JSON 是唯一数据源，Excel 每次全量重新生成，禁止手工编辑 Excel 后回写 JSON**。

工作簿含 7 个 Sheet：

| Sheet | 内容 | 关键列 |
|-------|------|--------|
| 概览 | 项目信息 + 统计卡片 + 里程碑概览 | 项目名/serviceCode/packageName/数据库(Oracle)/表数/API数/任务数/总工时/里程碑数 |
| 数据库设计 | 每表一个分组标题行 + 列级明细 | 表名/表说明/字段名/类型/长度/可空/主键/默认值/注释/索引/唯一/枚举 |
| API设计 | 全部 API 契约清单 | ID/分组/Method/Path/说明/权限编码/输入摘要/输出说明 |
| 开发任务 | 任务拆解清单（**评审重点**） | ID/标题/类型/模块/描述/依赖/估时(h)/负责人/关联表/API/页面/验收标准 |
| 任务序列 | 阶段化执行顺序 | 阶段/任务IDs/可并行/阶段工时小计 |
| 里程碑 | 关键里程碑 | 名称/说明/关联任务IDs/交付物 |
| 需求覆盖矩阵 | FR→API→任务 映射与覆盖率 | FR-ID/标题/优先级/模块/关联API/关联任务/是否覆盖 |

**样式规范**（HZERO 工作台风格，与原型预览一致）：
- 表头：`#1B83FF` 底 + 白色加粗 11pt，行高 26，冻结首行（概览 Sheet 冻结标题区）
- 数据区：白底/浅灰 `#F5F7FA` 斑马纹，细边框 `#D9DEE6`，垂直居中
- 类型/状态色：任务类型（DATABASE 灰 / BACKEND 蓝 / FRONTEND 绿 / CONFIG 橙）用列内填充色；工时数值右对齐并保留小数
- 列宽自适应（中文 2 字符宽度）、自动换行、`sheet.freeze_panes`、`auto_filter` 开启筛选
- 标题行：每个 Sheet 首行大标题（14pt 加粗 #001529），第二行生成时间说明（9pt 灰）

### 3.2 dev-plan.json 结构规范（数据源）

```json
{
  "_meta": {
    "stage": "dev-planning",
    "version": "2.0.0",
    "createdAt": "ISO 8601时间",
    "createdBy": "WorkBuddy",
    "upstreamArtifacts": [
      "../01-requirement/requirement-spec.json",
      "../02-prototype/prototype-spec.json"
    ],
    "qualityGateStatus": "PASSED",
    "deliverable": "dev-plan.xlsx"
  },
  "project": {
    "name": "项目名",
    "serviceCode": "服务编码（= Maven artifactId，取自 requirement-spec.project.serviceCode）",
    "packageName": "Java包名（= 后端包根，取自 requirement-spec.project.packageName）",
    "databaseType": "oracle",
    "dbScriptType": "liquibase-groovy"
  },
  "database": {
    "tables": [
      {
        "name": "表名（snake_case）",
        "description": "表说明",
        "multiTenant": true,
        "sequence": "{table}_s",
        "columns": [
          {
            "name": "字段名（snake_case）",
            "type": "BIGINT/VARCHAR/DATE/DATETIME/DECIMAL/NUMBER",
            "length": 64,
            "precision": 4,
            "scale": 2,
            "nullable": false,
            "primaryKey": false,
            "defaultValue": "1",
            "comment": "字段注释",
            "index": false,
            "unique": false,
            "enumValues": ["枚举值（如有）"]
          }
        ],
        "uniqueConstraints": [
          { "name": "表名_u1", "columns": ["code"] }
        ],
        "indexes": [
          { "name": "idx_表简_字段", "columns": ["tenant_id", "user_id"], "unique": false }
        ]
      }
    ],
    "initData": [
      { "table": "表名", "data": [ { "字段名": "值" } ] }
    ]
  },
  "apiDesign": [
    {
      "id": "API-001",
      "group": "API分组（如周报管理）",
      "method": "GET/POST/PUT/DELETE",
      "path": "/v1/worktime/{资源}",
      "description": "接口说明",
      "permissionCode": "权限编码（如 worktime.week-report.view）",
      "relatedFRs": ["FR-001"],
      "requestSummary": "输入摘要（查询条件/入参）",
      "responseSummary": "输出说明（返回字段/数据结构）"
    }
  ],
  "tasks": [
    {
      "id": "TASK-001",
      "title": "任务标题",
      "type": "DATABASE/BACKEND_ENTITY/BACKEND_SERVICE/BACKEND_API/FRONTEND_DATASET/FRONTEND_SERVICE/FRONTEND_PAGE/FRONTEND_COMPONENT/CONFIG",
      "module": "所属模块",
      "description": "任务详细描述（含 groovy 文件/类名/页面路径等落点）",
      "acceptanceCriteria": ["验收标准"],
      "dependencies": ["前置任务ID"],
      "estimatedHours": 4,
      "assignedTo": "BE/FE/DBA",
      "artifacts": {
        "databaseTable": "关联表名（DATABASE/BACKEND_ENTITY）",
        "apiIds": ["关联API ID（BACKEND_API）"],
        "pageIds": ["关联页面ID（FRONTEND）"],
        "dataSetIds": ["关联DataSet ID（FRONTEND_DATASET）"]
      }
    }
  ],
  "taskSequence": [
    {
      "phase": "阶段名称（如 数据库/后端基础/后端API/前端基础/前端页面/配置与联调）",
      "tasks": ["TASK-001", "TASK-002"],
      "canParallel": false,
      "phaseHours": 12
    }
  ],
  "milestones": [
    {
      "name": "里程碑名称",
      "description": "里程碑说明",
      "taskIds": ["TASK-001"],
      "deliverable": "交付物"
    }
  ],
  "coverageMatrix": [
    {
      "frId": "FR-001",
      "title": "功能需求标题",
      "priority": "HIGH",
      "module": "所属模块",
      "apiIds": ["关联API ID"],
      "taskIds": ["关联任务ID"],
      "covered": true
    }
  ]
}
```


### 阶段报告（人工交付物）

`reports/03-开发计划-阶段报告.md`

按《阶段报告编写规范》（`kb/07-项目管理/03-阶段报告编写规范.md`）输出，固定四段结构：

1. **阶段目标**：本环节在主流程中的定位、上游输入、完成标志
2. **主要产出**：产物清单表（产物/格式/路径/用途去向）
3. **关键结论**：核心指标与结论，用表格/流程图呈现，禁止大段纯文字
4. **风险与建议**：风险/遗留项 + 等级(高/中/低) + 建议动作

> 结构化数据（问题清单、测试结果等）另出 Excel 数据表，报告内以汇总表格引用。

## 4. 关键约束

### 4.1 数据库设计规范（Oracle + Liquibase groovy，对齐 demo）

#### 建表脚本模板（每表一份 `script/db/{table}.groovy`）
```groovy
package script.db

databaseChangeLog(logicalFilePath: 'script/db/{table}.groovy') {
    changeSet(author: "worktime@hand-china.com", id: "{yyyy-MM-dd}-{table}") {
        def weight = 1
        if (helper.isSqlServer()) {
            weight = 2
        } else if (helper.isOracle()) {
            weight = 3
        }
        if (helper.dbType().isSupportSequence()) {
            createSequence(sequenceName: '{table}_s', startValue: "1")
        }
        createTable(tableName: "{table}", remarks: "{表说明}") {
            column(name: "id", type: "bigint(20)", autoIncrement: true, remarks: "主键") { constraints(primaryKey: true) }
            column(name: "tenant_id", type: "bigint(20)", defaultValue: "0", remarks: "租户ID")
            // 业务字段：Oracle 下 varchar 长度放大，如 type: "varchar(" + 100 * weight + ")"
            column(name: "object_version_number", type: "bigint(20)", defaultValue: "1", remarks: "版本号")
            column(name: "created_by", type: "bigint(20)", defaultValue: "-1", remarks: "创建人")
            column(name: "creation_date", type: "datetime", defaultValueComputed: "CURRENT_TIMESTAMP", remarks: "创建时间")
            column(name: "last_updated_by", type: "bigint(20)", defaultValue: "-1", remarks: "最后更新人")
            column(name: "last_update_date", type: "datetime", defaultValueComputed: "CURRENT_TIMESTAMP", remarks: "最后更新时间")
        }
        addUniqueConstraint(columnNames: "{业务唯一列}", tableName: "{table}", constraintName: "{table}_u1")
    }
}
```

#### 表设计规则
| 规则 | 说明 |
|------|------|
| 表名 | 小写+下划线，如 `worktime_detail`，与实体名对应 |
| 字段名 | 小写+下划线，如 `work_date` |
| 主键 | 固定 `id bigint(20)`，Oracle 由序列 `{table}_s` 生成 |
| 租户字段 | 业务表必须含 `tenant_id bigint(20) DEFAULT 0` |
| 乐观锁 | 必须含 `object_version_number bigint(20) DEFAULT 1` |
| 审计字段 | 必须含 `creation_date`/`created_by`/`last_update_date`/`last_updated_by`（见模板） |
| 字符长度 | Oracle 下 varchar 按 `weight=3` 放大（demo 惯例：`64*weight`、`100*weight` 等），JSON 中 `length` 记录业务口径长度 |
| 唯一约束 | 用 `addUniqueConstraint`（`{table}_u1` 命名），不建物理外键 |
| 序列 | 支持序列的数据库（Oracle）必须 `createSequence('{table}_s')` |
| 注释 | 表和字段必须有 remarks |
| 外键 | 业务表不建外键，关联通过逻辑 ID + 索引实现 |

#### 标准字段（每表必含，不单独列为任务）
`id`（主键）、`tenant_id`、`object_version_number`、`creation_date`、`created_by`、`last_update_date`、`last_updated_by`

#### 索引规范
- 多租户表必须建 `(tenant_id, 业务唯一字段/常用查询字段)` 联合索引
- 外键/关联字段（如 `week_report_id`、`task_id`、`project_id`）建普通索引
- 索引名：`idx_{表简}_{字段}`，唯一索引并入 `uniqueConstraints`

### 4.2 API 设计规范

- **路径必须与原型 DataSet transport 一致**（以 `prototype-spec.json` 中 DataSet 的 transport.url/method 为权威，二者冲突时以原型为准并记录差异）
- RESTful 规则（HZERO demo 风格）：
  | 操作 | Method | Path |
  |------|--------|------|
  | 列表查询 | GET | /v1/worktime/{资源} |
  | 详情 | GET | /v1/worktime/{资源}/{id} |
  | 保存/批量 | POST | /v1/worktime/{资源} |
  | 更新 | PUT | /v1/worktime/{资源} |
  | 提交/审批等动作 | POST | /v1/worktime/{资源}/{id}/{action} |
- Controller 统一 `@RestController("{资源}Controller.v1")` + `/v1/{organizationId}/{资源}`，标准四接口 list/detail/save/remove + 动作接口
- 每个 API 必须有 `permissionCode`（格式 `worktime.{资源}.{action}`，如 `worktime.week-report.submit`），与 requirement-spec 的 `roles[].permissions` 对齐
- 响应统一 HZERO 格式（`Results.success` / 分页 `PageHelper`），错误码 `{serviceCode}.{资源}.{操作}.{错误}`

### 4.3 任务拆解规范

（本节定义任务类型与字段规范；**拆解方式遵循 §4.3.1 的 Tracer-Bullet 垂直切片与 Expand-Contract 纪律**）

### 4.3.1 Tracer-Bullet 垂直切片与 Expand-Contract（v2.3.0 新增）

> 方法论源自 to-tickets 技能（mattpocock/skills）：任务拆解是"把计划变成可执行的任务图"，粒度与依赖方向决定后续代码生成的成败。

#### Tracer-Bullet 垂直切片规则

- 每个任务尽量是**一条窄而完整的纵切路径**（Schema → API → UI → 测试），而不是某一层的横切；一个纵切完成即可独立演示或验证。
- 任务粒度以「一个新会话的上下文窗口能装下」为上限——超出即拆分。
- **前置重构（prefactoring）单独成任务且排在最前**："先让改动变容易，再做改动"。典型：抽取公共 transport、统一响应包装改造。
- 每个 FR 至少有一条纵切贯穿：需求覆盖矩阵（§4.3 之外，见 Excel 需求覆盖矩阵 Sheet）中每个 FR 必须映射到至少一个可演示任务。

#### 宽泛重构的例外：Expand-Contract 编排

**宽泛重构** = 单个机械改动（改列名、改共享符号类型）波及全库调用点，任何单一纵切都无法独立保持可构建。此时不硬塞纵切，按三阶段编排：

1. **Expand**：新形式与旧形式并存（加新列/新接口，不动旧调用点），单独成任务；
2. **Migrate**：调用点分批迁移（按包/目录分批，每批一个任务，全部被 Expand 任务阻塞），每批落地后旧形式仍在、构建保持绿色；
3. **Contract**：旧形式无调用者后删除，被所有 Migrate 批次阻塞。

批次间连"保持绿色"都做不到时，保留顺序但共享一个集成分支，由最终的 integrate-and-verify 任务统一承诺绿色。

#### 依赖边纪律

- 依赖边（`dependencies` 字段）只写**真实门禁**：被依赖任务不完成，本任务真的无法开工。评审时逐边检查"这是不是唯一真正的前置"。
- 无阻塞的任务标记为可立即开工（frontier）；代码生成环节按 frontier 并行推进。

#### 任务类型定义（对齐前后端技术基线）
| 类型 | 说明 | 典型内容 |
|------|------|---------|
| DATABASE | 数据库任务 | 1 张表的 Liquibase groovy（含序列/唯一约束）+ 初始化数据 |
| BACKEND_ENTITY | 后端实体 | Entity(Lombok, 继承 AuditDomain) + Repository + RepositoryImpl + Mapper |
| BACKEND_SERVICE | 后端服务 | Service + ServiceImpl（分页/批量保存/事务） |
| BACKEND_API | 后端接口 | Controller + DTO + Swagger + 权限编码（按 API 分组聚合，1 个 Controller 1 个任务） |
| FRONTEND_DATASET | 前端数据层 | `dsConfig.ts` 工厂（queryDs/listDs/formDs）+ services 请求方法（按页面聚合） |
| FRONTEND_SERVICE | 前端服务封装 | `services/index.ts` 统一 request/API_HOST/getCurrentTenantId |
| FRONTEND_PAGE | 前端页面 | `src/pages/{module}/index.tsx` 页面 + 路由 + 菜单（含 Mock） |
| FRONTEND_COMPONENT | 前端组件 | 跨页面复用组件（任务×日期矩阵、月历、汇总卡片等） |
| CONFIG | 配置任务 | 权限/菜单/多语言、移动端应用接入、全局配置 |

#### 拆解规则
1. 每个实体 = 1 个 DATABASE 任务 + 1 个 BACKEND_ENTITY 任务
2. 每个实体/资源域 = 1 个 BACKEND_SERVICE 任务（服务接口+实现聚合）；Controller 按资源域聚合为 BACKEND_API 任务（1 域 1 任务，任务内注明包含的 API ID 列表）
3. 每个页面 = 1 个 FRONTEND_PAGE 任务；页面依赖的 DataSet 工厂 = FRONTEND_DATASET 任务（按页面聚合）
4. 跨页复用组件（任务×日期矩阵/月历/汇总卡片）单独拆 FRONTEND_COMPONENT 任务，并被依赖它的页面任务引用
5. 依赖方向：DATABASE → BACKEND_ENTITY → BACKEND_SERVICE → BACKEND_API → FRONTEND_DATASET/FRONTEND_SERVICE → FRONTEND_COMPONENT → FRONTEND_PAGE → CONFIG
6. 所有 FR 必须有对应任务（coverageMatrix 覆盖），估算工时完整

#### 工时估算基准
| 任务类型 | 基准工时 | 调整因子 |
|---------|---------|---------|
| DATABASE | 2h/表 | 字段>15 +2h；含初始化数据 +1h |
| BACKEND_ENTITY | 3h/实体 | 含复杂校验 +2h |
| BACKEND_SERVICE | 4h/服务 | 含复杂业务（审批状态机/幂等/事务） +4h |
| BACKEND_API | 3h/资源域 | 含动作接口（submit/approve 等） +2h |
| FRONTEND_DATASET | 2h/页面 | 含 3+ DataSet +2h |
| FRONTEND_SERVICE | 1h/全局 | 一次性 |
| FRONTEND_PAGE | 6h/页面 | 含复杂表格/矩阵/表单 +4h |
| FRONTEND_COMPONENT | 8h/组件 | 矩阵/月历等复杂组件 |
| CONFIG | 1h/项 | 权限+多语言+菜单 |

#### 高频失败规避（v2.0.1，数据驱动）
> 来源：`logs/gate-check.jsonl` 周报高频失败 L2-10（任务缺估算工时，曾 3 次/周）。
> - **每个任务必须填写 `estimatedHours`**，数值型（>0），禁止 `null`/`"待补充"`/`0.5-1` 区间文本。
> - 产出后自检：`tools/gate-check.js` 的 L2-10 会过滤 `!(estimatedHours > 0)` 的任务并列出 id。
> - 任务模板示例：`{ id, title, type, estimatedHours, dependencyIds, milestoneId }` —— estimatedHours 不可省略。
> - 若任务含多个子项，估算为其合计（如 FRONTEND_PAGE 含复杂矩阵 +4h 一并计入）。

> **前端技术栈校验（v2.2.0，冒烟验证沉淀）**
> 来源：2026-08-18 端到端冒烟验证发现——旧文档选型 Vite/antd/Zustand/Tailwind 与真实工程 UMI3+choerodon-ui 脱节。
> - **制定前端任务前必须先读 `artifacts/00-input/workspace-scan.json`**，确认目标前端应用的 `framework`/`hzero` 标记，禁止沿用 PRD/旧文档中未经验证的技术栈选型。
> - 真实工程（如 `pms-front`）为 UMI3 HZERO 微前端 + choerodon-ui 1.6.8（禁 antd）；若旧文档写 antd/Vite/Zustand/Tailwind，一律以 workspace-scan 实测为准，并在 dev-plan 显式标注「技术栈纠偏」。
> - 后端同理：读 workspace-scan 的 `artifactId`/`layers`，识别「父工程 + 子模块」多模块结构，勿按单模块 demo 臆造。

### 4.4 HZERO 框架约束（对齐 demo）
- Controller：`@RestController("xxxController.v1")`、继承 `BaseController`、`@Permission`、`SecurityTokenHelper.validTokenIgnoreInsert`、保存时 `item.setTenantId(organizationId)`
- Service：批量 `saveData(List<T>)` 按主键 null/非 null 分流 insert/update；分页 `PageHelper.doPageAndSort`
- 实体：Lombok `@Getter/@Setter`，继承 `AuditDomain`（含审计字段），`@Table(name="xxx")` + `@Id/@GeneratedValue`，Jackson 忽略多余字段
- Mapper：继承 `BaseMapper<T>`，Mapper XML 用 Oracle jdbcType（`jdbcType=VARCHAR/NUMERIC/TIMESTAMP`）+ BaseSql 片段
- 建表：Liquibase groovy（§4.1），`logicalFilePath` 唯一

## 5. 衔接方式

### 5.1 与上游的接口协议
- 读取 `requirement-spec.json`：实体（`modules[].entities`）、功能需求（`functionalRequirements`）、角色权限（`roles[].permissions`）、页面（`pages`）
- 读取 `prototype-spec.json`：页面（`pages`）、DataSet transport（`dataSets[].transport`）、tsImports
- 验证两个上游 `qualityGateStatus` = "PASSED"

### 5.2 与下游的接口协议
| 下游环节 | 交付内容 | 使用方式 |
|---------|---------|---------|
| ④代码生成 | `dev-plan.json` 全文 | 读取 `database.tables` 生成 groovy 与实体；读取 `apiDesign` 生成 Controller/DTO；读取 `tasks` 逐个生成代码 |
| 人工评审/排期 | `dev-plan.xlsx` | 打开 Excel 评审数据库/API/任务/工时/里程碑，不参与机器流转 |

### 5.3 数据流转方式
- 产物路径：`artifacts/03-planning/dev-plan.xlsx` + `artifacts/03-planning/dev-plan.json`
- `_meta.upstreamArtifacts` 记录两个上游产物路径；`_meta.deliverable = "dev-plan.xlsx"`

### 5.4 质量门禁标准（`tools/gate-check.js` 自动执行）

#### L1 - 入口校验
- [ ] `requirement-spec.json` 与 `prototype-spec.json` 存在且合法
- [ ] 两者 `qualityGateStatus` = "PASSED"

#### L2 - 过程校验
- [ ] 每个实体有对应数据库表定义（含标准审计五列 + 租户列 + 主键）
- [ ] 每个 FR 有对应 API 定义（apiDesign 覆盖全部 apiEndpoint）
- [ ] 每个页面有对应前端任务（tasks 覆盖全部页面）
- [ ] API 路径与原型 DataSet transport 一致
- [ ] 任务依赖关系无环
- [ ] 所有任务有估算工时；无 abc/xxx/待补充 占位符

#### L3 - 出口校验
- [ ] FR 覆盖率 = 100%（所有 FR 在 coverageMatrix 中 covered=true 且有任务）
- [ ] 数据库/API/任务数据完整
- [ ] `dev-plan.xlsx` 存在、为合法 xlsx（文件头 PK）、非空
- [ ] Excel 内容与 JSON 一致（由 `generate-excel.py` 生成后自校验通过）
- [ ] `_meta.version` 与 SKILL.md frontmatter 对齐（v2.0.0）
- [ ] `_meta.qualityGateStatus` = "PASSED"

## 6. 交付标准

### 验收检查项清单
| 序号 | 检查项 | 标准 | 必须 |
|------|--------|------|------|
| 1 | Excel 产物已生成 | `dev-plan.xlsx` 存在且 7 个 Sheet 完整 | 是 |
| 2 | JSON 数据源合法 | `dev-plan.json` 通过 JSON 解析 | 是 |
| 3 | 数据库设计 | 所有实体有 Oracle 表定义，含标准字段/序列/唯一约束 | 是 |
| 4 | API 设计 | 所有 FR 的 apiEndpoint 有 API 定义，路径与原型 transport 一致 | 是 |
| 5 | 权限编码 | 每个 API 有 permissionCode 且与需求角色权限对齐 | 是 |
| 6 | 任务拆解 | 所有 FR/页面拆解为前后端任务 | 是 |
| 7 | 依赖关系 | 任务依赖无环，顺序合理 | 是 |
| 8 | 工时估算 | 所有任务有估时，符合基准 | 是 |
| 9 | 任务序列 | 定义了执行阶段、顺序与阶段工时 | 是 |
| 10 | 需求覆盖矩阵 | 每个 FR 有 API 与任务映射，覆盖率 100% | 是 |
| 11 | 质量门禁 | gate-check.js 全部通过 | 是 |
| 12 | 阶段报告 | `reports/03-开发计划-阶段报告.md` 已生成，四段结构完整 | 是 |

### 执行流程
```
Step 1: 读取 requirement-spec.json + prototype-spec.json，执行 L1 校验
Step 2: 数据库设计 — 实体→Oracle 表（含审计/租户/序列/唯一约束/索引），按 §4.1 模板
Step 3: API 设计 — 覆盖全部 FR apiEndpoint，路径与原型 transport 对齐，补权限编码
Step 4: 任务拆解 — FR/实体/页面 → DATABASE/ENTITY/SERVICE/API/DATASET/PAGE/COMPONENT/CONFIG 任务
Step 5: 依赖分析 — 按 §4.3 规则 5 确定依赖与 taskSequence 阶段
Step 6: 工时估算 — 按 §4.3 基准表估算，累加阶段工时/总工时
Step 7: 里程碑 + 需求覆盖矩阵 — 定义里程碑，建立 FR→API→任务映射
Step 8: 执行 L2 校验（依赖无环/路径一致/占位符）
Step 9: 生成 dev-plan.json（_meta.version=2.0.0）
Step 10: 运行 tools/generate-excel.py 生成 dev-plan.xlsx（自校验一致性）
Step 11: 运行 tools/gate-check.js 全量门禁，全部通过后标记 qualityGateStatus=PASSED 并流转
```

### 工具说明
| 工具 | 运行环境 | 用途 |
|------|---------|------|
| `tools/generate-excel.py` | Python 3.9+ / openpyxl | 从 dev-plan.json 生成 dev-plan.xlsx（7 Sheet，HZERO 风格），生成后自校验 |
| `tools/gate-check.js` | Node.js | L1/L2/L3 全量门禁，退出码 0=通过 1=失败 |
| `tools/gate-guard.py` | Python 3.9+（无第三方依赖） | 专家团段门校验（v2.4.0 新增）：产物存在性 + 关键内容标记 + pipeline-state 步骤状态对账；用法 `python tools/gate-guard.py --artifacts-dir <artifacts目录> --gate <part2\|part3\|finish>`，输出 JSON（gate/passed/checks），passed=false 时主理人拒绝过段并列出缺失项 |
| `templates/tds-template.md` | — | 结构化 TDS 模板（v2.4.0 新增）：技术方案设计（工序 2.1）按此模板产出，强制章节为段门校验项 |

## 7. 规则对接（Harness 平台工程治理）

> 规则清单与策略见工作区 `governance/rules-registry.md`、`governance/policies/`、`governance/rego-skill-mapping.md`。本环节是**数据库与 API 契约的唯一设计源**，直接决定生成代码能否通过后端质量门禁。

- **关联规则**：BE-DB-001~005（事务隔离/三字段体系/审计字段/索引/Liquibase groovy）、BE-DEV-005（API URI 规约：复数名词、无 `_`/大写）、FLOW-006（单测行覆盖率 ≥ 60%，关键模块 ≥ 80%）
- **关联策略**：`policies/be-quality-gates.rego`（BE-STYLE / BE-DEV / FLOW-005 / FLOW-006，Checkstyle + 覆盖率门禁）
- **对接方式**：数据库设计 Sheet 必须含审计字段（object_version_number/creation_date/created_by/last_update_date/last_updated_by）与序列/唯一约束，生成 Liquibase groovy 骨架（BE-DB-005）；API 设计按 BE-DEV-005 规约校验路径；测试计划内嵌覆盖率目标（≥ 60% / 关键模块 ≥ 80%）作为 FLOW-006 门禁的输入
- **门禁结论**：表设计缺审计字段/非 Liquibase → 生成代码被 BE-DB 模板策略阻断；计划未排覆盖率门禁 → CI On Run 被 FLOW-006 拦截

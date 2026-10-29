---
id: rd-code-review
name: 代码审查
description: 对生成的 HZERO 后端代码和 choerodon-ui 前端代码进行全面审查（含 DevSecOps 安全审查清单与可测试性审查），输出审查报告
version: 1.4.0
stage: 5
trigger_patterns:
  - 代码审查
  - 代码检查
  - code review
  - 审查代码
  - 代码质量检查
  - 安全审查
output_artifact: review-report.json
---

# Skill: 代码审查 (Code Review)

## 1. 职责范围

### 核心任务
对代码生成环节产出的全部源代码进行系统性审查，覆盖：HZERO框架规范符合性、choerodon-ui组件使用规范、编码质量、安全漏洞（DevSecOps 四类扫描）、性能隐患、业务逻辑正确性、可测试性。输出审查报告（`review-report.json`），作为测试环节的入口依据。

### 边界定义
- **负责**：代码规范审查、安全审查、性能审查、业务逻辑一致性审查、HZERO/choerodon-ui框架规范审查
- **不负责**：需求变更、代码修改（仅报告问题）、部署、测试执行
- **上游**：代码生成（④）
- **下游**：测试（⑥），审查通过后代码才可进入测试

## 2. 输入

### 输入产物
| 产物 | 路径 | 用途 |
|------|------|------|
| 代码清单 | `artifacts/04-code/code-manifest.json` | 获取所有生成文件清单 |
| 后端代码 | `artifacts/04-code/backend/` | 审查对象 |
| 前端代码 | `artifacts/04-code/frontend/` | 审查对象 |
| SQL脚本 | `artifacts/04-code/sql/` | 审查对象 |
| 开发计划 | `artifacts/03-planning/dev-plan.json` | 对照API设计和数据库设计 |
| 需求规格 | `artifacts/01-requirement/requirement-spec.json` | 对照业务需求 |

### L1 入口校验
- [ ] `code-manifest.json` 存在且格式合法
- [ ] `code-manifest.json._meta.qualityGateStatus` = "PASSED"
- [ ] `generatedFiles` 数组非空
- [ ] 后端代码目录存在且文件可读
- [ ] 前端代码目录存在且文件可读

## 3. 输出

### 产物文件
`artifacts/05-review/review-report.json`

### 产物结构规范

```json
{
  "_meta": {
    "stage": "code-review",
    "version": "1.0.0",
    "createdAt": "ISO 8601时间",
    "createdBy": "WorkBuddy",
    "upstreamArtifacts": ["../04-code/code-manifest.json"],
    "qualityGateStatus": "PASSED"
  },
  "summary": {
    "totalFiles": 10,
    "filesReviewed": 10,
    "findingsCount": 5,
    "criticalCount": 0,
    "majorCount": 1,
    "minorCount": 4,
    "suggestionCount": 2,
    "reviewDecision": "APPROVED/CONDITIONAL_APPROVE/REJECTED"
  },
  "findings": [
    {
      "id": "FIND-001",
      "severity": "CRITICAL/MAJOR/MINOR/SUGGESTION",
      "category": "HZERO_COMPLIANCE/CHOERODON_UI_COMPLIANCE/CODING_STANDARD/SECURITY/PERFORMANCE/BUSINESS_LOGIC/DATABASE",
      "file": "文件路径",
      "line": 42,
      "codeSnippet": "问题代码片段",
      "issue": "问题描述",
      "reason": "为什么是问题",
      "suggestion": "修复建议",
      "fixRequired": true,
      "source": "ai-review",
      "ruleId": null
    },
    {
      "id": "FIND-002",
      "severity": "MAJOR",
      "category": "HZERO_COMPLIANCE",
      "file": "src/main/java/.../Controller.java",
      "line": 30,
      "codeSnippet": "@Permission(permissionCode = 'xxx')",
      "issue": "@Permission 缺少 level 属性",
      "reason": "权限级别缺失导致租户级/平台级判定不明确",
      "suggestion": "补充 level = PermissionLevel.TENANT",
      "fixRequired": true,
      "source": "ast-grep",
      "ruleId": "java-permission-missing-level"
    }
  ],
  "staticScan": {
    "scanned": true,
    "tool": "ast-grep scan（降级时为 manual-checklist）",
    "config": "rd-code-review/ast-grep-rules/sgconfig.yml",
    "totalFindings": 1,
    "errorCount": 1,
    "warningCount": 0,
    "status": "PASSED/FAILED"
  },
  "categoryStats": {
    "HZERO_COMPLIANCE": {
      "total": 2,
      "critical": 0,
      "major": 1,
      "passed": true
    },
    "CHOERODON_UI_COMPLIANCE": {
      "total": 1,
      "critical": 0,
      "major": 0,
      "passed": true
    },
    "SECURITY": {
      "total": 0,
      "critical": 0,
      "major": 0,
      "passed": true
    }
  },
  "checklists": {
    "hzeroCompliance": [
      {
        "item": "检查项描述",
        "status": "PASSED/FAILED/NA"
      }
    ],
    "choerodonUiCompliance": [],
    "security": [],
    "performance": [],
    "testability": []
  },
  "securityFindings": {
    "secretScan": {
      "scanned": true,
      "tool": "gitleaks/grep 正则扫描",
      "findings": ["硬编码密码/密钥/Token（含 application.yml、配置文件、代码常量）"],
      "status": "PASSED/FAILED"
    },
    "dependencyScan": {
      "scanned": true,
      "tool": "npm audit / OWASP Dependency-Check",
      "criticalVulnerabilities": 0,
      "highVulnerabilities": 0,
      "status": "PASSED/FAILED"
    },
    "sastScan": {
      "scanned": true,
      "tool": "SonarQube / SpotBugs",
      "issues": [
        {
          "rule": "规则编码",
          "severity": "CRITICAL/MAJOR",
          "file": "文件路径",
          "disposition": "FIXED/WONTFIX/REVIEWED"
        }
      ],
      "status": "PASSED/FAILED"
    },
    "horizontalPrivilegeCheck": {
      "checked": true,
      "result": "所有数据访问已校验租户/归属（tenant_id + 数据权限）",
      "status": "PASSED/FAILED"
    }
  }
}
```


### 阶段报告（人工交付物）

`reports/05-代码审查-阶段报告.md`

按《阶段报告编写规范》（`kb/07-项目管理/03-阶段报告编写规范.md`）输出，固定四段结构：

1. **阶段目标**：本环节在主流程中的定位、上游输入、完成标志
2. **主要产出**：产物清单表（产物/格式/路径/用途去向）
3. **关键结论**：核心指标与结论，用表格/流程图呈现，禁止大段纯文字
4. **风险与建议**：风险/遗留项 + 等级(高/中/低) + 建议动作

> 结构化数据（问题清单、测试结果等）另出 Excel 数据表，报告内以汇总表格引用。

### Excel 数据表（结构化产物）

`artifacts/05-review/review-issues.xlsx`

- **Sheet1 问题清单**：编号 / 严重级别(P0~P3) / 类型 / 规则ID / 文件:行号 / 问题描述 / 修复建议 / 状态
- **Sheet2 汇总统计**：按严重级别与类型计数、修复率、门禁达标判定
- 样式：表头 `#1B83FF` 白字、冻结首行、斑马纹（对齐《开发计划 Excel 规范》）
- 与 `review-report.json` 同步生成，矛盾时以 JSON 为准

## 4. 关键约束

### 4.0 静态检查层（v1.4.0 新增，hzero-copilot 借鉴）

AI 审查开始前，先执行 **ast-grep 静态扫描**，用确定性规则滤掉机械性违规，AI 精力聚焦架构与逻辑层：

```bash
# 有 ast-grep 时（推荐）
ast-grep scan -c <技能目录>/ast-grep-rules/sgconfig.yml <工程源码目录> --json > ast-grep-result.json
# 未安装 ast-grep 时降级：按 §4.0.2 清单人工逐文件核对
```

#### 4.0.1 内置规则（11 条，位于 `ast-grep-rules/rules/`，来源 hzero-spec 0.3.5）

| 规则 ID | 检查内容 | severity |
|---|---|---|
| java-direct-jdbc-template | 禁直连 JdbcTemplate / NamedParameterJdbcTemplate | error |
| java-controller-depend-mapper | Controller 禁依赖 Mapper（必须走 Service/AppService） | error |
| java-permission-missing-level | `@Permission` 缺 level 属性 | error |
| java-controller-missing-api | Controller 缺 `@Api` 注解 | error |
| java-controller-api-tags-no-chinese | Swagger tags 禁用中文 | error |
| java-controller-extra-top-level-class | Controller 文件禁多余顶层类 | error |
| java-interface-method-missing-comment | 接口方法缺注释 | warning |
| java-serviceimpl-method-missing-comment | ServiceImpl 方法缺注释 | warning |
| java-entity-field-missing-comment | Entity 字段缺注释 | warning |
| java-entity-field-missing-column-marker | Entity 字段缺 `@Column` 标记 | warning |
| java-controller-serviceimpl-inner-class | Controller/ServiceImpl 内部类滥用 | warning |

#### 4.0.2 结果处理

- 命中项直接写入 `review-report.json` 的 findings：`source` 字段标 `"ast-grep"`（降级人工核对时标 `"manual-checklist"`），`ruleId` 取规则 ID，AI 自查项 `source` 标 `"ai-review"`；同时在 report 顶层新增 `staticScan` 汇总块
- severity 映射：`error → MAJOR`、`warning → MINOR`（对齐 §4.2 严重级别定义）；与 AI 审查发现的问题合并去重（同文件同行只保留一条，优先保留 AI 补充的上下文说明）
- **静态层命中不免除 AI 审查**：静态规则只覆盖语法可判定的机械违规，分层错误、事务缺失、租户遗漏等语义问题仍按 §4.1 各维度审查
- 降级模式（无 ast-grep）：将上表作为检查清单，对 `**/*Controller.java`、`**/*ServiceImpl.java`、`**/*Entity.java`、`**/repository/**/*.java` 逐文件核对，结果同样写入 issues（source 标 `"manual-checklist"`）

### 4.1 审查维度与检查项

#### 维度1：HZERO框架规范审查
| 检查项 | 审查标准 |
|--------|---------|
| DDD分层 | 类文件位于正确分层（api/app/domain/infra） |
| 实体规范 | 继承 `AuditDomain`，使用 `@Table`、`@Id`、`@GeneratedValue` 注解 |
| Repository规范 | 接口继承 `BaseRepository<Xxx>`，实现继承 `BaseRepositoryImpl` |
| Mapper规范 | 接口继承 `BaseMapper<Xxx>`，XML位于resources/mapper |
| Controller规范 | 继承 `BaseController`，使用 `@Permission`，返回 `ResponseEntity` |
| 事务控制 | Service层写操作使用 `@Transactional(rollbackFor = Exception.class)` |
| 乐观锁 | 更新/删除前调用 `SecurityTokenHelper.validToken(xxx)` |
| 多租户 | 业务表SQL含tenant_id条件，实体含租户注解 |
| 参数校验 | Controller使用 `validObject()` 或 `@Validated` 校验请求体 |
| 统一响应 | 使用 `Results.success()` 包装返回 |
| Swagger文档 | 类使用 `@Api`，方法使用 `@ApiOperation`，字段使用 `@ApiModelProperty` |
| 权限编码 | `@Permission` 已配置，权限编码与dev-plan一致 |

#### 维度2：choerodon-ui组件规范审查
| 检查项 | 审查标准 |
|--------|---------|
| 组件来源 | 仅从 `choerodon-ui` 或 `choerodon-ui/pro` 导入 |
| 禁止库 | 未引入 antd/antd-pro/material-ui 等 |
| DataSet | 数据组件已绑定DataSet，未直接操作DOM |
| 导入路径 | Pro组件从 `choerodon-ui/pro` 导入，核心组件从 `choerodon-ui` 导入 |
| 版本锁定 | package.json中 `choerodon-ui` 版本 = 1.6.6 |
| 样式规范 | 样式使用LESS，类名遵循BEM或模块化 |
| 国际化 | 文案未硬编码，使用多语言配置 |
| 组件API | 使用的props为choerodon-ui v1.6.6支持的API |

#### 维度3：编码质量审查
| 检查项 | 审查标准 |
|--------|---------|
| 命名规范 | 类PascalCase，方法/变量camelCase，常量UPPER_SNAKE_CASE |
| 注释规范 | 类有Javadoc注释（说明+作者+日期），方法有注释 |
| 代码重复 | 无重复代码块（可抽取公共方法） |
| 魔法数 | 无未命名魔法数（应使用常量/枚举） |
| 日志规范 | 使用SLF4J Logger，禁止System.out.println |
| 空值处理 | 合理处理null，避免NPE |
| 异常处理 | 禁止捕获后吞掉异常，应有明确处理 |
| 资源释放 | 流/连接正确关闭（try-with-resources） |
| 未使用代码 | 无未使用的import、变量、方法 |

#### 维度4：安全审查（DevSecOps，v1.1.0 扩充）
| 检查项 | 审查标准 |
|--------|---------|
| SQL注入 | Mapper XML使用`#{}`参数绑定，未拼接字符串 |
| XSS防护 | 前端渲染未使用dangerouslySetInnerHTML注入用户内容 |
| 越权防护 | Controller有`@Permission`权限控制 |
| 敏感数据 | 未硬编码密码/密钥，敏感字段脱敏 |
| 文件上传 | 上传校验文件类型和大小 |
| 越权访问 | 数据访问校验tenant_id归属 |
| 密钥扫描 | 无硬编码密码/密钥/Token（代码、application.yml、常量），凭据走配置中心/环境变量 |
| 依赖漏洞 | 依赖无已知高危漏洞（npm audit / OWASP Dependency-Check），高危已修复或风险评估 |
| SAST复核 | SonarQube/SpotBugs 扫描结果已逐条人工复核，CRITICAL 级全部修复 |
| 水平越权 | 数据级归属校验（tenant_id + 创建人/负责人），非仅接口级@Permission |
| 日志安全 | 日志不输出敏感信息（密码/Token/身份证/手机号等） |
| 传输安全 | 敏感接口走 HTTPS，前端代码不暴露任何密钥 |

#### 维度7：可测试性审查（质量左移，v1.1.0 新增）
| 检查项 | 审查标准 |
|--------|---------|
| 单测骨架 | 核心 Service/工具类含单元测试（命名 XxxTest.java，位于 src/test） |
| 可测试设计 | 依赖通过构造注入/接口注入，可 mock；无强耦合单例/静态调用阻碍测试 |
| 断言有效 | 测试断言具体结果，非空转（无空方法体/无断言测试） |
| 契约一致 | 前后端 API 路径/参数/响应与 dev-plan.apiDesign 契约一致（契约测试可执行） |
| 冒烟入口 | 系统含冒烟用例可自动执行的入口（健康检查端点 + 核心链路脚本） |

#### 维度5：性能审查
| 检查项 | 审查标准 |
|--------|---------|
| N+1查询 | 循环内未执行查询（应联查或批量查询） |
| 分页 | 列表查询使用PageHelper分页 |
| 索引利用 | 查询条件字段有索引 |
| 前端大数据 | 数据量>500行使用PerformanceTable |
| 前端性能 | 列表未一次性加载大量DOM节点 |
| 缓存使用 | 频繁访问数据考虑Redis缓存 |

#### 维度6：数据库审查
| 检查项 | 审查标准 |
|--------|---------|
| 标准字段 | 表含id/tenant_id/审计字段 |
| 索引 | 多租户联合索引，外键索引 |
| 字符集 | utf8mb4 |
| 存储引擎 | InnoDB |
| 字段类型 | 类型和长度合理（varchar长度、decimal精度） |
| 注释 | 表和字段有COMMENT |

### 4.2 严重级别定义

| 级别 | 定义 | 处理方式 |
|------|------|---------|
| CRITICAL | 数据损坏、安全漏洞、功能完全不可用 | 必须修复，否则REJECTED |
| MAJOR | 功能部分不可用、严重性能问题、明显规范违规 | 必须修复，否则CONDITIONAL_APPROVE |
| MINOR | 局部问题、轻微规范违规、边界场景缺陷 | 建议修复 |
| SUGGESTION | 优化建议、代码风格改进 | 可选 |

### 4.3 审查决策规则

| 决策 | 条件 | 是否流转 |
|------|------|---------|
| APPROVED | critical=0, major=0 | ✅ 流转至测试 |
| CONDITIONAL_APPROVE | critical=0, major≤3且均可快速修复 | ⚠️ 修复major后流转 |
| REJECTED | critical>0 或 major>3 | ❌ 退回代码生成环节 |

## 5. 衔接方式

### 5.1 与上游的接口协议
- 读取 `code-manifest.json` 获取文件清单
- 逐个读取文件进行审查
- 对照 `dev-plan.json` 和 `requirement-spec.json` 验证一致性

### 5.2 与下游的接口协议

| 下游环节 | 交付内容 | 使用方式 |
|---------|---------|---------|
| ⑥测试 | `review-report.json` 全文 | 仅当 `reviewDecision` = "APPROVED" 时测试方可启动 |

### 5.3 数据流转方式
- 产物文件路径：`artifacts/05-review/review-report.json`
- `_meta.upstreamArtifacts` 记录上游产物路径

### 5.4 质量门禁标准

#### L1 - 入口校验
- [ ] `code-manifest.json` 存在且 `qualityGateStatus` = "PASSED"
- [ ] 代码文件可读取

#### L2 - 过程校验
- [ ] 所有文件已逐个审查（filesReviewed = totalFiles）
- [ ] 七大维度均已覆盖检查（含安全 DevSecOps 与可测试性）
- [ ] 每个finding有严重级别和修复建议
- [ ] securityFindings 四类扫描（密钥/依赖/SAST/水平越权）已执行且状态明确

#### L3 - 出口校验（验收检查项）
- [ ] CRITICAL问题 = 0
- [ ] MAJOR问题 ≤ 3
- [ ] 所有CRITICAL/MAJOR问题有修复建议
- [ ] HZERO规范通过率 ≥ 90%
- [ ] choerodon-ui规范通过率 = 100%（无违规使用其他UI库）
- [ ] `_meta.qualityGateStatus` = "PASSED"

## 6. 交付标准

### 验收检查项清单

| 序号 | 检查项 | 标准 | 必须 |
|------|--------|------|------|
| 1 | 产物文件已生成 | `review-report.json` 存在 | 是 |
| 2 | JSON格式合法 | 通过JSON Schema校验 | 是 |
| 3 | 全覆盖审查 | 所有生成文件已审查 | 是 |
| 4 | 七维覆盖 | HZERO/choerodon-ui/编码/安全/性能/数据库/可测试性均覆盖 | 是 |
| 5 | 严重级别 | 每个finding有severity | 是 |
| 6 | 修复建议 | 每个finding有suggestion | 是 |
| 7 | 类别统计 | categoryStats完整 | 是 |
| 8 | 决策明确 | reviewDecision为APPROVED/CONDITIONAL_APPROVE/REJECTED | 是 |
| 9 | 质量门禁 | CRITICAL=0，MAJOR≤3 | 是 |
| 10 | 流转判定 | 决策为APPROVED才可流转 | 是 |
| 11 | 阶段报告 | `reports/05-代码审查-阶段报告.md` 已生成，四段结构完整 | 是 |

### 执行流程

```
Step 1: 读取 code-manifest.json，执行L1入口校验
Step 2: 遍历所有后端文件 — HZERO规范审查
  Step 2.1: DDD分层位置检查
  Step 2.2: 类结构/注解/继承检查
  Step 2.3: 事务/乐观锁/权限检查
  Step 2.4: SQL安全/多租户检查
Step 3: 遍历所有前端文件 — choerodon-ui规范审查
  Step 3.1: 组件来源检查
  Step 3.2: DataSet绑定检查
  Step 3.3: 国际化/样式检查
Step 4: 编码质量审查（命名/注释/重复/魔法数）
Step 5: 安全审查（DevSecOps 四类扫描）
  Step 5.1: 密钥/凭据扫描（gitleaks/grep：密码/Token/密钥）
  Step 5.2: 依赖漏洞扫描（npm audit / OWASP DC）
  Step 5.3: SAST 结果复核（SonarQube/SpotBugs CRITICAL/MAJOR）
  Step 5.4: 水平越权检查（tenant_id + 数据归属）
  Step 5.5: 注入/XSS/日志安全/敏感数据
Step 6: 性能审查（N+1/分页/索引/大数据渲染）
Step 7: 数据库审查（标准字段/索引/字符集）
Step 8: 可测试性审查（单测骨架/可测试设计/断言有效/契约一致/冒烟入口）
Step 9: 汇总finding，分类统计，填充 securityFindings
Step 10: 根据规则判定 reviewDecision
Step 11: 执行L2/L3质量门禁检查
Step 12: 生成 review-report.json
Step 13: 输出产物路径，标记流转就绪（或退回）
```

## 6.5 双轴评审（Two-Axis Review，v1.3.0 新增）

> 方法论源自 code-review 技能（mattpocock/skills）：一份变更可以规范全对但实现错了需求，也可以忠实实现了需求却破坏项目约定。**两条轴分开报告，互不合并、互不重排序**——否则一条轴会掩盖另一条。

### 双轴定义

| 轴 | 问题 | 数据源 | 输出位置 |
|----|------|--------|---------|
| **Standards（规范轴）** | 代码是否符合本项目成文规范与框架约定？ | §4.1 七维检查项 + 下方坏味道基线 | `findings` 中 category 为 HZERO_COMPLIANCE/CHOERODON_UI_COMPLIANCE/CODING_STANDARD 的条目 |
| **Spec（规格轴）** | 代码是否忠实实现了需求/契约？ | `requirement-spec.json` 验收标准 + `dev-plan.json` API 契约 | `findings` 中 category 为 BUSINESS_LOGIC 的条目，并新增 `specDeviation` 字段 |

### Spec 轴三类发现（新增到 finding 结构）

每个 FR / API 契约逐条对照代码，报告三类问题：

1. **缺失/部分实现**：规格要求了但代码没做或做了一半 → `specDeviation: "MISSING/PARTIAL"`
2. **范围蔓延（scope creep）**：代码做了规格没要求的事 → `specDeviation: "SCOPE_CREEP"`
3. **实现疑似错误**：看起来实现了但行为与规格相悖 → `specDeviation: "WRONG"`，引用对应规格条目原文

### 执行流程修订

在原 Step 1~9 基础上：Step 4.5（新增）**Spec 轴对照**——读取 requirement-spec 与 dev-plan，逐 FR/契约走查三类发现；Step 9 汇总时**保留两轴分列**，`summary` 新增 `specAxis: { missingCount, scopeCreepCount, wrongCount }`；阶段报告"关键结论"两轴各一行总结，**不跨轴选唯一最严重项**。

### 评审顺序约束（防上下文污染）

两轴走查分两遍独立执行（先 Standards 全量过一遍，再 Spec 全量过一遍），不逐文件混合评审——混合会让规格问题被规范问题淹没。有条件时分派两个并行子代理分别执行，主流程仅聚合。

### 规范轴坏味道基线（Fowler 基线，v1.3.0 新增）

在 §4.1 七维检查项之外，规范轴始终携带以下坏味道基线（源自《重构》第 3 章），逐条按「是什么 → 怎么修」对照 diff。两条约束：**项目成文规范优先**（规范明确认可的写法，压制对应坏味道）；**基线永远是判断题**（标注为"疑似 X 坏味道"，不是硬违规；工具已强制的项跳过）。

| 坏味道 | 识别特征 | 修复方向 |
|--------|---------|---------|
| Mysterious Name | 命名不能揭示用途 | 重命名；起不出诚实的名字说明设计混浊 |
| Duplicated Code | 同一逻辑形状出现在多处改动中 | 提取共享形状 |
| Feature Envy | 方法访问别的对象的数据多于自己的 | 把方法搬到它艳羡的数据上 |
| Data Clumps | 几个字段/参数总是结伴出现 | 捆成一个类型 |
| Primitive Obsession | 用原始类型/字符串顶替领域概念 | 给概念一个自己的小类型 |
| Repeated Switches | 同一类型上的 switch/if 级联反复出现 | 多态或共享映射表 |
| Shotgun Surgery | 一个逻辑变更迫使散落多文件的编辑 | 把一起变的聚到一个模块 |
| Divergent Change | 一个文件因多个不相关原因被改 | 按变更原因拆分模块 |
| Speculative Generality | 规格没需求的抽象/参数/钩子 | 删掉，等真需求出现 |
| Message Chains | 长链 `a.b().c().d()` 导航 | 首对象上封一个方法藏住链 |
| Middle Man | 类/函数几乎只做转发 | 去掉中间人直连目标 |
| Refused Bequest | 子类无视/覆盖大部分继承内容 | 弃继承用组合 |

`findings` 中对应条目 `category: "CODING_STANDARD"`，`issue` 格式为「疑似 {坏味道}：{特征描述}」，`fixRequired: false`（判断题不强制）。

## 7. 规则对接（Harness 平台工程治理）

> 规则清单与策略见工作区 `governance/rules-registry.md`、`governance/policies/`、`governance/rego-skill-mapping.md`。审查是本体系消费规则最多的环节。

- **关联规则**：BE-DEV-002/007/009（跨层调用/异常/DDD 分层）、BE-SQL 系列（SQL 红线）、SEC-001（凭据不入代码）、FE-CODE 系列（前端代码规范）
- **关联策略**：`policies/be-quality-gates.rego`、`policies/git-governance.rego`
- **对接方式**：审查报告 findings 按**规则 ID** 组织（如 `BE-DEV-002: Controller 调 Mapper`）；严重级别对齐规则分级（P0→Blocker / P1→Major / P2→Minor）；可调用 Harness API 拉取该分支最近 OPA 评估结果作为审查输入（只读，不绕过）
- **门禁结论**：P0 违规 → `reviewDecision` 不得 APPROVED；P1（稳定期）违规 → 同 P0 阻断，先修复再流转

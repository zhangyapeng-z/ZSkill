# JSON 结构化审查报告 Schema

本文件定义 `review-report.json` 的结构，作为机器可读的标准化审查报告格式，便于 CI/CD 门禁对接与二次开发。

---

## 顶层结构

```
ReviewReport
├── meta                      # 审查元信息
├── projectInfo               # 工程信息
├── techStack                 # 技术栈识别结果
├── serviceInventory          # 服务清单
├── callGraph                 # 服务间调用关系图
├── summary                   # 问题统计汇总
├── issues[]                  # 问题详情列表
└── modificationPlan[]         # 结构化修改计划
```

---

## 字段定义

### meta — 审查元信息

| 字段 | 类型 | 说明 |
|------|------|------|
| reportId | string | 报告唯一 ID（时间戳+工程名哈希） |
| generatedAt | string | 生成时间 ISO 8601 |
| toolVersion | string | 工具版本 |
| ruleVersion | string | 规则版本 |
| reviewer | string | 审查者（脚本/人工） |

### projectInfo — 工程信息

| 字段 | 类型 | 说明 |
|------|------|------|
| projectRoot | string | 工程根路径 |
| buildTool | string | 构建工具（Maven/Gradle） |
| rootArtifactId | string | 根 artifactId |
| serviceCount | int | 服务数 |
| moduleCount | int | 模块数 |
| totalJavaFiles | int | Java 文件总数 |
| totalLines | int | 代码总行数 |

### techStack — 技术栈识别结果

```json
{
  "isMicroservice": true,
  "frameworks": [
    { "name": "Spring Cloud OpenFeign", "category": "communication", "version": "3.1.x" },
    { "name": "Sentinel", "category": "circuit-breaker", "version": "1.8.x" },
    { "name": "Nacos", "category": "discovery", "version": "2.x" }
  ],
  "gaps": ["未识别到分布式事务方案"]
}
```

### serviceInventory — 服务清单

```json
[
  {
    "serviceName": "order-service",
    "artifactId": "order-app",
    "port": 8081,
    "mainClass": "com.xxx.order.OrderApplication",
    "techStack": ["spring-boot", "openfeign", "nacos"],
    "javaFileCount": 86,
    "totalLines": 12000,
    "apiCount": 24,
    "database": "jdbc:mysql://db:3306/order_db"
  }
]
```

### callGraph — 服务间调用关系图

```json
{
  "nodes": ["order-service", "payment-service", "inventory-service"],
  "edges": [
    { "from": "order-service", "to": "payment-service", "type": "feign", "method": "createPayment", "hasFallback": true },
    { "from": "order-service", "to": "inventory-service", "type": "feign", "method": "deductStock", "hasFallback": false }
  ],
  "maxDepth": 3,
  "cycles": []
}
```

### summary — 问题统计汇总

```json
{
  "totalIssues": 23,
  "bySeverity": { "Blocker": 2, "Critical": 6, "Major": 11, "Minor": 4 },
  "byDimension": {
    "architecture": 12,
    "code-quality": 11
  },
  "byRule": {
    "M-03": 1, "M-04": 2, "M-05": 3,
    "Q-02": 2, "Q-03": 4, "Q-05": 3
  },
  "confirmedCount": 18,
  "pendingCount": 5
}
```

### issues[] — 问题详情列表

```json
[
  {
    "issueId": "ISS-001",
    "ruleId": "M-03",
    "ruleName": "数据一致性（共享业务库）",
    "severity": "Blocker",
    "dimension": "architecture",
    "confidence": "high",
    "status": "confirmed",
    "serviceName": "order-service,payment-service",
    "filePath": "order-service/src/main/resources/application.yml",
    "lineNumber": 12,
    "description": "order-service 与 payment-service 共享同一业务数据库 order_db，破坏服务自治",
    "ruleReference": "M-03: 多服务直连同一业务库",
    "impact": "服务耦合，无法独立部署/扩缩容，故障连锁",
    "solution": "按服务拆分独立数据库，跨服务数据通过 API 获取；过渡期建立拆分计划表",
    "bestPractice": "Database-per-service 模式，每个微服务独占数据存储",
    "priority": "P0",
    "estimatedEffort": "高"
  }
]
```

**issue 字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| issueId | string | 问题唯一编号 ISS-NNN |
| ruleId | string | 规则编号（M-xx/Q-xx） |
| ruleName | string | 规则名称 |
| severity | enum | Blocker/Critical/Major/Minor |
| dimension | enum | architecture/code-quality |
| confidence | enum | high/medium/low（置信度） |
| status | enum | confirmed/pending（已确认/待人工复核） |
| serviceName | string | 涉及服务 |
| filePath | string | 文件路径 |
| lineNumber | int | 行号 |
| description | string | 问题描述 |
| ruleReference | string | 规则条款引用 |
| impact | string | 影响说明 |
| solution | string | 具体解决方案 |
| bestPractice | string | 最佳实践建议 |
| priority | enum | P0/P1/P2/P3 |
| estimatedEffort | enum | 低/中/高 |

### modificationPlan[] — 结构化修改计划

```json
[
  {
    "planId": "PLAN-P0-01",
    "priority": "P0",
    "severity": "Blocker",
    "title": "消除 order/payment 共享业务库",
    "issueIds": ["ISS-001"],
    "steps": [
      { "step": 1, "action": "梳理 order_db 中各表的归属服务（order 域/payment 域）", "files": ["order_db schema"] },
      { "step": 2, "action": "为 payment-service 创建独立 payment_db，迁移 payment 域表", "files": ["payment-service/**"] },
      { "step": 3, "action": "order-service 跨服务获取 payment 数据改为 Feign 调用", "files": ["order-service/**FeignClient"] },
      { "step": 4, "action": "数据校验与双写过渡期对账，确认无误后切除共享连接", "files": ["order-service/application.yml"] }
    ],
    "impactScope": "order-service、payment-service 两个服务的数据库与数据访问层",
    "riskAssessment": {
      "riskLevel": "高",
      "risks": ["数据迁移期间双写一致性", "跨服务调用增加延迟", "回滚复杂度高"],
      "mitigation": ["迁移期保留双写+对账", "跨服务查询加缓存", "分表灰度迁移可回滚"]
    },
    "verification": "迁移后对账数据一致；服务独立部署验证；故障注入验证隔离性",
    "owner": "待分配",
    "dueDate": "待定"
  }
]
```

**modificationPlan 字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| planId | string | 计划编号 PLAN-PN-NN |
| priority | enum | P0 立即/P1 本迭代/P2 下迭代/P3 择机 |
| severity | enum | 对应问题最高严重级别 |
| title | string | 修改计划标题 |
| issueIds | string[] | 关联问题编号 |
| steps[] | array | 修改步骤（step/action/files） |
| impactScope | string | 影响范围 |
| riskAssessment | object | 风险评估（riskLevel/risks/mitigation） |
| verification | string | 验证方式 |
| owner | string | 负责人 |
| dueDate | string | 截止日期 |

---

## CI/CD 门禁对接

报告为 JSON，可直接用于流水线门禁：

```yaml
# 示例门禁策略：存在 Blocker 或 Critical > 阈值则阻断
gate:
  block_on_severity: [Blocker]
  block_on_critical_count_above: 0
  warn_on_pending_above: 10
```

解析 `review-report.json` → 检查 `summary.bySeverity.Blocker > 0` → 阻断流水线。

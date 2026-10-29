# 报告输出模板与格式规范

本文档定义架构与代码质量检查报告的标准格式。

---

## 一、Markdown 报告模板

```markdown
# 微服务架构规范与代码质量检查报告

> 检查时间: YYYY-MM-DD HH:MM:SS
> 工程名称: {rootArtifactId}
> 模块数量: {moduleCount}
> 源文件数: {totalJavaFiles}
> 代码行数: {totalLines}

---

## 一、问题统计

| 严重级别 | 数量 | 说明 |
|----------|------|------|
| Blocker | N | 阻塞性问题，立即修复 |
| Critical | N | 严重问题，本迭代修复 |
| Major | N | 重要问题，下迭代修复 |
| Minor | N | 次要问题，择机修复 |
| **合计** | **N** | |

## 二、架构检查结果

### A-XX [严重级别] (N 个问题)

**规则:** 规则条款引用

**问题 1:**
- 文件: `path/to/file.java`
- 行号: N
- 描述: 问题描述
- 建议: 修复建议

## 三、代码质量检查结果

### 命名规范 (N 个问题)

| # | 级别 | 规则 | 文件 | 行号 | 问题描述 | 修复建议 |
|---|------|------|------|------|----------|----------|
| 1 | Major | N-01 | `file.java` | 10 | 描述 | 建议 |

## 四、修复优先级计划

### P0 — 立即修复（阻塞发布） (N 个)

1. [A-03] `file.java:0` — 问题描述
2. [A-01] `file.java:0` — 问题描述

### P1 — 本迭代修复 (N 个)

1. [E-01] `file.java:25` — 问题描述

### P2 — 下个迭代修复 (N 个)

...

### P3 — 择机修复 (N 个)

...

---
*报告生成时间: YYYY-MM-DD HH:MM:SS*
```

---

## 二、HTML 报告结构

HTML 报告包含以下区域：

1. **页头区域** — 渐变背景，显示工程名称、检查时间、基本统计
2. **统计卡片** — 4 个卡片分别显示 Blocker/Critical/Major/Minor 数量
3. **架构检查结果** — 表格形式，每行一个问题
4. **代码质量检查结果** — 按类别分组，每组一个表格
5. **修复优先级计划** — 按 P0-P3 分组，带优先级颜色标记
6. **页脚** — 生成时间

### 颜色方案

| 级别 | 颜色 | 用途 |
|------|------|------|
| Blocker | #dc3545 (红色) | 统计数字、徽章、P0 标题 |
| Critical | #fd7e14 (橙色) | 统计数字、徽章、P1 标题 |
| Major | #ffc107 (黄色) | 统计数字、徽章、P2 标题 |
| Minor | #6c757d (灰色) | 统计数字、徽章、P3 标题 |

---

## 三、JSON 数据格式

### arch-issues.json / code-issues.json

```json
[
  {
    "ruleId": "A-03",
    "severity": "Blocker",
    "category": "architecture",
    "filePath": "pcm-common/pom.xml",
    "lineNumber": 0,
    "description": "循环依赖: pcm-common -> pcm-product-cost -> pcm-common",
    "ruleReference": "DDD分层规范: 模块间不允许循环依赖",
    "suggestion": "提取公共依赖到 common 模块"
  }
]
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| ruleId | string | 规则编号，如 A-01、N-01、E-01 |
| severity | string | 严重级别: Blocker / Critical / Major / Minor |
| category | string | 类别: architecture / naming / comments / exception / logging / collections / concurrency / control / oop |
| filePath | string | 问题所在文件路径（相对路径） |
| lineNumber | number | 问题所在行号（0 表示文件级问题） |
| description | string | 问题描述 |
| ruleReference | string | 规范条款引用 |
| suggestion | string | 修复建议 |

---

## 四、修复优先级矩阵

| 优先级 | 对应级别 | 处理时限 | 处理要求 |
|--------|----------|----------|----------|
| P0 | Blocker | 立即 | 阻塞发布，修复后才能合并代码 |
| P1 | Critical | 本迭代 | 当前迭代内必须修复 |
| P2 | Major | 下迭代 | 下个迭代计划修复 |
| P3 | Minor | 择机 | 技术债跟踪，择机修复 |

### 修复建议顺序

1. 先修复架构 Blocker（循环依赖、分层缺失）— 否则工程无法正常编译
2. 再修复架构 Critical（跨层调用、公共模块污染）— 影响架构可维护性
3. 然后修复代码 Critical（异常处理、并发问题）— 影响运行时稳定性
4. 最后批量修复 Major/Minor（命名规范、注释、日志）— 提升代码质量

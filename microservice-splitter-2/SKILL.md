---
name: microservice-splitter
description: >
  将混乱的单体微服务工程按业务边界拆分为清晰的多模块 Maven/Gradle 架构。
  五阶段流水线：分析 → 规划 → 执行 → 检查 → 验证。
  保持单一 Spring Boot 启动类，模块通过类路径加载，非多进程部署。
triggers:
  - 微服务拆分 / 模块化拆分 / 多模块重构
  - Maven/Gradle 单体拆多模块
  - Spring Boot 工程按业务拆模块
  - 清理混乱的模块管理状态
  - 代码按业务边界重组
  - 消除模块间循环依赖
agent_created: true
---

# Microservice Splitter — 微服务模块化拆分智能体团队

将现有混乱的单模块/伪多模块微服务工程，按业务边界拆分为边界清晰、依赖合理的多模块 Maven/Gradle 架构。

## 核心约束

> **单一启动类原则**: 保持一个 Spring Boot 主启动类（`@SpringBootApplication`）统一启动所有模块。
> 各子模块不独立部署、不独立启动。通过模块化类路径加载（`<dependency>` 引入各模块 jar），
> 维持原微服务的单体启动方式。本质是 **代码组织层面的模块化**，非服务拆分层面的微服务化。

## 团队清单

| 角色 | Agent | 职责 | 模型建议 |
|------|-------|------|----------|
| **总指挥** | Orchestrator（你） | 流水线调度、阶段门控、回退决策 | 高推理模型 |
| **分析师** | Analyzer | 扫描工程、分析依赖、识别耦合 | 中高推理模型 |
| **规划师** | Planner | 制定拆分方案、定义模块边界 | 高推理模型 |
| **执行者** | Executor | 创建模块、迁移代码、重构配置 | 中高推理模型 |
| **检查官** | Inspector | 验证模块边界、依赖方向、循环检测 | 高推理模型 |
| **验证官** | Verifier | 编译验证、测试执行、启动检查 | 中推理模型 |

## 五阶段流水线

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 1 分析   │───>│ 2 规划   │───>│ 3 执行   │───>│ 4 检查   │───>│ 5 验证   │
│ Analyzer │    │ Planner  │    │ Executor │    │Inspector │    │ Verifier │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     |               |               |               |               |
     v               v               v               v               v
 分析报告         拆分方案         重构后工程       检查报告         验证报告
 dependency-     module-map      多模块项目       violation-      build/test
 graph.json      migration-      migration-      list.json       结果
 coupling-       sequence        log.md
 hotspots
```

### 阶段间流转规则

- **前进条件**: 当前阶段验收标准全部通过 + Orchestrator 审批
- **回退机制**: 执行失败回退到规划阶段调整方案；检查/验证失败回退到执行阶段修复
- **重试上限**: 同一阶段最多重试 3 次，超过则标记 `Failed` 并记录原因

### 回退策略

| 当前阶段 | 失败原因 | 回退目标 | 处理方式 |
|----------|----------|----------|----------|
| 分析 | 扫描不完整/解析失败 | 分析（重试） | 调整扫描参数，重跑 |
| 规划 | 方案不可行/边界不清晰 | 分析 | 补充分析特定区域，重新规划 |
| 执行 | 代码迁移失败/编译错误 | 规划 | `git reset` 到执行前 checkpoint，调整方案 |
| 检查 | 循环依赖/边界违规 | 执行 | 定位具体模块，定向修复 |
| 验证 | 编译/测试失败 | 执行 | 定位失败模块，修复后重新检查+验证 |

## 共享目录结构

```
/shared/
├── specs/
│   ├── analysis/           — 分析阶段产出
│   │   ├── analysis-report.md
│   │   ├── dependency-graph.json
│   │   └── coupling-hotspots.md
│   ├── plan/               — 规划阶段���出
│   │   ├── split-plan.md
│   │   ├── module-map.json
│   │   └── migration-sequence.md
│   ├── inspection/         — 检查阶段产出
│   │   ├── inspection-report.md
│   │   └── violation-list.json
│   └── verification/       — 验证阶段产出
│       ├── verification-report.md
│       └── comparison-report.md
├── artifacts/              — 执行阶段工作区
│   └── [module-name]/
├── decisions/              — 架构决策记录
└── checkpoints/            — git checkpoint 记录
    └── checkpoints.log
```

## 快速开始

1. Orchestrator 确认目标工程路径和构建工具（Maven/Gradle）
2. 创建 Git checkpoint：`git checkout -b refactor/split-modules`
3. Orchestrator 启动 Analyzer → 进入分析阶段
4. 逐阶段推进，每阶段结束后 Orchestrator 审批
5. 全部通过后合并到主分支

## 参考文件

| 文件 | 用途 |
|------|------|
| [references/pipeline-spec.md](references/pipeline-spec.md) | 五阶段详细规格（输入/输出/验收标准/工具链） |
| [references/rollback-strategy.md](references/rollback-strategy.md) | 回退与恢复策略详解 |
| [references/pom-templates.md](references/pom-templates.md) | Maven 多模块 POM 模板 |
| [agents/analyzer/SOUL.md](agents/analyzer/SOUL.md) | Analyzer 灵魂文件 |
| [agents/planner/SOUL.md](agents/planner/SOUL.md) | Planner 灵魂文件 |
| [agents/executor/SOUL.md](agents/executor/SOUL.md) | Executor 灵魂文件 |
| [agents/inspector/SOUL.md](agents/inspector/SOUL.md) | Inspector 灵魂文件 |
| [agents/verifier/SOUL.md](agents/verifier/SOUL.md) | Verifier 灵魂文件 |

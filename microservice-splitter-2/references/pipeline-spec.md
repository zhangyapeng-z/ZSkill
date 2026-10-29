# 五阶段流水线规格说明

---

## 阶段一：分析阶段（Analyzer）

### 目标
全面扫描现有工程，产出工程结构全貌、模块间依赖关系和业务逻辑边界分析。

### 输入

| 输入项 | 类型 | 说明 |
|--------|------|------|
| 工程根路径 | `string` | 绝对路径，如 `/workspace/project` |
| 构建工具 | `enum` | `MAVEN` 或 `GRADLE` |
| 主模块标识 | `string`（可选） | Spring Boot 主启动类所在模块路径 |
| 已知业务域 | `string[]`（可选） | 用户提供的业务域名称列表，辅助边界识别 |

### 执行流程

```
1. 目录扫描
   ├── 递归列出所有目录和关键文件（排除 target/build/.git）
   ├── 识别现有模块结构（所有 pom.xml / build.gradle 文件位置）
   └── 输出：完整目录树（Markdown 格式）

2. 构建配置解析
   ├── 解析根 POM/build.gradle → 提取 GAV 坐标
   ├── 解析子模块声明（<modules> / settings.gradle include）
   ├── 解析依赖声明（<dependencies> / dependencies {}）
   ├── 执行 mvn dependency:tree -DoutputType=json 或 gradle dependencies --configuration compileClasspath
   └── 输出：依赖树 JSON（节点=artifact，边=依赖关系）

3. 代码层分析
   ├── 扫描所有 Spring 注解：@Service, @Component, @Repository, @Controller, @RestController
   ├── 扫描 @Configuration, @Bean, @SpringBootApplication
   ├── 按包路径对类进行聚类，形成"候选模块"
   ├── 提取每个 Java 文件的 import 语句
   ├── 构建包级依赖图：节点=包路��，边=import 关系，权重=引用次数
   └── 输出：包依赖矩阵

4. 业务边界识别
   ├── 从包命名推断业务域（如 com.xxx.order → "订单域"）
   ├── 按 Spring 注解聚类 → 识别各域内的 Controller/Service/Repository 分层
   ├── 检测跨域调用：包 A 的 Service 被包 B 的 Controller import
   ├── 识别职责重叠：同一业务逻辑（类名+方法签名相似度>80%）出现在多个包中
   └── 输出：业务域边界提案

5. 耦合热点检测
   ├── 循环依赖检测：DFS 遍历依赖图，找出所有环路
   ├── 高扇出包识别：被 10+ 个其他包依赖
   ├── 高扇入包识别：依赖 10+ 个其他包
   ├── 共享代码散落检测：util/constant/dto 类分布在多个包中
   └── 输出：耦合热点清单（含严重等级）
```

### 输出

| 输出文件 | 路径 | 内容 |
|----------|------|------|
| `analysis-report.md` | `/shared/specs/analysis/` | 目录树、模块清单、业务边界分析、Spring 组件统计 |
| `dependency-graph.json` | `/shared/specs/analysis/` | 完整依赖图数据（节点+边+权重），可被 d3.js/Graphviz 消费 |
| `coupling-hotspots.md` | `/shared/specs/analysis/` | 耦合热点清单，含严重等级（CRITICAL/WARNING/INFO）和处理建议 |

#### `analysis-report.md` 结构

```markdown
# 工程分析报告

## 1. 基本信息
- 工程路径: /path/to/project
- 构建工具: Maven 3.9 / Gradle 8.x
- 现有模块数: N
- Spring 组件总数: 含 Controller X, Service Y, Repository Z

## 2. 目录结构
(完整目录树，标注关键文件)

## 3. 现有模块清单
| 模块名 | 路径 | 类型 | 职责简述 | 问题标记 |
|--------|------|------|----------|----------|
| xxx    | /    | 单体 | ...      | 职责过重 |

## 4. 业务边界分析
### 识别的业务域
#### 域 A：订单（order）
- 包含类: N 个（Controller X, Service Y, Repository Z）
- 对外暴露: OrderController, OrderQueryService
- 对外依赖: UserService（用户域）, PaymentService（支付域）

#### 域 B：用户（user）
...

## 5. 依赖关系总览
(依赖图 Mermaid/ASCII art 可视化)

## 6. 初步建议
- 推荐拆分方向
- 注意风险区域
```

#### `dependency-graph.json` 结构

```json
{
  "project": "project-name",
  "buildTool": "MAVEN",
  "nodes": [
    {
      "id": "com.example.order",
      "label": "order",
      "type": "package",
      "componentCount": 25,
      "layer": "business"
    }
  ],
  "edges": [
    {
      "source": "com.example.order.controller",
      "target": "com.example.order.service",
      "type": "import",
      "weight": 15,
      "annotation": "OrderController -> OrderService"
    }
  ],
  "cycles": [
    {
      "path": ["com.example.a", "com.example.b", "com.example.c", "com.example.a"],
      "severity": "CRITICAL"
    }
  ]
}
```

### 验收标准

- [ ] 所有 `pom.xml` / `build.gradle` 已被解析，依赖关系完整
- [ ] 依赖图包含所有包级节点和 import 边
- [ ] 至少识别出 2 个有意义的业务域边界
- [ ] 至少识别出 3 个耦合热点（循环依赖、高扇出、职责重叠）
- [ ] 业务域边界提案有合理的命名和描述
- [ ] 分析报告包含可视化依赖图

### 异常处理

| 异常 | 处理 |
|------|------|
| `mvn dependency:tree` 执行失败 | 检查 Maven 配置和网络，回退到纯 POM 解析 |
| 包结构混乱无法推断业务域 | 请求用户提供业务域名称列表 |
| 项目过大（>500 类）扫描超时 | 分批扫描，按顶层包分组并行 |

---

## 阶段二：规划阶段（Planner）

### 目标
基于分析报告，制定精确的多模块拆分方案，包括模块清单、职责边界、依赖规则和迁移顺序。

### 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 分析报告 | 阶段一产出 | `analysis-report.md` |
| 依赖图数据 | 阶段一产出 | `dependency-graph.json` |
| 耦合热点清单 | 阶段一产出 | `coupling-hotspots.md` |
| 用户偏好 | Orchestrator 收集 | 模块命名约定、公共模块命名偏好 |

### 执行流程

```
1. 模块定义
   ├── 每个业务域 → 一个独立业务模块
   ├── 识别跨域共享代码 → common 模块候选
   ├── 识别基础设施代码 → infra/support 模块候选
   ├── 定义启动模块（含 @SpringBootApplication 的模块）
   └── 输出：目标模块清单

2. 边界定义
   ├── 每个模块：定义公开 API（对外暴露的接口/Service）
   ├── 每个模块：定义内部实现（不对外暴露的类）
   ├── 定义模块间通信契约（仅通过公开 API，禁止直接访问内部实现）
   └── 输出：模块边界文档

3. 依赖规则制定
   ├── 依赖方向：业务模块 → common 模块（单向，禁止反向）
   ├── 业务模块间：仅允许上层依赖下层（如 order → user，禁止 user → order）
   ├── 禁止跨层调用：Controller 层不可直接调用其他模块的 Repository
   ├── 启动模块：依赖所有业务模块和 common 模块
   └── 输出：依赖规则矩阵

4. common 模块抽取策略
   ├── 被 3+ 个业务模块引用的 DTO/VO → common-dto
   ├── 被 3+ 个模块使用的工具类 → common-util
   ├── 全局常量/枚举 → common-constant
   ├── 全局异常定义 → common-exception
   ├── 基础配置类/拦截器 → common-config
   └── 输出：common 模块内容清单

5. 迁移优先级排序
   ├── 依赖拓扑排序：被依赖最多的模块最后迁移
   ├── 排序规则：common 模块最先，叶子业务模块次之，聚合模块最后
   └── 输出：有序迁移序列
```

### 输出

| 输出文件 | 路径 | 内容 |
|----------|------|------|
| `split-plan.md` | `/shared/specs/plan/` | 完整拆分方案文档 |
| `module-map.json` | `/shared/specs/plan/` | 当前包→目标模块映射表 |
| `migration-sequence.md` | `/shared/specs/plan/` | 有序迁移步骤列表 |

#### `split-plan.md` 结构

```markdown
# 多模块拆分方案

## 1. 目标架构
(架构图：模块及依赖关系)

## 2. 模块清单
### common（公共模块）
- **职责**: 跨模块共享的 DTO、工具类、常量、异常
- **包路径**: com.example.common
- **内容**: DTO 15 个, Util 8 个, Constant 3 个, Exception 5 个
- **依赖**: 仅依赖第三方库，不依赖任何业务模块

### order（订单模块）
- **职责**: 订单 CRUD、订单状态流转、订单查询
- **包路径**: com.example.order
- **内容**: Controller 3, Service 5, Repository 2, Entity 4
- **依赖**: common, user（查询用户信息）
- **公开 API**: OrderService, OrderQueryService

### user（用户模块）
...

### app（启动模块）
- **职责**: Spring Boot 启动，全局配置，安全配置
- **包路径**: com.example.app
- **内容**: Application.java, 全局配置类
- **依赖**: 所有业务模块 + common

## 3. 依赖规则矩阵
|         | common | order | user | payment | app |
|---------|--------|-------|------|---------|-----|
| common  |   -    |       |      |         |     |
| order   |   Y    |   -   |  Y   |    Y    |     |
| user    |   Y    |       |  -   |         |     |
| payment |   Y    |       |      |    -    |     |
| app     |   Y    |   Y   |  Y   |    Y    |  -  |

## 4. 模块边界
(每个模块的公开 API 列表和内部实现范围)

## 5. 风险评估
- 风险 1: order 和 payment 双向引用，需拆出中间契约模块
- 风险 2: ...
```

#### `module-map.json` 结构

```json
{
  "mappings": [
    {
      "sourcePath": "src/main/java/com/example/order",
      "sourceType": "package",
      "targetModule": "order",
      "targetPath": "order/src/main/java/com/example/order",
      "fileCount": 25,
      "action": "MOVE",
      "notes": "全部 move 到 order 模块"
    },
    {
      "sourcePath": "src/main/java/com/example/common/dto/OrderDTO.java",
      "sourceType": "file",
      "targetModule": "common",
      "targetPath": "common/src/main/java/com/example/common/dto/OrderDTO.java",
      "action": "MOVE",
      "notes": "被 4 个模块引用，迁入 common"
    }
  ],
  "refactors": [
    {
      "type": "PACKAGE_RENAME",
      "oldPackage": "com.example.mess.util",
      "newPackage": "com.example.common.util",
      "files": ["DateUtils.java", "StringUtils.java"]
    }
  ]
}
```

#### `migration-sequence.md` 结构

```markdown
# 迁移执行序列

**总步骤数**: 12
**预估影响文件数**: 150+

## 前置检查
- [ ] 创建 git checkpoint: `git checkout -b refactor/split-modules`
- [ ] 确认工作区干净

## 迁移步骤

### Step 1: 创建 common 模块
- 操作: 创建目录、pom.xml、迁入 DTO/Util/Constant
- 影响文件: 31
- 依赖: 无
- 验证: mvn compile -pl common

### Step 2: 创建 user 模块
- 操作: 创建目录、pom.xml、迁移 user 包
- 影响文件: 18
- 依赖: common
- 验证: mvn compile -pl user
...
```

### 验收标准

- [ ] 每个模块有明确的单一职责，无职责重叠
- [ ] 目标架构中不存在循环依赖
- [ ] 依赖方向全部为单向（从业务模块到 common，从上层到下��）
- [ ] common 模块内容均为被 3+ 模块引用的真正共享代码
- [ ] 迁移序列按依赖拓扑排序，从底层到上层
- [ ] 所有现有代码都有明确的目标模块归属
- [ ] 单一启动模块正确依赖所有业务模块

### 异常处理

| 异常 | 处理 |
|------|------|
| 存在无法消除的循环依赖 | 提出中间契约模块或接口层解耦方案 |
| 业务边界模糊无法划分 | 请求 Orchestrator 获取用户输入 |
| common 模块过大（>50类） | 拆分为 common-dto / common-util / common-config |

---

## 阶段三：执行阶段（Executor）

### 目标
按迁移序列逐步实施模块拆分，创建子模块目录、迁移代码与资源、重构配置。

### 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 拆分方案 | 阶段二产出 | `split-plan.md` |
| 模块映射表 | 阶段二产出 | `module-map.json` |
| 迁移序列 | 阶段二产出 | `migration-sequence.md` |
| 完整分析 | 阶段一产出 | 作为上下文参考 |

### 执行流程

**对每个迁移步骤（按 sequence 顺序）执行：**

```
1. 前置检查
   ├── 确认 Git 工作区干净
   ├── 创建步骤级 Git checkpoint: git add -A && git commit -m "checkpoint: before step N"
   └── 验证目标目录不存在（避免覆盖）

2. 创建模块骨架
   ├── 创建模块目录: {module}/src/main/java, src/main/resources, src/test/java
   ├── 生成模块 pom.xml（基于模板 + 实际依赖）
   │   ├── <parent> 指向根 POM
   │   ├── <dependencies> 包含 common + 依赖的其他业务模块
   │   └── 排除 spring-boot-maven-plugin（仅 app 模块需要）
   └── 输出：模块骨架就绪

3. 代码迁移
   ├── 遍历 module-map.json 中 targetModule={module} 的所有条目
   ├── 对每个条目：
   │   ├── 复制目录/文件到目标模块
   │   ├── 更新 Java 文件的 package 声明
   │   ├── 更新所有 import 语句中的包路径
   │   └── 从原位置删除已迁移的代码
   └── 输出：代码已迁移

4. 跨模块引用更新
   ├── 扫描所有模块的 import 语句
   ├── 对跨模块引用：更新为新模块的 GAV 坐标
   │   ├── import com.example.foo → 确保 order/pom.xml 包含 foo 依赖
   │   └── Spring @Autowired / 构造注入 → 验证目标 Bean 在新模块中
   └── 输出：依赖关系更新

5. 构建配置更新
   ├── 更新根 POM：
   │   ├── <packaging>pom</packaging>
   │   ├── <modules> 添加新模块
   │   └── <dependencyManagement> 统一版本
   ├── 更新 app 模块 POM：添加对所有业务模块的依赖
   └── 输出：构建配置更新

6. Spring 组件扫描调整
   ├── 检查 @SpringBootApplication 的 scanBasePackages
   ├── 确保能扫到所有模块的 @Component/@Service
   ├── 推荐使用 scanBasePackages = "com.example"（包前缀）
   └── 输出：Spring 扫描配置验证

7. 步骤验证
   ├── 执行 mvn compile -pl {module} 验证子模块编译
   ├── 如失败 → git reset --hard 回到 checkpoint → 标记失败
   └── 如成功 → git add -A && git commit -m "step N: {module} migrated"
```

### 输出

| 输出文件 | 路径 | 内容 |
|----------|------|------|
| 重构后工程 | 工程根路径 | 多模块目录结构，所有 POM 已更新 |
| `migration-log.md` | `/shared/artifacts/` | 每个步骤的执行日志（成功/失败/耗时） |

#### `migration-log.md` 结构

```markdown
# 迁移执行日志

## Step 1: common 模块 — SUCCESS
- 耗时: 1.2s
- 迁移文件: 31 个
- 新建文件: common/pom.xml, common/src/...
- Git commit: a1b2c3d

## Step 2: user 模块 — SUCCESS
...

## Step 5: order 模块 — FAILED
- 耗时: 3.1s
- 失败原因: OrderController 引用了未迁移的 PaymentUtils
- 操作: git reset --hard → 已回退
- 建议: 规划阶段补充 PaymentUtils 迁移步骤
```

### 验收标准

- [ ] 所有代码已按 module-map.json 迁移到目标模块
- [ ] 根 POM 的 `<packaging>` 已改为 `pom`
- [ ] 根 POM 的 `<modules>` 包含所有子模块
- [ ] 每个子模块 pom.xml 正确声明了所需依赖
- [ ] Spring Boot 主启动类所在模块依赖了所有业务模块
- [ ] 无编译错误（每个步骤局部验证通过）
- [ ] 每个步骤有 Git commit，可追溯

### 操作规则

- **绝不修改业务逻辑**：只移动文件、更新 import/package，不改方法实现
- **绝不断开 Git 历史**：使用 Git 支持的操作（`git mv` 或等效），避免文件历史丢失
- **每步原子性**：一个模块的迁移在一个步骤内完成，要么全成功，要么全回退
- **渐进提交**：每完成一个步骤就 commit，便于 git bisect 定位问题

### 异常处理

| 异常 | 处理 |
|------|------|
| 文件复制冲突 | 先确认目标路径内无同名文件，否则标记冲突 |
| 编译失败 | `git reset --hard` 回退当前步骤，输出失败信息 |
| import 更新遗漏 | 编译阶段会发现，按编译错误逐文件修复 |
| `git mv` 失败 | 检查文件是否已在之前的步骤中迁移 |

---

## 阶段四：检查阶段（Inspector）

### 目标
验证拆分后的模块架构质量：边界清晰性、依赖合理性、无循环依赖、无遗漏迁移。

### 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 重构后工程 | 阶段三产出 | 多模块项目 |
| 拆分方案 | 阶段二产出 | `split-plan.md`（对比目标架构） |
| 模块映射表 | 阶段二产出 | `module-map.json`（验证完整性） |

### 执行流程

```
1. 模块边界检查
   ├── 验证��个模块包含的类是否符合计划
   ├── 检查是否有业务逻辑泄漏到 common 模块
   ├── 检查 common 中是否有仅被 1 个模块引用的代码（不应在 common 中）
   └── 输出：边界违规列表

2. 依赖方向检查
   ├── 解析所有模块的 pom.xml → 提取模块间依赖关系
   ├── 构建模块级依赖图
   ├── 验证：全部符合计划中的依赖规则矩阵
   ├── 验证：common 不依赖任何业务模块
   ├── 验证：业务模块间无违反方向的依赖
   └── 输出：依赖违规列表

3. 循环依赖检测
   ├── 对模块级依赖图执行 DFS 环路检测
   ├── 同时检查包级别的 import 循环（Java 层）
   ├── 同时运行 mvn dependency:analyze 检查未使用的依赖
   └── 输出：循环依赖列表

4. 遗漏检查
   ├── 对比 module-map.json 和实际文件系统
   ├── 检查原路径是否有残留代码未迁移
   ├── 检查是否有代码未映射到任何目标模块
   └── 输出：遗漏列表

5. 包命名一致性检查
   ├── 验证包名与模块名一致
   ├── 检查是否有跨模块的同名包
   └── 输出：命名问题列表
```

### 输出

| 输出文件 | 路径 | 内容 |
|----------|------|------|
| `inspection-report.md` | `/shared/specs/inspection/` | 检查结果总结 + 每项检查的详细发现 |
| `violation-list.json` | `/shared/specs/inspection/` | 结构化违规列表，含严重等级和修复建议 |

#### `violation-list.json` 结构

```json
{
  "violations": [
    {
      "id": "V001",
      "type": "CIRCULAR_DEPENDENCY",
      "severity": "CRITICAL",
      "description": "order 模块和 payment 模块存在循环依赖",
      "detail": "order/pom.xml -> payment; payment/pom.xml -> order",
      "suggestion": "提取共享接口到 common 或新建 contract 模块",
      "modules": ["order", "payment"]
    },
    {
      "id": "V002",
      "type": "BOUNDARY_LEAK",
      "severity": "WARNING",
      "description": "common 模块中包含仅被 order 引用的 OrderValidator",
      "detail": "common/src/.../OrderValidator.java 仅被 order 模块 import",
      "suggestion": "移回 order 模块",
      "modules": ["common", "order"]
    },
    {
      "id": "V003",
      "type": "ORPHAN_CODE",
      "severity": "INFO",
      "description": "原路径下存在未迁移的 BackUpService.java",
      "detail": "src/main/java/.../BackUpService.java 未被 module-map.json 覆盖",
      "suggestion": "确认是否需要迁移或删除",
      "files": ["src/main/java/com/example/legacy/BackUpService.java"]
    }
  ],
  "summary": {
    "totalViolations": 3,
    "critical": 1,
    "warning": 1,
    "info": 1
  }
}
```

### 验收标准

- [ ] CRITICAL 级别违规数为 0
- [ ] WARNING 级别违规数 ≤ 2（且都有合理解释）
- [ ] 无模块级循环依赖
- [ ] common 模块中仅包含被 2+ 模块引用的共享代码
- [ ] 原路径无遗漏的业务代码
- [ ] 依赖方向符合 `split-plan.md` 中的依赖规则矩阵

### 异常处理

| 异常 | 处理 |
|------|------|
| 发现 CRITICAL 违规 | 输出 violation list，返回执行阶段修复 |
| `mvn dependency:analyze` 失败 | 回退到纯 pom.xml 解析方式 |
| 无法确定代码归属 | 标记为 WARNING，请求 Orchestrator 决策 |

---

## 阶段五：验证阶段（Verifier）

### 目标
验证拆分后的工程功能完整性和构建正确性：编译、测试、打包、启动全链路验证。

### 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 重构后工程 | 阶段三产出（经过阶段四检查通过） | 多模块项目 |
| 检查报告 | 阶段四产出 | `inspection-report.md`（确认无 CRITICAL 违规） |

### 执行流程

```
1. 全量编译验证
   ├── mvn clean compile（根目录执行）
   ├── 验证所有模块均编译成功
   ├── 检查编译警告（未使用的 import 等）
   └── 输出：编译报告

2. 测试执行
   ├── mvn test（运行所有模块的测试）
   ├── 统计测试通过率
   ├── 对比拆分前的测试通过率（如有 baseline）
   └── 输出：测试报告

3. 打包验证
   ├── mvn package -DskipTests（生成最终 artifact）
   ├── 检查生成的 jar/war 文件
   ├── 验证 jar 中包含所有模块的 class
   └── 输出：打包报告

4. Spring Boot 启动验证
   ├── 启动应用：java -jar app/target/*.jar 或 mvn spring-boot:run
   ├── 检查启动日志：无 Bean 创建失败、无配置错误
   ├── 检查所有模块的 Bean 是否成功注册
   └── 输出：启动日志摘要

5. 接口契约验证（可选）
   ├── 如果项目有 API 测试/集成测试 → 执行
   ├── 如果有 Swagger/OpenAPI 文档 → 检���端点完整性
   ├── 对比拆分前后 API 端点列表
   └── 输出：API 对比报告

6. 最终对比
   ├── 对比拆分前后的：
   │   ├── 编译时间
   │   ├── jar 包大小
   │   ├── 模块数量
   │   └── 依赖关系复杂度
   └── 输出：对比报告
```

### 输出

| 输出文件 | 路径 | 内容 |
|----------|------|------|
| `verification-report.md` | `/shared/specs/verification/` | 编译/测试/打包/启动结果汇总 |
| `comparison-report.md` | `/shared/specs/verification/` | 拆分前后对比数据 |

#### `verification-report.md` 结构

```markdown
# 验证报告

## 1. 编译结果
- 状态: PASSED / FAILED
- 耗时: 12.3s
- 模块编译结果:
  | 模块 | 状态 | 耗时 |
  |------|------|------|
  | common | PASSED | 1.2s |
  | order  | PASSED | 3.1s |
  ...

## 2. 测试结果
- 状态: PASSED (45/45) / PARTIAL (42/45)
- 失败测试: (如有)

## 3. 打包结果
- artifact: app/target/project-1.0.0.jar
- 大小: 45.2 MB
- 包含模块: 5

## 4. 启动验证
- 状态: SUCCESS / FAILED
- 启动耗时: 4.2s
- Bean 注册数: 156
- 错误/警告: (如有)

## 5. 最终结论
- 总体状态: PASSED / FAILED
- 待处理问题: ...
```

### 验收标准

- [ ] 所有模块编译成功，零编译错误
- [ ] 所有测试通过（或与拆分前一致，无新增失败）
- [ ] 最终 artifact 成功构建，包含所有业务模块
- [ ] Spring Boot 应用启动成功，无 Bean 创建失败
- [ ] 无新增的启动警告或错误日志
- [ ] （可选）API 端点与拆分前一致

### 异常处理

| 异常 | 处理 |
|------|------|
| 编译器找不到跨模块类 | 检查模块 pom.xml 的依赖声明，补充缺失依赖 |
| 测试失败 | 检查测试类是否被正确迁移，Spring 测试上下文是否完整 |
| Bean 注入失败 | 检查 @ComponentScan 范围，确认跨模块 Bean 可见 |
| 启动失败 | 查看完整启动日志，定位缺失的配置或 Bean |

---

## 附录：阶段间数据流

```
输入 → [分析] → analysis-report.md, dependency-graph.json, coupling-hotspots.md
                    │
                    ▼
              [规划] → split-plan.md, module-map.json, migration-sequence.md
                    │
                    ▼
              [执行] → 重构后工程, migration-log.md
                    │
                    ▼
              [检查] → inspection-report.md, violation-list.json
                    │
                    ▼
              [验证] → verification-report.md, comparison-report.md
                    │
                    ▼
                  完成
```

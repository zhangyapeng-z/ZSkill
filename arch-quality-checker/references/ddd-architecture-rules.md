# DDD 分层架构规范与检查规则

本文档定义微服务多模块工程的 DDD 分层规范，以及对应的自动化检查规则。

---

## 一、DDD 分层模型

### 1.1 标准四层架构

每个业务模块应遵循 DDD 分层架构，自上而下分为四层：

```
┌─────────────────────────────────────────────────────┐
│  Interface / Controller 层 (接口层)                  │
│  职责：接收请求、参数校验、调用应用服务、返回响应      │
│  包名模式：*.controller / *.api / *.interfaces       │
├─────────────────────────────────────────────────────┤
│  Application Service 层 (应用服务层)                 │
│  职责：业务编排、事务管理、领域服务调度、DTO 转换      │
│  包名模式：*.service / *.application / *.app         │
├─────────────────────────────────────────────────────┤
│  Domain 层 (领域层)                                  │
│  职责：领域模型、领域服务、领域事件、业务规则          │
│  包名模式：*.domain / *.model / *.entity             │
│        *.domain.service / *.domain.event             │
├─────────────────────────────────────────────────────┤
│  Infrastructure / Repository 层 (基础设施层)          │
│  职责：数据持久化、外部服务调用、消息队列、缓存         │
│  包名模式：*.repository / *.mapper / *.infra         │
│        *.infrastructure / *.dao                      │
└─────────────────────────────────────────────────────┘
```

### 1.2 Spring Boot + MyBatis 分层映射

在 Spring Boot + MyBatis 技术栈中，各层对应的组件类型：

| DDD 层 | 组件类型 | Spring 注解 | MyBatis 组件 |
|--------|----------|-------------|-------------|
| Controller 层 | Controller | `@RestController` / `@Controller` | - |
| Application Service 层 | Service 接口 + ServiceImpl | `@Service` | - |
| Domain 层 | Entity / VO / Domain Service | `@Component`（领域服务） | - |
| Infrastructure 层 | Repository / Mapper | `@Repository` / `@Mapper` | Mapper XML |

### 1.3 公共模块定义

工程中通常包含以下非业务模块：

| 模块类型 | 命名模式 | 职责 |
|----------|----------|------|
| Common 模块 | `*-common` / `*-core` | 通用工具类、常量、枚举、基础 DTO、异常定义 |
| API 模块 | `*-api` / `*-facade` | 对外暴露的 Service 接口和 DTO |
| App/Bootstrap 模块 | `*-app` / `*-bootstrap` / `*-starter` | 启动类、主配置、集成测试 |
| BOM 模块 | `*-bom` / `*-dependencies` | 依赖版本管理 |

---

## 二、架构检查规则详解

### A-01: DDD 分层完整性检查 [Blocker]

**规则描述：** 每个业务模块必须包含完整的四层结构（或至少包含 Controller/Service/Repository 三层），缺少关键层即为架构缺陷。

**检查逻辑：**
1. 遍历每个业务模块的 `src/main/java/` 目录
2. 按包名模式匹配各层：
   - Controller 层：包含 `@RestController` 或 `@Controller` 注解的类
   - Service 层：包含 `@Service` 注解的类
   - Domain 层：包含实体类（`@Table`、`@Entity` 或继承 BaseEntity 的类）
   - Repository 层：包含 `@Mapper` 或 `@Repository` 注解的接口
3. 缺少任一层则报 Blocker

**通过条件：** 每个业务模块至少包含 Service 层和 Repository 层。Controller 层和 Domain 层可根据模块性质（如纯领域模块可能无 Controller）豁免。

**报告示例：**
```
[Blocker] A-01: 模块 pcm-parts-cost 缺少 Domain 层
  文件: pcm-parts-cost/src/main/java/com/hpis/pcm/parts/
  说明: 未找到实体类或领域模型，该模块可能未遵循 DDD 分层规范
  建议: 检查该模块是否有独立的领域模型，或确认该模块为纯应用服务模块
```

### A-02: 分层依赖方向检查 [Blocker]

**规则描述：** 分层依赖必须自上而下单向流动，禁止反向依赖。

**合法依赖方向：**
```
Controller → Application Service → Domain Service → Repository
Controller → Application Service → Repository (简单CRUD可跳过Domain)
Application Service → Domain Model (实体/值对象)
```

**非法依赖方向：**
```
Repository → Service (反向)
Repository → Controller (跨层反向)
Domain → Controller (跨层反向)
Service → Controller (反向)
Mapper → Service (反向)
```

**检查逻辑：**
1. 对每个 Java 源文件，识别其所属层（通过包名和注解）
2. 解析 import 语句，识别被引用类所属的层
3. 如果存在反向依赖或跨层依赖，则报 Blocker

**通过条件：** 所有跨层引用均符合自上而下的依赖方向。

### A-03: 循环依赖检测 [Blocker]

**规则描述：** 模块间不允许存在循环依赖链。即如果模块 A 依赖模块 B，则模块 B 不能（直接或间接）依赖模块 A。

**检查逻辑：**
1. 解析所有模块的 POM 文件，提取 `<dependency>` 中属于同工程的模块依赖
2. 构建有向依赖图：节点=模块，边=依赖关系
3. 使用 DFS（深度优先搜索）检测环：
   - 维护访问状态：white(未访问) / gray(正在访问) / black(已完成)
   - 遇到 gray 节点即发现环
4. 输出环上的模块链

**通过条件：** 依赖图中不存在环。

**报告示例：**
```
[Blocker] A-03: 检测到循环依赖
  依赖链: pcm-common → pcm-product-cost → pcm-common
  说明: pcm-common 依赖 pcm-product-cost，同时 pcm-product-cost 依赖 pcm-common，形成循环
  建议: 将 pcm-product-cost 中被 pcm-common 引用的类下沉到 common，或提取为独立模块
```

### A-04: 跨层调用检测 [Critical]

**规则描述：** 禁止 Controller 层直接调用 Repository/Mapper 层，必须通过 Service 层中转。

**检查逻辑：**
1. 遍历 Controller 类（`@RestController` / `@Controller`）
2. 检查 `@Autowired` / `@Resource` / 构造器注入的字段类型
3. 如果注入了 `Mapper` 接口或 `Repository` 接口，则报 Critical

**例外：** 简单的查询类 Controller 在特殊情况下可直接调用 Repository，但需要在代码中添加注释说明原因。

### A-05: 公共模块纯净性检查 [Critical]

**规则描述：** Common 模块（`*-common` / `*-core`）不允许依赖任何业务模块，且不应包含业务逻辑。

**检查逻辑：**
1. 检查 common 模块的 POM 文件中是否有对其他业务模块的 `<dependency>`
2. 检查 common 模块中是否有 `@Service`、`@RestController`、`@Mapper` 注解的类
3. 检查 common 模块中是否有业务实体类（`@Table`、`@Entity`）

**通过条件：** Common 模块仅包含工具类、常量、枚举、通用 DTO、异常定义等无业务语义的代码。

### A-06: 领域模型独立性检查 [Critical]

**规则描述：** Domain 层（实体、值对象、领域服务）不应依赖 Infrastructure 层（Repository/Mapper）的具体实现。

**检查逻辑：**
1. 遍历 Domain 层的类（entity、domain.service 包下的类）
2. 检查 import 语句是否引用了 `*.mapper.*` 或 `*.repository.*` 包下的类
3. 如果引用，则报 Critical

**通过条件：** Domain 层仅依赖自身和 JDK/Spring 核心库。

### A-07: Service 接口隔离检查 [Major]

**规则描述：** 模块间通过 Service 接口交互，禁止直接注入 Service 实现类（`*ServiceImpl`）。

**检查逻辑：**
1. 遍历所有 `@Autowired` / `@Resource` 注入点
2. 检查注入类型是否为 `*ServiceImpl`（以 Impl 结尾的具体类）
3. 如果注入的是实现类而非接口，则报 Major

**通过条件：** 所有跨模块的 Service 注入均使用接口类型。

### A-08: Mapper 层隔离检查 [Major]

**规则描述：** Mapper 接口仅在 Repository/DAO 层使用，不应暴露到 Service 层或 Controller 层。

**检查逻辑：**
1. 遍历 Service 层和 Controller 层的类
2. 检查是否直接 `@Autowired` 注入了 `@Mapper` 注解的接口
3. 如果发现，则报 Major

**例外：** 如果项目未采用 Repository 模式，Service 直接使用 Mapper 是可接受的，但建议增加 Repository 层封装。

### A-09: DTO 跨模块传递检查 [Major]

**规则描述：** 跨模块传递数据时必须使用 DTO，禁止直接传递领域实体（Entity）。

**检查逻辑：**
1. 检查模块间 Service 接口的方法签名
2. 如果方法参数或返回值类型属于其他模块的 entity 包，则报 Major

**通过条件：** 跨模块 Service 接口的方法参数和返回值均为 DTO 或基本类型。

### A-10: 启动模块单一性检查 [Critical]

**规则描述：** 整个工程仅允许一个模块包含 `@SpringBootApplication` 注解的启动类，通常位于 `*-app` 或 `*-bootstrap` 模块。

**检查逻辑：**
1. 遍历所有 Java 源文件，搜索 `@SpringBootApplication` 注解
2. 如果在多个模块中发现该注解，则报 Critical

---

## 三、模块依赖关系规范

### 3.1 合法依赖模式

```
                    pcm-common (无依赖)
                        ↑
                   pcm-master-data
                     ↑        ↑
               pcm-bom    pcm-cad-bom
                     ↑
              pcm-product-cost
                 ↑        ↑
          pcm-parts-cost  pcm-sales-cost
                     ↑
                 pcm-app (依赖所有模块)
```

### 3.2 依赖方向规则

| 源模块 | 可依赖的目标模块 | 禁止依赖的模块 |
|--------|-----------------|---------------|
| pcm-common | 无（不依赖任何业务模块） | 所有业务模块 |
| pcm-bom | pcm-common, pcm-master-data | pcm-product-cost, pcm-app |
| pcm-product-cost | pcm-common, pcm-master-data, pcm-bom | pcm-app, pcm-parts-cost |
| pcm-app | 所有模块 | 无 |

### 3.3 MyBatis 专项检查

| 检查项 | 规则 | 严重级别 |
|--------|------|----------|
| Mapper XML 文件位置 | 必须在 `src/main/resources/mapper/` 目录下 | Major |
| Mapper XML namespace | 必须与对应 Mapper 接口全限定名一致 | Blocker |
| Mapper 接口方法名 | 必须与 XML 中的 statement id 一致 | Critical |
| Mapper XML 引用 resultType | resultType 必须为已存在的类 | Critical |
| MyBatis 配置扫描路径 | `@MapperScan` 必须覆盖所有模块的 mapper 包 | Major |

---

## 四、检查流程伪代码

```
function checkArchitecture(projectRoot):
    # 1. 扫描模块结构
    modules = parsePomModules(projectRoot)
    
    # 2. 构建依赖图
    depGraph = buildDependencyGraph(modules)
    
    # 3. 检查循环依赖
    cycles = detectCycles(depGraph)
    for cycle in cycles:
        report(A-03, Blocker, cycle)
    
    # 4. 检查各模块 DDD 分层
    for module in modules:
        layers = detectLayers(module)
        checkLayerCompleteness(A-01, module, layers)
        checkDependencyDirection(A-02, module, layers)
        checkCrossLayerCall(A-04, module, layers)
    
    # 5. 检查公共模块纯净性
    checkCommonModulePurity(A-05, commonModule)
    
    # 6. 检查领域模型独立性
    checkDomainIndependence(A-06, allModules)
    
    # 7. 检查 Service 接口隔离
    checkServiceInterfaceIsolation(A-07, allModules)
    
    # 8. 检查 Mapper 层隔离
    checkMapperIsolation(A-08, allModules)
    
    # 9. 检查 DTO 跨模块传递
    checkDtoTransfer(A-09, allModules)
    
    # 10. 检查启动模块单一性
    checkBootstrapSingularity(A-10, allModules)
    
    return issues
```

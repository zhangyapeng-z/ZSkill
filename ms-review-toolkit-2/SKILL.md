---
name: ms-review-toolkit
description: "专业的微服务后端架构审查与代码审查工具。自动扫描微服务架构设计缺陷（服务拆分合理性、服务间通信效率、数据一致性、容错熔断机制、API网关配置）与代码质量问题（安全漏洞、性能瓶颈、依赖管理、重复代码、代码规范）。支持 Spring Cloud、Dubbo 等主流微服务技术栈，严格判定规则避免误报。针对每个问题给出具体解决方案与最佳实践，输出结构化修改计划（问题优先级、修改步骤、影响范围、风险评估）与 JSON 结构化审查报告。适用于微服务工程的上线前架构审查、技术债评估与代码巡检。"
---

# MS Review Toolkit — 微服务架构审查与代码审查工具

专业的微服务后端架构审查与代码审查工具，自动扫描架构设计缺陷与代码质量问题，输出结构化修改计划与 JSON 结构化报告。

## 适用场景

- 微服务后端工程（单服务为 Spring Boot 应用，多服务组成微服务集群）
- 技术栈：Spring Cloud（Gateway / Feign / Hystrix / Sentinel / Nacos / Eureka）、Apache Dubbo、Spring Boot + MyBatis/JPA
- 适用时机：上线前架构审查、技术债评估、代码巡检、重构前体检、新成员接手工程评估

## 技术栈识别

工具自动识别目标工程的技术栈，并据此加载对应的检查规则，避免对非微服务工程误报。

| 技术栈 | 识别特征 | 关联检查 |
|--------|----------|----------|
| Spring Cloud Gateway | `spring-cloud-starter-gateway`、`@EnableDiscoveryClient` | 网关配置、路由、限流 |
| Spring Cloud OpenFeign | `spring-cloud-starter-openfeign`、`@FeignClient` | 间通信、超时、降级 |
| Hystrix | `spring-cloud-starter-netflix-hystrix`、`@EnableCircuitBreaker`、`@HystrixCommand` | 熔断、降级、隔离 |
| Sentinel | `spring-cloud-starter-alibaba-sentinel`、`@SentinelResource` | 流控、熔断 |
| Nacos | `spring-cloud-starter-alibaba-nacos-discovery` | 注册发现、配置中心 |
| Eureka | `spring-cloud-starter-netflix-eureka-server/client` | 注册发现 |
| Apache Dubbo | `dubbo-spring-boot-starter`、`@DubboService/@DubboReference/@Service/@Reference` | RPC 通信、注册中心 |
| Spring Boot | `spring-boot-starter`、`@SpringBootApplication` | 基础设施识别 |

**识别脚本：** `scripts/detect_tech_stack.py`

## 执行流程

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. 技术栈识别  │──>│ 2. 工程扫描   │──>│ 3. 架构审查   │──>│ 4. 代码审查   │──>│ 5. 报告生成   │
│ Tech Stack    │   │ Project Scan │   │ Arch Review  │   │ Code Review  │   │ Report Gen   │
└───────┬───────┘   └───────┬──────┘   └───────┬──────┘   └───────┬──────┘   └───────┬──────┘
        │                   │                  │                  │                  │
        v                   v                  v                  v                  v
   tech-stack.json     module-tree.json    arch-issues.json   code-issues.json   report.md
                       dep-graph.json      modification-plan   rule-summary.json  report.html
                                                                                    review-report.json
```

### 阶段 1：技术栈识别与工程扫描

**执行步骤：**

1. 确认目标工程根路径（微服务工程通常为多模块 Maven/Gradle，每个服务一个可启动模块）
2. 运行技术栈识别：
   ```bash
   python scripts/detect_tech_stack.py <project-root> --output <output-dir>
   ```
   产出 `tech-stack.json`，含每个服务的技术栈标签
3. 运行工程扫描（复用 scan_architecture 的工程结构收集能力，扩展为多服务）：
   ```bash
   python scripts/scan_microservice_arch.py <project-root> --scan --output <output-dir>
   ```
   产出：
   - `service-inventory.json` — 服务清单（服务名、端口、启动类、技术栈、对外接口数）
   - `service-call-graph.json` — 服务间调用关系图（Feign/Dubbo/RestTemplate 调用链）
   - `module-tree.json` — 模块树结构
   - `java-file-index.json` — Java 源文件索引

**关键判断：**
- 识别服务边界：每个含 `@SpringBootApplication` 的模块为一个独立服务
- 识别服务间调用：Feign（`@FeignClient`）、Dubbo（`@DubboReference`）、RestTemplate、`WebClient`
- 识别数据源归属：解析 `application.yml`/`application.properties` 的 `spring.datasource`，判断是否多服务共享同一库

### 阶段 2：微服务架构审查

验证微服务架构设计合理性，**严格判定避免误报**：每条规则都有正向命中条件与排除条件。

**加载规则：** 阅读 `references/microservice-arch-rules.md` 获取完整规则定义、判定条件与误报排除逻辑。

**检查项清单（架构维度）：**

| 序号 | 检查项 | 严重级别 | 核心判定逻辑 |
|------|--------|----------|--------------|
| M-01 | 服务拆分合理性 | Critical | 单服务类数/行数过大或过小；服务内多业务上下文混杂（领域边界不清） |
| M-02 | 服务间通信效率 | Major | 同步链路过长（调用链 ≥3 跳）；高频循环调用；未用异步消息可解耦的强同步依赖 |
| M-03 | 数据一致性（共享库） | Blocker | 多服务直连同一业务库（破坏服务自治）；跨服务直接联表查询 |
| M-04 | 分布式事务缺失 | Critical | 跨服务写操作无 TCC/Saga/消息最终一致性方案；`@Transactional` 跨服务无效 |
| M-05 | 容错熔断缺失 | Critical | Feign/Dubbo 调用未配置 fallback/熔断；无超时控制；无重试上限 |
| M-06 | API 网关配置 | Major | 网关未配置限流/鉴权；路由裸暴露内部服务；未配置跨域/CORS |
| M-07 | 服务注册发现 | Major | 硬编码 IP/端口调用；未通过注册中心发现；多环境配置混乱 |
| M-08 | 配置管理 | Major | 密钥/连接串硬编码在源码；未使用配置中心；多环境配置不一致 |
| M-09 | 接口幂等性 | Critical | 写接口未做幂等设计（重复提交/重试导致脏数据） |
| M-10 | API 版本管理 | Minor | 对外 API 无版本号；破坏性变更无版本隔离 |

**执行方式：**

```bash
python scripts/scan_microservice_arch.py <project-root> --check --output <output-dir>
```

脚本产出 `arch-issues.json`。对于需语义判断的项（如领域边界是否清晰），脚本给出可疑线索后，结合 `references/microservice-arch-rules.md` 的人工审查清单逐项确认，**确认命中后才计入问题**，避免误报。

### 阶段 3：代码质量审查

在单服务内部检查代码规范、安全、性能、依赖、重复代码。

**加载规则：** 阅读 `references/code-quality-rules.md` 获取完整规则定义。

**检查项清单（代码质量维度）：**

| 序号 | 检查类别 | 严重级别 | 核心检查项 |
|------|----------|----------|-----------|
| Q-01 | 代码规范 | Major | 命名规范、注释规范、异常处理、日志规范（阿里巴巴 Java 手册核心条款） |
| Q-02 | 安全漏洞 | Blocker | SQL 注入（拼接 SQL）、硬编码密钥、不安全的反序列化、XSS、SSRF、越权风险 |
| Q-03 | 性能瓶颈 | Critical | N+1 查询、循环内 DB 调用、大结果集未分页、同步阻塞调用可异步化、锁粒度过大 |
| Q-04 | 依赖管理 | Major | 依赖版本冲突、使用有漏洞的依赖版本（已知 CVE）、scope 滥用、SNAPSHOT 进入生产 |
| Q-05 | 重复代码 | Major | 重复块（≥6 行且相似度 ≥80%）、复制粘贴的 DAO/转换逻辑、跨服务重复工具类 |
| Q-06 | 并发处理 | Critical | new Thread、线程池未管控、共享可变状态无同步、SimpleDateFormat 复用 |
| Q-07 | 资源管理 | Critical | 未关闭的连接/流、连接池配置不合理、try-with-resources 未用 |

**执行方式：**

```bash
python scripts/scan_code_quality.py <project-root> --output <output-dir>
```

脚本产出 `code-issues.json` 与 `rule-summary.json`。

### 阶段 4：报告生成（结构化修改计划 + JSON 报告）

汇总架构与代码审查结果，生成**结构化修改计划**与多格式报告。

**执行步骤：**

```bash
python scripts/generate_review_report.py \
  --arch <output-dir>/arch-issues.json \
  --code <output-dir>/code-issues.json \
  --tech <output-dir>/tech-stack.json \
  --output <output-dir>
```

**产出文件：**

| 文件 | 用途 |
|------|------|
| `review-report.json` | 结构化审查报告（机器可读，含修改计划） |
| `report.md` | Markdown 报告（便于版本控制与 CI 集成） |
| `report.html` | 可视化 HTML 报告（含统计图表、问题列表、修改计划） |
| `modification-plan.json` | 独立的结构化修改计划（优先级/步骤/影响范围/风险） |

**报告结构：**

```
1. 审查概览
   - 工程信息（服务数、模块数、文件数、代码行数、技术栈）
   - 审查范围与时间
   - 问题统计（按严重级别、按维度分类计数）
2. 架构审查结果
   2.1 服务拆分合理性
   2.2 服务间通信分析（含调用关系图）
   2.3 数据一致性与分布式事务
   2.4 容错熔断机制
   2.5 API 网关与注册发现
3. 代码质量审查结果
   3.1 代码规范
   3.2 安全漏洞
   3.3 性能瓶颈
   3.4 依赖管理
   3.5 重复代码
4. 问题详情列表
   - 每个问题：编号 | 严重级别 | 维度 | 服务/模块 | 文件:行号 | 描述 | 规则引用 | 解决方案
5. 结构化修改计划
   - P0 (Blocker)：立即修复，阻塞上线
   - P1 (Critical)：本迭代修复
   - P2 (Major)：下迭代修复
   - P3 (Minor)：择机修复
   - 每项含：修改步骤、影响范围、风险评估、验证方式
6. 修复进度跟踪表
```

## 问题严重级别定义

| 级别 | 含义 | 处理要求 | 示例 |
|------|------|----------|------|
| **Blocker** | 阻塞性问题，存在架构崩塌或安全风险 | 立即修复，阻塞上线 | 共享业务库、SQL 注入、硬编码密钥 |
| **Critical** | 严重问题，存在运行时风险 | 本迭代内修复 | 无熔断、分布式事务缺失、N+1 查询、并发不安全 |
| **Major** | 重要问题，影响可维护性 | 下迭代修复 | 调用链过长、依赖版本冲突、重复代码、命名不规范 |
| **Minor** | 次要问题，建议改进 | 择机修复 | 注释缺失、API 无版本号、可选优化 |

## 严格判定原则（避免误报）

工具遵循"命中条件 + 排除条件"双重判定，降低误报：

1. **每条规则定义正向命中条件**（如 M-05 熔断缺失：存在 `@FeignClient` 调用且未配置 `fallback`/`fallbackFactory`）
2. **定义排除条件**（如服务为纯只读查询服务、内部管理后台、调用方在熔断器外层已统一兜底）
3. **置信度标注**：脚本对每个疑似问题给出置信度（high/medium/low），仅 high 自动计入，medium/low 标记为"待确认"交人工复核
4. **技术栈感知**：非微服务工程（单服务无注册发现）不触发微服务架构规则，避免误报

## 使用示例

### 示例 1：完整微服务审查

用户请求："审查 D:\projects\order-platform 微服务工程的架构和代码质量"

执行步骤：
1. `python scripts/detect_tech_stack.py D:\projects\order-platform --output ./review-output`
2. `python scripts/scan_microservice_arch.py D:\projects\order-platform --scan --output ./review-output`
3. `python scripts/scan_microservice_arch.py D:\projects\order-platform --check --output ./review-output`
4. `python scripts/scan_code_quality.py D:\projects\order-platform --output ./review-output`
5. `python scripts/generate_review_report.py --arch ./review-output/arch-issues.json --code ./review-output/code-issues.json --tech ./review-output/tech-stack.json --output ./review-output`
6. 使用 `present_files` 展示 `report.html`

### 示例 2：仅架构审查

用户请求："检查这几个微服务之间的调用链路和熔断配置"

执行步骤：
1. 运行技术栈识别与扫描
2. 重点解读 `service-call-graph.json`、`arch-issues.json` 中 M-02/M-05 项

### 示例 3：仅安全与性能审查

用户请求："扫描代码里的安全漏洞和性能问题"

执行步骤：
1. 运行 `scan_code_quality.py`
2. 重点解读 `code-issues.json` 中 Q-02/Q-03 项

## 检测规则配置方式

规则采用"声明式配置 + 脚本执行"模式，支持自定义扩展：

- **内置规则**：`references/*.md` 中定义，脚本内置对应检测函数
- **阈值配置**：服务拆分阈值（类数上限/下限）、调用链深度、重复代码行数与相似度均可在脚本顶部常量区调整
- **技术栈扩展**：在 `detect_tech_stack.py` 的 `TECH_STACK_SIGNATURES` 字典中新增技术栈识别特征即可扩展支持新框架

## 可扩展性方案

1. **新增检查规则**：在规则参考文件中定义规则，在对应脚本中实现检测函数并注册到检查列表
2. **新增技术栈**：扩展 `TECH_STACK_SIGNATURES`，新增该技术栈的识别特征与关联检查
3. **自定义报告模板**：修改 `assets/report-template.html` 与报告生成脚本
4. **CI/CD 集成**：`review-report.json` 为机器可读格式，可直接对接流水线门禁（按严重级别设置阻断阈值）

## 脚本依赖

- Python 3.9+
- 标准库：`os`, `re`, `json`, `pathlib`, `xml.etree.ElementTree`, `collections`, `argparse`, `hashlib`, `difflib`
- 无需安装第三方包

## 参考文件

| 文件 | 用途 |
|------|------|
| [references/microservice-arch-rules.md](references/microservice-arch-rules.md) | 微服务架构检查规则（服务拆分/通信/一致性/熔断/网关） |
| [references/code-quality-rules.md](references/code-quality-rules.md) | 代码质量检查规则（安全/性能/依赖/重复代码/规范） |
| [references/springcloud-dubbo-patterns.md](references/springcloud-dubbo-patterns.md) | Spring Cloud / Dubbo 技术栈识别特征与检查映射 |
| [references/report-json-schema.md](references/report-json-schema.md) | JSON 结构化审查报告 Schema 定义 |
| [scripts/detect_tech_stack.py](scripts/detect_tech_stack.py) | 技术栈识别脚本 |
| [scripts/scan_microservice_arch.py](scripts/scan_microservice_arch.py) | 微服务架构检查脚本 |
| [scripts/scan_code_quality.py](scripts/scan_code_quality.py) | 代码质量检查脚本（安全/性能/依赖/重复代码） |
| [scripts/generate_review_report.py](scripts/generate_review_report.py) | 报告生成脚本（JSON + Markdown + HTML） |
| [assets/report-template.html](assets/report-template.html) | HTML 报告模板 |
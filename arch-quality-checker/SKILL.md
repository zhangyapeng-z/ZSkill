---
name: arch-quality-checker
description: "自动化检查微服务多模块工程的架构规范与代码质量。架构检查：验证 Maven/Gradle 多模块 DDD 分层结构，检测模块间循环依赖、跨层调用、依赖方向违规。代码检查：基于阿里巴巴Java开发手册标准，覆盖命名规范、注释规范、异常处理、日志规范、集合处理、并发处理、控制语句、OOP规范等核心检查项。输出分级报告 Blocker/Critical/Major/Minor，包含文件路径、行号、问题描述、规范条款引用及修复建议。适用于 Spring Boot + MyBatis 技术栈的 DDD 多模块微服务工程。"
triggers:
  - 架构检查 / 代码质量检查 / 代码审查
  - DDD 分层规范检查 / 模块依赖分析
  - 循环依赖检测 / 跨层调用检测
  - 阿里巴巴Java规范检查 / 代码规范扫描
  - 微服务架构审核 / 工程质量报告
  - architecture review / code quality scan
agent_created: true
---

# Arch Quality Checker — 微服务架构规范与代码质量检查

自动化检查 Spring Boot + MyBatis 多模块 DDD 微服务工程的架构规范与代码质量，输出分级问题报告与修复优先级计划。

## 适用场景

- 多模块 Maven/Gradle 工程，每个模块采用 DDD 分层架构
- 技术栈：Spring Boot + MyBatis（Mapper接口 + XML映射）
- 需要架构合规性审查和代码质量评估的场景

## 执行流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1. 工程扫描  │───>│ 2. 架构检查  │───>│ 3. 代码检查  │───>│ 4. 报告生成  │
│ Scan Project │    │ Arch Check  │    │ Code Check  │    │ Report Gen  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       |                  |                  |                  |
       v                  v                  v                  v
  project-info.json   arch-issues.json   code-issues.json   report.html
  module-tree.json    dep-graph.json     rule-summary.json   report.md
```

### 阶段 1：工程扫描

扫描目标工程的模块结构、源码文件、POM 依赖关系。

**执行步骤：**

1. 确认目标工程根路径（含 `pom.xml` 或 `build.gradle`）
2. 运行架构扫描脚本收集工程信息：
   ```bash
   python scripts/scan_architecture.py <project-root> --output <output-dir>
   ```
3. 脚本产出：
   - `project-info.json` — 工程基本信息（构建工具、模块列表、技术栈）
   - `module-tree.json` — 模块树结构（模块名、路径、子模块）
   - `dep-graph.json` — 模块间依赖关系图
   - `java-file-index.json` — Java 源文件索引（包名、类名、文件路径、行数）

**关键判断：**
- 识别构建工具：存在 `pom.xml` → Maven；存在 `build.gradle` → Gradle
- 识别模块：解析父 POM 的 `<modules>` 或 Gradle 的 `include` 语句
- 识别 DDD 分层：通过包名模式匹配（详见 `references/ddd-architecture-rules.md`）

### 阶段 2：架构检查

验证 DDD 分层规范、模块依赖关系、循环依赖、跨层调用。

**加载规则：** 阅读 `references/ddd-architecture-rules.md` 获取完整 DDD 分层规则定义。

**检查项清单：**

| 序号 | 检查项 | 严重级别 | 说明 |
|------|--------|----------|------|
| A-01 | DDD 分层完整性 | Blocker | 每个业务模块必须包含 controller/api、service、domain、repository 四层 |
| A-02 | 分层依赖方向 | Blocker | 依赖方向必须为 controller → service → domain → repository，禁止反向 |
| A-03 | 循环依赖检测 | Blocker | 模块间不允许存在循环依赖链 |
| A-04 | 跨层调用检测 | Critical | 禁止 Controller 直接调用 Repository/Mapper |
| A-05 | 公共模块纯净性 | Critical | common 模块不允许依赖业务模块，不含业务逻辑 |
| A-06 | 领域模型独立性 | Critical | domain 层不依赖 infrastructure 层的具体实现 |
| A-07 | Service 接口隔离 | Major | 模块间通过 Service 接口交互，禁止直接注入 Impl 类 |
| A-08 | Mapper 层隔离 | Major | Mapper 接口仅在 repository 层使用，不暴露到 service/controller |
| A-09 | DTO 跨模块传递 | Major | 跨模块传递必须使用 DTO，禁止直接传递领域实体 |
| A-10 | 启动模块单一性 | Critical | 仅 app 模块包含 `@SpringBootApplication`，其他模块禁止独立启动 |

**执行方式：**

1. 基于阶段 1 产出的 `dep-graph.json` 和 `java-file-index.json`
2. 运行架构检查脚本：
   ```bash
   python scripts/scan_architecture.py <project-root> --check --output <output-dir>
   ```
3. 脚本执行后结合人工审查：对于脚本无法判定的语义级问题（如 DTO 是否包含领域行为），参考 `references/ddd-architecture-rules.md` 中的规则定义进行逐项核查

### 阶段 3：代码质量检查

基于《阿里巴巴Java开发手册》标准检查代码规范。

**加载规则：** 阅读 `references/alibaba-java-rules.md` 获取完整规则定义。

**检查项清单：**

| 序号 | 检查类别 | 严重级别 | 核心检查项 |
|------|----------|----------|-----------|
| C-01 | 命名规范 | Major | 类名 UpperCamelCase；方法/变量 lowerCamelCase；常量全大写下划线；包名全小写；抽象类以 Abstract/Base 开头；异常类以 Exception 结尾；测试类以 Test 结尾 |
| C-02 | 注释规范 | Minor | 类/公有方法/公有字段必须有 Javadoc；注释使用中文；废弃方法标注 @Deprecated；TODO/FIXME 需标注负责人和时间 |
| C-03 | 异常处理 | Critical | 禁止捕获 Exception/Throwable 后不做处理；catch 块不能为空；禁止用 return/continue/break 退出 finally；方法返回值可以为 null 时必须用 @Nullable 标注 |
| C-04 | 日志规范 | Major |使用 SLF4J 门面；日志使用占位符 `{}` 而非字符串拼接；ERROR 日志必须记录异常堆栈；禁止在循环中打印日志；DEBUG 日志需判断级别 |
| C-05 | 集合处理 | Critical | 禁止在 foreach 中增删集合元素；使用 isEmpty() 而非 size()==0；集合转 Map 注意 key 冲突；使用 Collections.unmodifiableXxx 返回只读集合；多线程使用 ConcurrentHashMap |
| C-06 | 并发处理 | Critical | 禁止使用 new Thread() 创建线程；线程池必须通过 ThreadPoolExecutor 创建；SimpleDateFormat 线程不安全；对共享变量使用 volatile/Atomic；避免锁嵌套 |
| C-07 | 控制语句 | Major | if/else/for/while/do 必须使用大括号；禁止魔法值；switch 必须有 default；三目运算符注意自动拆箱空指针 |
| C-08 | OOP 规范 | Major | 禁止使用过时方法（@Deprecated）；equals 方法要用常量或确定非 null 对象调用；所有 POJO 类必须重写 toString；构造方法禁止业务逻辑；序列化类新增字段需加 serialVersionUID |

**执行方式：**

1. 运行代码质量扫描脚本：
   ```bash
   python scripts/scan_code_quality.py <project-root> --output <output-dir>
   ```
2. 脚本自动检测可静态分析的规则项，产出 `code-issues.json`
3. 对于需要语义理解的规则项（如魔法值是否合理、异常处理是否恰当），结合 `references/alibaba-java-rules.md` 中的规则定义进行人工审查补充

### 阶段 4：报告生成

汇总架构检查和代码检查结果，生成分级报告和修复优先级计划。

**执行步骤：**

1. 汇总 `arch-issues.json` 和 `code-issues.json`
2. 运行报告生成脚本：
   ```bash
   python scripts/generate_report.py --arch <arch-issues.json> --code <code-issues.json> --output <output-dir>
   ```
3. 产出文件：
   - `report.html` — 可视化 HTML 报告（含统计图表、问题列表、修复计划）
   - `report.md` — Markdown 格式报告（便于版本控制和 CI/CD 集成）

**报告模板格式：** 参见 `references/report-template.md` 获取详细模板定义。

**报告结构：**

```
1. 检查概览
   - 工程信息（模块数、文件数、代码行数）
   - 检查范围和时间
   - 问题统计（按严重级别分类计数）

2. 架构检查结果
   2.1 DDD 分层检查
   2.2 模块依赖分析（含依赖关系图）
   2.3 循环依赖检测结果
   2.4 跨层调用检测结果

3. 代码质量检查结果
   3.1 命名规范
   3.2 注释规范
   3.3 异常处理
   3.4 日志规范
   3.5 集合处理
   3.6 并发处理
   3.7 控制语句
   3.8 OOP 规范

4. 问题详情列表
   - 每个问题：编号 | 严重级别 | 文件路径 | 行号 | 问题描述 | 规范条款 | 修复建议

5. 修复优先级计划
   - P0 (Blocker)：立即修复，阻塞发布
   - P1 (Critical)：本迭代修复
   - P2 (Major)：下个迭代修复
   - P3 (Minor)：择机修复

6. 修复进度跟踪表
```

## 问题严重级别定义

| 级别 | 含义 | 处理要求 | 示例 |
|------|------|----------|------|
| **Blocker** | 阻塞性问题，会导致编译失败或架构崩溃 | 立即修复，阻塞发布 | 循环依赖、分层缺失、依赖方向反转 |
| **Critical** | 严重问题，存在运行时风险或重大规范违反 | 本迭代内修复 | 空 catch 块、线程不安全、跨层调用 |
| **Major** | 重要问题，影响代码可维护性和可读性 | 下个迭代修复 | 命名不规范、日志拼接、魔法值 |
| **Minor** | 次要问题，建议改进 | 择机修复 | 注释缺失、代码风格、可选优化 |

## 使用示例

### 示例 1：完整检查

用户请求："检查 D:\projects\my-service 工程的架构和代码质量"

执行步骤：
1. 确认工程路径，检查 `pom.xml` 是否存在
2. 运行 `python scripts/scan_architecture.py D:\projects\my-service --output ./check-output`
3. 运行 `python scripts/scan_code_quality.py D:\projects\my-service --output ./check-output`
4. 运行 `python scripts/generate_report.py --arch ./check-output/arch-issues.json --code ./check-output/code-issues.json --output ./check-output`
5. 使用 `present_files` 展示 `report.html`

### 示例 2：仅架构检查

用户请求："分析这个多模块工程的模块依赖关系，看看有没有循环依赖"

执行步骤：
1. 运行 `python scripts/scan_architecture.py <project-root> --output ./check-output`
2. 阅读 `dep-graph.json` 和 `arch-issues.json`
3. 重点解读循环依赖检测结果和依赖关系图

### 示例 3：仅代码规范检查

用户请求："扫描代码里的阿里巴巴Java规范问题"

执行步骤：
1. 运行 `python scripts/scan_code_quality.py <project-root> --output ./check-output`
2. 阅读 `code-issues.json` 和 `rule-summary.json`
3. 按严重级别汇总问题

## 脚本依赖

- Python 3.9+
- 标准库：`os`, `re`, `json`, `pathlib`, `xml.etree.ElementTree`, `collections`, `argparse`
- 无需安装第三方包

## 参考文件

| 文件 | 用途 |
|------|------|
| [references/ddd-architecture-rules.md](references/ddd-architecture-rules.md) | DDD 分层规范、模块依赖约束、检查规则详解 |
| [references/alibaba-java-rules.md](references/alibaba-java-rules.md) | 阿里巴巴Java开发手册检查规则详解 |
| [references/report-template.md](references/report-template.md) | 报告输出模板与格式规范 |
| [scripts/scan_architecture.py](scripts/scan_architecture.py) | 架构检查脚本（DDD分层、依赖分析、循环检测） |
| [scripts/scan_code_quality.py](scripts/scan_code_quality.py) | 代码质量检查脚本（阿里规范8大类） |
| [scripts/generate_report.py](scripts/generate_report.py) | 报告生成脚本（HTML + Markdown） |
| [assets/report-template.html](assets/report-template.html) | HTML 报告模板 |

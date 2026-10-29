---
name: doc-generator
description: "面向微服务工程的文档自动生成技能。支持生成四类文档：开发手册（项目概述、技术栈、模块划分、代码结构、本地环境搭建、编码规范、调试方法、常见问题）、部署文档（环境要求、依赖安装、配置项、构建打包、Docker/K8s 部署、健康检查、回滚策略）、依赖拓扑图（服务间调用关系、外部中间件依赖、Mermaid 可视化拓扑）、变更日志（基于 Git 提交记录自动汇总）。从项目源码和配置文件自动提取信息，输出 Markdown 格式，支持全量或按模块筛选生成。"
---

# Doc Generator — 微服务工程文档自动生成

从微服务工程源码和配置文件中自动提取信息，生成四类结构化文档，输出为 Markdown 格式，存放在工作空间的 `docs-output/` 文件夹中。

## 适用场景

- Maven/Gradle 多模块微服务工程（Spring Boot / Spring Cloud）
- 需要生成开发手册、部署文档、依赖拓扑图、变更日志的场景
- 新人入项需要快速了解工程全貌
- 运维需要部署和运维参考文档
- 架构评审需要依赖拓扑视图

## 四类文档

| 类型 | 文件名 | 内容 |
|------|--------|------|
| 开发手册 | `DEVELOPMENT.md` | 项目概述、技术栈、模块划分、代码结构、本地环境搭建、编码规范、调试方法、常见问题 |
| 部署文档 | `DEPLOYMENT.md` | 环境要求、依赖安装、配置项说明、构建打包、Docker/K8s 部署、健康检查、回滚策略 |
| 依赖拓扑图 | `dependency-topology.md` | 服务间调用关系、外部中间件依赖、Mermaid 可视化拓扑图 |
| 变更日志 | `CHANGELOG.md` | 基于 Git 提交记录的版本变更汇总 |

## 执行流程

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ 1. 工程扫描   │───>│ 2. 依赖分析   │───>│ 3. 日志生成   │───>│ 4. 文档生成   │
│ scan_project  │    │ analyze_deps │    │ gen_changelog│    │ LLM 润色     │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       |                   |                   |                   |
       v                   v                   v                   v
  project-info.json   service-deps.json    CHANGELOG.md      DEVELOPMENT.md
  module-tree.json    middleware-deps.json                  DEPLOYMENT.md
  config-items.json   dependency-topology.mmd               dependency-topology.md
  source-summary.json
  tech-stack.json
  deployment-files.json
```

### 阶段 1：工程扫描

扫描目标工程结构、POM/Gradle 配置、配置文件、源码结构、技术栈、部署文件。

**执行脚本：**

```bash
python scripts/scan_project.py <project-root> [--modules <m1,m2,...>] [--output <dir>]
```

**参数说明：**
- `<project-root>` — 工程根目录路径（必填）
- `--modules` — 模块名称过滤，逗号分隔（可选，如 `pcm-app,pcm-common`）
- `--output` — 输出目录（默认 `<project-root>/docs-output`）

**脚本产出：**

| 文件 | 内容 |
|------|------|
| `project-info.json` | 工程基本信息：构建工具、GroupId/ArtifactId/Version、模块列表、Profile |
| `module-tree.json` | 模块树结构：每个模块的 artifactId、packaging、依赖列表、构建插件 |
| `config-items.json` | 配置项提取：从 application.yml/properties 中提取的所有配置项 |
| `source-summary.json` | 源码结构：Java 文件数、总行数、包分层统计、关键类、注解统计 |
| `tech-stack.json` | 技术栈检测：检测到的所有技术/框架及证据 |
| `deployment-files.json` | 部署文件：Dockerfile、docker-compose、K8s manifests、Helm Chart、CI/CD 文件 |

**技术栈检测规则：** 参见 `references/tech-stack-detection.md` 获取完整检测规则定义。

### 阶段 2：依赖分析

解析服务间调用关系（Feign/RestTemplate/WebClient/Dubbo/gRPC）和外部中间件依赖（数据库/缓存/消息队列/搜索引擎/注册中心），生成 Mermaid 拓扑图。

**执行脚本：**

```bash
python scripts/analyze_dependencies.py <project-root> [--modules <m1,m2,...>] [--output <dir>]
```

**脚本产出：**

| 文件 | 内容 |
|------|------|
| `service-dependencies.json` | 服务间调用关系列表：源模块/类 → 目标服务，含协议和调用方式 |
| `middleware-dependencies.json` | 中间件依赖：检测到的数据库/缓存/MQ等，含数据源详情 |
| `dependency-topology.mmd` | Mermaid 格式拓扑图源文件 |
| `dependency-topology.md` | 含 Mermaid 图的 Markdown 报告 |

### 阶段 3：变更日志生成

从 Git 提交记录自动汇总版本变更内容，支持 Conventional Commits 格式和自由格式提交消息。

**执行脚本：**

```bash
python scripts/generate_changelog.py <project-root> [--since <date>] [--until <date>] [--max-count <n>] [--output <file>] [--format <markdown|json>]
```

**参数说明：**
- `--since` — 开始日期（如 `2024-01-01`）
- `--until` — 结束日期
- `--max-count` — 最大提交数量
- `--output` — 输出文件路径（默认 `docs-output/CHANGELOG.md`）
- `--format` — 输出格式（`markdown` 或 `json`，默认 markdown）

**脚本产出：**

文件：`CHANGELOG.md`，包含：
- Breaking Changes 汇总
- 按类型分类的变更统计（New Features / Bug Fixes / Refactoring / Docs / Tests 等）
- 按日期分组的提交时间线
- Tags/Releases 列表

### 阶段 4：文档生成

结合前三阶段脚本的 JSON 产出和 `references/doc-templates.md` 中的模板，使用 LLM 生成最终的四类 Markdown 文档。

**文档模板：** 参见 `references/doc-templates.md` 获取四类文档的完整模板结构。

**生成步骤：**

1. 读取阶段 1-3 的所有 JSON 产出文件
2. 阅读模板参考 `references/doc-templates.md`
3. 按 `DEVELOPMENT.md` 模板填充：项目概述 → 技术栈表格 → 模块列表 → 目录结构 → 环境搭建步骤 → 配置项表 → 编码规范 → 调试方法 → 常见问题
4. 按 `DEPLOYMENT.md` 模板填充：环境要求 → 中间件列表 → 配置项说明 → 构建命令 → Docker/K8s 部署步骤 → 健康检查 → 回滚策略
5. 将 `dependency-topology.md` 整合为最终拓扑报告（脚本已生成，LLM 润色补充说明）
6. 将 `CHANGELOG.md` 整合为最终变更日志（脚本已生成，LLM 润色补充摘要）

**输出目录结构：**

```
docs-output/
├── project-info.json
├── module-tree.json
├── config-items.json
├── source-summary.json
├── tech-stack.json
├── deployment-files.json
├── service-dependencies.json
├── middleware-dependencies.json
├── dependency-topology.mmd
├── dependency-topology.md
├── CHANGELOG.md
├── DEVELOPMENT.md         ← LLM 生成
└── DEPLOYMENT.md          ← LLM 生成
```

## 使用示例

### 示例 1：全量文档生成

用户请求："为 D:\projects\my-service 工程生成完整文档"

执行步骤：
1. 确认工程路径，检查 `pom.xml` 或 `build.gradle` 是否存在
2. 运行工程扫描：
   ```bash
   python scripts/scan_project.py D:\projects\my-service
   ```
3. 运行依赖分析：
   ```bash
   python scripts/analyze_dependencies.py D:\projects\my-service
   ```
4. 运行变更日志生成：
   ```bash
   python scripts/generate_changelog.py D:\projects\my-service
   ```
5. 读取 `references/doc-templates.md` 获取模板
6. 读取阶段 1-3 产出的 JSON 文件，按模板填充生成 `DEVELOPMENT.md` 和 `DEPLOYMENT.md`
7. 润色 `dependency-topology.md` 和 `CHANGELOG.md`
8. 使用 `present_files` 展示 `docs-output/` 目录中的最终文档

### 示例 2：按模块筛选

用户请求："只生成 pcm-app 和 pcm-common 模块的文档"

执行步骤：
1. 运行扫描和依赖分析时加 `--modules` 参数：
   ```bash
   python scripts/scan_project.py D:\projects\hpis-pcm --modules pcm-app,pcm-common
   python scripts/analyze_dependencies.py D:\projects\hpis-pcm --modules pcm-app,pcm-common
   ```
2. 变更日志不受模块筛选影响（基于 Git 全量提交）
3. 文档生成时仅包含指定模块的内容

### 示例 3：仅生成变更日志

用户请求："生成这个工程的变更日志"

执行步骤：
1. 运行变更日志生成：
   ```bash
   python scripts/generate_changelog.py D:\projects\my-service --max-count 200
   ```
2. 展示 `docs-output/CHANGELOG.md`

### 示例 4：仅生成依赖拓扑图

用户请求："分析这个微服务的依赖关系，画个拓扑图"

执行步骤：
1. 运行依赖分析：
   ```bash
   python scripts/analyze_dependencies.py D:\projects\my-service
   ```
2. 展示 `docs-output/dependency-topology.md`（含 Mermaid 图）

## 脚本依赖

- Python 3.9+
- 标准库：`os`, `re`, `json`, `pathlib`, `xml.etree.ElementTree`, `collections`, `argparse`, `subprocess`, `datetime`
- 无需安装第三方包
- Git（变更日志功能需要，工程扫描和依赖分析不需要）

## 参考文件

| 文件 | 用途 |
|------|------|
| [references/doc-templates.md](references/doc-templates.md) | 四类文档的 Markdown 模板结构定义（开发手册、部署文档、拓扑报告、变更日志） |
| [references/tech-stack-detection.md](references/tech-stack-detection.md) | 技术栈检测规则：从 POM/Gradle/配置/源码中识别框架和中间件 |
| [scripts/scan_project.py](scripts/scan_project.py) | 工程扫描脚本：提取项目信息、模块树、配置项、源码结构、技术栈、部署文件 |
| [scripts/analyze_dependencies.py](scripts/analyze_dependencies.py) | 依赖分析脚本：解析服务间调用、中间件依赖、生成 Mermaid 拓扑图 |
| [scripts/generate_changelog.py](scripts/generate_changelog.py) | 变更日志脚本：从 Git 提交记录生成结构化变更日志 |
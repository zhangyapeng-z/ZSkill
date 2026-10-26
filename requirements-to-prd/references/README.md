# requirements-to-prd · references

[English](README.en.md)

**需求分析 / PRD 方法论附件**

本目录是 Agent Skill [`requirements-to-prd`](../SKILL.md) 的**渐进式资料层**：主文件 `SKILL.md` 负责双文档工作流与模板；此处放需求拆解、方案可行性、AI PRD、验收测试边界、方法论速查与配图规则，避免上下文塞满大段说明。

| 主 Skill | 父目录 |
|----------|--------|
| [../SKILL.md](../SKILL.md) | `requirements-to-prd/` |

---

## 目录

- [本目录解决什么问题](#本目录解决什么问题)
- [Before / After](#before--after)
- [文件结构](#文件结构)
- [与主 Skill 的分工](#与主-skill-的分工)

---

## 本目录解决什么问题

- **想先做需求分析再写 PRD**，需要拆功能原子、判断方案可行性、处理 AI/传统方案 → 用本目录新增的需求分析资料。
- **想按七层法写全 PRD**，但不想在对话里反复贴同一套理论 → 用 [`methodology.md`](methodology.md) 速查。
- **需要决定何时配图、Mermaid 如何写** → 用 [`diagram-guide.md`](diagram-guide.md) 与 [`mermaid-compatibility.md`](mermaid-compatibility.md)。

## Before / After

| | 无 `references/`，全塞进 SKILL.md | 有本目录（当前） |
|---|:---:|:---:|
| **方法论** | 主文件冗长、难维护 | 主文件保留模板，理论独立成 [`methodology.md`](methodology.md) |
| **拆解与验收** | 规则分散在对话里 | 独立成 `requirement-decomposition.md`、`acceptance-testing.md` 等 |

---

## 文件结构

```
references/
├── README.md / README.en.md
├── methodology.md
├── requirement-decomposition.md
├── solution-feasibility.md
├── ai-prd-patterns.md
├── acceptance-testing.md
├── diagram-guide.md
├── mermaid-compatibility.md
└── agile-iteration.md
```

| 文件 | 用途 | 何时打开 |
|------|------|----------|
| [methodology.md](methodology.md) | 七层方法论、10 个核心工具、PRD 四层次补全 | 需要对照理论或术语时 |
| [requirement-decomposition.md](requirement-decomposition.md) | 需求意图识别、功能原子化、EARS 转换、追溯链 | 需求模糊、零散、需要拆解或编号时 |
| [solution-feasibility.md](solution-feasibility.md) | 候选方案、落地可行性、V1 推荐与反模式 | 用户提出方案但需要判断真正解决路径时 |
| [ai-prd-patterns.md](ai-prd-patterns.md) | 传统/AI增强/AI核心分类，AI能力卡、兜底、评估指标 | 涉及 AI、LLM、预测、分类、抽取、推荐时 |
| [acceptance-testing.md](acceptance-testing.md) | PRD 验收标准与独立测试用例的边界、模板 | 用户问验收/测试用例，或需要单独测试文档时 |
| [diagram-guide.md](diagram-guide.md) | 需求特征与流程/时序/架构等配图规则 | 写 §3～§8 时需决定是否画 Mermaid 图 |
| [mermaid-compatibility.md](mermaid-compatibility.md) | 跨平台 Mermaid 语法约束 | 交付含 Mermaid 图时自检 |
| [agile-iteration.md](agile-iteration.md) | MVP、迭代与范围管理补充 | 需要拆分版本或迭代节奏时 |

---

## 与主 Skill 的分工

| 内容 | 放在哪里 |
|------|----------|
| 双文档输出流程、文件命名、主模板、自检清单 | [../SKILL.md](../SKILL.md) |
| 需求拆解、功能原子化、EARS 转换 | [requirement-decomposition.md](requirement-decomposition.md) |
| 候选方案与可行性判断 | [solution-feasibility.md](solution-feasibility.md) |
| AI/传统方案组合写法 | [ai-prd-patterns.md](ai-prd-patterns.md) |
| PRD 验收与测试用例边界 | [acceptance-testing.md](acceptance-testing.md) |
| 七层法展开、工具到层的映射 | [methodology.md](methodology.md) |
| PRD 配图类型与触发条件 | [diagram-guide.md](diagram-guide.md) |
| Mermaid 兼容性自检 | [mermaid-compatibility.md](mermaid-compatibility.md) |

交付物默认为 **Markdown**（对话全文或用户指定本地路径）。归档到协作平台由用户自行粘贴或选用其他工具，本技能不绑定任何第三方 CLI。

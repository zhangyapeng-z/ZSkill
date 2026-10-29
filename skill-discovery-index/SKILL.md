---
name: "skill-discovery-index"
version: "1.0.0"
display_name: "技能发现与选型索引"
display_name_en: "Skill Discovery Index"
description: "帮用户在 1000+ 技能生态里快速找到对的那一个：11 大功能分类地图、按「真实用例」选型的判断流程、技能质量评估标准（可移植性 / 零依赖 / 可验证产出）、以及自建技能时的查重与贡献规范。当用户问「有没有能干 X 的技能」「该装哪个技能」「这个技能靠谱吗」「怎么找技能」时触发。"
description_zh: "帮用户在 1000+ 技能生态里快速找到对的那一个：11 大功能分类地图、按「真实用例」选型的判断流程、技能质量评估标准（可移植性、零依赖、可验证产出）、以及自建技能时的查重与贡献规范。当用户问「有没有能干 X 的技能」「该装哪个技能」「这个技能靠谱吗」「怎么找技能」时触发。"
description_en: "Find the right skill among a 1000+ ecosystem: a category map of 11 functional domains, a real-use-case driven selection flow, skill quality criteria (portability, zero dependencies, verifiable output), and duplication checks plus contribution standards for authoring new skills. Trigger when the user asks whether a skill exists for X, which skill to install, whether a skill is trustworthy, or how to find skills."
---

# 技能发现与选型索引（原创重制版）

> 基于 ComposioHQ/awesome-claude-skills 公开方法论重制。原仓库是 1000+ 技能的**精选索引**（awesome list 性质），本包抽取其**分类体系与选型/质量判断标准**做成可执行技能。不搬运索引内容。

## 定位

这是一个**导航与选型**技能，不是执行技能。它帮你回答三个问题：

1. 有没有现成技能能干这件事？
2. 有几个候选时该选哪个？
3. 没有的话，自己做一个要按什么标准？

## 11 大功能分类地图

按场景找，不要按技术名词找：

| 分类 | 典型技能 |
|---|---|
| **文档处理** Document Processing | docx / pdf / pptx / xlsx 生成与解析 |
| **开发与代码工具** Development & Code Tools | artifacts-builder、Changelog Generator、MCP Builder、Webapp Testing |
| **数据与分析** Data & Analysis | CSV 汇总、deep-research、postgres |
| **商业与营销** Business & Marketing | Brand Guidelines、竞品广告提取、Lead Research |
| **沟通与写作** Communication & Writing | Content Research Writer、会议纪要洞察 |
| **创意与媒体** Creative & Media | Canvas Design、图片增强、GIF 生成、视频下载 |
| **生产力与组织** Productivity & Organization | 文件整理、发票归档、简历定制 |
| **协作与项目管理** Collaboration & Project Management | Google Workspace、outline、review-implementing |
| **安全与系统** Security & Systems | 计算机取证、威胁狩猎 |
| **辅助技术** Assistive Technology | 无障碍 / 神经多样性辅助 |
| **应用自动化** App Automation | 按 SaaS 类型细分：CRM、工单、邮件、代码与 DevOps、存储、表格与数据库、日历、社媒、营销、客服、电商与支付、设计协作、分析、HR、自动化平台、会议 |

详见 `references/01-category-map.md`。

## 选型判断流程

按**真实用例**找，而不是按关键词：

1. **说清你要完成的真实用例**（不是「我要个 PDF 技能」，而是「我要从 200 份合同里抽出签约日期汇成表」）。
2. **先在分类地图里定位**可能命中哪些分类（可能跨类）。
3. **查重**：是否已有技能覆盖？有就直接用/改，不要重造。
4. **评估候选**：按下面的质量标准筛。
5. **验证**：装上跑一遍真实用例，跑不通就换。

## 质量标准（判断一个技能靠不靠谱）

| 维度 | 好技能 | 危险信号 |
|---|---|---|
| **真实用例** | 解决一个具体的、有人真的会做的事 | 演示性质、没人会真用 |
| **可移植性** | 遵循开放标准，跨 Agent 可用 | 绑定单一平台/私有注解 |
| **依赖** | 零依赖或依赖明确可装 | 隐式依赖，装了跑不起来 |
| **产出可验证** | 有明确产出与验收方式 | 「大概能帮你优化一下」 |
| **描述** | 说清做什么 + 何时用 | 只有形容词 |
| **触发** | 该触发时触发，不该触发时安静 | 什么请求都跳出来 |

详见 `references/02-evaluation-standards.md`。

## 自建技能的贡献规范

找不到合适的，就自己做一个。规范：

1. **基于真实用例**——你或别人真的会用到。
2. **先查重**——确认没有已有技能覆盖同一件事。
3. **遵循结构模板**——`SKILL.md` + 可选 `references/`、`scripts/`。
4. **跨平台测试**——至少在两个 Agent 环境验证能跑。
5. **文档清晰**——写清定位、触发条件、用法、边界。

## 使用纪律

- 装新技能前先问「已有的是否够用」，技能太多会互相抢触发。
- 同一领域的多个技能容易重叠，保留一个主力，其余卸载。
- 定期清理：三个月没用过的技能，大概率不会再用了。

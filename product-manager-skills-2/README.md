# 产品经理技能包

**不是模板包。是给 AI 助手安装的 PM 大脑。**

把 AI 助手变成一个能够评审PRD、诊断SaaS指标、规划路线图、运行发现调研和辅导职业转型的产品经理。

[![发布](https://img.shields.io/github/v/release/Digidai/product-manager-skills)](https://github.com/Digidai/product-manager-skills/releases)
[![许可证](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)](LICENSE)
[![安全](https://img.shields.io/badge/security-zero%20scripts%2C%20pure%20markdown-brightgreen)](https://github.com/Digidai/product-manager-skills)
[![适用平台](https://img.shields.io/badge/works%20with-WorkBuddy%20Agent%20Skills-blue)](#60秒安装)

> 零脚本。零依赖。零网络调用。纯Markdown知识，你可以逐行检查后再安装。

## 为什么人们重用它

大多数AI PM工具擅长写漂亮的废话。这个技能专为严谨性重要的重复工作流设计：

- 将模糊的功能需求转化为问题框架、可衡量成果和可用的PRD。
- 从原始指标诊断SaaS健康状况，而不是得到"改善留存"这样的通用建议。
- 压力测试优先级、路线图和策略，明确权衡取舍。
- 用具体差距和行动计划辅导PM到总监再到VP的转型。

## 从这三个工作流开始

| 工作流 | 提示词 | 示例 |
|---|---|---|
| **SaaS健康诊断** | "分析这些指标：MRR $50k，500客户，毛利率80%，月流失8%，CAC $500。" | [SaaS诊断演示](examples/saas-health-diagnostic.md) |
| **PRD反馈和评审** | "像一位强势PM同行一样评审这份PRD草稿。标记糟糕的框架、缺失的指标、解决方案走私和交付风险。" | [PRD评审演示](examples/prd-review.md) |
| **总监就绪度辅导** | "我是一位高级PM，在90天内面试总监角色。诊断我的差距并辅导我。" | [总监辅导演示](examples/director-coaching.md) |

更多提示词：[STARTER-PROMPTS.md](STARTER-PROMPTS.md)

## 60秒安装

从 WorkBuddy 技能市场安装后，技能会自动激活。手动安装方式：

1. 下载本技能包并解压。
2. 将整个 `product-manager-skills/` 目录（目录名必须与 `SKILL.md` 中的 `name` 字段一致）放入用户级技能目录：

```bash
# Windows
~/.workbuddy/skills/product-manager-skills/

# macOS / Linux
~/.workbuddy/skills/product-manager-skills/
```

3. 重启客户端或执行 `/reload-skills`，在技能列表中确认出现新条目。

然后粘贴以下之一：

```text
帮我为一个通知偏好功能写PRD。做出合理假设并标注它们。

分析这些指标：MRR $50k，500客户，毛利率80%，月流失8%，CAC $500。

评审我的路线图，告诉我哪些利益相关者请求超过了证据支持。
```

## 好的输出是什么样的

### 1. SaaS诊断

输入：

```text
分析这些指标：MRR $50k，500客户，毛利率80%，月流失8%，CAC $500。
```

预期行为：

```text
- 8%的月流失率年化约为63%。这是红旗，不是"略高"的指标。
- ARPA约为$100/月。凭借80%毛利率和8%月流失率，更好的LTV约为$1,000。
- LTV:CAC约为2:1。投资回收期约为6.25个月。
- 诊断：回收期可行，留存不行。在按队列理解流失之前不要扩大获客。
```

完整示例：[examples/saas-health-diagnostic.md](examples/saas-health-diagnostic.md)

### 2. PRD评审

输入：

```text
评审这份通知偏好中心的PRD。标记解决方案走私、弱指标、范围蔓延和交付风险。
```

预期行为：

```text
- 你的问题陈述是解决方案走私的："用户需要一个偏好仪表板。"
- 成功指标没有基线、目标或护栏。
- 范围混合了渠道、摘要、免打扰时间、管理规则和迁移。这是多个版本。
- 建议更薄的第一刀：邮件退订 + 账户级别偏好 + 可衡量的退订驱动流失减少。
```

完整示例：[examples/prd-review.md](examples/prd-review.md)

### 3. 职业辅导

输入：

```text
我是一位管理两个PM的高级PM，执行力强，组织影响力弱，3个月后面试总监角色。辅导我。
```

预期行为：

```text
- 诊断：强团队高度，弱组织高度。
- 差距：你描述执行胜利很好但不描述组合权衡或跨职能影响力。
- 计划：收集3个展示组织层面影响的故事，建立每周可见性循环，练习带权衡的决策框架。
```

完整示例：[examples/director-coaching.md](examples/director-coaching.md)

## 你将获得什么

| 领域 | 帮助内容 | 示例框架 |
|---|---|---|
| **发现与研究** | 验证问题、准备访谈、映射旅程、设计实验 | JTBD、Mom Test、机会解决方案树、Lean UX画布、PoL探测 |
| **策略与定位** | 产品定位、工作优先级、市场规模、路线图 | Geoffrey Moore、PESTEL、TAM/SAM/SOM、RICE、ICE、Kano |
| **制品与交付** | 编写和评审PRD、用户故事、史诗、PRFAQ、推荐文档 | Cohn + Gherkin、故事映射、史诗分解、PRFAQ |
| **财务与指标** | 计算32个SaaS指标并诊断业务健康 | MRR、ARR、NRR、CAC、LTV、40法则、魔法数字 |
| **职业与领导力** | 辅导PM到总监到VP转型 | 高度-视野框架、三个P、30-60-90入职 |
| **AI产品打造** | 压力测试AI原生产品决策 | AI形态就绪度、上下文工程、Agent编排 |

## 为什么它比通用提示词表现更好

| 通用提示词 | 这个技能 |
|---|---|
| 写看似合理的PM文本 | 应用PM框架和质量门 |
| 接受糟糕的框架 | push back解决方案走私、指标剧场、特性工厂等 |
| 给出通用流失建议 | 计算流失、LTV、回收期并命名真正瓶颈 |
| 每节课重复PM上下文 | 携带可复用的PM工作流和路由系统 |
| 优化礼貌 | 优化决策、权衡和下一步 |

## 适用人群

- 使用 AI 助手工作的技术PM、创始人和产品负责人。
- 希望拥有可复用的PM大脑而不向另一个SaaS发送产品上下文的团队。
- 重视push back、假设和明确权衡而非听起来不错的输出的用户。

## 不适用人群

- 寻找具有审批、评论和共享工作流的协作Web应用的团队。
- 只想要被动模板填写而不希望AI挑战框架的用户。
- 喜欢交钥匙SaaS入职而非本地或基于仓库安装的非技术买家。

## 交互风格

这个技能针对快速获得第一个有用的草稿进行优化：

- 如果请求足够清楚，它立即回答并内联标注假设。
- 如果上下文不完整，它先给出最佳草稿，只问最少的后续问题。
- 如果任务是真正探索性的，它可以切换到一次一个问题引导模式。
- 每个答案都应该以做出的决策、要验证的假设和推荐的下一步结束。

## 为重复使用而构建

大多数PM工作是重复的。这个技能在你每周重用时最强大：

- 周一：评审路线图变更和优先级请求。
- 周中：在分享给工程之前评审PRD、史诗和用户故事。
- 周五：运行SaaS健康诊断或功能ROI检查。
- 职业季：排练访谈故事、运营高度和领导力差距。

## 结构

```text
product-manager-skills/
├── SKILL.md              # 技能入口：路由表 + 互动协议 + 质量门
├── knowledge/            # 六大知识领域的框架与方法论
│   ├── discovery-research.md
│   ├── strategy-positioning.md
│   ├── artifacts-delivery.md
│   ├── finance-metrics.md
│   ├── career-leadership.md
│   └── ai-product-craft.md
├── templates/            # 12 个可直接填充的产出模板
├── examples/             # 3 个完整输出示例
├── STARTER-PROMPTS.md    # 可直接复用的提示词
├── README.md
├── README.zh-CN.md
└── LICENSE
```

核心内容：25个Markdown文件，约2,400行，约130KB的PM知识和模板。

## 触发方式

说出你的需求即可，例如「帮我写一份 XX 功能的 PRD」「分析这些 SaaS 指标」「评审这份路线图」「我该怎么准备总监面试」。详见 [STARTER-PROMPTS.md](STARTER-PROMPTS.md)。

## 信任与安全

本项目仅包含指令：

- 无可执行脚本
- 无外部网络调用
- 无需环境变量或凭证
- 无权限提升
- 每个发布的文件都是人类可读的Markdown

## 反馈与贡献

- 如果框架缺失或工作流感觉薄弱，请在 [GitHub 开issue](https://github.com/Digidai/product-manager-skills/issues)。
- 如果你想要新领域或更强的示例，请在 [GitHub 开discussion](https://github.com/Digidai/product-manager-skills/discussions)。
- 如果这个技能帮助了你，请给仓库加星或分享用模板生成的输出。

## 许可证与署名

[CC BY-NC-SA 4.0](LICENSE)

原作者 [Gene Dai](https://genedai.me/)，源自真实产品工作，而非教科书总结。
本版本为适配 WorkBuddy 技能市场发布规范的改编版本，遵循相同许可协议。

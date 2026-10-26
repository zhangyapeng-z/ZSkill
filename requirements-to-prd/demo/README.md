# requirements-to-prd · Demo 与回归

本目录仅用于维护者回归验证，不作为日常生成上下文。正常使用 [../SKILL.md](../SKILL.md) 时，不应读取本目录，除非用户明确要求检查 demo 或做回归。

固定输入用于验证技能是否能输出两份协调文档：**需求分析文档**与**PRD**。

## 文件

| 文件 | 说明 |
|------|------|
| [input-requirement.md](input-requirement.md) | 用户侧原始需求（测试时勿改**字面表述**） |
| [expected-requirement-analysis.md](expected-requirement-analysis.md) | 需求分析文档参考输出（轻量金样） |
| [expected-prd.md](expected-prd.md) | PRD 参考输出（历史完整金样，可按新版模板继续迭代） |
| [expected-traceability.md](expected-traceability.md) | 追溯矩阵 + OQ 登记金样（Agent/下游消费） |
| [TEST-RUN.md](TEST-RUN.md) | 每次回归的简要记录（可追加） |

## 如何通过自检

对照 [../SKILL.md](../SKILL.md) **Self-Check**：

- [ ] 是否先输出需求分析，再输出 PRD  
- [ ] 需求分析是否含功能原子、方案可行性、AI/传统适配判断  
- [ ] PRD §5 EARS 是否可测试、少模糊词（「友好」等是否在 §9/§10 量化）  
- [ ] PRD 是否含权限、数据、NFR、异常边界  
- [ ] PRD 验收是否覆盖主成功与关键失败  
- [ ] PRD 是否含 MVP、Out of Scope、上线后指标  
- [ ] 若需求命中 [../references/diagram-guide.md](../references/diagram-guide.md) 的「应配图」条件，是否已配图或说明为何不画  
- [ ] ID 符合 `FA-001` / `FR-001` / `AC-01` / `OQ-01` 约定（无 `AC-001` 混用）  
- [ ] 阻塞项以 `OQ-{nn}` 登记 Owner，而非零散「待补充」  

**与金样比较**：不必逐字相同，但需求分析与 PRD 的职责边界、功能原子到 FR/AC 的追溯关系应一致；业务内容允许随评审迭代。追溯矩阵见 [expected-traceability.md](expected-traceability.md)。

## 与仓库根目录关系

- 本技能根目录为 `requirements-to-prd/`。  
- 交付物为 Markdown；勿将真实业务机密或未脱敏凭证提交公开库：见 [../SECURITY.md](../SECURITY.md)。

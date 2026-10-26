---
name: feishu-weekly-report
description: "飞书智能周报/月报：自动读取本人有权访问、且与本人工作相关的飞书文档、会议纪要、任务、多维表格、电子表格、知识库及明确指定的群聊/消息，跨源聚合去重、判定状态，按周/月维度生成有事实依据、可直接向领导汇报的中文周报或月报（领导版摘要 + 完整版）。触发词：生成周报、写周报、本周周报、上周周报、工作周报、汇报周报、生成月报、写月报、本月月报、上月月报、weekly report、monthly report。默认只读；写飞书前必须先预览并经用户确认。"
description_zh: "飞书智能周报/月报：自动读取飞书文档/会议/任务/多维表格/电子表格/知识库/群聊消息，跨源去重、判定状态，按周或月维度输出领导版摘要+完整周报/月报，事实与判断分离，默认只读、写前必确认。"
version: "1.1.0"
allowed-tools: Bash, Read
metadata:
  requires:
    bins: ["lark-cli"]
    skills: ["lark-unified"]
---

# 飞书智能周报/月报（feishu-weekly-report）

编排型工作流技能：复用 `lark-cli`（见 `lark-unified`）读取飞书各数据源，核心价值在**周期推断、相关性判断、跨源去重、状态真实性判定、事实/判断分离**这几层周报/月报逻辑上。

**开始前 MUST 先用 Read 读取 `lark-unified` 的 SKILL.md**，认证、身份、`lark-cli` 命令模型与 JSON 契约（检查 `ok` 而非 `code`）以其为准。

## 适用场景

- "生成这周周报" / "写周报" / "上周周报" / "帮我汇报一下最近的工作"
- "生成这个月的月报" / "上月月报" / "本月月报" / "把本月会议、任务、表格里的事整理成月报"
- "把这周会议、任务、表格里的事整理成周报"

## 五条铁律（不可违反）

1. **默认只读**：不修改文档/任务/表格/知识库，不发消息，不建/覆盖文档，除非用户明确要求且已确认。
2. **事实与判断分离**：禁止编造完成度、金额、业务效果、负责人、截止日期、项目状态、领导意见。
3. **不把"计划/准备/讨论中"写成"已完成"**：状态判定只认证据（见 `references/status-rules.md`）。
4. **最小权限**：缺 scope 时用 `--scope` 精确补授权，绝不 `--domain all`。
5. **时间用系统命令算，不心算**：周期起止由 `date`/Python 计算（见 `references/period-rules.md`）。

## 编排流程

```
① 定周期  → 解析"周报/月报 + 本周/上周/本月/上月/最近N天/指定区间"，用 date+Python 算起止，输出中固化周期（见 references/period-rules.md）
② 预检    → lark-cli auth status / auth check，缺 scope 只补精确 scope
③ 拉取    → 各数据源并行只读拉取（--as user），命令见 references/data-sources.md；月报/跨月范围按自然月拆段查询
④ 相关性  → 过滤出"我相关 + 周期内有变化"（见 data-sources.md 的过滤逻辑）
⑤ 抽取    → 每条转结构化字段：项目/事项/状态/负责人/截止/结果/来源链接/更新时间
⑥ 去重    → 跨源归并同一事项，保留最新状态 + 全部主要来源（见 dedup-rules.md）
⑦ 判状态  → 已核验事实 / 综合判断 / 待确认；冲突→"状态冲突"（见 status-rules.md）
⑧ 归类    → 按业务主题分组，不按"文档/会议/表格"分
⑨ 脱敏    → 敏感字段清洗（见 privacy-rules.md）
⑩ 输出    → 生成领导版摘要 + 完整周报/月报，对话内预览，等确认
```

## 硬规则速查

| 事项 | 规则 |
|---|---|
| 身份 | 仅 `--as user`（读个人资源必须 user token） |
| 输出格式 | `--format json`，便于解析 |
| JSON 判定 | 检查 `ok == true` 或退出码，**不要看 `code`** |
| 分页 | `--page-all`，`--page-limit` 上限按 tier 区分（shortcut 1-1000，api 0=无限） |
| 时间范围超 1 个月 | 拆成多段查询（按自然月或按周拆段，合并时去重） |
| 周期默认（周报） | 周一→上周一~上周日；其他日→本周一~现在 |
| 周期默认（月报） | 每月1~3日→上月整月；其他日→本月1日~现在 |
| 写飞书门槛 | 仅用户说"创建飞书周报/月报"→ 预览 → 确认 → `docs +create` → 返回链接 |

## 参考文件

- [references/period-rules.md](references/period-rules.md) — 周期推断 + 日期计算（date/Python）
- [references/data-sources.md](references/data-sources.md) — 各源命令映射 + scope 表 + 相关性过滤
- [references/dedup-rules.md](references/dedup-rules.md) — 跨源去重与状态冲突处理
- [references/status-rules.md](references/status-rules.md) — 状态枚举 + 事实/判断/待确认判定标准
- [references/report-template.md](references/report-template.md) — 双版本周报/月报模板 + 句式规范
- [references/privacy-rules.md](references/privacy-rules.md) — 脱敏清单与处理规则
- [references/write-back-rules.md](references/write-back-rules.md) — 写飞书的门槛与安全流程

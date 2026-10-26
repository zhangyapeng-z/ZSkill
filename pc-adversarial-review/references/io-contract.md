# 输入/输出契约（I/O Contract）

为 MCP 接入和自动化处理提供结构化接口。正常对话模式下不使用，MCP 调用或用户要求结构化输出时使用。

---

## 一、输入契约（Input Schema）

```json
{
  "content": "string（必填，待审查的内容：方案文本/代码/文档）",
  "type": "plan-decision | code-tech | document-content | mixed（可选，自动推断）",
  "mode": "quick | standard | deep（可选，默认自动判断）",
  "context": {
    "domain": "string（领域/行业）",
    "audience": "string（目标受众）",
    "goal": "string（核心目标）",
    "constraints": "string（已知约束）"
  },
  "language": "zh-CN | en（可选，跟随输入）",
  "options": {
    "include_revised": "boolean（是否生成修订版，深度模式默认 true）",
    "max_experts": "number（最大专家数，默认按模式）",
    "focus_areas": ["string（重点关注的领域，可选）"]
  }
}
```

---

## 二、输出契约（Output Schema）

```json
{
  "summary": {
    "review_type": "string",
    "mode": "string",
    "experts": ["string（参与专家列表）"],
    "overall_conclusion": "pass | conditional-pass | fail",
    "conclusion_basis": "string（一句话结论，大白话）"
  },
  "requirements_checklist": [
    {
      "requirement": "string（用户需求/功能点，用用户的话描述）",
      "status": "implemented | partial | missing | uncertain",
      "explanation": "string（大白话说明）"
    }
  ],
  "chain_alignment": [
    {
      "node": "string（链路环节）",
      "role": "string（该环节作用，大白话）",
      "status": "ok | broken | misaligned | uncertain",
      "misalignment": "string（对不齐的地方，无则 null）",
      "related_issue_id": "string（对应问题ID，无则 null）"
    }
  ],
  "issues": [
    {
      "id": "string（如 P0-1、P1-2）",
      "severity": "P0 | P1 | P2",
      "problem": "string（问题是什么，大白话）",
      "evidence": "string（依据，引用输入中的实际内容）",
      "analysis": "string（原因分析，大白话）",
      "chain_impact": "string（链路影响：位置/上下游/牵动面）",
      "suggestion": "string（修改建议，具体可执行）",
      "plain_version": "string（大白话版，P0/P1 必填）",
      "source_expert": "string（哪位专家提出的）",
      "consensus": "boolean（是否是共识问题）"
    }
  ],
  "divergence": {
    "consensus_points": ["string（共识问题）"],
    "divergence_points": [
      {
        "issue": "string（分歧点）",
        "opinions": [
          {
            "expert": "string",
            "view": "string"
          }
        ],
        "verdict": "string（主持人裁定）"
      }
    ],
    "dissenting_opinions": ["string（保留意见）"]
  },
  "verification": {
    "officer_check": [
      {
        "issue_id": "string",
        "issue_summary": "string",
        "fix_method": "string",
        "result": "passed | failed | uncertain",
        "evidence": "string（验证依据）"
      }
    ],
    "overall_result": "string（验收总结论）"
  },
  "revised_content": {
    "full_content": "string（修订后完整内容，仅深度模式）",
    "change_log": [
      {
        "position": "string（改动位置）",
        "original": "string（原内容）",
        "revised": "string（修订后）",
        "reason": "string（为什么改）",
        "corresponding_issue": "string（对应哪个问题）"
      }
    ],
    "revision_notes": {
      "total_changes": "number",
      "by_severity": { "P0": 0, "P1": 0, "P2": 0 },
      "known_issues": ["string（已知遗留问题）"]
    }
  },
  "context_gaps": [
    {
      "missing_info": "string（缺什么信息）",
      "impact": "string（影响什么判断）",
      "resolution": "string（补充后能确认什么）"
    }
  ],
  "is_preliminary": "boolean（是否为初步审查）",
  "follow_up_suggestion": "string（后续建议，如续审指引）"
}
```

### 字段说明

| 字段 | 极速模式 | 标准模式 | 深度模式 | 说明 |
|---|---|---|---|---|
| summary | ✅ | ✅ | ✅ | 审查摘要 |
| requirements_checklist | ✅ | ✅ | ✅ | 需求落实速览 |
| chain_alignment | ✅ | ✅ | ✅ | 链路对齐清单 |
| issues | 仅 P0/P1 | 全量 | 全量 | 问题清单 |
| divergence | 简化 | ✅ | ✅ 详尽 | 分歧与共识 |
| verification | 简化 | ✅ | ✅ 详尽 | 质问官验收 |
| revised_content | ❌ | ❌ | ✅ | 自动修订版 |
| context_gaps | （如有） | （如有） | （如有） | 信息缺口 |
| is_preliminary | ✅ | ✅ | ✅ | 是否初步审查 |

### 使用说明

- MCP 调用时，默认返回此 JSON 结构
- 正常对话模式下，输出按 `output-template.md` 的大白话格式
- 结构化输出与大白话报告内容必须一致，不能出现矛盾
- 极速/标准模式下，`revised_content` 字段可为 `null`
- 没有信息缺口时，`context_gaps` 为空数组

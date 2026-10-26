---
name: company-research
version: 1.0.0
display_name: Exa 企业调研
display_name_en: Exa Company Research
description_zh: 用 Exa 搜索做企业调研：查找公司信息、竞争对手、新闻、推文、财务数据、LinkedIn 档案，并批量构建公司名录。强制约束：只使用 Exa 的 web_search_advanced 工具，不要使用 web_search_exa 或其他 Exa 工具；且绝不在主上下文里直接跑 Exa 搜索，必须派发 Task 子代理执行搜索与提炼，只回传精简的 JSON 或简短 Markdown，避免污染主上下文。
description_en: "Company research powered by Exa search. Finds company profiles, competitors, news, tweets, financials and LinkedIn profiles, and builds company lists in bulk. Two hard constraints apply: only use the web_search_advanced tool from Exa, never web_search_exa or any other Exa tool, and never run Exa searches in the main context. Always spawn Task subagents instead, which run the search internally, process results with model intelligence and return only distilled output as compact JSON or brief markdown, keeping the main context clean."
description: 用 Exa 搜索做企业调研：查找公司信息、竞争对手、新闻、推文、财务数据、LinkedIn 档案，并批量构建公司名录。强制约束：只使用 Exa 的 web_search_advanced 工具，不要使用 web_search_exa 或其他 Exa 工具；且绝不在主上下文里直接跑 Exa 搜索，必须派发 Task 子代理执行搜索与提炼，只回传精简的 JSON 或简短 Markdown，避免污染主上下文。
triggers: company research, competitor analysis, market research, find companies, research company, company intel.
requires_mcp: exa
context: fork
---


# Company Research

## Tool Restriction (Critical)

ONLY use `web_search_advanced` from Exa. Do NOT use `web_search_exa` or any other Exa tools.

## Token Isolation (Critical)

Never run Exa searches in main context. Always spawn Task agents:

- Agent runs Exa search internally
- Agent processes results using LLM intelligence
- Agent returns only distilled output (compact JSON or brief markdown)
- Main context stays clean regardless of search volume

## Dynamic Tuning

No hardcoded numResults. Tune to user intent:

- User says "a few" → 10-20
- User says "comprehensive" → 50-100
- User specifies number → match it
- Ambiguous? Ask: "How many companies would you like?"

## Query Variation

Exa returns different results for different phrasings. For coverage:

- Generate 2-3 query variations
- Run in parallel
- Merge and deduplicate

## Categories

Use appropriate Exa category:

- company → homepages, gargantuan amount of metadata such as headcount,
  location, funding, revenue
- news → press coverage
- tweet → social presence
- people → LinkedIn profiles (public data)

## LinkedIn

Public LinkedIn via Exa: category "people", no other filters
Auth-required LinkedIn → use Claude in Chrome browser fallback

## Browser Fallback

Auto-fallback to Claude in Chrome when:

- Exa returns insufficient results
- Content is auth-gated
- Dynamic pages need JavaScript

## Models

- haiku: fast extraction (listing, discovery)
- opus: synthesis, analysis, browser automation


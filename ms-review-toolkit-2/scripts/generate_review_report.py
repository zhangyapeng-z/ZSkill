#!/usr/bin/env python3
"""
Review Report Generator — 审查报告生成脚本
汇总架构与代码审查结果，生成结构化修改计划与 JSON/Markdown/HTML 报告。

用法:
    python generate_review_report.py --arch <arch-issues.json> --code <code-issues.json> \
        [--tech <tech-stack.json>] [--services <service-inventory.json>] [--callgraph <service-call-graph.json>] \
        --output <output-dir>

产出文件:
    review-report.json       — 结构化审查报告（机器可读，含修改计划）
    modification-plan.json   — 独立结构化修改计划
    report.md                — Markdown 报告
    report.html              — 可视化 HTML 报告
"""

import os
import re
import json
import argparse
import hashlib
from datetime import datetime
from collections import defaultdict


SEVERITY_ORDER = {"Blocker": 0, "Critical": 1, "Major": 2, "Minor": 3}
PRIORITY_MAP = {"Blocker": "P0", "Critical": "P1", "Major": "P2", "Minor": "P3"}

# 规则名称映射
RULE_NAMES = {
    "M-01": "服务拆分合理性", "M-02": "服务间通信效率", "M-03": "数据一致性（共享库）",
    "M-04": "分布式事务缺失", "M-05": "容错熔断缺失", "M-06": "API 网关配置",
    "M-07": "服务注册发现", "M-08": "配置管理", "M-09": "接口幂等性", "M-10": "API 版本管理",
    "Q-01": "代码规范", "Q-02": "安全漏洞", "Q-03": "性能瓶颈", "Q-04": "依赖管理",
    "Q-05": "重复代码", "Q-06": "并发处理", "Q-07": "资源管理",
}

# 规则解决方案与最佳实践映射
RULE_SOLUTIONS = {
    "M-01": ("按 DDD 限界上下文重新划分服务边界，过大服务拆分、过细服务合并",
             "一个微服务对应一个业务子域，命名体现领域"),
    "M-02": ("调用链≥3跳引入聚合/BFF，串行改并行；通知类改消息异步解耦；重构消除循环调用",
             "事件驱动解耦，本地缓存减少跨服务往返"),
    "M-03": ("每个服务独占数据库，跨服务数据通过 API 获取；过渡期建立拆分计划表",
             "Database-per-service 模式"),
    "M-04": ("强一致用 Seata @GlobalTransactional；最终一致用事务消息+本地消息表+幂等",
             "禁止依赖 @Transactional 覆盖跨服务事务"),
    "M-05": ("Feign 配置 fallbackFactory；全局超时；写接口 retries=0；Sentinel 配置熔断规则",
             "降级返回兜底数据而非抛错，保证核心链路可用"),
    "M-06": ("网关 GlobalFilter 鉴权；全局限流；路由最小暴露；CORS 白名单",
             "网关统一鉴权与限流，禁止内部服务裸暴露"),
    "M-07": ("内部服务调用走注册中心服务名，RestTemplate 加 @LoadBalanced",
             "禁止硬编码 IP/直连 url，多环境 namespace 隔离"),
    "M-08": ("敏感配置走配置中心/环境变量/KMS，源码零明文",
             "Nacos 配置加密，pre-commit 钩子拦截明文密钥"),
    "M-09": ("写接口加幂等键（requestId+Redis SETNX）/唯一约束/分布式锁",
             "重试接口必须幂等，否则 retries=0"),
    "M-10": ("对外 API 路径带版本号 /api/v1/xxx，破坏性变更新增版本",
             "旧版本保留一个迭代并标注废弃"),
    "Q-01": ("引入 checkstyle/p3c，CI 强制阻断；全局异常处理；SLF4J 统一",
             "阿里巴巴 Java 开发手册"),
    "Q-02": ("SQL 参数化 #{}；密钥走 KMS；反序列化白名单；升级有漏洞依赖",
             "OWASP Top10 防护清单"),
    "Q-03": ("N+1 改批量查询；循环 DB 提批量操作；大结果集强制分页；IO 异步化",
             "缩小锁粒度，IO 移出临界区"),
    "Q-04": ("BOM 统一版本；CVE 依赖立即升级；scope 规范；生产禁 SNAPSHOT",
             "CI 集成 OWASP Dependency-Check"),
    "Q-05": ("公共逻辑抽取到 common 模块；DTO 转换用 MapStruct；工具类统一沉淀",
             "跨服务重复领域逻辑评估合并"),
    "Q-06": ("用 ThreadPoolExecutor 显式配置；SimpleDateFormat 换 DateTimeFormatter",
             "共享状态用 Atomic/ConcurrentHashMap，锁按统一顺序获取"),
    "Q-07": ("try-with-resources 自动关闭；连接池参数压测调优",
             "HikariCP 池化，禁止裸 new Connection"),
}


def load_json(path):
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return None


def enrich_issue(iss, index):
    """为 issue 补充完整字段"""
    rule_id = iss.get("ruleId", "")
    solution, best_practice = RULE_SOLUTIONS.get(rule_id, ("", ""))
    severity = iss.get("severity", "Major")
    confidence = iss.get("confidence", "high")
    return {
        "issueId": f"ISS-{index:03d}",
        "ruleId": rule_id,
        "ruleName": RULE_NAMES.get(rule_id, ""),
        "severity": severity,
        "dimension": iss.get("category", ""),
        "confidence": confidence,
        "status": "confirmed" if confidence == "high" else "pending",
        "serviceName": iss.get("serviceName", ""),
        "filePath": iss.get("filePath", ""),
        "lineNumber": iss.get("lineNumber", 0),
        "description": iss.get("description", ""),
        "ruleReference": f"{rule_id}: {RULE_NAMES.get(rule_id, '')}",
        "impact": iss.get("impact", ""),
        "solution": iss.get("suggestion", "") or solution,
        "bestPractice": best_practice,
        "priority": PRIORITY_MAP.get(severity, "P3"),
        "estimatedEffort": "高" if severity in ("Blocker", "Critical") else "中",
    }


def build_modification_plan(issues):
    """按规则/服务聚合问题，生成结构化修改计划"""
    plan = []
    # 按 priority -> ruleId 聚合
    grouped = defaultdict(list)
    for iss in issues:
        grouped[(iss["priority"], iss["ruleId"])].append(iss)

    plan_idx = 0
    for (priority, rule_id) in sorted(grouped.keys(), key=lambda x: (["P0", "P1", "P2", "P3"].index(x[0]), x[1])):
        group = grouped[(priority, rule_id)]
        plan_idx += 1
        severity = max((i["severity"] for i in group), key=lambda s: SEVERITY_ORDER[s])
        issue_ids = [i["issueId"] for i in group]
        services = sorted(set(i["serviceName"] for i in group if i["serviceName"])) or ["工程级"]
        solution = RULE_SOLUTIONS.get(rule_id, ("", ""))[0]
        steps = []
        for i, iss in enumerate(group[:5], 1):
            steps.append({
                "step": i,
                "action": iss["solution"][:120],
                "files": [iss["filePath"]] if iss["filePath"] and iss["filePath"] != "N/A" else [],
            })
        plan.append({
            "planId": f"PLAN-{priority}-{plan_idx:02d}",
            "priority": priority,
            "severity": severity,
            "title": f"修复 {rule_id} {RULE_NAMES.get(rule_id, '')} 问题（{len(group)} 处）",
            "issueIds": issue_ids,
            "steps": steps,
            "impactScope": f"涉及服务: {', '.join(services)}",
            "riskAssessment": {
                "riskLevel": "高" if severity in ("Blocker", "Critical") else "中" if severity == "Major" else "低",
                "risks": [f"{severity} 级问题，{RULE_NAMES.get(rule_id, '')}"] + (
                    ["修改期间需保证服务可用，灰度发布"] if severity in ("Blocker", "Critical") else []
                ),
                "mitigation": ["充分测试验证", "灰度发布可回滚", "修改前后数据对账"] if severity in ("Blocker", "Critical") else ["测试验证"],
            },
            "verification": "单元测试 + 集成测试 + 回归验证；架构类问题需联调验证",
            "owner": "待分配",
            "dueDate": "待定",
        })
    return plan


def build_summary(issues):
    by_severity = defaultdict(int)
    by_dimension = defaultdict(int)
    by_rule = defaultdict(int)
    confirmed = 0
    pending = 0
    for iss in issues:
        by_severity[iss["severity"]] += 1
        by_dimension[iss["dimension"]] += 1
        by_rule[iss["ruleId"]] += 1
        if iss["status"] == "confirmed":
            confirmed += 1
        else:
            pending += 1
    return {
        "totalIssues": len(issues),
        "bySeverity": dict(by_severity),
        "byDimension": dict(by_dimension),
        "byRule": dict(by_rule),
        "confirmedCount": confirmed,
        "pendingCount": pending,
    }


def build_report(arch_issues, code_issues, tech_stack, services, call_graph, project_root):
    all_raw = (arch_issues or []) + (code_issues or [])
    issues = [enrich_issue(iss, i+1) for i, iss in enumerate(all_raw)]
    # 按严重级别排序
    issues.sort(key=lambda x: (SEVERITY_ORDER.get(x["severity"], 9), x["ruleId"]))

    summary = build_summary(issues)
    modification_plan = build_modification_plan(issues)

    report_id = hashlib.md5((project_root + str(datetime.now())).encode()).hexdigest()[:12]
    report = {
        "meta": {
            "reportId": report_id,
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
            "toolVersion": "ms-review-toolkit 1.0",
            "ruleVersion": "M/Q 1.0",
            "reviewer": "ms-review-toolkit (脚本+人工复核)",
        },
        "projectInfo": {
            "projectRoot": project_root,
            "buildTool": "Maven" if os.path.isfile(os.path.join(project_root, "pom.xml")) else "Gradle/Unknown",
            "serviceCount": len(services) if services else 0,
            "totalJavaFiles": sum(s.get("javaFileCount", 0) for s in (services or [])),
            "totalLines": sum(s.get("totalLines", 0) for s in (services or [])),
        },
        "techStack": {
            "isMicroservice": tech_stack.get("isMicroservice", True) if tech_stack else None,
            "frameworks": [fw["name"] for fw in tech_stack.get("frameworks", [])] if tech_stack else [],
            "gaps": tech_stack.get("gaps", []) if tech_stack else [],
        } if tech_stack else None,
        "serviceInventory": services[:20] if services else [],
        "callGraph": {"maxDepth": call_graph.get("maxDepth", 0), "cycles": call_graph.get("cycles", [])} if call_graph else None,
        "summary": summary,
        "issues": issues,
        "modificationPlan": modification_plan,
    }
    return report


# ============================================================
# Markdown 报告生成
# ============================================================

def generate_markdown(report):
    lines = []
    m = report["meta"]
    p = report["projectInfo"]
    ts = report["techStack"] or {}
    s = report["summary"]

    lines.append(f"# 微服务架构审查与代码审查报告")
    lines.append("")
    lines.append(f"> 报告ID: `{m['reportId']}` ｜ 生成时间: {m['generatedAt']} ｜ 工具版本: {m['toolVersion']}")
    lines.append("")

    lines.append("## 1. 审查概览")
    lines.append("")
    lines.append("| 项目 | 值 |")
    lines.append("|------|----|")
    lines.append(f"| 工程路径 | {p['projectRoot']} |")
    lines.append(f"| 构建工具 | {p['buildTool']} |")
    lines.append(f"| 服务数 | {p['serviceCount']} |")
    lines.append(f"| Java 文件数 | {p['totalJavaFiles']} |")
    lines.append(f"| 代码总行数 | {p['totalLines']} |")
    is_ms = ts.get("isMicroservice")
    lines.append(f"| 是否微服务工程 | {is_ms if is_ms is not None else '未检测'} |")
    lines.append(f"| 技术栈 | {', '.join(ts.get('frameworks', [])) or '未检测'} |")
    if ts.get("gaps"):
        lines.append(f"| 能力缺口 | {'; '.join(ts['gaps'])} |")
    lines.append(f"| 问题总数 | **{s['totalIssues']}**（已确认 {s['confirmedCount']}，待复核 {s['pendingCount']}）|")
    lines.append("")

    lines.append("### 问题统计（按严重级别）")
    lines.append("")
    lines.append("| 级别 | 数量 | 处理要求 |")
    lines.append("|------|------|----------|")
    for sev in ["Blocker", "Critical", "Major", "Minor"]:
        cnt = s["bySeverity"].get(sev, 0)
        handle = {"Blocker": "立即修复，阻塞上线", "Critical": "本迭代修复", "Major": "下迭代修复", "Minor": "择机修复"}[sev]
        lines.append(f"| **{sev}** | {cnt} | {handle} |")
    lines.append("")

    lines.append("### 问题统计（按维度）")
    lines.append("")
    dim_names = {"architecture": "架构审查", "code-quality": "代码质量"}
    for dim, cnt in s["byDimension"].items():
        lines.append(f"- {dim_names.get(dim, dim)}: {cnt}")
    lines.append("")

    lines.append("## 2. 架构审查结果")
    lines.append("")
    arch_issues = [i for i in report["issues"] if i["dimension"] == "architecture"]
    if arch_issues:
        lines.append("| 编号 | 规则 | 级别 | 服务 | 位置 | 描述 | 置信度 |")
        lines.append("|------|------|------|------|------|------|--------|")
        for iss in arch_issues:
            loc = f"{iss['filePath'].split('/')[-1]}:{iss['lineNumber']}" if iss["filePath"] and iss["filePath"] != "N/A" else "—"
            lines.append(f"| {iss['issueId']} | {iss['ruleId']} | {iss['severity']} | {iss['serviceName'] or '—'} | {loc} | {iss['description'][:50]} | {iss['confidence']} |")
    else:
        lines.append("未发现架构问题。")
    lines.append("")

    if report.get("callGraph"):
        cg = report["callGraph"]
        lines.append(f"### 服务间调用关系（最大调用深度: {cg.get('maxDepth', 0)}）")
        if cg.get("cycles"):
            lines.append(f"⚠️ 检测到循环调用: {cg['cycles']}")
        lines.append("")

    lines.append("## 3. 代码质量审查结果")
    lines.append("")
    code_issues = [i for i in report["issues"] if i["dimension"] == "code-quality"]
    if code_issues:
        lines.append("| 编号 | 规则 | 级别 | 位置 | 描述 | 置信度 |")
        lines.append("|------|------|------|------|------|--------|")
        for iss in code_issues:
            loc = f"{iss['filePath'].split('/')[-1]}:{iss['lineNumber']}" if iss["filePath"] and iss["filePath"] != "N/A" else "—"
            lines.append(f"| {iss['issueId']} | {iss['ruleId']} | {iss['severity']} | {loc} | {iss['description'][:50]} | {iss['confidence']} |")
    else:
        lines.append("未发现代码质量问题。")
    lines.append("")

    lines.append("## 4. 问题详情与解决方案")
    lines.append("")
    for iss in report["issues"]:
        lines.append(f"### {iss['issueId']} [{iss['severity']}] {iss['ruleId']} {iss['ruleName']}")
        lines.append(f"- **位置**: {iss['filePath']}:{iss['lineNumber']}")
        lines.append(f"- **服务**: {iss['serviceName'] or '—'}")
        lines.append(f"- **描述**: {iss['description']}")
        if iss["impact"]:
            lines.append(f"- **影响**: {iss['impact']}")
        lines.append(f"- **置信度**: {iss['confidence']}（{iss['status']}）")
        lines.append(f"- **解决方案**: {iss['solution']}")
        lines.append(f"- **最佳实践**: {iss['bestPractice']}")
        lines.append("")

    lines.append("## 5. 结构化修改计划")
    lines.append("")
    for plan in report["modificationPlan"]:
        lines.append(f"### {plan['planId']} [{plan['priority']}] {plan['title']}")
        lines.append(f"- **严重级别**: {plan['severity']}")
        lines.append(f"- **关联问题**: {', '.join(plan['issueIds'][:5])}{'...' if len(plan['issueIds']) > 5 else ''}")
        lines.append(f"- **影响范围**: {plan['impactScope']}")
        lines.append(f"- **风险等级**: {plan['riskAssessment']['riskLevel']}")
        lines.append(f"- **风险项**: {'; '.join(plan['riskAssessment']['risks'])}")
        lines.append(f"- **缓解措施**: {'; '.join(plan['riskAssessment']['mitigation'])}")
        lines.append(f"- **修改步骤**:")
        for step in plan["steps"]:
            files_str = f" (文件: {', '.join(step['files'])})" if step.get("files") else ""
            lines.append(f"  {step['step']}. {step['action']}{files_str}")
        lines.append(f"- **验证方式**: {plan['verification']}")
        lines.append(f"- **负责人**: {plan['owner']} ｜ **截止**: {plan['dueDate']}")
        lines.append("")

    lines.append("## 6. 修复优先级总览")
    lines.append("")
    lines.append("| 优先级 | 含义 | 处理要求 |")
    lines.append("|--------|------|----------|")
    lines.append("| P0 | Blocker | 立即修复，阻塞上线 |")
    lines.append("| P1 | Critical | 本迭代修复 |")
    lines.append("| P2 | Major | 下迭代修复 |")
    lines.append("| P3 | Minor | 择机修复 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*本报告由 ms-review-toolkit 自动生成，待复核项（confidence=medium/low）需人工确认后计入正式修改计划。*")

    return "\n".join(lines)


# ============================================================
# HTML 报告生成
# ============================================================

def generate_html(report):
    s = report["summary"]
    issues = report["issues"]
    plan = report["modificationPlan"]
    ts = report["techStack"] or {}
    p = report["projectInfo"]
    cg = report.get("callGraph") or {}

    sev_colors = {"Blocker": "#e74c3c", "Critical": "#e67e22", "Major": "#f1c40f", "Minor": "#3498db"}
    sev_text_color = {"Blocker": "#fff", "Critical": "#fff", "Major": "#333", "Minor": "#fff"}

    def sev_badge(sev):
        c = sev_colors.get(sev, "#999")
        tc = sev_text_color.get(sev, "#fff")
        return f'<span class="badge" style="background:{c};color:{tc}">{sev}</span>'

    # 统计柱状条
    sev_total = s["totalIssues"] or 1
    bars = ""
    for sev in ["Blocker", "Critical", "Major", "Minor"]:
        cnt = s["bySeverity"].get(sev, 0)
        pct = cnt / sev_total * 100
        c = sev_colors.get(sev, "#999")
        bars += f'<div class="bar-row"><span class="bar-label">{sev}</span><div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{c}"></div></div><span class="bar-count">{cnt}</span></div>'

    # 问题表格行
    issue_rows = ""
    for iss in issues:
        loc = f'{iss["filePath"].split("/")[-1]}:{iss["lineNumber"]}' if iss["filePath"] and iss["filePath"] != "N/A" else "—"
        issue_rows += f'''<tr>
            <td>{iss["issueId"]}</td><td>{iss["ruleId"]}</td>{sev_badge(iss["severity"])}
            <td>{iss["ruleName"]}</td><td>{iss["serviceName"] or "—"}</td><td class="path">{loc}</td>
            <td class="desc">{iss["description"][:80]}</td>
            <td><span class="conf-{iss["confidence"]}">{iss["confidence"]}</span></td>
            <td class="desc">{iss["solution"][:60]}</td>
        </tr>'''

    # 修改计划卡片
    plan_cards = ""
    for pl in plan:
        steps_html = "".join(f'<li>{st["step"]}. {st["action"]}</li>' for st in pl["steps"])
        plan_cards += f'''<div class="plan-card priority-{pl["priority"].lower()}">
            <h3>{pl["planId"]} <span class="badge" style="background:{sev_colors.get(pl["severity"], "#999")}">{pl["priority"]}</span> {pl["title"]}</h3>
            <p><b>影响范围:</b> {pl["impactScope"]}</p>
            <p><b>风险等级:</b> <span class="risk-{pl['riskAssessment']['riskLevel']}">{pl['riskAssessment']['riskLevel']}</span> — {'; '.join(pl['riskAssessment']['risks'])}</p>
            <p><b>缓解措施:</b> {'; '.join(pl['riskAssessment']['mitigation'])}</p>
            <ol class="steps">{steps_html}</ol>
            <p class="verify"><b>验证:</b> {pl["verification"]}</p>
        </div>'''

    frameworks = ", ".join(ts.get("frameworks", [])) or "未检测"
    gaps_html = "".join(f'<li>{g}</li>' for g in ts.get("gaps", []))
    cycles_html = ""
    if cg.get("cycles"):
        cycles_html = f'<div class="warn">⚠️ 检测到服务间循环调用: {cg["cycles"]}</div>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>微服务架构审查与代码审查报告</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; background:#0f1419; color:#e6e6e6; line-height:1.6; padding:24px; }}
h1 {{ font-size:24px; border-bottom:2px solid #3498db; padding-bottom:10px; margin-bottom:16px; }}
h2 {{ font-size:19px; color:#3498db; margin:28px 0 14px; border-left:4px solid #3498db; padding-left:10px; }}
h3 {{ font-size:15px; margin:12px 0 8px; color:#e6e6e6; }}
.meta {{ color:#888; font-size:13px; margin-bottom:20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:10px; margin-bottom:20px; }}
.stat-card {{ background:#1a2332; border:1px solid #2a3441; border-radius:8px; padding:14px; }}
.stat-card .num {{ font-size:28px; font-weight:bold; color:#3498db; }}
.stat-card .lbl {{ font-size:12px; color:#888; }}
.bar-row {{ display:flex; align-items:center; margin:6px 0; }}
.bar-label {{ width:70px; font-size:13px; }}
.bar-track {{ flex:1; height:20px; background:#1a2332; border-radius:4px; overflow:hidden; margin:0 8px; }}
.bar-fill {{ height:100%; border-radius:4px; }}
.bar-count {{ width:30px; text-align:right; font-weight:bold; }}
table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; }}
th,td {{ border:1px solid #2a3441; padding:8px; text-align:left; vertical-align:top; }}
th {{ background:#1a2332; color:#3498db; font-weight:600; }}
tr:nth-child(even) {{ background:#141a24; }}
td.path, td.desc {{ font-size:12px; color:#aaa; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold; }}
.conf-high {{ color:#2ecc71; font-weight:bold; }}
.conf-medium {{ color:#f1c40f; }}
.conf-low {{ color:#888; }}
.plan-card {{ background:#1a2332; border:1px solid #2a3441; border-radius:8px; padding:16px; margin:12px 0; }}
.priority-p0 {{ border-left:4px solid #e74c3c; }}
.priority-p1 {{ border-left:4px solid #e67e22; }}
.priority-p2 {{ border-left:4px solid #f1c40f; }}
.priority-p3 {{ border-left:4px solid #3498db; }}
.steps {{ margin:8px 0 8px 20px; font-size:13px; }}
.verify {{ font-size:12px; color:#888; border-top:1px dashed #2a3441; padding-top:8px; }}
.warn {{ background:rgba(231,76,60,.15); border:1px solid #e74c3c; color:#e74c3c; padding:10px; border-radius:6px; margin:10px 0; }}
.risk-高 {{ color:#e74c3c; font-weight:bold; }}
.risk-中 {{ color:#f1c40f; font-weight:bold; }}
.risk-低 {{ color:#2ecc71; font-weight:bold; }}
.gaps {{ color:#e67e22; font-size:13px; margin-top:6px; }}
.footer {{ margin-top:30px; padding-top:14px; border-top:1px solid #2a3441; color:#666; font-size:12px; }}
</style>
</head>
<body>
<h1>微服务架构审查与代码审查报告</h1>
<div class="meta">报告ID: <code>{report["meta"]["reportId"]}</code> ｜ 生成时间: {report["meta"]["generatedAt"]} ｜ 工具版本: {report["meta"]["toolVersion"]}</div>

<h2>1. 审查概览</h2>
<div class="grid">
  <div class="stat-card"><div class="num">{p["serviceCount"]}</div><div class="lbl">服务数</div></div>
  <div class="stat-card"><div class="num">{p["totalJavaFiles"]}</div><div class="lbl">Java 文件</div></div>
  <div class="stat-card"><div class="num">{p["totalLines"]}</div><div class="lbl">代码行数</div></div>
  <div class="stat-card"><div class="num" style="color:#e74c3c">{s["totalIssues"]}</div><div class="lbl">问题总数</div></div>
  <div class="stat-card"><div class="num" style="color:#2ecc71">{s["confirmedCount"]}</div><div class="lbl">已确认</div></div>
  <div class="stat-card"><div class="num" style="color:#f1c40f">{s["pendingCount"]}</div><div class="lbl">待复核</div></div>
</div>
<p><b>工程路径:</b> {p["projectRoot"]} ｜ <b>构建工具:</b> {p["buildTool"]} ｜ <b>技术栈:</b> {frameworks} ｜ <b>微服务工程:</b> {ts.get("isMicroservice", "未检测")}</p>
{("<ul class='gaps'>能力缺口:<br>" + gaps_html + "</ul>") if gaps_html else ""}
{cycles_html}

<h2>2. 问题统计（按严重级别）</h2>
{bars}

<h2>3. 问题详情列表</h2>
<table>
<tr><th>编号</th><th>规则</th><th>级别</th><th>规则名</th><th>服务</th><th>位置</th><th>问题描述</th><th>置信度</th><th>解决方案</th></tr>
{issue_rows}
</table>

<h2>4. 结构化修改计划</h2>
{plan_cards if plan_cards else "<p>无修改计划项。</p>"}

<h2>5. 修复优先级说明</h2>
<table>
<tr><th>优先级</th><th>严重级别</th><th>处理要求</th></tr>
<tr><td><span class="badge" style="background:#e74c3c;color:#fff">P0</span></td><td>Blocker</td><td>立即修复，阻塞上线</td></tr>
<tr><td><span class="badge" style="background:#e67e22;color:#fff">P1</span></td><td>Critical</td><td>本迭代修复</td></tr>
<tr><td><span class="badge" style="background:#f1c40f;color:#333">P2</span></td><td>Major</td><td>下迭代修复</td></tr>
<tr><td><span class="badge" style="background:#3498db;color:#fff">P3</span></td><td>Minor</td><td>择机修复</td></tr>
</table>

<div class="footer">本报告由 ms-review-toolkit 自动生成。待复核项（confidence=medium/low）需人工确认后计入正式修改计划，以避免误报。</div>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="Review Report Generator")
    parser.add_argument("--arch", default=None, help="arch-issues.json")
    parser.add_argument("--code", default=None, help="code-issues.json")
    parser.add_argument("--tech", default=None, help="tech-stack.json")
    parser.add_argument("--services", default=None, help="service-inventory.json")
    parser.add_argument("--callgraph", default=None, help="service-call-graph.json")
    parser.add_argument("--project-root", default=".", help="project root path")
    parser.add_argument("--output", "-o", required=True, help="output directory")
    args = parser.parse_args()

    arch_issues = load_json(args.arch) or []
    code_issues = load_json(args.code) or []
    tech_stack = load_json(args.tech)
    services = load_json(args.services)
    call_graph = load_json(args.callgraph)

    report = build_report(arch_issues, code_issues, tech_stack, services, call_graph, args.project_root)

    os.makedirs(args.output, exist_ok=True)
    # JSON 报告
    with open(os.path.join(args.output, "review-report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Written: review-report.json")
    # 独立修改计划
    with open(os.path.join(args.output, "modification-plan.json"), "w", encoding="utf-8") as f:
        json.dump(report["modificationPlan"], f, ensure_ascii=False, indent=2)
    print(f"[INFO] Written: modification-plan.json")
    # Markdown
    with open(os.path.join(args.output, "report.md"), "w", encoding="utf-8") as f:
        f.write(generate_markdown(report))
    print(f"[INFO] Written: report.md")
    # HTML
    with open(os.path.join(args.output, "report.html"), "w", encoding="utf-8") as f:
        f.write(generate_html(report))
    print(f"[INFO] Written: report.html")
    print(f"[INFO] Report generation complete. Total issues: {report['summary']['totalIssues']}")


if __name__ == "__main__":
    main()

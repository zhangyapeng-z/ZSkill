#!/usr/bin/env python3
"""
Report Generator — 生成架构与代码质量检查报告
读取 arch-issues.json 和 code-issues.json，生成 HTML 和 Markdown 格式的分级报告。

用法:
    python generate_report.py --arch <arch-issues.json> --code <code-issues.json> [--project-info <project-info.json>] --output <dir>
"""

import os
import json
import argparse
from datetime import datetime
from collections import defaultdict


SEVERITY_ORDER = {"Blocker": 0, "Critical": 1, "Major": 2, "Minor": 3}
SEVERITY_COLORS = {
    "Blocker": "#dc3545",
    "Critical": "#fd7e14",
    "Major": "#ffc107",
    "Minor": "#6c757d",
}
SEVERITY_ICONS = {
    "Blocker": "🔴",
    "Critical": "🟠",
    "Major": "🟡",
    "Minor": "⚪",
}


def load_json(filepath):
    if not filepath or not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_markdown_report(arch_issues, code_issues, project_info, output_path):
    """生成 Markdown 格式报告"""
    all_issues = arch_issues + code_issues
    all_issues.sort(key=lambda x: SEVERITY_ORDER.get(x.get("severity", "Minor"), 99))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("# 微服务架构规范与代码质量检查报告\n")
    lines.append(f"> 检查时间: {now}\n")
    lines.append(f"> 工程名称: {project_info.get('rootArtifactId', 'N/A')}\n")
    lines.append(f"> 模块数量: {project_info.get('moduleCount', 'N/A')}\n")
    lines.append(f"> 源文件数: {project_info.get('totalJavaFiles', 'N/A')}\n")
    lines.append(f"> 代码行数: {project_info.get('totalLines', 'N/A')}\n")
    lines.append("\n---\n")

    # 1. 问题统计
    lines.append("\n## 一、问题统计\n")
    lines.append("| 严重级别 | 数量 | 说明 |")
    lines.append("|----------|------|------|")
    for sev in ["Blocker", "Critical", "Major", "Minor"]:
        count = sum(1 for i in all_issues if i.get("severity") == sev)
        desc = {
            "Blocker": "阻塞性问题，立即修复",
            "Critical": "严重问题，本迭代修复",
            "Major": "重要问题，下迭代修复",
            "Minor": "次要问题，择机修复",
        }
        lines.append(f"| {sev} | {count} | {desc[sev]} |")
    lines.append(f"| **合计** | **{len(all_issues)}** | |")

    # 2. 架构检查结果
    if arch_issues:
        lines.append("\n## 二、架构检查结果\n")
        by_rule = defaultdict(list)
        for issue in arch_issues:
            by_rule[issue["ruleId"]].append(issue)

        for rule_id in sorted(by_rule.keys()):
            issues = by_rule[rule_id]
            sev = issues[0]["severity"]
            lines.append(f"\n### {rule_id} [{sev}] ({len(issues)} 个问题)\n")
            lines.append(f"**规则:** {issues[0]['ruleReference']}\n")
            for idx, issue in enumerate(issues, 1):
                lines.append(f"\n**问题 {idx}:**")
                lines.append(f"- 文件: `{issue['filePath']}`")
                lines.append(f"- 行号: {issue['lineNumber']}")
                lines.append(f"- 描述: {issue['description']}")
                lines.append(f"- 建议: {issue['suggestion']}")

    # 3. 代码质量检查结果
    if code_issues:
        lines.append("\n## 三、代码质量检查结果\n")
        by_cat = defaultdict(list)
        for issue in code_issues:
            by_cat[issue["category"]].append(issue)

        cat_names = {
            "naming": "命名规范",
            "comments": "注释规范",
            "exception": "异常处理",
            "logging": "日志规范",
            "collections": "集合处理",
            "concurrency": "并发处理",
            "control": "控制语句",
            "oop": "OOP规范",
        }

        for cat in ["naming", "comments", "exception", "logging", "collections", "concurrency", "control", "oop"]:
            if cat not in by_cat:
                continue
            issues = by_cat[cat]
            lines.append(f"\n### {cat_names.get(cat, cat)} ({len(issues)} 个问题)\n")
            lines.append("| # | 级别 | 规则 | 文件 | 行号 | 问题描述 | 修复建议 |")
            lines.append("|---|------|------|------|------|----------|----------|")
            for idx, issue in enumerate(issues, 1):
                short_path = issue["filePath"].split("src/main/java/")[-1] if "src/main/java/" in issue["filePath"] else issue["filePath"]
                lines.append(
                    f"| {idx} | {issue['severity']} | {issue['ruleId']} | "
                    f"`{short_path}` | {issue['lineNumber']} | "
                    f"{issue['description']} | {issue['suggestion']} |"
                )

    # 4. 修复优先级计划
    lines.append("\n## 四、修复优先级计划\n")
    for sev in ["Blocker", "Critical", "Major", "Minor"]:
        count = sum(1 for i in all_issues if i.get("severity") == sev)
        if count == 0:
            continue
        priority = {
            "Blocker": "P0 — 立即修复（阻塞发布）",
            "Critical": "P1 — 本迭代修复",
            "Major": "P2 — 下个迭代修复",
            "Minor": "P3 — 择机修复",
        }
        lines.append(f"\n### {priority[sev]} ({count} 个)\n")
        sev_issues = [i for i in all_issues if i["severity"] == sev]
        for idx, issue in enumerate(sev_issues, 1):
            short_path = issue["filePath"].split("src/main/java/")[-1] if "src/main/java/" in issue["filePath"] else issue["filePath"]
            lines.append(f"{idx}. [{issue['ruleId']}] `{short_path}:{issue['lineNumber']}` — {issue['description']}")

    lines.append("\n---\n")
    lines.append(f"\n*报告生成时间: {now}*\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[INFO] Markdown report: {output_path}")


def generate_html_report(arch_issues, code_issues, project_info, output_path):
    """生成 HTML 格式报告"""
    all_issues = arch_issues + code_issues
    all_issues.sort(key=lambda x: SEVERITY_ORDER.get(x.get("severity", "Minor"), 99))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 统计
    sev_counts = {sev: sum(1 for i in all_issues if i["severity"] == sev) for sev in SEVERITY_ORDER}
    cat_counts = defaultdict(int)
    for i in code_issues:
        cat_counts[i["category"]] += 1

    arch_counts = defaultdict(int)
    for i in arch_issues:
        arch_counts[i["ruleId"]] += 1

    # 构建 HTML
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>架构与代码质量检查报告</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 30px; border-radius: 12px; margin-bottom: 24px; }}
.header h1 {{ font-size: 24px; margin-bottom: 8px; }}
.header .meta {{ font-size: 14px; opacity: 0.9; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
.stat-card {{ background: #fff; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.stat-card .count {{ font-size: 36px; font-weight: 700; }}
.stat-card .label {{ font-size: 14px; color: #666; margin-top: 4px; }}
.section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.section h2 {{ font-size: 18px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #eee; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ background: #f8f9fa; padding: 10px 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #dee2e6; }}
td {{ padding: 10px 12px; border-bottom: 1px solid #eee; vertical-align: top; }}
tr:hover {{ background: #f8f9fa; }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; color: #fff; }}
.badge-Blocker {{ background: {SEVERITY_COLORS['Blocker']}; }}
.badge-Critical {{ background: {SEVERITY_COLORS['Critical']}; }}
.badge-Major {{ background: {SEVERITY_COLORS['Major']}; color: #333; }}
.badge-Minor {{ background: {SEVERITY_COLORS['Minor']}; }}
.file-path {{ font-family: "Consolas", "Monaco", monospace; font-size: 12px; color: #0066cc; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.rule-id {{ font-family: monospace; font-weight: 600; }}
.priority-section {{ margin-bottom: 20px; }}
.priority-header {{ font-size: 16px; font-weight: 700; margin-bottom: 12px; padding: 8px 12px; border-radius: 6px; color: #fff; }}
.priority-P0 {{ background: {SEVERITY_COLORS['Blocker']}; }}
.priority-P1 {{ background: {SEVERITY_COLORS['Critical']}; }}
.priority-P2 {{ background: {SEVERITY_COLORS['Major']}; color: #333; }}
.priority-P3 {{ background: {SEVERITY_COLORS['Minor']}; }}
.footer {{ text-align: center; color: #999; font-size: 12px; padding: 20px; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>微服务架构规范与代码质量检查报告</h1>
  <div class="meta">
    检查时间: {now} &nbsp;|&nbsp;
    工程名称: {project_info.get('rootArtifactId', 'N/A')} &nbsp;|&nbsp;
    模块数量: {project_info.get('moduleCount', 'N/A')} &nbsp;|&nbsp;
    源文件数: {project_info.get('totalJavaFiles', 'N/A')} &nbsp;|&nbsp;
    代码行数: {project_info.get('totalLines', 'N/A')}
  </div>
</div>
""")

    # 统计卡片
    html_parts.append('<div class="stats-grid">')
    for sev in ["Blocker", "Critical", "Major", "Minor"]:
        html_parts.append(f"""<div class="stat-card">
  <div class="count" style="color: {SEVERITY_COLORS[sev]}">{sev_counts[sev]}</div>
  <div class="label">{sev}</div>
</div>""")
    html_parts.append('</div>')

    # 架构检查结果
    if arch_issues:
        html_parts.append('<div class="section"><h2>架构检查结果</h2>')
        html_parts.append('<table><thead><tr><th>规则</th><th>级别</th><th>文件</th><th>行号</th><th>问题描述</th><th>修复建议</th></tr></thead><tbody>')
        for issue in arch_issues:
            html_parts.append(f"""<tr>
  <td class="rule-id">{issue['ruleId']}</td>
  <td><span class="badge badge-{issue['severity']}">{issue['severity']}</span></td>
  <td class="file-path" title="{issue['filePath']}">{issue['filePath']}</td>
  <td>{issue['lineNumber']}</td>
  <td>{issue['description']}</td>
  <td>{issue['suggestion']}</td>
</tr>""")
        html_parts.append('</tbody></table></div>')

    # 代码质量检查结果
    if code_issues:
        cat_names = {
            "naming": "命名规范", "comments": "注释规范", "exception": "异常处理",
            "logging": "日志规范", "collections": "集合处理", "concurrency": "并发处理",
            "control": "控制语句", "oop": "OOP规范",
        }
        for cat in ["naming", "comments", "exception", "logging", "collections", "concurrency", "control", "oop"]:
            cat_issues = [i for i in code_issues if i["category"] == cat]
            if not cat_issues:
                continue
            html_parts.append(f'<div class="section"><h2>{cat_names.get(cat, cat)} ({len(cat_issues)} 个问题)</h2>')
            html_parts.append('<table><thead><tr><th>#</th><th>级别</th><th>规则</th><th>文件</th><th>行号</th><th>问题描述</th><th>修复建议</th></tr></thead><tbody>')
            for idx, issue in enumerate(cat_issues, 1):
                short_path = issue["filePath"].split("src/main/java/")[-1] if "src/main/java/" in issue["filePath"] else issue["filePath"]
                html_parts.append(f"""<tr>
  <td>{idx}</td>
  <td><span class="badge badge-{issue['severity']}">{issue['severity']}</span></td>
  <td class="rule-id">{issue['ruleId']}</td>
  <td class="file-path" title="{issue['filePath']}">{short_path}</td>
  <td>{issue['lineNumber']}</td>
  <td>{issue['description']}</td>
  <td>{issue['suggestion']}</td>
</tr>""")
            html_parts.append('</tbody></table></div>')

    # 修复优先级计划
    html_parts.append('<div class="section"><h2>修复优先级计划</h2>')
    priorities = {
        "Blocker": "P0 — 立即修复（阻塞发布）",
        "Critical": "P1 — 本迭代修复",
        "Major": "P2 — 下个迭代修复",
        "Minor": "P3 — 择机修复",
    }
    p_classes = {"Blocker": "priority-P0", "Critical": "priority-P1", "Major": "priority-P2", "Minor": "priority-P3"}
    for sev in ["Blocker", "Critical", "Major", "Minor"]:
        sev_issues = [i for i in all_issues if i["severity"] == sev]
        if not sev_issues:
            continue
        html_parts.append(f'<div class="priority-section">')
        html_parts.append(f'<div class="priority-header {p_classes[sev]}">{priorities[sev]} ({len(sev_issues)} 个)</div>')
        html_parts.append('<table><thead><tr><th>#</th><th>规则</th><th>文件</th><th>行号</th><th>问题描述</th></tr></thead><tbody>')
        for idx, issue in enumerate(sev_issues, 1):
            short_path = issue["filePath"].split("src/main/java/")[-1] if "src/main/java/" in issue["filePath"] else issue["filePath"]
            html_parts.append(f"""<tr>
  <td>{idx}</td>
  <td class="rule-id">{issue['ruleId']}</td>
  <td class="file-path" title="{issue['filePath']}">{short_path}</td>
  <td>{issue['lineNumber']}</td>
  <td>{issue['description']}</td>
</tr>""")
        html_parts.append('</tbody></table></div>')
    html_parts.append('</div>')

    html_parts.append(f'<div class="footer">报告生成时间: {now} | Arch Quality Checker</div>')
    html_parts.append('</div></body></html>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))
    print(f"[INFO] HTML report: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate architecture and code quality report")
    parser.add_argument("--arch", default=None, help="Path to arch-issues.json")
    parser.add_argument("--code", default=None, help="Path to code-issues.json")
    parser.add_argument("--project-info", default=None, help="Path to project-info.json")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    args = parser.parse_args()

    arch_issues = load_json(args.arch)
    code_issues = load_json(args.code)
    project_info = load_json(args.project_info) or {}

    if not arch_issues and not code_issues:
        print("[WARN] No issues found in either input file.")

    os.makedirs(args.output, exist_ok=True)
    generate_html_report(arch_issues, code_issues, project_info, os.path.join(args.output, "report.html"))
    generate_markdown_report(arch_issues, code_issues, project_info, os.path.join(args.output, "report.md"))
    print("[INFO] Report generation complete.")


if __name__ == "__main__":
    main()

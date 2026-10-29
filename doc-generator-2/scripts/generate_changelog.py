#!/usr/bin/env python3
"""
Changelog Generator — Git Commit History to Structured Changelog
Parses Git commit history and generates a structured changelog in Markdown format.
Supports Conventional Commits and free-form commit messages.

Usage:
    python generate_changelog.py <project-root> [--since <date>] [--until <date>]
                                  [--max-count <n>] [--output <file>] [--format <markdown|json>]

Output:
    CHANGELOG.md  — Structured changelog in Markdown
    (or changelog.json if --format json)
"""

import re
import json
import argparse
import subprocess
from datetime import datetime
from collections import defaultdict, OrderedDict
from pathlib import Path


# ============================================================
# Conventional Commit Parsing
# ============================================================

CONVENTIONAL_PATTERN = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|hotfix|wip|merge|release)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?:"
    r"\s*(?P<description>.+)",
    re.IGNORECASE
)

# Map commit types to changelog sections
TYPE_LABELS = OrderedDict([
    ("feat", "New Features"),
    ("fix", "Bug Fixes"),
    ("hotfix", "Hotfixes"),
    ("perf", "Performance Improvements"),
    ("refactor", "Code Refactoring"),
    ("revert", "Reverts"),
    ("docs", "Documentation"),
    ("style", "Styles"),
    ("test", "Tests"),
    ("build", "Build System"),
    ("ci", "CI/CD"),
    ("chore", "Chores"),
    ("wip", "Work in Progress"),
    ("merge", "Merges"),
    ("release", "Releases"),
])

# ============================================================
# Git Log Retrieval
# ============================================================

def get_git_log(project_root, since=None, until=None, max_count=None, author=None):
    """Retrieve git log entries."""
    project_root = Path(project_root).resolve()

    # Build git log command
    cmd = ["git", "-C", str(project_root), "log",
           "--pretty=format:%H%x1f%an%x1f%ad%x1f%s%x1f%b%x1e",
           "--date=iso"]

    if since:
        cmd.append(f"--since={since}")
    if until:
        cmd.append(f"--until={until}")
    if max_count:
        cmd.append(f"-{max_count}")
    if author:
        cmd.extend(["--author", author])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            print(f"[generate_changelog] Git log command failed: {result.stderr}")
            return []
    except FileNotFoundError:
        print("[generate_changelog] Git not found. Ensure git is installed and in PATH.")
        return []
    except Exception as e:
        print(f"[generate_changelog] Error running git log: {e}")
        return []

    # Parse the custom format output
    commits = []
    raw = result.stdout

    # Split by record separator (0x1e)
    for record in raw.split("\x1e"):
        record = record.strip()
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 5:
            parts.extend([""] * (5 - len(parts)))
        commit = {
            "hash": parts[0].strip(),
            "author": parts[1].strip(),
            "date": parts[2].strip(),
            "subject": parts[3].strip(),
            "body": parts[4].strip(),
        }
        commits.append(commit)

    return commits


def get_git_tags(project_root):
    """Get git tags with dates."""
    project_root = Path(project_root).resolve()
    cmd = ["git", "-C", str(project_root), "log",
           "--tags", "--simplify-by-decoration",
           "--pretty=format:%d%x1f%ad%x1f%H",
           "--date=iso"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except Exception:
        return []

    tags = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\x1f")
        if len(parts) >= 3:
            tag_str = parts[0].strip().strip("()")
            # Parse tag names from "(tag: v1.0.0, tag: v1.0.1)"
            tag_names = re.findall(r"tag:\s*([^,)]+)", tag_str)
            for tn in tag_names:
                tags.append({
                    "tag": tn.strip(),
                    "date": parts[1].strip() if len(parts) > 1 else "",
                    "commit": parts[2].strip() if len(parts) > 2 else "",
                })

    return tags


def get_current_branch(project_root):
    """Get the current git branch."""
    project_root = Path(project_root).resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def get_commit_count(project_root):
    """Get total commit count."""
    project_root = Path(project_root).resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-list", "--count", "HEAD"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return int(result.stdout.strip()) if result.returncode == 0 else 0
    except Exception:
        return 0


# ============================================================
# Commit Classification
# ============================================================

def classify_commit(subject):
    """Classify a commit into a type and scope."""
    # Try conventional commit format
    m = CONVENTIONAL_PATTERN.match(subject)
    if m:
        return {
            "type": m.group("type").lower(),
            "scope": m.group("scope") or "",
            "breaking": bool(m.group("breaking")),
            "description": m.group("description").strip(),
            "conventional": True,
        }

    # Fallback: keyword-based classification
    subject_lower = subject.lower()
    for ctype, _ in TYPE_LABELS.items():
        if ctype in subject_lower:
            return {
                "type": ctype,
                "scope": "",
                "breaking": False,
                "description": subject.strip(),
                "conventional": False,
            }

    # Default: other
    # Check for common keywords
    if any(kw in subject_lower for kw in ["add", "新增", "增加", "添加", "implement", "create"]):
        return {"type": "feat", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}
    if any(kw in subject_lower for kw in ["fix", "修复", "bug", "patch", "hotfix"]):
        return {"type": "fix", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}
    if any(kw in subject_lower for kw in ["update", "更新", "upgrade", "bump", "refactor", "重构"]):
        return {"type": "refactor", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}
    if any(kw in subject_lower for kw in ["doc", "文档", "readme", "comment"]):
        return {"type": "docs", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}
    if any(kw in subject_lower for kw in ["test", "测试"]):
        return {"type": "test", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}
    if any(kw in subject_lower for kw in ["config", "部署", "deploy", "docker", "ci/cd", "jenkins"]):
        return {"type": "build", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}

    return {"type": "other", "scope": "", "breaking": False, "description": subject.strip(), "conventional": False}


# ============================================================
# Group Commits by Date
# ============================================================

def group_commits_by_date(commits):
    """Group commits by date (YYYY-MM-DD)."""
    groups = defaultdict(list)
    for commit in commits:
        date_str = commit.get("date", "")
        # Parse ISO date and extract YYYY-MM-DD
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
        if date_match:
            date_key = date_match.group(1)
        else:
            date_key = "unknown"
        groups[date_key].append(commit)
    return OrderedDict(sorted(groups.items(), reverse=True))


def group_commits_by_type(commits):
    """Group commits by their classified type."""
    groups = defaultdict(list)
    for commit in commits:
        classified = classify_commit(commit["subject"])
        commit["classified"] = classified
        groups[classified["type"]].append(commit)
    return OrderedDict(
        (t, groups[t]) for t in TYPE_LABELS if t in groups
    )


def extract_breaking_changes(commits):
    """Extract breaking change descriptions from commit bodies."""
    breaking = []
    breaking_pattern = re.compile(
        r"BREAKING\s+CHANGE\s*:?\s*(.+?)(?=\n\n|\Z)",
        re.DOTALL | re.IGNORECASE
    )
    for commit in commits:
        classified = commit.get("classified", classify_commit(commit["subject"]))
        if classified["breaking"]:
            breaking.append({
                "hash": commit["hash"][:8],
                "description": classified["description"],
                "subject": commit["subject"],
            })
        # Also check body for BREAKING CHANGE
        body = commit.get("body", "")
        for m in breaking_pattern.finditer(body):
            breaking.append({
                "hash": commit["hash"][:8],
                "description": m.group(1).strip().split("\n")[0],
                "subject": commit["subject"],
            })
    return breaking


# ============================================================
# Markdown Generation
# ============================================================

def generate_markdown_changelog(project_name, commits, tags, branch, total_commits, breaking_changes):
    """Generate structured Markdown changelog."""
    lines = []
    lines.append(f"# Changelog - {project_name}")
    lines.append("")
    lines.append(f"> **Branch:** {branch} | **Total Commits:** {total_commits} | **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Breaking changes summary
    if breaking_changes:
        lines.append("## :rotating_light: Breaking Changes")
        lines.append("")
        for bc in breaking_changes:
            lines.append(f"- **{bc['hash']}**: {bc['description']}")
        lines.append("")

    # Stats summary
    type_counts = defaultdict(int)
    for commit in commits:
        c = commit.get("classified", classify_commit(commit["subject"]))
        type_counts[c["type"]] += 1

    lines.append("## Summary")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for t, label in TYPE_LABELS.items():
        if type_counts.get(t, 0) > 0:
            lines.append(f"| {label} | {type_counts[t]} |")
    if type_counts.get("other", 0) > 0:
        lines.append(f"| Other | {type_counts['other']} |")
    lines.append(f"| **Total** | **{sum(type_counts.values())}** |")
    lines.append("")

    # Group by type
    by_type = group_commits_by_type(commits)
    lines.append("## Changes by Category")
    lines.append("")

    for ctype, label in TYPE_LABELS.items():
        if ctype not in by_type:
            continue
        type_commits = by_type[ctype]
        lines.append(f"### {label} ({len(type_commits)})")
        lines.append("")

        # Group by scope within type
        by_scope = defaultdict(list)
        for c in type_commits:
            scope = c["classified"]["scope"] or "general"
            by_scope[scope].append(c)

        for scope in sorted(by_scope.keys()):
            scope_commits = by_scope[scope]
            if scope != "general":
                lines.append(f"#### `{scope}`")
                lines.append("")
            for c in scope_commits:
                short_hash = c["hash"][:8] if c["hash"] else ""
                desc = c["classified"]["description"]
                author = c.get("author", "")
                date = ""
                date_match = re.match(r"(\d{4}-\d{2}-\d{2})", c.get("date", ""))
                if date_match:
                    date = date_match.group(1)
                lines.append(f"- {desc} ({short_hash}, {author}, {date})")
            lines.append("")

    # Timeline view
    lines.append("---")
    lines.append("")
    lines.append("## Commit Timeline")
    lines.append("")
    by_date = group_commits_by_date(commits)
    for date, date_commits in by_date.items():
        lines.append(f"### {date} ({len(date_commits)} commits)")
        lines.append("")
        for c in date_commits:
            short_hash = c["hash"][:8] if c["hash"] else ""
            subject = c["subject"]
            author = c.get("author", "")
            lines.append(f"- `{short_hash}` {subject} — _{author}_")
        lines.append("")

    # Tags / Releases
    if tags:
        lines.append("---")
        lines.append("")
        lines.append("## Tags / Releases")
        lines.append("")
        lines.append("| Tag | Date | Commit |")
        lines.append("|-----|------|--------|")
        for tag in tags[:50]:
            lines.append(f"| {tag['tag']} | {tag.get('date', '')} | {tag.get('commit', '')[:8]} |")
        lines.append("")

    return "\n".join(lines)


def generate_json_changelog(project_name, commits, tags, branch, total_commits, breaking_changes):
    """Generate JSON format changelog."""
    data = {
        "project": project_name,
        "branch": branch,
        "total_commits": total_commits,
        "generated_at": datetime.now().isoformat(),
        "summary": {},
        "breaking_changes": breaking_changes,
        "changes_by_type": {},
        "timeline": {},
        "tags": tags,
    }

    type_counts = defaultdict(int)
    by_type = defaultdict(list)
    by_date = defaultdict(list)

    for commit in commits:
        c = classify_commit(commit["subject"])
        commit["classified"] = c
        type_counts[c["type"]] += 1
        by_type[c["type"]].append({
            "hash": commit["hash"],
            "description": c["description"],
            "scope": c["scope"],
            "author": commit.get("author", ""),
            "date": commit.get("date", ""),
            "subject": commit["subject"],
        })
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", commit.get("date", ""))
        date_key = date_match.group(1) if date_match else "unknown"
        by_date[date_key].append({
            "hash": commit["hash"],
            "subject": commit["subject"],
            "author": commit.get("author", ""),
        })

    data["summary"] = dict(type_counts)
    data["changes_by_type"] = {k: v for k, v in by_type.items()}
    data["timeline"] = {k: v for k, v in sorted(by_date.items(), reverse=True)}

    return data


# ============================================================
# Main
# ============================================================

def generate_changelog(project_root, since=None, until=None, max_count=None,
                       author=None, output_file=None, fmt="markdown"):
    """Main changelog generation function."""
    project_root = Path(project_root).resolve()
    project_name = project_root.name

    if output_file:
        output_path = Path(output_file)
    else:
        output_dir = project_root / "docs-output"
        output_dir.mkdir(parents=True, exist_ok=True)
        if fmt == "json":
            output_path = output_dir / "changelog.json"
        else:
            output_path = output_dir / "CHANGELOG.md"

    # Get git info
    commits = get_git_log(project_root, since, until, max_count, author)
    tags = get_git_tags(project_root)
    branch = get_current_branch(project_root)
    total_commits = get_commit_count(project_root)

    if not commits:
        print("[generate_changelog] No commits found. Is this a git repository?")
        # Still create an empty changelog
        if fmt == "json":
            data = generate_json_changelog(project_name, [], [], branch, 0, [])
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            content = f"# Changelog - {project_name}\n\n_No git commits found._\n"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
        return

    # Classify commits and extract breaking changes
    breaking_changes = extract_breaking_changes(commits)

    # Generate output
    if fmt == "json":
        data = generate_json_changelog(project_name, commits, tags, branch, total_commits, breaking_changes)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        markdown = generate_markdown_changelog(project_name, commits, tags, branch, total_commits, breaking_changes)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

    print(f"[generate_changelog] Changelog generated: {output_path}")
    print(f"  Project: {project_name}")
    print(f"  Branch: {branch}")
    print(f"  Total commits: {total_commits}")
    print(f"  Commits in changelog: {len(commits)}")
    print(f"  Tags/releases: {len(tags)}")
    print(f"  Breaking changes: {len(breaking_changes)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate changelog from git commit history")
    parser.add_argument("project_root", help="Root directory of the git project")
    parser.add_argument("--since", default=None, help="Start date (e.g., 2024-01-01)")
    parser.add_argument("--until", default=None, help="End date (e.g., 2024-12-31)")
    parser.add_argument("--max-count", type=int, default=None, help="Maximum number of commits")
    parser.add_argument("--author", default=None, help="Filter by author")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format")
    args = parser.parse_args()

    generate_changelog(
        args.project_root,
        since=args.since,
        until=args.until,
        max_count=args.max_count,
        author=args.author,
        output_file=args.output,
        fmt=args.format,
    )

#!/usr/bin/env python3
"""
Code Quality Scanner — 阿里巴巴 Java 开发手册规范检查脚本
扫描 Java 源代码，检查命名规范、注释规范、异常处理、日志规范、集合处理、并发处理、控制语句、OOP 规范。

用法:
    python scan_code_quality.py <project-root> [--output <dir>] [--rules <rule-ids>]

产出文件:
    code-issues.json   — 代码质量问题列表
    rule-summary.json   — 规则检查汇总统计
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict


# ============================================================
# 工具函数
# ============================================================

def read_lines(filepath):
    """读取文件所有行"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read().split("\n")
    except IOError:
        return []


def read_content(filepath):
    """读取文件全部内容"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except IOError:
        return ""


def is_comment(line):
    """判断是否为注释行"""
    stripped = line.strip()
    return stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*")


def is_annotation(line):
    """判断是否为注解行"""
    stripped = line.strip()
    return stripped.startswith("@")


def make_issue(rule_id, severity, category, filepath, line_num, description, rule_ref, suggestion):
    """构造问题对象"""
    return {
        "ruleId": rule_id,
        "severity": severity,
        "category": category,
        "filePath": filepath.replace("\\", "/"),
        "lineNumber": line_num,
        "description": description,
        "ruleReference": rule_ref,
        "suggestion": suggestion,
    }


def find_java_files(project_root):
    """递归查找所有 Java 文件"""
    java_files = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ("target", ".git", "node_modules")]
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(root, f))
    return java_files


def extract_brace_block(lines, start_idx):
    """提取从 start_idx 开始的大括号块内容"""
    depth = 0
    block_lines = []
    started = False
    for i in range(start_idx, min(start_idx + 200, len(lines))):
        for ch in lines[i]:
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
            if started:
                block_lines.append((i, lines[i]))
                if depth == 0:
                    return block_lines
    return block_lines


# ============================================================
# 命名规范检查 [C-01]
# ============================================================

def check_naming(filepath, lines):
    """检查命名规范"""
    issues = []
    CLASS_DECL_RE = re.compile(
        r"\b(public\s+)?(abstract\s+)?(class|interface|enum)\s+(\w+)"
    )
    METHOD_RE = re.compile(r"\b(public|private|protected)\s+(?:static\s+)?(?:final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(")
    VAR_RE = re.compile(r"\b(?:private|public|protected)\s+(?:static\s+)?(?:final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*[;=]")
    CONST_RE = re.compile(r"\b(?:private|public|protected)\s+static\s+final\s+\w+\s+(\w+)\s*=")
    PKG_RE = re.compile(r"\s*package\s+([\w.]+)\s*;")
    EXTENDS_EXCEPTION_RE = re.compile(r"\bextends\s+\w*Exception\b")

    in_class = False
    class_name = None
    is_abstract_class = False
    extends_exception = False

    for i, line in enumerate(lines):
        # N-08: 包名全小写
        m = PKG_RE.match(line)
        if m:
            pkg = m.group(1)
            if pkg != pkg.lower():
                issues.append(make_issue(
                    "N-08", "Major", "naming", filepath, i + 1,
                    f"包名 {pkg} 含大写字母，应全小写",
                    "阿里巴巴Java手册-命名规范: 包名全小写",
                    "将包名改为全小写",
                ))

        # 类声明
        m = CLASS_DECL_RE.search(line)
        if m:
            class_name = m.group(4)
            is_abstract_class = bool(m.group(2))
            in_class = True
            extends_exception = bool(EXTENDS_EXCEPTION_RE.search(line))

            # N-01: 类名 UpperCamelCase
            if not re.match(r"^[A-Z][a-zA-Z0-9]*$", class_name):
                issues.append(make_issue(
                    "N-01", "Major", "naming", filepath, i + 1,
                    f"类名 '{class_name}' 不符合 UpperCamelCase 规范",
                    "阿里巴巴Java手册-命名规范: 类名使用 UpperCamelCase",
                    f"将类名改为 PascalCase 格式",
                ))

            # N-02: 抽象类前缀
            if is_abstract_class and not re.match(r"^(Abstract|Base)", class_name):
                issues.append(make_issue(
                    "N-02", "Major", "naming", filepath, i + 1,
                    f"抽象类 '{class_name}' 应以 Abstract 或 Base 开头",
                    "阿里巴巴Java手册-命名规范: 抽象类以 Abstract 或 Base 开头",
                    f"重命名为 Abstract{class_name} 或 Base{class_name}",
                ))

            # N-03: 异常类后缀
            if extends_exception and not class_name.endswith("Exception"):
                issues.append(make_issue(
                    "N-03", "Major", "naming", filepath, i + 1,
                    f"异常类 '{class_name}' 应以 Exception 结尾",
                    "阿里巴巴Java手册-命名规范: 异常类以 Exception 结尾",
                    f"重命名为 {class_name}Exception",
                ))

        # N-09: boolean 变量不以 is 开头
        m = VAR_RE.search(line)
        if m:
            var_type = m.group(1)
            var_name = m.group(2)
            if var_type == "boolean" and var_name.startswith("is") and not var_name.startswith("isA"):
                issues.append(make_issue(
                    "N-09", "Major", "naming", filepath, i + 1,
                    f"boolean 变量 '{var_name}' 不应以 is 开头",
                    "阿里巴巴Java手册-命名规范: boolean 变量不以 is 开头",
                    f"重命名为 '{var_name[2:]}' 并在 getter 中使用 is 前缀",
                ))

        # N-07: 常量全大写下划线
        m = CONST_RE.search(line)
        if m:
            const_name = m.group(1)
            if not re.match(r"^[A-Z][A-Z0-9_]*$", const_name):
                issues.append(make_issue(
                    "N-07", "Major", "naming", filepath, i + 1,
                    f"常量 '{const_name}' 应全大写、下划线分隔",
                    "阿里巴巴Java手册-命名规范: 常量名全大写、下划线分隔",
                    f"重命名为 {const_name.upper()}",
                ))

    return issues


# ============================================================
# 注释规范检查 [C-02]
# ============================================================

def check_comments(filepath, lines):
    """检查注释规范"""
    issues = []
    CLASS_RE = re.compile(r"\b(public\s+)?(abstract\s+)?(class|interface|enum)\s+\w+")
    PUB_METHOD_RE = re.compile(r"\bpublic\s+(?:static\s+)?(?:\w+(?:<[^>]+>)?\s+)+(\w+)\s*\(")

    for i, line in enumerate(lines):
        # CM-01: 类缺少 Javadoc
        m = CLASS_RE.search(line)
        if m:
            if i > 0 and not lines[i - 1].strip().endswith("*/"):
                # 检查上方多行是否有 Javadoc
                has_javadoc = False
                for j in range(max(0, i - 5), i):
                    if "/**" in lines[j] or "*/" in lines[j]:
                        has_javadoc = True
                        break
                if not has_javadoc:
                    issues.append(make_issue(
                        "CM-01", "Minor", "comments", filepath, i + 1,
                        "类缺少 Javadoc 注释",
                        "阿里巴巴Java手册-注释规范: 类必须有 Javadoc",
                        "添加包含 @author 和功能说明的 Javadoc",
                    ))

        # CM-02: 公有方法缺少 Javadoc
        m = PUB_METHOD_RE.search(line)
        if m and "class " not in line:
            method_name = m.group(1)
            # 跳过 getter/setter/main
            if method_name in ("get", "set", "main", "toString", "equals", "hashCode"):
                continue
            if i > 0 and not lines[i - 1].strip().endswith("*/") and not lines[i - 1].strip().startswith("@"):
                has_javadoc = False
                for j in range(max(0, i - 5), i):
                    if "/**" in lines[j]:
                        has_javadoc = True
                        break
                if not has_javadoc and not is_annotation(lines[i - 1] if i > 0 else ""):
                    issues.append(make_issue(
                        "CM-02", "Minor", "comments", filepath, i + 1,
                        f"公有方法 '{method_name}' 缺少 Javadoc 注释",
                        "阿里巴巴Java手册-注释规范: 公有方法必须有 Javadoc",
                        "添加包含参数、返回值说明的 Javadoc",
                    ))

    # CM-05: TODO/FIXME 格式
    for i, line in enumerate(lines):
        if re.search(r"\b(TODO|FIXME)\b", line):
            if not re.search(r"(TODO|FIXME)\s*\([^)]+\)", line):
                issues.append(make_issue(
                    "CM-05", "Minor", "comments", filepath, i + 1,
                    "TODO/FIXME 注释缺少负责人标注",
                    "阿里巴巴Java手册-注释规范: TODO/FIXME 需标注负责人和时间",
                    "格式: TODO(负责人 2026-01-01): 描述",
                ))

    return issues


# ============================================================
# 异常处理检查 [C-03]
# ============================================================

def check_exception(filepath, lines):
    """检查异常处理规范"""
    issues = []

    for i, line in enumerate(lines):
        # E-01: 捕获 Exception/Throwable 后不处理
        if re.search(r"catch\s*\(\s*(Exception|Throwable)\s+\w+\s*\)", line):
            block = extract_brace_block(lines, i)
            block_text = " ".join(bl[1] for bl in block)
            stripped = block_text.replace("{", "").replace("}", "").strip()
            # 检查是否有实际处理（日志、重抛、注释）
            has_logging = bool(re.search(r"log\.|logger\.", stripped, re.I))
            has_rethrow = "throw" in stripped
            has_comment_only = all(
                bl[1].strip().startswith("//") or bl[1].strip().startswith("*")
                or bl[1].strip() in ("{", "}", "")
                for bl in block
            )
            if has_comment_only or (not has_logging and not has_rethrow and len(stripped) < 20):
                issues.append(make_issue(
                    "E-01", "Critical", "exception", filepath, i + 1,
                    "捕获 Exception/Throwable 后未做任何处理（空 catch 或无日志无重抛）",
                    "阿里巴巴Java手册-异常处理: 禁止捕获异常后不处理",
                    "至少记录日志或重新抛出异常",
                ))

        # E-03: finally 中 return/continue/break
        if re.search(r"\bfinally\s*\{", line):
            block = extract_brace_block(lines, i)
            for bl_idx, bl_line in block:
                if re.search(r"\b(return|continue|break)\b", bl_line) and not is_comment(bl_line):
                    issues.append(make_issue(
                        "E-03", "Critical", "exception", filepath, bl_idx + 1,
                        f"finally 块中使用了 return/continue/break",
                        "阿里巴巴Java手册-异常处理: finally 中禁止 return/continue/break",
                        "移除 finally 中的控制流语句",
                    ))
                    break

        # E-04: throw new RuntimeException
        if re.search(r"throw\s+new\s+RuntimeException\s*\(", line) and not is_comment(line):
            issues.append(make_issue(
                "E-04", "Major", "exception", filepath, i + 1,
                "使用 RuntimeException 替代具体异常，丢失异常语义",
                "阿里巴巴Java手册-异常处理: 禁止用 RuntimeException 替代具体异常",
                "使用具体的业务异常类或自定义异常",
            ))

    return issues


# ============================================================
# 日志规范检查 [C-04]
# ============================================================

def check_logging(filepath, lines):
    """检查日志规范"""
    issues = []
    content = "\n".join(lines)
    has_slf4j = "org.slf4j" in content or "lombok.extern.slf4j" in content

    for i, line in enumerate(lines):
        if is_comment(line):
            continue

        # L-01: 非 SLF4J 日志
        if re.search(r"import\s+org\.apache\.log4j\.", line) or \
           re.search(r"import\s+org\.apache\.logging\.log4j\.", line) or \
           re.search(r"import\s+org\.slf4j\.impl\.", line):
            issues.append(make_issue(
                "L-01", "Major", "logging", filepath, i + 1,
                "使用了非 SLF4J 日志门面",
                "阿里巴巴Java手册-日志规范: 使用 SLF4J 门面",
                "改为使用 org.slf4j.Logger 和 LoggerFactory",
            ))

        # L-02: 日志中使用字符串拼接
        log_call = re.search(r"log\w*\.(debug|info|warn|error)\s*\((.+)\)", line)
        if log_call and '+"' in log_call.group(2) and "{}" not in log_call.group(2):
            issues.append(make_issue(
                "L-02", "Major", "logging", filepath, i + 1,
                "日志中使用字符串拼接而非占位符 {}",
                "阿里巴巴Java手册-日志规范: 使用占位符 {} 而非字符串拼接",
                "改为 log.xxx(\"消息 {}\", variable) 格式",
            ))

        # L-03: ERROR 日志未记录异常堆栈
        error_call = re.search(r"log\w*\.(error)\s*\((.+)\)", line)
        if error_call and error_call.group(1) == "error":
            args = error_call.group(2)
            # 检查是否没有传入 Throwable 参数
            if "e)" not in args and "exception" not in args.lower() and "throwable" not in args.lower() and "ex)" not in args:
                # 可能在下一行有异常参数，简单跳过多行场景
                if not args.endswith(","):
                    issues.append(make_issue(
                        "L-03", "Critical", "logging", filepath, i + 1,
                        "ERROR 日志未记录异常堆栈信息",
                        "阿里巴巴Java手册-日志规范: ERROR 日志需传入异常对象",
                        "添加异常参数: log.error(\"消息\", e)",
                    ))

        # L-05: DEBUG 日志缺少级别判断
        if re.search(r"log\w*\.debug\s*\(", line) and "isDebugEnabled" not in line:
            # 检查前一行是否有 isDebugEnabled
            if i > 0 and "isDebugEnabled" not in lines[i - 1]:
                issues.append(make_issue(
                    "L-05", "Major", "logging", filepath, i + 1,
                    "DEBUG 日志未判断日志级别",
                    "阿里巴巴Java手册-日志规范: DEBUG 日志需判断 isDebugEnabled()",
                    "添加 if (log.isDebugEnabled()) 包裹",
                ))

        # L-06: System.out / System.err
        if re.search(r"System\.(out|err)\.print", line) and not is_comment(line):
            issues.append(make_issue(
                "L-06", "Major", "logging", filepath, i + 1,
                "使用 System.out/err 而非日志框架",
                "阿里巴巴Java手册-日志规范: 禁止 System.out.println",
                "改为使用 SLF4J 日志输出",
            ))

        # L-07: printStackTrace
        if re.search(r"\.printStackTrace\s*\(", line) and not is_comment(line):
            issues.append(make_issue(
                "L-07", "Critical", "logging", filepath, i + 1,
                "使用 e.printStackTrace() 而非日志框架记录",
                "阿里巴巴Java手册-日志规范: 禁止 printStackTrace",
                "改为 log.error(\"异常信息\", e)",
            ))

    return issues


# ============================================================
# 集合处理检查 [C-05]
# ============================================================

def check_collections(filepath, lines):
    """检查集合处理规范"""
    issues = []

    in_foreach = False
    foreach_depth = 0

    for i, line in enumerate(lines):
        if is_comment(line):
            continue

        # CL-01: foreach 中 remove/add
        if re.search(r"for\s*\([^)]*:\s*\w+\s*\)", line):
            in_foreach = True
        if in_foreach:
            if re.search(r"\.(remove|add)\s*\(", line):
                issues.append(make_issue(
                    "CL-01", "Critical", "collections", filepath, i + 1,
                    "在 foreach 循环中对集合执行 remove/add 操作",
                    "阿里巴巴Java手册-集合处理: foreach 中禁止增删元素",
                    "使用 Iterator.remove() 或 Java8 removeIf/filter",
                ))
            if line.strip() == "}":
                in_foreach = False

        # CL-02: size() == 0
        if re.search(r"\.size\(\)\s*==\s*0", line):
            issues.append(make_issue(
                "CL-02", "Major", "collections", filepath, i + 1,
                "使用 size()==0 判断空集合，应使用 isEmpty()",
                "阿里巴巴Java手册-集合处理: 使用 isEmpty() 判断空集合",
                "改为 collection.isEmpty()",
            ))

        # CL-03: Collectors.toMap 缺少 mergeFunction
        if "Collectors.toMap(" in line:
            # 简单检查参数数量（需要3个参数才安全）
            if not re.search(r"Collectors\.toMap\([^,]+,[^,]+,[^,]+", line):
                issues.append(make_issue(
                    "CL-03", "Critical", "collections", filepath, i + 1,
                    "Collectors.toMap 未指定 mergeFunction，可能导致 key 冲突异常",
                    "阿里巴巴Java手册-集合处理: toMap 需指定合并函数",
                    "添加第三个参数: (v1, v2) -> v1",
                ))

        # CL-06: ArrayList 无参构造
        if re.search(r"new\s+ArrayList\s*<[^>]*>\s*\(\s*\)", line):
            issues.append(make_issue(
                "CL-06", "Minor", "collections", filepath, i + 1,
                "ArrayList 初始化未指定容量",
                "阿里巴巴Java手册-集合处理: 集合初始化指定容量",
                "指定预期大小: new ArrayList<>(expectedSize)",
            ))

    return issues


# ============================================================
# 并发处理检查 [C-06]
# ============================================================

def check_concurrency(filepath, lines):
    """检查并发处理规范"""
    issues = []

    for i, line in enumerate(lines):
        if is_comment(line):
            continue

        # CC-01: new Thread()
        if re.search(r"new\s+Thread\s*\(", line):
            issues.append(make_issue(
                "CC-01", "Critical", "concurrency", filepath, i + 1,
                "使用 new Thread() 创建线程，应使用线程池",
                "阿里巴巴Java手册-并发处理: 禁止 new Thread()",
                "使用 ThreadPoolExecutor 创建线程池",
            ))

        # CC-02: Executors 工具类
        if re.search(r"Executors\.(newFixedThreadPool|newCachedThreadPool|newSingleThreadExecutor|newScheduledThreadPool)", line):
            issues.append(make_issue(
                "CC-02", "Critical", "concurrency", filepath, i + 1,
                "使用 Executors 创建线程池，应使用 ThreadPoolExecutor",
                "阿里巴巴Java手册-并发处理: 禁止 Executors 工具类",
                "直接使用 new ThreadPoolExecutor(...) 并指定队列容量和拒绝策略",
            ))

        # CC-03: static SimpleDateFormat
        if re.search(r"static\s+.*SimpleDateFormat", line):
            issues.append(make_issue(
                "CC-03", "Critical", "concurrency", filepath, i + 1,
                "SimpleDateFormat 作为静态变量，线程不安全",
                "阿里巴巴Java手册-并发处理: SimpleDateFormat 线程不安全",
                "使用 DateTimeFormatter 或 ThreadLocal<SimpleDateFormat>",
            ))

        # CC-08: Thread.stop/suspend/resume
        if re.search(r"Thread\.(stop|suspend|resume)\s*\(", line):
            issues.append(make_issue(
                "CC-08", "Critical", "concurrency", filepath, i + 1,
                "使用已废弃的线程控制方法",
                "阿里巴巴Java手册-并发处理: 禁止 Thread.stop/suspend/resume",
                "使用中断机制 (interrupt) 或标志位控制线程",
            ))

    return issues


# ============================================================
# 控制语句检查 [C-07]
# ============================================================

def check_control_statements(filepath, lines):
    """检查控制语句规范"""
    issues = []

    for i, line in enumerate(lines):
        if is_comment(line):
            continue

        # CS-01: 控制语句缺少大括号
        control_match = re.search(r"\b(if|else|for|while|do)\b\s*(\(|\{)", line)
        if control_match:
            keyword = control_match.group(1)
            if keyword in ("if", "else", "for", "while"):
                # 检查是否在同一行或下一行有 {
                rest_of_line = line[control_match.end():]
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                # 简单检查：如果 if/for/while 后面有条件且行尾没有 { 且下一行不是 {
                if keyword != "else":
                    # 查找 ) 后面的内容
                    paren_end = rest_of_line.find(")")
                    if paren_end >= 0:
                        after_paren = rest_of_line[paren_end + 1:].strip()
                        if after_paren and not after_paren.startswith("{") and not after_paren.startswith("//"):
                            issues.append(make_issue(
                                "CS-01", "Major", "control", filepath, i + 1,
                                f"{keyword} 语句未使用大括号",
                                "阿里巴巴Java手册-控制语句: 必须使用大括号",
                                f"为 {keyword} 语句添加大括号",
                            ))
                elif keyword == "else" and "if" not in rest_of_line[:5]:
                    after_else = rest_of_line.strip()
                    if after_else and not after_else.startswith("{") and not after_else.startswith("//"):
                        issues.append(make_issue(
                            "CS-01", "Major", "control", filepath, i + 1,
                            "else 语句未使用大括号",
                            "阿里巴巴Java手册-控制语句: 必须使用大括号",
                            "为 else 语句添加大括号",
                        ))

        # CS-02: 魔法值
        if not is_annotation(line) and not line.strip().startswith("//"):
            # 排除常量定义、import、package
            if not re.search(r"(static\s+final|final\s+static|import|package)", line):
                # 查找数字魔法值（排除 0, 1, -1, 2）
                numbers = re.findall(r"(?<![A-Za-z_\.])(\d{2,})(?![A-Za-z_\.])", line)
                for num in numbers:
                    # 排除注释中的数字
                    code_part = line.split("//")[0]
                    if num in code_part:
                        issues.append(make_issue(
                            "CS-02", "Major", "control", filepath, i + 1,
                            f"魔法值 {num}，建议定义为常量",
                            "阿里巴巴Java手册-控制语句: 禁止魔法值",
                            f"将 {num} 定义为有意义的常量",
                        ))

        # CS-03: switch 缺少 default
        if re.search(r"\bswitch\s*\(", line):
            # 向后搜索找到 switch 块结束
            block = extract_brace_block(lines, i)
            block_text = " ".join(bl[1] for bl in block)
            if "default" not in block_text:
                issues.append(make_issue(
                    "CS-03", "Major", "control", filepath, i + 1,
                    "switch 语句缺少 default 分支",
                    "阿里巴巴Java手册-控制语句: switch 必须有 default",
                    "添加 default 分支处理未知情况",
                ))

    return issues


# ============================================================
# OOP 规范检查 [C-08]
# ============================================================

def check_oop(filepath, lines):
    """检查 OOP 规范"""
    issues = []
    content = "\n".join(lines)
    filename = os.path.basename(filepath)

    # O-03: POJO 类缺少 toString
    has_getter = bool(re.search(r"public\s+\w+\s+get\w+\s*\(", content))
    has_setter = bool(re.search(r"public\s+void\s+set\w+\s*\(", content))
    has_tostring = "toString" in content
    is_pojo = has_getter and has_setter

    if is_pojo and not has_tostring:
        for i, line in enumerate(lines):
            if re.search(r"\bclass\s+\w+", line):
                issues.append(make_issue(
                    "O-03", "Minor", "oop", filepath, i + 1,
                    "POJO 类未重写 toString()",
                    "阿里巴巴Java手册-OOP规范: POJO 类必须重写 toString",
                    "添加 toString() 方法（可用 Lombok @ToString）",
                ))
                break

    # O-05: Serializable 类缺少 serialVersionUID
    if "Serializable" in content and "serialVersionUID" not in content:
        for i, line in enumerate(lines):
            if "implements" in line and "Serializable" in line:
                issues.append(make_issue(
                    "O-05", "Minor", "oop", filepath, i + 1,
                    "Serializable 类缺少 serialVersionUID",
                    "阿里巴巴Java手册-OOP规范: 序列化类需声明 serialVersionUID",
                    "添加 private static final long serialVersionUID = 1L;",
                ))
                break

    for i, line in enumerate(lines):
        if is_comment(line):
            continue

        # O-02: equals 空指针风险
        eq_match = re.search(r"(\w+)\.equals\s*\(", line)
        if eq_match:
            var_name = eq_match.group(1)
            # 如果调用方不是字面量/常量/null/this
            if var_name not in ("this", "super") and not var_name.isupper() and not var_name.startswith('"'):
                # 简单检查前几行是否有 null 判断
                has_null_check = False
                for j in range(max(0, i - 10), i):
                    if re.search(rf"\b{re.escape(var_name)}\s*!=\s*null", lines[j]):
                        has_null_check = True
                        break
                if not has_null_check:
                    issues.append(make_issue(
                        "O-02", "Critical", "oop", filepath, i + 1,
                        f"equals 调用方 '{var_name}' 可能为 null",
                        "阿里巴巴Java手册-OOP规范: equals 使用常量或非null对象调用",
                        "使用 Objects.equals(a, b) 或 常量.equals(变量)",
                    ))

        # O-07: 金额使用 double/float
        if re.search(r"\b(double|float|Double|Float)\s+\w*(amount|price|money|cost|fee|total|balance)", line, re.I):
            issues.append(make_issue(
                "O-07", "Critical", "oop", filepath, i + 1,
                "金额计算使用 double/float，存在精度丢失风险",
                "阿里巴巴Java手册-OOP规范: 金额使用 BigDecimal",
                "改为使用 BigDecimal 类型",
            ))

    return issues


# ============================================================
# 主流程
# ============================================================

CHECKERS = [
    ("命名规范", "naming", check_naming),
    ("注释规范", "comments", check_comments),
    ("异常处理", "exception", check_exception),
    ("日志规范", "logging", check_logging),
    ("集合处理", "collections", check_collections),
    ("并发处理", "concurrency", check_concurrency),
    ("控制语句", "control", check_control_statements),
    ("OOP规范", "oop", check_oop),
]


def scan_code_quality(project_root, output_dir=None):
    """扫描代码质量"""
    project_root = os.path.abspath(project_root)
    print(f"[INFO] Scanning code quality: {project_root}")

    java_files = find_java_files(project_root)
    if not java_files:
        print("[WARN] No Java files found.")
        return None

    print(f"[INFO] Found {len(java_files)} Java files")

    all_issues = []
    rule_stats = defaultdict(lambda: {"count": 0, "severity": "", "category": ""})

    for idx, java_file in enumerate(java_files):
        if (idx + 1) % 50 == 0:
            print(f"[INFO] Processing {idx + 1}/{len(java_files)}...")

        lines = read_lines(java_file)
        for checker_name, category, checker_func in CHECKERS:
            issues = checker_func(java_file, lines)
            for issue in issues:
                all_issues.append(issue)
                rule_stats[issue["ruleId"]]["count"] += 1
                rule_stats[issue["ruleId"]]["severity"] = issue["severity"]
                rule_stats[issue["ruleId"]]["category"] = issue["category"]

    # 按严重级别排序
    severity_order = {"Blocker": 0, "Critical": 1, "Major": 2, "Minor": 3}
    all_issues.sort(key=lambda x: severity_order.get(x["severity"], 99))

    # 汇总统计
    summary = {
        "totalIssues": len(all_issues),
        "bySeverity": {
            "Blocker": sum(1 for i in all_issues if i["severity"] == "Blocker"),
            "Critical": sum(1 for i in all_issues if i["severity"] == "Critical"),
            "Major": sum(1 for i in all_issues if i["severity"] == "Major"),
            "Minor": sum(1 for i in all_issues if i["severity"] == "Minor"),
        },
        "byCategory": {
            cat: sum(1 for i in all_issues if i["category"] == cat)
            for _, cat, _ in CHECKERS
        },
        "byRule": dict(rule_stats),
        "filesScanned": len(java_files),
    }

    print(f"\n[INFO] Scan complete:")
    print(f"  Total issues: {len(all_issues)}")
    for sev, count in summary["bySeverity"].items():
        print(f"  {sev}: {count}")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "code-issues.json"), "w", encoding="utf-8") as f:
            json.dump(all_issues, f, ensure_ascii=False, indent=2)
        with open(os.path.join(output_dir, "rule-summary.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Results written to: {output_dir}")

    return {"issues": all_issues, "summary": summary}


def main():
    parser = argparse.ArgumentParser(
        description="Code Quality Scanner based on Alibaba Java Development Manual"
    )
    parser.add_argument("project_root", help="Path to the project root directory")
    parser.add_argument("--output", "-o", default=None, help="Output directory for results")
    args = parser.parse_args()

    if not os.path.isdir(args.project_root):
        print(f"[ERROR] Project root not found: {args.project_root}")
        return

    scan_code_quality(args.project_root, args.output)


if __name__ == "__main__":
    main()

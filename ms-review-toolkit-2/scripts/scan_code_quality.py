#!/usr/bin/env python3
"""
Code Quality Scanner — 代码质量检查脚本
检查安全漏洞、性能瓶颈、依赖管理、重复代码、代码规范、并发与资源管理（Q-01~Q-07）。

用法:
    python scan_code_quality.py <project-root> [--output <dir>]

产出文件:
    code-issues.json   — 代码质量问题列表（含置信度）
    rule-summary.json  — 规则命中统计
"""

import os
import re
import json
import argparse
import hashlib
from collections import defaultdict
from xml.etree import ElementTree as ET


# ============================================================
# 已知 CVE 依赖版本映射（Q-04）
# ============================================================
KNOWN_CVE_VERSIONS = [
    {"artifactId": "log4j-core", "vulnerableRange": "<2.17.1", "cve": "CVE-2021-44228 Log4Shell RCE", "severity": "Blocker"},
    {"artifactId": "fastjson", "vulnerableRange": "<1.2.83", "cve": "CVE-2022 AutoType RCE", "severity": "Blocker"},
    {"artifactId": "spring-core", "vulnerableRange": "<5.3.20", "cve": "CVE-2022-22965 Spring4Shell", "severity": "Blocker"},
    {"artifactId": "shiro-core", "vulnerableRange": "<1.7.1", "cve": "CVE-2022 认证绕过", "severity": "Blocker"},
    {"artifactId": "jackson-databind", "vulnerableRange": "<2.13", "cve": "CVE 反序列化", "severity": "Critical"},
    {"artifactId": "commons-collections", "vulnerableRange": "<3.2.2", "cve": "CVE-2015-7501 反序列化RCE", "severity": "Blocker"},
    {"artifactId": "snakeyaml", "vulnerableRange": "<1.32", "cve": "CVE-2022 SnakeYAML 反序列化", "severity": "Critical"},
]

# 重复代码检测参数
DUP_BLOCK_LINES = 6
DUP_SIMILARITY = 0.8


def strip_ns(tag):
    if "}" in tag:
        return tag.split("}")[1]
    return tag


def find_java_files(project_root):
    java_files = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ("target", ".git", "node_modules", "test", "build")]
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(root, f))
    return java_files


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except IOError:
        return ""


def is_generated(filepath, content):
    """排除生成代码（@Generated / mapstruct / lombok 生成）"""
    if "@Generated" in content or "GENERATED CODE" in content.upper():
        return True
    if "/target/" in filepath.replace("\\", "/"):
        return True
    if "implements" in content and "Mapper" in content and "@Mapper" in content and "generated" in content.lower():
        return True
    return False


def issue(rule_id, severity, desc, suggestion, confidence="high", **extra):
    d = {
        "ruleId": rule_id, "severity": severity, "category": "code-quality",
        "confidence": confidence, "status": "confirmed" if confidence == "high" else "pending",
        "description": desc, "suggestion": suggestion,
    }
    d.update(extra)
    return d


# ============================================================
# Q-01 代码规范
# ============================================================

def check_naming(filepath, content, lines):
    issues = []
    # 类名 UpperCamelCase
    for i, line in enumerate(lines):
        m = re.search(r'\b(class|interface|enum)\s+(\w+)', line)
        if m:
            name = m.group(2)
            if name != name[0].upper() + name[1:] or "_" in name:
                issues.append(issue("Q-01", "Major",
                    f"类名 {name} 不符合 UpperCamelCase", "类名首字母大写，UpperCamelCase",
                    filePath=filepath, lineNumber=i+1))
            # 抽象类命名
            if "abstract " in line and not (name.startswith("Abstract") or name.startswith("Base")):
                issues.append(issue("Q-01", "Major", "pending",
                    f"抽象类 {name} 未以 Abstract/Base 开头", "抽象类以 Abstract 或 Base 开头",
                    confidence="medium", filePath=filepath, lineNumber=i+1))
    # 常量非全大写
    for i, line in enumerate(lines):
        m = re.search(r'\b(?:static\s+)?final\s+[\w<>]+\s+(\w+)\s*=', line)
        if m and re.match(r'[A-Z_]+', m.group(1)) is None:
            issues.append(issue("Q-01", "Major",
                f"常量 {m.group(1)} 应全大写下划线", "常量全大写下划线 UPPER_SNAKE_CASE",
                filePath=filepath, lineNumber=i+1))
    return issues


def check_exception_handling(filepath, content, lines):
    issues = []
    for i, line in enumerate(lines):
        # 空 catch 块
        if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', content):
            for m in re.finditer(r'catch\s*\([^)]+\)\s*\{\s*\}', content):
                line_no = content[:m.start()].count("\n") + 1
                issues.append(issue("Q-01", "Critical",
                    "空 catch 块，异常被吞没", "记录日志并处理或抛出，禁止空 catch",
                    filePath=filepath, lineNumber=line_no))
            break
        # 仅 printStackTrace
        if "e.printStackTrace()" in line:
            issues.append(issue("Q-01", "Critical",
                "catch 块仅 printStackTrace，未真正处理异常", "用日志记录并抛出业务异常或返回错误码",
                filePath=filepath, lineNumber=i+1))
        # finally 中 return
        if re.match(r'\s*finally\s*\{', line):
            block = content[content.find(line):content.find(line)+500]
            if re.search(r'return\s', block):
                issues.append(issue("Q-01", "Critical",
                    "finally 块中含 return，会覆盖 try 返回值", "finally 中禁止 return/continue/break",
                    filePath=filepath, lineNumber=i+1))
    return issues


def check_logging(filepath, content, lines):
    issues = []
    # System.out
    for i, line in enumerate(lines):
        if "System.out.println" in line or "System.err.println" in line:
            issues.append(issue("Q-01", "Major", "pending",
                "使用 System.out 而非日志门面", "使用 SLF4J 门面", confidence="medium",
                filePath=filepath, lineNumber=i+1))
    # 日志字符串拼接
    for m in re.finditer(r'log\w*\.error\s*\(\s*"([^"]*)"\s*\+', content):
        line_no = content[:m.start()].count("\n") + 1
        issues.append(issue("Q-01", "Major",
            f"ERROR 日志使用字符串拼接: {m.group(0)[:50]}", "日志用占位符 {} 而非拼接",
            filePath=filepath, lineNumber=line_no))
    # ERROR 无异常堆栈
    for m in re.finditer(r'log\w*\.error\s*\(\s*"([^"]*)"\s*\)', content):
        line_no = content[:m.start()].count("\n") + 1
        issues.append(issue("Q-01", "Major", "pending",
            f"ERROR 日志未记录异常堆栈: {m.group(0)[:50]}", "ERROR 日志带异常对象 log.error(\"msg\", e)",
            confidence="medium", filePath=filepath, lineNumber=line_no))
    return issues


# ============================================================
# Q-02 安全漏洞
# ============================================================

def check_security(filepath, content, lines):
    issues = []
    # SQL 注入：MyBatis ${} 拼接（需在 XML 中，这里扫 java 内联 SQL）
    for i, line in enumerate(lines):
        if re.search(r'"select\s+.*\$\{', line, re.IGNORECASE) or re.search(r'"insert\s+.*\$\{', line, re.IGNORECASE):
            issues.append(issue("Q-02", "Blocker",
                f"SQL 拼接用户输入（${{}}）疑似 SQL 注入: {line.strip()[:60]}",
                "SQL 一律参数化 #{}；动态表名用白名单校验",
                filePath=filepath, lineNumber=i+1, impact="SQL 注入可导致数据泄露/篡改"))
    # 硬编码密钥
    for m in re.finditer(r'(?:password|passwd|secret|accessKey|apiKey|privateKey|token)\s*[=:]\s*["\']([^"\']{8,})["\']', content, re.IGNORECASE):
        val = m.group(1)
        if val in ("changeme", "xxxooo", "testtest", "none", "example", "placeholder") or "${" in val:
            continue
        line_no = content[:m.start()].count("\n") + 1
        issues.append(issue("Q-02", "Blocker",
            f"源码硬编码密钥/凭据", "密钥走配置中心/环境变量/KMS，源码零明文",
            filePath=filepath, lineNumber=line_no, impact="密钥泄露导致系统被入侵"))
    # 不安全反序列化
    if "ObjectInputStream" in content and "readObject" in content:
        for i, line in enumerate(lines):
            if "readObject" in line:
                issues.append(issue("Q-02", "Blocker",
                    "ObjectInputStream.readObject 反序列化，疑似 RCE 漏洞",
                    "反序列化用白名单，禁用未受限 readObject",
                    filePath=filepath, lineNumber=i+1, impact="反序列化 RCE"))
    if "JSON.parseObject" in content and "Feature.SupportAutoType" in content:
        issues.append(issue("Q-02", "Blocker",
            "Fastjson 启用 AutoType，疑似 RCE",
            "升级 Fastjson >=1.2.83 并启用 SafeMode，禁用 AutoType",
            filePath=filepath, lineNumber=0, impact="Fastjson AutoType RCE"))
    # SSRF：接收 URL 直接请求
    for i, line in enumerate(lines):
        if re.search(r'restTemplate\.\w+\s*\(\s*\w*[Uu]rl', line) or re.search(r'httpClient\.\w+\s*\(\s*\w*[Uu]rl', line):
            issues.append(issue("Q-02", "Critical", "pending",
                f"接口疑似接收 URL 直接请求（SSRF 风险）: {line.strip()[:60]}",
                "URL 校验协议与目标白名单，禁止访问内网地址", confidence="medium",
                filePath=filepath, lineNumber=i+1, impact="SSRF 可探测/攻击内网"))
    return issues


# ============================================================
# Q-03 性能瓶颈
# ============================================================

def check_performance(filepath, content, lines):
    issues = []
    # N+1 / 循环内 DB 调用
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'(for|while|forEach)', stripped):
            block = "\n".join(lines[i:i+15])
            if re.search(r'(?:mapper|dao|jdbcTemplate|repository)\.\w+\s*\(', block):
                issues.append(issue("Q-03", "Critical",
                    f"循环内调用 DB/DAO，疑似 N+1 查询: 第 {i+1} 行循环",
                    "改为批量查询 selectByIds 一次取回，应用层组装",
                    filePath=filepath, lineNumber=i+1, impact="N 次查询导致慢响应"))
            if "@FeignClient" in content or "feignClient" in content:
                if re.search(r'feignClient\w*\.\w+\s*\(', block):
                    issues.append(issue("Q-03", "Critical",
                        f"循环内调用 Feign，疑似 N+1 远程调用",
                        "改为批量接口，减少跨服务往返",
                        filePath=filepath, lineNumber=i+1))
    # 大结果集未分页
    for m in re.finditer(r'(?:selectList|findAll|list\(\)|selectByExample)\s*\(', content):
        if "Page" not in content and "limit" not in content.lower():
            line_no = content[:m.start()].count("\n") + 1
            issues.append(issue("Q-03", "Critical", "pending",
                f"全量查询无分页: {m.group(0)}",
                "强制分页 PageHelper.startPage，禁绝全表返回", confidence="medium",
                filePath=filepath, lineNumber=line_no, impact="大结果集 OOM/慢响应"))
    # synchronized 锁整个方法且含 IO
    for m in re.finditer(r'synchronized\s*\([^)]*\)\s*\{', content):
        block = content[m.start():m.start()+800]
        if re.search(r'(restTemplate|httpClient|mapper|dao|\.getForObject|\.postForObject)', block):
            line_no = content[:m.start()].count("\n") + 1
            issues.append(issue("Q-03", "Critical",
                f"synchronized 临界区含 IO/远程调用，锁粒度过大",
                "缩小临界区，IO 移出锁；用 ReentrantLock.tryLock 带超时",
                filePath=filepath, lineNumber=line_no, impact="锁持有过久导致并发瓶颈"))
    return issues


# ============================================================
# Q-04 依赖管理
# ============================================================

def find_pom_files(project_root):
    poms = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ("target", ".git", "node_modules")]
        if "pom.xml" in files:
            poms.append(os.path.join(root, "pom.xml"))
    return poms


def parse_pom_dependencies_with_version(pom_path):
    """解析 POM 提取 dependency（含 version）"""
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except ET.ParseError:
        return []
    deps = []
    for child in root:
        if strip_ns(child.tag) == "dependencies":
            for dep in child:
                if strip_ns(dep.tag) == "dependency":
                    info = {}
                    for d in dep:
                        dtag = strip_ns(d.tag)
                        if dtag in ("groupId", "artifactId", "version", "scope"):
                            info[dtag] = d.text.strip() if d.text else None
                    if info.get("artifactId"):
                        deps.append(info)
    return deps


def version_lt(v1, v2):
    """简单版本比较 v1 < v2"""
    def parse(v):
        return tuple(int(x) for x in re.findall(r'\d+', v)[:3]) if v else (0, 0, 0)
    try:
        return parse(v1) < parse(v2)
    except Exception:
        return False


def check_dependencies(project_root):
    issues = []
    all_deps = defaultdict(list)  # artifactId -> [(version, pom)]
    for pom in find_pom_files(project_root):
        for dep in parse_pom_dependencies_with_version(pom):
            all_deps[dep["artifactId"]].append((dep.get("version"), pom.replace("\\", "/")))

    # 版本冲突
    for art, versions in all_deps.items():
        real_versions = [v for v, _ in versions if v and not v.startswith("${")]
        if len(set(real_versions)) > 1:
            issues.append(issue("Q-04", "Major", "pending",
                f"依赖 {art} 存在多个版本: {sorted(set(real_versions))}",
                "用 BOM 统一版本管理，dependency:tree 排查冲突", confidence="medium",
                filePath=versions[0][1], lineNumber=0, impact="版本冲突导致运行时类不一致"))

    # 已知 CVE
    for cve in KNOWN_CVE_VERSIONS:
        if cve["artifactId"] in all_deps:
            for ver, pom in all_deps[cve["artifactId"]]:
                if ver and not ver.startswith("${") and version_lt(ver, cve["vulnerableRange"].replace("<", "")):
                    issues.append(issue("Q-04", cve["severity"],
                        f"依赖 {cve['artifactId']}:{ver} 命中已知漏洞 {cve['cve']}",
                        f"升级 {cve['artifactId']} 到安全版本（{cve['vulnerableRange']} 以上）",
                        filePath=pom, lineNumber=0, impact=cve["cve"]))

    # SNAPSHOT 进生产（粗略：所有显式 SNAPSHOT）
    for art, versions in all_deps.items():
        for ver, pom in versions:
            if ver and "SNAPSHOT" in ver:
                issues.append(issue("Q-04", "Major", "pending",
                    f"依赖 {art}:{ver} 含 SNAPSHOT，不应进生产",
                    "生产禁用 SNAPSHOT，用正式 release 版本", confidence="medium",
                    filePath=pom, lineNumber=0))
    return issues


# ============================================================
# Q-05 重复代码
# ============================================================

def tokenize_lines(content):
    """将代码行转为 token 序列（去除空白与注释）"""
    lines = []
    for line in content.split("\n"):
        line = re.sub(r'//.*$', '', line)
        line = re.sub(r'/\*.*?\*/', '', line)
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("/*") or line.startswith("*"):
            continue
        if line in ("{", "}", "});", ");"):
            continue
        lines.append(line)
    return lines


def line_hash(line):
    """归一化 token 哈希（忽略变量名差异）"""
    norm = re.sub(r'\b[A-Za-z_]\w*\b', 'X', line)
    norm = re.sub(r'\b\d+\b', 'N', norm)
    return hashlib.md5(norm.encode()).hexdigest()


def check_duplicate_code(java_files):
    issues = []
    # 构建所有文件的行哈希索引
    blocks = []  # (file, start_line, hash_seq)
    file_contents = {}
    for fp in java_files:
        content = read_file(fp)
        if is_generated(fp, content):
            continue
        file_contents[fp] = content
        token_lines = tokenize_lines(content)
        content_lines = content.split("\n")
        # 滑动窗口
        for i in range(len(token_lines) - DUP_BLOCK_LINES + 1):
            window = token_lines[i:i+DUP_BLOCK_LINES]
            seq = "".join(line_hash(l) for l in window)
            # 找到窗口在原文件的起始行
            start_line = content_lines.index(token_lines[i]) if token_lines[i] in content_lines else i
            blocks.append((fp, start_line, seq))

    # 哈希碰撞即疑似重复
    seq_map = defaultdict(list)
    for fp, start, seq in blocks:
        seq_map[seq].append((fp, start))

    reported = set()
    for seq, locations in seq_map.items():
        if len(locations) < 2:
            continue
        # 去重同一文件内
        files = set(fp for fp, _ in locations)
        if len(files) < 2:
            continue
        key = tuple(sorted(files))
        if key in reported:
            continue
        reported.add(key)
        first = locations[0]
        issues.append(issue("Q-05", "Major", "pending",
            f"重复代码块（≥{DUP_BLOCK_LINES} 行）跨 {len(files)} 个文件: {', '.join(f.replace(chr(92),'/').split('/')[-1] for f in files)}",
            "公共逻辑抽取到 common 模块；DTO 转换用 MapStruct；工具类统一沉淀",
            confidence="medium", filePath=first[0].replace("\\", "/"), lineNumber=first[1]+1))
    return issues


# ============================================================
# Q-06 并发处理
# ============================================================

def check_concurrency(filepath, content, lines):
    issues = []
    for i, line in enumerate(lines):
        if re.search(r'\bnew\s+Thread\s*\(', line):
            issues.append(issue("Q-06", "Critical",
                "直接 new Thread()，未用线程池",
                "用 ThreadPoolExecutor，明确核心/最大线程数、队列、拒绝策略",
                filePath=filepath, lineNumber=i+1))
        if re.search(r'Executors\.new(Fixed|Cached|Single|Scheduled)ThreadPool', line):
            issues.append(issue("Q-06", "Critical",
                f"使用 {line.strip()[:40]}，无界队列 OOM 风险",
                "用 ThreadPoolExecutor 显式配置，禁用 Executors 工厂方法",
                filePath=filepath, lineNumber=i+1))
        if "static" in line and "SimpleDateFormat" in line:
            issues.append(issue("Q-06", "Critical",
                "SimpleDateFormat 作为静态字段，线程不安全",
                "用 DateTimeFormatter（线程安全）或 ThreadLocal 包装",
                filePath=filepath, lineNumber=i+1))
    return issues


# ============================================================
# Q-07 资源管理
# ============================================================

def check_resource_management(filepath, content, lines):
    issues = []
    # 手动 close 未用 try-with-resources
    for i, line in enumerate(lines):
        if ".close()" in line and "finally" in "\n".join(lines[max(0,i-5):i]):
            issues.append(issue("Q-07", "Critical", "pending",
                "资源在 finally 手动 close，建议 try-with-resources",
                "用 try-with-resources 自动关闭",
                confidence="medium", filePath=filepath, lineNumber=i+1))
    # new RestTemplate 无超时配置
    if "new RestTemplate()" in content:
        issues.append(issue("Q-07", "Critical", "pending",
            "new RestTemplate() 无超时与连接池配置",
            "配置 connectTimeout/readTimeout 与连接池",
            confidence="medium", filePath=filepath, lineNumber=0))
    return issues


# ============================================================
# 主流程
# ============================================================

def scan_code_quality(project_root, output_dir=None):
    project_root = os.path.abspath(project_root)
    print(f"[INFO] Scanning code quality: {project_root}")
    java_files = find_java_files(project_root)
    print(f"[INFO] Found {len(java_files)} Java source files")

    all_issues = []

    # 依赖检查（Q-04）
    all_issues += check_dependencies(project_root)

    # 逐文件检查 Q-01/02/03/06/07
    for fp in java_files:
        content = read_file(fp)
        if is_generated(fp, content):
            continue
        lines = content.split("\n")
        all_issues += check_naming(fp, content, lines)
        all_issues += check_exception_handling(fp, content, lines)
        all_issues += check_logging(fp, content, lines)
        all_issues += check_security(fp, content, lines)
        all_issues += check_performance(fp, content, lines)
        all_issues += check_concurrency(fp, content, lines)
        all_issues += check_resource_management(fp, content, lines)

    # 重复代码（Q-05，需全量索引）
    all_issues += check_duplicate_code(java_files)

    # 统计
    rule_summary = defaultdict(lambda: {"count": 0, "bySeverity": defaultdict(int)})
    for iss in all_issues:
        rule_summary[iss["ruleId"]]["count"] += 1
        rule_summary[iss["ruleId"]]["bySeverity"][iss["severity"]] += 1
    rule_summary = {k: {"count": v["count"], "bySeverity": dict(v["bySeverity"])} for k, v in rule_summary.items()}

    print(f"[INFO] Found {len(all_issues)} code quality issues")
    for iss in all_issues:
        print(f"  [{iss['severity']}|{iss['confidence']}] {iss['ruleId']}: {iss['description'][:80]}")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        write_json(os.path.join(output_dir, "code-issues.json"), all_issues)
        write_json(os.path.join(output_dir, "rule-summary.json"), rule_summary)

    return all_issues


def write_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Written: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Code Quality Scanner (Security/Performance/Dependency/Duplicate)")
    parser.add_argument("project_root", help="Path to project root")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    args = parser.parse_args()
    if not os.path.isdir(args.project_root):
        print(f"[ERROR] Project root not found: {args.project_root}")
        return
    scan_code_quality(args.project_root, args.output)


if __name__ == "__main__":
    main()

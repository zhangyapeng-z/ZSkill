#!/usr/bin/env python3
"""
Architecture Scanner — DDD 分层架构检查脚本
扫描 Maven 多模块工程，检查 DDD 分层规范、模块依赖关系、循环依赖、跨层调用。

用法:
    python scan_architecture.py <project-root> [--check] [--output <dir>]

产出文件:
    project-info.json    — 工程基本信息
    module-tree.json     — 模块树结构
    dep-graph.json       — 模块依赖关系图
    java-file-index.json — Java 源文件索引
    arch-issues.json     — 架构问题列表 (仅 --check 模式)
"""

import os
import re
import json
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict, deque


# ============================================================
# 常量定义
# ============================================================

MAVEN_NS = "http://maven.apache.org/POM/4.0.0"

LAYER_PATTERNS = {
    "controller": [
        r"\.controller\b", r"\.interfaces\b", r"\.web\.controller\b",
        r"\.api\.controller\b",
    ],
    "service": [
        r"\.service\b", r"\.application\b", r"\.app\.service\b",
    ],
    "domain": [
        r"\.domain\b", r"\.model\b", r"\.entity\b", r"\.vo\b",
    ],
    "repository": [
        r"\.repository\b", r"\.mapper\b", r"\.infra\b",
        r"\.infrastructure\b", r"\.dao\b",
    ],
    "dto": [
        r"\.api\.dto\b", r"\.dto\b", r"\.api\.facade\b",
    ],
}

COMMON_MODULE_KEYWORDS = ["common", "core", "base", "shared", "util"]
APP_MODULE_KEYWORDS = ["app", "bootstrap", "starter", "main", "launch"]
BOM_MODULE_KEYWORDS = ["bom", "dependencies", "parent"]

SPRING_ANNOTATIONS = {
    "controller": ["@RestController", "@Controller"],
    "service": ["@Service"],
    "repository": ["@Repository", "@Mapper"],
    "entity": ["@Table", "@Entity", "@TableName"],
}


# ============================================================
# POM 解析
# ============================================================

def strip_ns(tag):
    """移除 XML 命名空间前缀"""
    if "}" in tag:
        return tag.split("}")[1]
    return tag


def parse_pom(pom_path):
    """解析 POM 文件，提取模块、依赖信息"""
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except ET.ParseError:
        return None

    result = {
        "groupId": None,
        "artifactId": None,
        "version": None,
        "packaging": "jar",
        "modules": [],
        "dependencies": [],
        "parent": None,
    }

    for child in root:
        tag = strip_ns(child.tag)
        if tag == "groupId":
            result["groupId"] = child.text.strip() if child.text else None
        elif tag == "artifactId":
            result["artifactId"] = child.text.strip() if child.text else None
        elif tag == "version":
            result["version"] = child.text.strip() if child.text else None
        elif tag == "packaging":
            result["packaging"] = child.text.strip() if child.text else "jar"
        elif tag == "modules":
            for module in child:
                if strip_ns(module.tag) == "module":
                    result["modules"].append(module.text.strip())
        elif tag == "dependencies":
            for dep in child:
                if strip_ns(dep.tag) == "dependency":
                    dep_info = {}
                    for d in dep:
                        dtag = strip_ns(d.tag)
                        if dtag in ("groupId", "artifactId", "version", "scope"):
                            dep_info[dtag] = d.text.strip() if d.text else None
                    if dep_info.get("artifactId"):
                        result["dependencies"].append(dep_info)
        elif tag == "parent":
            parent_info = {}
            for p in child:
                ptag = strip_ns(p.tag)
                if ptag in ("groupId", "artifactId", "version"):
                    parent_info[ptag] = p.text.strip() if p.text else None
            result["parent"] = parent_info

    return result


def find_pom_files(project_root):
    """递归查找所有 pom.xml 文件"""
    pom_files = []
    for root, dirs, files in os.walk(project_root):
        # 跳过 target 目录
        dirs[:] = [d for d in dirs if d != "target" and d != ".git"]
        if "pom.xml" in files:
            pom_files.append(os.path.join(root, "pom.xml"))
    return pom_files


# ============================================================
# Java 文件解析
# ============================================================

def parse_java_file(filepath):
    """解析 Java 文件，提取包名、类名、注解、import"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except IOError:
        return None

    lines = content.split("\n")
    info = {
        "filePath": filepath.replace("\\", "/"),
        "fileName": os.path.basename(filepath),
        "packageName": None,
        "className": None,
        "isInterface": False,
        "isAbstract": False,
        "annotations": [],
        "imports": [],
        "layer": None,
        "lineCount": len(lines),
        "fields": [],
        "methods": [],
    }

    # 提取 package
    for line in lines:
        m = re.match(r"\s*package\s+([\w.]+)\s*;", line)
        if m:
            info["packageName"] = m.group(1)
            break

    # 提取 imports
    for line in lines:
        m = re.match(r"\s*import\s+(?:static\s+)?([\w.*]+)\s*;", line)
        if m:
            info["imports"].append(m.group(1))

    # 提取类/接口声明和注解
    for i, line in enumerate(lines):
        # 收集注解（简单匹配 @ 开头的行）
        ann_match = re.findall(r"@(\w+)", line)
        info["annotations"].extend(ann_match)

        # 类/接口/枚举声明
        class_match = re.search(
            r"\b(public\s+)?(abstract\s+)?(class|interface|enum)\s+(\w+)",
            line,
        )
        if class_match:
            info["className"] = class_match.group(4)
            info["isAbstract"] = bool(class_match.group(2))
            info["isInterface"] = class_match.group(3) == "interface"
            break

    # 判断层归属
    info["layer"] = detect_layer(info)

    return info


def detect_layer(java_info):
    """根据包名和注解判断 Java 文件所属的 DDD 层"""
    pkg = java_info.get("packageName", "") or ""
    annotations = set(java_info.get("annotations", []))

    # 优先通过注解判断
    for ann in annotations:
        for layer, anns in SPRING_ANNOTATIONS.items():
            if ann in anns:
                return layer

    # 通过包名模式匹配
    for layer, patterns in LAYER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, pkg):
                return layer

    return "unknown"


# ============================================================
# 模块分类
# ============================================================

def classify_module(module_name):
    """判断模块类型"""
    name_lower = module_name.lower()

    for kw in COMMON_MODULE_KEYWORDS:
        if kw in name_lower:
            return "common"
    for kw in APP_MODULE_KEYWORDS:
        if kw in name_lower:
            return "app"
    for kw in BOM_MODULE_KEYWORDS:
        if kw in name_lower:
            return "bom"
    return "business"


# ============================================================
# 依赖图构建与循环检测
# ============================================================

def build_dependency_graph(modules):
    """构建模块间依赖关系图"""
    graph = {}
    for module_name, module_info in modules.items():
        deps = []
        for dep in module_info.get("pom", {}).get("dependencies", []):
            dep_artifact = dep.get("artifactId", "")
            # 只记录同工程内的模块依赖
            if dep_artifact in modules:
                deps.append(dep_artifact)
        graph[module_name] = {
            "dependencies": deps,
            "type": module_info.get("type", "business"),
        }
    return graph


def detect_cycles(graph):
    """使用 DFS 检测依赖图中的环"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)

        for neighbor in graph.get(node, {}).get("dependencies", []):
            if neighbor not in graph:
                continue
            if color[neighbor] == GRAY:
                # 发现环
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    for node in graph:
        if color[node] == WHITE:
            dfs(node, [])

    return cycles


# ============================================================
# 架构检查规则
# ============================================================

def check_architecture(project_root, modules, dep_graph, java_index):
    """执行所有架构检查规则"""
    issues = []

    # A-03: 循环依赖检测
    cycles = detect_cycles(dep_graph)
    for cycle in cycles:
        issues.append({
            "ruleId": "A-03",
            "severity": "Blocker",
            "category": "architecture",
            "filePath": "N/A",
            "lineNumber": 0,
            "description": f"循环依赖: {' -> '.join(cycle)}",
            "ruleReference": "DDD分层规范: 模块间不允许循环依赖",
            "suggestion": "提取公共依赖到 common 模块，或引入接口解耦",
        })

    # A-01: DDD 分层完整性
    for module_name, module_info in modules.items():
        if module_info.get("type") in ("bom",):
            continue
        layers_found = set()
        for java_file in module_info.get("javaFiles", []):
            if java_file["layer"] and java_file["layer"] != "unknown":
                layers_found.add(java_file["layer"])

        if module_info.get("type") == "business":
            required = {"service", "repository"}
            missing = required - layers_found
            if missing:
                issues.append({
                    "ruleId": "A-01",
                    "severity": "Blocker",
                    "category": "architecture",
                    "filePath": f"{module_name}/src/main/java/",
                    "lineNumber": 0,
                    "description": f"模块 {module_name} 缺少 DDD 层: {', '.join(missing)}",
                    "ruleReference": "DDD分层规范: 业务模块必须包含 service 和 repository 层",
                    "suggestion": f"检查模块 {module_name} 的包结构，补充缺失的层",
                })

    # A-02: 分层依赖方向检查
    layer_order = {"controller": 0, "dto": 1, "service": 2, "domain": 3, "repository": 4, "unknown": -1}
    for java_file in java_index:
        src_layer = java_file["layer"]
        if src_layer is None or src_layer == "unknown":
            continue
        for imp in java_file.get("imports", []):
            tgt_layer = match_layer_by_import(imp)
            if tgt_layer and tgt_layer != "unknown":
                # DTO 层可被 controller 和 service 引用，不算反向依赖
                if tgt_layer == "dto" and src_layer in ("controller", "service", "dto"):
                    continue
                src_order = layer_order.get(src_layer, -1)
                tgt_order = layer_order.get(tgt_layer, -1)
                if src_order >= 0 and tgt_order >= 0 and tgt_order < src_order:
                    issues.append({
                        "ruleId": "A-02",
                        "severity": "Blocker",
                        "category": "architecture",
                        "filePath": java_file["filePath"],
                        "lineNumber": 0,
                        "description": (
                            f"分层依赖方向违规: {src_layer} 层引用了 {tgt_layer} 层 "
                            f"(import: {imp})"
                        ),
                        "ruleReference": "DDD分层规范: 依赖方向必须 controller → service → domain → repository",
                        "suggestion": "调整依赖方向，通过上层中转或接口隔离",
                    })

    # A-04: 跨层调用检测 (Controller 直接调用 Repository/Mapper)
    for java_file in java_index:
        if java_file["layer"] == "controller":
            for imp in java_file.get("imports", []):
                if re.search(r"\.(mapper|repository|dao)\.\w+", imp):
                    issues.append({
                        "ruleId": "A-04",
                        "severity": "Critical",
                        "category": "architecture",
                        "filePath": java_file["filePath"],
                        "lineNumber": 0,
                        "description": f"Controller 直接引用 Repository/Mapper: {imp}",
                        "ruleReference": "DDD分层规范: Controller 禁止直接调用 Repository/Mapper",
                        "suggestion": "通过 Service 层中转数据访问",
                    })

    # A-05: 公共模块纯净性
    for module_name, module_info in modules.items():
        if module_info.get("type") != "common":
            continue
        # 检查是否依赖了业务模块
        for dep in module_info.get("pom", {}).get("dependencies", []):
            dep_artifact = dep.get("artifactId", "")
            if dep_artifact in modules and modules[dep_artifact].get("type") == "business":
                issues.append({
                    "ruleId": "A-05",
                    "severity": "Critical",
                    "category": "architecture",
                    "filePath": f"{module_name}/pom.xml",
                    "lineNumber": 0,
                    "description": f"公共模块 {module_name} 依赖了业务模块 {dep_artifact}",
                    "ruleReference": "DDD分层规范: common 模块不允许依赖业务模块",
                    "suggestion": f"移除对 {dep_artifact} 的依赖，或将公共代码下沉到 common",
                })
        # 检查是否包含业务注解
        for java_file in module_info.get("javaFiles", []):
            anns = set(java_file.get("annotations", []))
            if anns & {"@Service", "@RestController", "@Controller", "@Mapper"}:
                issues.append({
                    "ruleId": "A-05",
                    "severity": "Critical",
                    "category": "architecture",
                    "filePath": java_file["filePath"],
                    "lineNumber": 0,
                    "description": f"公共模块包含业务组件: {anns & {'@Service', '@RestController', '@Controller', '@Mapper'}}",
                    "ruleReference": "DDD分层规范: common 模块不应包含业务逻辑",
                    "suggestion": "将业务组件移到对应的业务模块中",
                })

    # A-06: 领域模型独立性
    for java_file in java_index:
        if java_file["layer"] == "domain":
            for imp in java_file.get("imports", []):
                if re.search(r"\.(mapper|repository|dao|infra)\.\w+", imp):
                    issues.append({
                        "ruleId": "A-06",
                        "severity": "Critical",
                        "category": "architecture",
                        "filePath": java_file["filePath"],
                        "lineNumber": 0,
                        "description": f"领域模型引用了基础设施层: {imp}",
                        "ruleReference": "DDD分层规范: domain 层不依赖 infrastructure 层",
                        "suggestion": "通过领域服务接口解耦，或使用依赖注入",
                    })

    # A-07: Service 接口隔离 (禁止注入 Impl)
    for java_file in java_index:
        for imp in java_file.get("imports", []):
            if re.search(r"\.impl\.\w+ServiceImpl\b", imp) or imp.endswith("ServiceImpl"):
                issues.append({
                    "ruleId": "A-07",
                    "severity": "Major",
                    "category": "architecture",
                    "filePath": java_file["filePath"],
                    "lineNumber": 0,
                    "description": f"直接引用 Service 实现类: {imp}",
                    "ruleReference": "DDD分层规范: 模块间通过 Service 接口交互",
                    "suggestion": "改为引用 Service 接口，通过 Spring 注入实现类",
                })

    # A-08: Mapper 层隔离
    for java_file in java_index:
        if java_file["layer"] in ("controller",):
            for imp in java_file.get("imports", []):
                if re.search(r"\.mapper\.\w+Mapper\b", imp):
                    issues.append({
                        "ruleId": "A-08",
                        "severity": "Major",
                        "category": "architecture",
                        "filePath": java_file["filePath"],
                        "lineNumber": 0,
                        "description": f"Controller 层直接引用 Mapper: {imp}",
                        "ruleReference": "DDD分层规范: Mapper 接口仅在 Repository 层使用",
                        "suggestion": "通过 Service 层中转数据访问",
                    })

    # A-10: 启动模块单一性
    boot_modules = []
    for module_name, module_info in modules.items():
        for java_file in module_info.get("javaFiles", []):
            if "@SpringBootApplication" in java_file.get("annotations", []):
                boot_modules.append((module_name, java_file["filePath"]))

    if len(boot_modules) > 1:
        for mod, path in boot_modules:
            issues.append({
                "ruleId": "A-10",
                "severity": "Critical",
                "category": "architecture",
                "filePath": path,
                "lineNumber": 0,
                "description": f"模块 {mod} 包含 @SpringBootApplication，工程中存在多个启动类",
                "ruleReference": "DDD分层规范: 仅 app 模块包含启动类",
                "suggestion": "移除多余的启动类，统一使用 app 模块启动",
            })

    return issues


def match_layer_by_import(import_path):
    """根据 import 路径判断所属层"""
    for layer, patterns in LAYER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, import_path):
                return layer
    return None


# ============================================================
# 主流程
# ============================================================

def scan_project(project_root, output_dir=None, do_check=False):
    """扫描工程并输出结果"""
    project_root = os.path.abspath(project_root)
    print(f"[INFO] Scanning project: {project_root}")

    # 1. 查找所有 POM 文件
    pom_files = find_pom_files(project_root)
    if not pom_files:
        print("[ERROR] No pom.xml found. Is this a Maven project?")
        return None

    # 2. 解析所有 POM
    modules = {}
    root_pom = parse_pom(os.path.join(project_root, "pom.xml"))
    root_groupId = root_pom["groupId"] if root_pom else None

    for pom_file in pom_files:
        pom_info = parse_pom(pom_file)
        if not pom_info or not pom_info["artifactId"]:
            continue

        module_name = pom_info["artifactId"]
        module_dir = os.path.dirname(pom_file)
        module_type = classify_module(module_name)

        # 收集 Java 文件
        java_files = []
        java_src_dir = os.path.join(module_dir, "src", "main", "java")
        if os.path.isdir(java_src_dir):
            for root, dirs, files in os.walk(java_src_dir):
                for f in files:
                    if f.endswith(".java"):
                        java_info = parse_java_file(os.path.join(root, f))
                        if java_info:
                            java_files.append(java_info)

        modules[module_name] = {
            "pom": pom_info,
            "path": module_dir.replace("\\", "/"),
            "type": module_type,
            "javaFiles": java_files,
            "javaFileCount": len(java_files),
        }

    # 3. 构建依赖图
    dep_graph = build_dependency_graph(modules)

    # 4. 构建 Java 文件索引
    java_index = []
    for module_name, module_info in modules.items():
        java_index.extend(module_info["javaFiles"])

    # 5. 汇总工程信息
    project_info = {
        "projectRoot": project_root.replace("\\", "/"),
        "buildTool": "Maven",
        "rootArtifactId": root_pom["artifactId"] if root_pom else None,
        "rootGroupId": root_groupId,
        "rootVersion": root_pom["version"] if root_pom else None,
        "moduleCount": len(modules),
        "totalJavaFiles": len(java_index),
        "totalLines": sum(j["lineCount"] for j in java_index),
    }

    # 6. 构建模块树
    module_tree = {
        m: {
            "type": info["type"],
            "path": info["path"],
            "javaFileCount": info["javaFileCount"],
            "dependencies": dep_graph.get(m, {}).get("dependencies", []),
            "layers": sorted(set(
                j["layer"] for j in info["javaFiles"]
                if j["layer"] and j["layer"] != "unknown"
            )),
        }
        for m, info in modules.items()
    }

    # 7. 输出
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        write_json(os.path.join(output_dir, "project-info.json"), project_info)
        write_json(os.path.join(output_dir, "module-tree.json"), module_tree)
        write_json(os.path.join(output_dir, "dep-graph.json"), dep_graph)
        write_json(os.path.join(output_dir, "java-file-index.json"), java_index)

    # 8. 架构检查
    if do_check:
        print("[INFO] Running architecture checks...")
        issues = check_architecture(project_root, modules, dep_graph, java_index)
        if output_dir:
            write_json(os.path.join(output_dir, "arch-issues.json"), issues)
        print(f"[INFO] Found {len(issues)} architecture issues")
        for issue in issues:
            print(f"  [{issue['severity']}] {issue['ruleId']}: {issue['description']}")

    print("[INFO] Scan complete.")
    return {
        "projectInfo": project_info,
        "moduleTree": module_tree,
        "depGraph": dep_graph,
        "javaIndex": java_index,
    }


def write_json(filepath, data):
    """写入 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Written: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="DDD Architecture Scanner for Maven multi-module projects"
    )
    parser.add_argument("project_root", help="Path to the project root directory")
    parser.add_argument("--check", action="store_true", help="Run architecture checks")
    parser.add_argument("--output", "-o", default=None, help="Output directory for results")
    args = parser.parse_args()

    if not os.path.isdir(args.project_root):
        print(f"[ERROR] Project root not found: {args.project_root}")
        return

    scan_project(args.project_root, args.output, args.check)


if __name__ == "__main__":
    main()

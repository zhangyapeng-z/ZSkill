#!/usr/bin/env python3
"""
Project Scanner — Microservice Project Info Extractor
Scans Maven/Gradle multi-module projects, extracts project basics,
module tree, tech stack, config items, and source structure summary.

Usage:
    python scan_project.py <project-root> [--modules <m1,m2,...>] [--output <dir>]

Outputs:
    project-info.json     — project basic info (build tool, modules, tech stack, version)
    module-tree.json       — module tree structure
    config-items.json      — extracted configuration items
    source-summary.json    — source code structure summary (packages, key classes)
    tech-stack.json        — detected tech stack and frameworks
"""

import os
import re
import json
import argparse
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict, Counter

MAVEN_NS = "http://maven.apache.org/POM/4.0.0"

# ============================================================
# POM Parsing
# ============================================================

def strip_ns(tag):
    if "}" in tag:
        return tag.split("}")[1]
    return tag

def find_all_elements(root, tag_name):
    result = root.findall(f".//{{{MAVEN_NS}}}{tag_name}")
    if not result:
        result = root.findall(f".//{tag_name}")
    return result

def parse_pom(pom_path):
    """Parse a POM file, extract key information."""
    info = {
        "groupId": "",
        "artifactId": "",
        "version": "",
        "packaging": "",
        "name": "",
        "description": "",
        "parent": {},
        "modules": [],
        "dependencies": [],
        "properties": {},
        "build_plugins": [],
        "profiles": [],
    }
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except ET.ParseError:
        return info

    def get_text(elem, tag):
        child = elem.find(tag)
        if child is not None and child.text:
            return child.text.strip()
        return ""

    info["groupId"] = get_text(root, f"{{{MAVEN_NS}}}groupId") or get_text(root, "groupId")
    info["artifactId"] = get_text(root, f"{{{MAVEN_NS}}}artifactId") or get_text(root, "artifactId")
    info["version"] = get_text(root, f"{{{MAVEN_NS}}}version") or get_text(root, "version")
    info["packaging"] = get_text(root, f"{{{MAVEN_NS}}}packaging") or get_text(root, "packaging") or "jar"
    info["name"] = get_text(root, f"{{{MAVEN_NS}}}name") or get_text(root, "name")
    info["description"] = get_text(root, f"{{{MAVEN_NS}}}description") or get_text(root, "description")

    parent_elem = root.find(f"{{{MAVEN_NS}}}parent")
    if parent_elem is None:
        parent_elem = root.find("parent")
    if parent_elem is not None:
        info["parent"] = {
            "groupId": get_text(parent_elem, f"{{{MAVEN_NS}}}groupId") or get_text(parent_elem, "groupId"),
            "artifactId": get_text(parent_elem, f"{{{MAVEN_NS}}}artifactId") or get_text(parent_elem, "artifactId"),
            "version": get_text(parent_elem, f"{{{MAVEN_NS}}}version") or get_text(parent_elem, "version"),
        }

    modules = root.findall(f"{{{MAVEN_NS}}}modules/{{{MAVEN_NS}}}module")
    if not modules:
        modules = root.findall("modules/module")
    info["modules"] = [m.text.strip() for m in modules if m.text]

    props = root.find(f"{{{MAVEN_NS}}}properties")
    if props is None:
        props = root.find("properties")
    if props is not None:
        for prop in props:
            tag = strip_ns(prop.tag)
            if prop.text:
                info["properties"][tag] = prop.text.strip()

    deps = find_all_elements(root, "dependency")
    for dep in deps:
        info["dependencies"].append({
            "groupId": get_text(dep, f"{{{MAVEN_NS}}}groupId") or get_text(dep, "groupId"),
            "artifactId": get_text(dep, f"{{{MAVEN_NS}}}artifactId") or get_text(dep, "artifactId"),
            "version": get_text(dep, f"{{{MAVEN_NS}}}version") or get_text(dep, "version"),
            "scope": get_text(dep, f"{{{MAVEN_NS}}}scope") or get_text(dep, "scope"),
        })

    plugins = root.findall(f".//{{{MAVEN_NS}}}plugin")
    if not plugins:
        plugins = root.findall(".//plugin")
    for plugin in plugins:
        gid = get_text(plugin, f"{{{MAVEN_NS}}}groupId") or get_text(plugin, "groupId")
        aid = get_text(plugin, f"{{{MAVEN_NS}}}artifactId") or get_text(plugin, "artifactId")
        if gid or aid:
            info["build_plugins"].append({"groupId": gid, "artifactId": aid})

    profiles = root.findall(f"{{{MAVEN_NS}}}profiles/{{{MAVEN_NS}}}profile")
    if not profiles:
        profiles = root.findall("profiles/profile")
    for prof in profiles:
        pid = get_text(prof, f"{{{MAVEN_NS}}}id") or get_text(prof, "id")
        if pid:
            info["profiles"].append(pid)

    return info


def parse_gradle(gradle_path):
    """Parse a build.gradle file for basic info."""
    info = {
        "group": "", "version": "", "name": "", "description": "",
        "dependencies": [], "plugins": [], "subprojects": [],
    }
    try:
        content = gradle_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return info

    m = re.search(r"group\s*=\s*['\"]([^'\"]+)['\"]", content)
    if m:
        info["group"] = m.group(1)
    m = re.search(r"version\s*=\s*['\"]([^'\"]+)['\"]", content)
    if m:
        info["version"] = m.group(1)

    for m in re.finditer(r"implementation\s+['\"]([^:]+):([^:]+):([^'\"]+)['\"]", content):
        info["dependencies"].append({"groupId": m.group(1), "artifactId": m.group(2), "version": m.group(3), "scope": "implementation"})
    for m in re.finditer(r"(?:testImplementation|testCompile)\s+['\"]([^:]+):([^:]+):([^'\"]+)['\"]", content):
        info["dependencies"].append({"groupId": m.group(1), "artifactId": m.group(2), "version": m.group(3), "scope": "test"})

    for m in re.finditer(r"include\s+['\"]([^'\"]+)['\"]", content):
        info["subprojects"].append(m.group(1))

    for m in re.finditer(r"id\s+['\"]([^'\"]+)['\"]\s*(?:version\s+['\"]([^'\"]+)['\"])?", content):
        info["plugins"].append({"id": m.group(1), "version": m.group(2) or ""})

    return info


# ============================================================
# Tech Stack Detection
# ============================================================

TECH_STACK_RULES = {
    "Spring Boot": {
        "pom_keywords": ["spring-boot-starter", "spring-boot-dependencies", "spring-boot-maven-plugin"],
        "gradle_keywords": ["org.springframework.boot", "spring-boot-starter"],
        "file_hints": ["application.yml", "application.properties", "bootstrap.yml"],
    },
    "Spring Cloud": {
        "pom_keywords": ["spring-cloud-starter", "spring-cloud-dependencies"],
        "gradle_keywords": ["spring-cloud-starter"],
    },
    "Spring Cloud Alibaba": {
        "pom_keywords": ["spring-cloud-alibaba", "nacos", "sentinel", "seata", "dubbo"],
    },
    "MyBatis": {
        "pom_keywords": ["mybatis", "mybatis-spring", "mybatis-plus", "mybatis-spring-boot-starter"],
        "file_hints": ["mapper.xml", "mybatis-config.xml"],
    },
    "MyBatis-Plus": {
        "pom_keywords": ["mybatis-plus", "mybatis-plus-boot-starter"],
    },
    "JPA/Hibernate": {
        "pom_keywords": ["hibernate-core", "spring-data-jpa", "jpa"],
    },
    "Redis": {
        "pom_keywords": ["spring-boot-starter-data-redis", "jedis", "lettuce", "redisson"],
        "config_keywords": ["redis"],
    },
    "Kafka": {
        "pom_keywords": ["kafka", "spring-kafka"],
        "config_keywords": ["kafka"],
    },
    "RabbitMQ": {
        "pom_keywords": ["spring-boot-starter-amqp", "rabbitmq"],
        "config_keywords": ["rabbitmq"],
    },
    "RocketMQ": {
        "pom_keywords": ["rocketmq", "rocketmq-spring-boot-starter"],
        "config_keywords": ["rocketmq"],
    },
    "Elasticsearch": {
        "pom_keywords": ["elasticsearch", "spring-data-elasticsearch"],
        "config_keywords": ["elasticsearch"],
    },
    "MongoDB": {
        "pom_keywords": ["spring-boot-starter-data-mongodb", "mongodb"],
        "config_keywords": ["mongodb"],
    },
    "Feign": {
        "pom_keywords": ["spring-cloud-starter-openfeign", "feign"],
        "source_keywords": ["@FeignClient"],
    },
    "gRPC": {
        "pom_keywords": ["grpc", "grpc-spring-boot-starter"],
    },
    "Dubbo": {
        "pom_keywords": ["dubbo-spring-boot-starter", "dubbo"],
    },
    "Swagger/OpenAPI": {
        "pom_keywords": ["springfox", "springdoc", "swagger"],
    },
    "Lombok": {
        "pom_keywords": ["lombok"],
    },
    "MapStruct": {
        "pom_keywords": ["mapstruct"],
    },
    "Hutool": {
        "pom_keywords": ["hutool"],
    },
    "ShardingSphere": {
        "pom_keywords": ["shardingsphere", "sharding-jdbc"],
    },
    "Spring Security": {
        "pom_keywords": ["spring-security", "spring-boot-starter-security"],
    },
    "JWT": {
        "pom_keywords": ["jjwt", "java-jwt", "auth0"],
    },
    "Docker": {
        "file_hints": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    },
    "Kubernetes": {
        "file_hints": ["k8s", "kubernetes", "values.yaml", "Chart.yaml", "deployment.yaml"],
    },
    "Helm Chart": {
        "file_hints": ["Chart.yaml", "values.yaml"],
    },
}


def detect_tech_stack(project_root, all_deps, config_content, source_keywords_counter):
    """Detect tech stack from dependencies, config files, and source code."""
    detected = []
    all_dep_str = " ".join(
        f"{d.get('groupId', '')}:{d.get('artifactId', '')}" for d in all_deps
    ).lower()

    for tech, rules in TECH_STACK_RULES.items():
        matched = False
        evidence = []

        for kw in rules.get("pom_keywords", []):
            if kw.lower() in all_dep_str:
                matched = True
                evidence.append(f"dependency: {kw}")

        for kw in rules.get("gradle_keywords", []):
            if kw.lower() in all_dep_str:
                matched = True
                evidence.append(f"gradle: {kw}")

        for kw in rules.get("config_keywords", []):
            if kw.lower() in config_content.lower():
                matched = True
                evidence.append(f"config: {kw}")

        for kw in rules.get("source_keywords", []):
            if source_keywords_counter.get(kw, 0) > 0:
                matched = True
                evidence.append(f"source: {kw} ({source_keywords_counter[kw]} occurrences)")

        for hint in rules.get("file_hints", []):
            for f in project_root.rglob("*"):
                if hint.lower() in f.name.lower():
                    matched = True
                    evidence.append(f"file: {f.name}")
                    break

        if matched:
            detected.append({"technology": tech, "evidence": evidence})

    return detected


# ============================================================
# Config Extraction
# ============================================================

def find_config_files(project_root, module_filter=None):
    """Find application.yml/yaml/properties files."""
    config_files = []
    patterns = [
        "application*.yml", "application*.yaml",
        "application*.properties", "bootstrap*.yml", "bootstrap*.yaml",
    ]
    for pattern in patterns:
        for f in project_root.rglob(pattern):
            if "target" in f.parts or "build" in f.parts:
                continue
            if module_filter and not any(mf in str(f) for mf in module_filter):
                continue
            config_files.append(f)
    return config_files


def parse_yaml_config(content):
    """Simple YAML config parser for key-value extraction."""
    items = []
    current_path = []
    in_list = False
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("---"):
            current_path = []
            continue
        indent = len(line) - len(line.lstrip())
        level = indent // 2
        current_path = current_path[:level]

        if stripped.startswith("- "):
            val = stripped[2:].strip()
            items.append({
                "path": ".".join(current_path),
                "value": val,
                "type": "list_item",
            })
            continue

        if ":" in stripped:
            parts = stripped.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip() if len(parts) > 1 else ""
            current_path.append(key)
            full_path = ".".join(current_path)
            if val and not val.startswith("${"):
                items.append({"path": full_path, "value": val, "type": "value"})
            elif val.startswith("${"):
                items.append({"path": full_path, "value": val, "type": "placeholder"})
            else:
                items.append({"path": full_path, "value": "", "type": "section"})
    return items


def parse_properties_config(content):
    """Parse .properties config file."""
    items = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        if "=" in line:
            parts = line.split("=", 1)
        elif ":" in line:
            parts = line.split(":", 1)
        else:
            continue
        key = parts[0].strip()
        val = parts[1].strip() if len(parts) > 1 else ""
        items.append({"path": key, "value": val, "type": "value"})
    return items


def extract_config_items(project_root, module_filter=None):
    """Extract configuration items from config files."""
    config_files = find_config_files(project_root, module_filter)
    all_items = []
    file_summaries = []

    for cf in config_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel_path = str(cf.relative_to(project_root))
        if cf.suffix in (".yml", ".yaml"):
            items = parse_yaml_config(content)
        else:
            items = parse_properties_config(content)

        file_summaries.append({"file": rel_path, "item_count": len(items)})
        all_items.extend(items)

    return all_items, file_summaries


# ============================================================
# Source Code Analysis
# ============================================================

SPRING_ANNOTATIONS = {
    "RestController": [r"@RestController", r"@Controller"],
    "Service": [r"@Service"],
    "Repository": [r"@Repository", r"@Mapper"],
    "Configuration": [r"@Configuration"],
    "FeignClient": [r"@FeignClient"],
    "Component": [r"@Component"],
    "Entity": [r"@Entity", r"@TableName", r"@Table"],
    "Scheduled": [r"@Scheduled"],
    "RestControllerAdvice": [r"@RestControllerAdvice"],
}

PACKAGE_LAYER_PATTERNS = {
    "controller": [r"\.controller\b", r"\.api\b", r"\.web\b", r"\.interfaces\b"],
    "service": [r"\.service\b", r"\.application\b"],
    "domain": [r"\.domain\b", r"\.model\b", r"\.entity\b"],
    "repository": [r"\.repository\b", r"\.mapper\b", r"\.infrastructure\b", r"\.infra\b"],
    "config": [r"\.config\b", r"\.configuration\b"],
    "dto": [r"\.dto\b", r"\.vo\b", r"\.request\b", r"\.response\b"],
}


def scan_source_files(project_root, module_filter=None):
    """Scan Java source files for structural summary."""
    java_files = []
    keywords_counter = Counter()
    package_layers = defaultdict(lambda: defaultdict(int))
    key_classes = []
    import_patterns = defaultdict(list)

    src_dirs = list(project_root.rglob("src/main/java"))
    if not src_dirs:
        src_dirs = list(project_root.rglob("src"))

    for src_dir in src_dirs:
        if "target" in str(src_dir) or "build" in str(src_dir):
            continue
        if module_filter and not any(mf in str(src_dir) for mf in module_filter):
            continue

        for java_file in src_dir.rglob("*.java"):
            try:
                content = java_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            rel_path = str(java_file.relative_to(project_root))
            lines = content.splitlines()
            file_info = {
                "path": rel_path,
                "lines": len(lines),
                "package": "",
                "class_name": "",
                "annotations": [],
                "layer": "",
            }

            for line in lines[:50]:
                m = re.match(r"^\s*package\s+([\w.]+)\s*;", line)
                if m:
                    file_info["package"] = m.group(1)
                    pkg = m.group(1)
                    for layer, patterns in PACKAGE_LAYER_PATTERNS.items():
                        if any(re.search(p, pkg) for p in patterns):
                            file_info["layer"] = layer
                            module_name = rel_path.split(os.sep)[0] if os.sep in rel_path else "root"
                            package_layers[module_name][layer] += 1
                    break

            class_match = re.search(r"\b(?:public\s+)?(?:class|interface|enum|record)\s+(\w+)", content)
            if class_match:
                file_info["class_name"] = class_match.group(1)

            for ann_name, patterns in SPRING_ANNOTATIONS.items():
                for pat in patterns:
                    if re.search(pat, content):
                        file_info["annotations"].append(ann_name)
                        keywords_counter[pat] += 1

            for pat in ["@FeignClient"]:
                if re.search(pat, content):
                    url_match = re.search(r'@FeignClient\s*\([^)]*(?:name|value)\s*=\s*["\']([^"\']+)', content)
                    if url_match:
                        key_classes.append({
                            "class": file_info["class_name"],
                            "type": "FeignClient",
                            "target": url_match.group(1),
                            "file": rel_path,
                        })

            datasource_match = re.search(r'@DS\s*\(\s*["\']([^"\']+)', content)
            if datasource_match:
                key_classes.append({
                    "class": file_info["class_name"],
                    "type": "DynamicDataSource",
                    "target": datasource_match.group(1),
                    "file": rel_path,
                })

            for imp in re.finditer(r"import\s+([\w.]+);", content):
                pkg = imp.group(1)
                if any(kw in pkg for kw in ["feign", "resttemplate", "webclient", "dubbo", "rpc", "grpc"]):
                    import_patterns[file_info["package"]].append(pkg)

            java_files.append(file_info)

    return {
        "total_java_files": len(java_files),
        "total_lines": sum(f["lines"] for f in java_files),
        "package_layers": {k: dict(v) for k, v in package_layers.items()},
        "key_classes": key_classes,
        "import_patterns": {k: v[:10] for k, v in import_patterns.items()},
        "annotation_counts": {ann: sum(1 for f in java_files if ann in f["annotations"]) for ann in SPRING_ANNOTATIONS},
        "keywords_counter": dict(keywords_counter),
    }


# ============================================================
# Dockerfile / K8s Detection
# ============================================================

def scan_deployment_files(project_root):
    """Scan for Dockerfile, docker-compose, K8s manifests, Helm charts."""
    results = {
        "dockerfiles": [],
        "docker_compose": [],
        "k8s_manifests": [],
        "helm_charts": [],
        "ci_cd_files": [],
        "shell_scripts": [],
    }

    dockerfile_dirs = set()

    for f in project_root.rglob("*"):
        if "target" in f.parts or "build" in f.parts or ".git" in f.parts:
            continue
        name = f.name.lower()
        rel = str(f.relative_to(project_root))

        if name == "dockerfile" or name.startswith("dockerfile."):
            results["dockerfiles"].append(rel)
            dockerfile_dirs.add(str(f.parent))
        elif name in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"):
            results["docker_compose"].append(rel)
        elif name in ("deployment.yaml", "deployment.yml", "service.yaml", "service.yml",
                       "ingress.yaml", "configmap.yaml", "secret.yaml", "hpa.yaml"):
            results["k8s_manifests"].append(rel)
        elif name == "chart.yaml":
            chart_dir = str(f.parent)
            results["helm_charts"].append(chart_dir)
        elif name in (".gitlab-ci.yml", "jenkinsfile", ".github", "azure-pipelines.yml"):
            results["ci_cd_files"].append(rel)
        elif name.endswith(".sh") and "init" in name:
            results["shell_scripts"].append(rel)

    # Also look in charts/ directory (common Helm pattern)
    charts_dir = project_root / "charts"
    if charts_dir.exists():
        for chart_yaml in charts_dir.rglob("Chart.yaml"):
            results["helm_charts"].append(str(chart_yaml.parent.relative_to(project_root)))

    return results


# ============================================================
# Main Scan Function
# ============================================================

def scan_project(project_root, module_filter=None, output_dir=None):
    """Main scan function."""
    project_root = Path(project_root).resolve()
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = project_root / "docs-output"

    module_filter_list = module_filter.split(",") if module_filter else None

    # Detect build tool
    pom_path = project_root / "pom.xml"
    gradle_path = project_root / "build.gradle"
    settings_gradle = project_root / "settings.gradle"

    build_tool = "unknown"
    root_pom_info = {}
    gradle_info = {}

    if pom_path.exists():
        build_tool = "maven"
        root_pom_info = parse_pom(pom_path)
    elif gradle_path.exists():
        build_tool = "gradle"
        gradle_info = parse_gradle(gradle_path)
        if settings_gradle.exists():
            settings_info = parse_gradle(settings_gradle)
            gradle_info["subprojects"] = settings_info.get("subprojects", [])

    # Build module list
    modules = []
    module_dirs = []

    if build_tool == "maven":
        module_names = root_pom_info.get("modules", [])
    elif build_tool == "gradle":
        module_names = gradle_info.get("subprojects", [])
    else:
        module_names = []

    for mod_name in module_names:
        mod_path = project_root / mod_name
        if not mod_path.exists():
            mod_path = project_root / mod_name.replace("/", os.sep)
        if not mod_path.exists():
            continue

        if module_filter_list and mod_name not in module_filter_list:
            continue

        mod_pom = mod_path / "pom.xml"
        mod_info = parse_pom(mod_pom) if mod_pom.exists() else {}
        modules.append({
            "name": mod_name,
            "path": str(mod_path.relative_to(project_root)),
            "artifactId": mod_info.get("artifactId", mod_name),
            "packaging": mod_info.get("packaging", "jar"),
            "description": mod_info.get("description", ""),
            "dependencies": mod_info.get("dependencies", []),
            "build_plugins": mod_info.get("build_plugins", []),
        })
        module_dirs.append(mod_path)

    # Collect all dependencies for tech stack detection
    all_deps = root_pom_info.get("dependencies", []) + gradle_info.get("dependencies", [])
    for mod in modules:
        all_deps.extend(mod.get("dependencies", []))

    # Extract config items
    config_items, config_files = extract_config_items(project_root, module_filter_list)
    config_content = ""
    for cf in config_items:
        config_content += cf.get("path", "") + " " + cf.get("value", "") + " "

    # Scan source code
    source_summary = scan_source_files(project_root, module_filter_list)

    # Detect tech stack
    tech_stack = detect_tech_stack(
        project_root, all_deps, config_content, source_summary.get("keywords_counter", {})
    )

    # Scan deployment files
    deployment_files = scan_deployment_files(project_root)

    # Check for README
    readme_path = None
    for name in ["README.md", "readme.md", "README.MD", "README"]:
        candidate = project_root / name
        if candidate.exists():
            readme_path = str(candidate.relative_to(project_root))
            break

    # Check for .git
    is_git_repo = (project_root / ".git").exists()

    # Build project info
    project_info = {
        "project_root": str(project_root),
        "project_name": root_pom_info.get("name", "") or gradle_info.get("name", "") or project_root.name,
        "project_description": root_pom_info.get("description", "") or gradle_info.get("description", ""),
        "group_id": root_pom_info.get("groupId", "") or gradle_info.get("group", ""),
        "artifact_id": root_pom_info.get("artifactId", "") or project_root.name,
        "version": root_pom_info.get("version", "") or gradle_info.get("version", ""),
        "build_tool": build_tool,
        "parent_pom": root_pom_info.get("parent", {}),
        "properties": root_pom_info.get("properties", {}),
        "profiles": root_pom_info.get("profiles", []),
        "module_count": len(modules),
        "module_names": [m["name"] for m in modules],
        "is_git_repo": is_git_repo,
        "has_readme": readme_path is not None,
        "readme_path": readme_path,
    }

    module_tree = {
        "project_name": project_info["project_name"],
        "build_tool": build_tool,
        "modules": modules,
    }

    config_summary = {
        "config_files": config_files,
        "total_items": len(config_items),
        "items": config_items,
    }

    output = {
        "project-info.json": project_info,
        "module-tree.json": module_tree,
        "config-items.json": config_summary,
        "source-summary.json": source_summary,
        "tech-stack.json": {
            "detected_technologies": tech_stack,
            "total_count": len(tech_stack),
        },
        "deployment-files.json": deployment_files,
    }

    # Write output files
    for filename, data in output.items():
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[scan_project] Scan complete. Output directory: {output_dir}")
    print(f"  Project: {project_info['project_name']} (v{project_info['version']})")
    print(f"  Build tool: {build_tool}")
    print(f"  Modules: {project_info['module_count']}")
    print(f"  Tech stack detected: {len(tech_stack)} technologies")
    print(f"  Config files: {len(config_files)}")
    print(f"  Java source files: {source_summary['total_java_files']}")
    print(f"  Deployment files: Docker={len(deployment_files['dockerfiles'])}, "
          f"K8s={len(deployment_files['k8s_manifests'])}, "
          f"Helm={len(deployment_files['helm_charts'])}")

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan microservice project for documentation generation")
    parser.add_argument("project_root", help="Root directory of the project")
    parser.add_argument("--modules", default=None, help="Comma-separated module names to filter (e.g., pcm-app,pcm-common)")
    parser.add_argument("--output", default=None, help="Output directory (default: <project>/docs-output)")
    args = parser.parse_args()

    scan_project(args.project_root, args.modules, args.output)

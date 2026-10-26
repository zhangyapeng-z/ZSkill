#!/usr/bin/env python3
"""
Dependency Analyzer — Service & Middleware Dependency Topology
Parses inter-service call relationships (Feign/RestTemplate/WebClient/gRPC/Dubbo)
and external middleware dependencies (DB/Cache/MQ/Search), generates Mermaid topology diagram.

Usage:
    python analyze_dependencies.py <project-root> [--modules <m1,m2,...>] [--output <dir>]

Outputs:
    service-dependencies.json    — service-to-service call relationships
    middleware-dependencies.json — external middleware (DB, cache, MQ, etc.)
    dependency-topology.mmd      — Mermaid topology diagram
    dependency-topology.md       — Markdown report with embedded Mermaid
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter

# ============================================================
# Feign Client Detection
# ============================================================

FEIGN_PATTERN = re.compile(
    r'@FeignClient\s*\(\s*(?:name|value)\s*=\s*["\']([^"\']+)["\']'
    r'(?:[^)]*url\s*=\s*["\']([^"\']+)["\'])?'
    r'[^)]*\)',
    re.DOTALL
)

FEIGN_FALLBACK_PATTERN = re.compile(
    r'@FeignClient\s*\([^)]*fallback\s*=\s*(\w+)\.class', re.DOTALL
)

# ============================================================
# RestTemplate / WebClient Detection
# ============================================================

RESTTEMPLATE_URL_PATTERN = re.compile(
    r'(?:restTemplate|restOperations)\s*\.\s*(?:getForObject|postForObject|exchange|getForEntity|postForEntity)\s*\(\s*["\']([^"\']+)["\']',
    re.MULTILINE
)

WEBCLIENT_URL_PATTERN = re.compile(
    r'(?:webClient|WebClient)\s*\.\s*(?:get|post|put|delete)\s*\(\s*\)\s*\.\s*uri\s*\(\s*["\']([^"\']+)["\']',
    re.MULTILINE
)

HTTP_URL_PATTERN = re.compile(
    r'(?:http://|https://)([a-zA-Z0-9._-]+)',
    re.MULTILINE
)

# ============================================================
# Dubbo Reference Detection
# ============================================================

DUBBO_REFERENCE_PATTERN = re.compile(
    r'@DubboReference\s*\(\s*(?:interfaceClass\s*=\s*)?(\w+)\.class', re.DOTALL
)

DUBBO_REFERENCE_PATTERN2 = re.compile(
    r'@Reference\s*\(\s*(?:interfaceClass\s*=\s*)?(\w+)\.class', re.DOTALL
)

# ============================================================
# Middleware Detection Patterns
# ============================================================

MIDDLEWARE_PATTERNS = {
    "MySQL": {
        "config_patterns": [r"jdbc:mysql://", r"com\.mysql", r"mysql-connector"],
        "pom_patterns": [r"mysql-connector-java", r"mysql-connector"],
    },
    "PostgreSQL": {
        "config_patterns": [r"jdbc:postgresql://", r"org\.postgresql"],
        "pom_patterns": [r"postgresql"],
    },
    "Oracle": {
        "config_patterns": [r"jdbc:oracle:", r"oracle\.jdbc"],
        "pom_patterns": [r"ojdbc", r"oracle"],
    },
    "SQLServer": {
        "config_patterns": [r"jdbc:sqlserver:", r"com\.microsoft\.sqlserver"],
        "pom_patterns": [r"mssql-jdbc", r"sqljdbc"],
    },
    "Redis": {
        "config_patterns": [r"redis:", r"spring\.redis", r"lettuce", r"jedis"],
        "pom_patterns": [r"spring-boot-starter-data-redis", r"jedis", r"lettuce", r"redisson"],
    },
    "MongoDB": {
        "config_patterns": [r"mongodb://", r"spring\.data\.mongodb"],
        "pom_patterns": [r"spring-boot-starter-data-mongodb", r"mongodb-driver"],
    },
    "Kafka": {
        "config_patterns": [r"spring\.kafka", r"bootstrap-servers", r"kafka"],
        "pom_patterns": [r"spring-kafka", r"kafka-clients"],
    },
    "RabbitMQ": {
        "config_patterns": [r"spring\.rabbitmq", r"amqp"],
        "pom_patterns": [r"spring-boot-starter-amqp", r"amqp-client"],
    },
    "RocketMQ": {
        "config_patterns": [r"rocketmq", r"spring\.rocketmq"],
        "pom_patterns": [r"rocketmq-spring-boot-starter", r"rocketmq-client"],
    },
    "Elasticsearch": {
        "config_patterns": [r"spring\.elasticsearch", r"elasticsearch"],
        "pom_patterns": [r"spring-data-elasticsearch", r"elasticsearch-rest-high-level-client"],
    },
    "Nacos": {
        "config_patterns": [r"spring\.cloud\.nacos", r"nacos"],
        "pom_patterns": [r"spring-cloud-starter-alibaba-nacos", r"nacos-client"],
    },
    "MinIO": {
        "config_patterns": [r"minio", r"minio\.endpoint"],
        "pom_patterns": [r"minio"],
    },
    "Zookeeper": {
        "config_patterns": [r"zookeeper", r"curator"],
        "pom_patterns": [r"zookeeper", r"curator"],
    },
    "Seata": {
        "config_patterns": [r"seata", r"spring\.cloud\.alibaba\.seata"],
        "pom_patterns": [r"seata-spring-boot-starter", r"spring-cloud-starter-alibaba-seata"],
    },
    "Sentinel": {
        "config_patterns": [r"sentinel", r"spring\.cloud\.sentinel"],
        "pom_patterns": [r"spring-cloud-starter-alibaba-sentinel", r"sentinel"],
    },
}


def find_java_files(project_root, module_filter=None):
    """Find all Java source files, excluding build outputs."""
    java_files = []
    for f in project_root.rglob("*.java"):
        if "target" in f.parts or "build" in f.parts or ".git" in f.parts:
            continue
        if module_filter and not any(mf in str(f) for mf in module_filter):
            continue
        java_files.append(f)
    return java_files


def find_config_files(project_root, module_filter=None):
    """Find config files (yml, yaml, properties)."""
    config_files = []
    for f in project_root.rglob("*"):
        if f.suffix not in (".yml", ".yaml", ".properties"):
            continue
        if "target" in f.parts or "build" in f.parts or ".git" in f.parts:
            continue
        if module_filter and not any(mf in str(f) for mf in module_filter):
            continue
        config_files.append(f)
    return config_files


def find_pom_files(project_root, module_filter=None):
    """Find all pom.xml files."""
    pom_files = []
    for f in project_root.rglob("pom.xml"):
        if module_filter and not any(mf in str(f) for mf in module_filter):
            continue
        pom_files.append(f)
    return pom_files


# ============================================================
# Service Dependency Extraction
# ============================================================

def extract_service_dependencies(java_files, project_root):
    """Extract inter-service call relationships."""
    dependencies = []

    for java_file in java_files:
        try:
            content = java_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel_path = str(java_file.relative_to(project_root))
        module_name = rel_path.split(os.sep)[0] if os.sep in rel_path else "root"

        class_match = re.search(r"\b(?:public\s+)?(?:class|interface)\s+(\w+)", content)
        class_name = class_match.group(1) if class_match else java_file.stem

        # Feign clients
        for m in FEIGN_PATTERN.finditer(content):
            target = m.group(1)
            url = m.group(2) or ""
            dep = {
                "source_module": module_name,
                "source_class": class_name,
                "source_file": rel_path,
                "target_service": target,
                "target_url": url,
                "protocol": "HTTP (Feign)",
                "call_type": "Feign Client",
            }
            dependencies.append(dep)

        # RestTemplate calls
        for m in RESTTEMPLATE_URL_PATTERN.finditer(content):
            url = m.group(1)
            target = re.search(r"https?://([^/]+)", url) or re.search(r"//([^/]+)", url)
            target_service = target.group(1) if target else url
            dependencies.append({
                "source_module": module_name,
                "source_class": class_name,
                "source_file": rel_path,
                "target_service": target_service,
                "target_url": url,
                "protocol": "HTTP (RestTemplate)",
                "call_type": "RestTemplate",
            })

        # WebClient calls
        for m in WEBCLIENT_URL_PATTERN.finditer(content):
            url = m.group(1)
            dependencies.append({
                "source_module": module_name,
                "source_class": class_name,
                "source_file": rel_path,
                "target_service": url,
                "target_url": url,
                "protocol": "HTTP (WebClient)",
                "call_type": "WebClient",
            })

        # Dubbo references
        for m in DUBBO_REFERENCE_PATTERN.finditer(content):
            dependencies.append({
                "source_module": module_name,
                "source_class": class_name,
                "source_file": rel_path,
                "target_service": m.group(1),
                "target_url": "",
                "protocol": "Dubbo RPC",
                "call_type": "Dubbo Reference",
            })

        for m in DUBBO_REFERENCE_PATTERN2.finditer(content):
            dependencies.append({
                "source_module": module_name,
                "source_class": class_name,
                "source_file": rel_path,
                "target_service": m.group(1),
                "target_url": "",
                "protocol": "Dubbo RPC",
                "call_type": "@Reference",
            })

        # HTTP URL references (less precise, but useful)
        for m in HTTP_URL_PATTERN.finditer(content):
            host = m.group(1)
            if host in ("localhost", "127.0.0.1", "0.0.0.0"):
                continue
            if any(c["target_service"] == host and c["source_class"] == class_name
                   for c in dependencies):
                continue
            dependencies.append({
                "source_module": module_name,
                "source_class": class_name,
                "source_file": rel_path,
                "target_service": host,
                "target_url": f"http://{host}",
                "protocol": "HTTP",
                "call_type": "HTTP URL",
            })

    return dependencies


# ============================================================
# Middleware Dependency Extraction
# ============================================================

def extract_middleware_dependencies(config_files, pom_files):
    """Extract external middleware dependencies from config and POM files."""
    detected = []
    config_content = ""
    pom_content = ""

    for cf in config_files:
        try:
            config_content += cf.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            continue

    for pf in pom_files:
        try:
            pom_content += pf.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            continue

    all_content = config_content + "\n" + pom_content

    for mw_name, patterns in MIDDLEWARE_PATTERNS.items():
        evidence = []
        matched = False

        for pat in patterns.get("config_patterns", []):
            matches = re.findall(pat, all_content, re.IGNORECASE)
            if matches:
                matched = True
                evidence.append(f"config pattern: {pat} ({len(matches)} matches)")

        for pat in patterns.get("pom_patterns", []):
            matches = re.findall(pat, pom_content, re.IGNORECASE)
            if matches:
                matched = True
                evidence.append(f"pom pattern: {pat} ({len(matches)} matches)")

        if matched:
            detected.append({
                "middleware": mw_name,
                "evidence": evidence,
                "type": classify_middleware(mw_name),
            })

    return detected


def classify_middleware(name):
    """Classify middleware by type."""
    db_keywords = ["MySQL", "PostgreSQL", "Oracle", "SQLServer", "MongoDB"]
    cache_keywords = ["Redis"]
    mq_keywords = ["Kafka", "RabbitMQ", "RocketMQ"]
    search_keywords = ["Elasticsearch"]
    registry_keywords = ["Nacos", "Zookeeper"]
    storage_keywords = ["MinIO"]
    tx_keywords = ["Seata"]
    flow_keywords = ["Sentinel"]

    if name in db_keywords:
        return "database"
    elif name in cache_keywords:
        return "cache"
    elif name in mq_keywords:
        return "message-queue"
    elif name in search_keywords:
        return "search-engine"
    elif name in registry_keywords:
        return "service-registry"
    elif name in storage_keywords:
        return "object-storage"
    elif name in tx_keywords:
        return "distributed-transaction"
    elif name in flow_keywords:
        return "flow-control"
    else:
        return "other"


# ============================================================
# DataSource Extraction
# ============================================================

DATASOURCE_PATTERN = re.compile(
    r'(?:spring\.datasource|hzero|dynamic)\.?\w*\.?\w*\.?\w*\.url\s*[=:]\s*(\S+)',
    re.IGNORECASE
)

DATASOURCE_NAME_PATTERN = re.compile(
    r'(?:spring\.datasource|datasource)\.(\w+)\.url\s*[=:]\s*(\S+)',
    re.IGNORECASE
)


def extract_datasources(config_files):
    """Extract datasource configurations."""
    datasources = []
    for cf in config_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for m in DATASOURCE_NAME_PATTERN.finditer(content):
            ds_name = m.group(1)
            url = m.group(2)
            db_type = "unknown"
            if "mysql" in url.lower():
                db_type = "MySQL"
            elif "postgresql" in url.lower():
                db_type = "PostgreSQL"
            elif "oracle" in url.lower():
                db_type = "Oracle"
            elif "sqlserver" in url.lower():
                db_type = "SQLServer"

            host = ""
            port = ""
            db = ""
            host_match = re.search(r"//([^:/]+)(?::(\d+))?(?:/([^?]+))?", url)
            if host_match:
                host = host_match.group(1)
                port = host_match.group(2) or ""
                db = host_match.group(3) or ""

            datasources.append({
                "name": ds_name,
                "type": db_type,
                "host": host,
                "port": port,
                "database": db,
                "url": url,
                "config_file": str(cf.name),
            })

        # Also match simple patterns
        for m in re.finditer(r"jdbc:(mysql|postgresql|oracle|sqlserver)://([^:/]+)(?::(\d+))?(?:/([^?]+))?", content):
            db_type = m.group(1).capitalize()
            if db_type == "Mysql":
                db_type = "MySQL"
            host = m.group(2)
            port = m.group(3) or ""
            db = m.group(4) or ""
            ds_entry = {
                "name": "default",
                "type": db_type,
                "host": host,
                "port": port,
                "database": db,
                "url": f"jdbc:{m.group(1)}://{host}:{port}/{db}",
                "config_file": str(cf.name),
            }
            if not any(d["host"] == host and d["port"] == port for d in datasources):
                datasources.append(ds_entry)

    return datasources


# ============================================================
# Mermaid Topology Generation
# ============================================================

def generate_mermaid_topology(project_name, service_deps, middleware_deps, datasources, modules):
    """Generate Mermaid topology diagram."""

    # Determine nodes
    service_nodes = set()
    infra_nodes = set()

    for dep in service_deps:
        service_nodes.add(dep["source_module"])
        service_nodes.add(dep["target_service"])

    for mw in middleware_deps:
        infra_nodes.add(mw["middleware"])

    for ds in datasources:
        service_nodes.add(f"{ds['type']} ({ds['name']})")

    lines = []
    lines.append("graph TB")
    lines.append("    %% ===== Service Nodes =====")

    # Group by module
    for mod in sorted(service_nodes):
        if mod in [m["name"] for m in modules]:
            lines.append(f"    {sanitize_node_id(mod)}[\"{mod}\"]")
        else:
            lines.append(f"    {sanitize_node_id(mod)}[\"{mod}\"]:::externalService")

    lines.append("")
    lines.append("    %% ===== Infrastructure Nodes =====")

    type_icons = {
        "database": "[(\"Database\")]",
        "cache": "[(\"Cache\")]",
        "message-queue": "[(\"Message Queue\")]",
        "search-engine": "[(\"Search Engine\")]",
        "service-registry": "((\"Registry\"))",
        "object-storage": "[(\"Object Storage\")]",
        "distributed-transaction": "[\"TX Coordinator\"]",
        "flow-control": "[\"Flow Control\"]",
    }

    for mw in sorted(infra_nodes, key=lambda x: classify_middleware(x)):
        mw_type = classify_middleware(mw)
        icon = type_icons.get(mw_type, "[\"Infrastructure\"]")
        lines.append(f"    {sanitize_node_id(mw)}{icon}")

    lines.append("")
    lines.append("    %% ===== Service-to-Service Edges =====")

    seen_edges = set()
    for dep in service_deps:
        src_id = sanitize_node_id(dep["source_module"])
        tgt_id = sanitize_node_id(dep["target_service"])
        edge_key = f"{src_id}->{tgt_id}"
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)
        proto = dep.get("protocol", "")
        lines.append(f"    {src_id} -->|{proto}| {tgt_id}")

    lines.append("")
    lines.append("    %% ===== Infrastructure Dependencies =====")

    for mw in middleware_deps:
        mw_id = sanitize_node_id(mw["middleware"])
        mw_type = mw["type"]
        lines.append(f"    {mw_id}.--- infrastructure dependency")

    lines.append("")
    lines.append("    %% ===== Styling =====")
    lines.append("    classDef externalService fill:#fff3cd,stroke:#856404,stroke-width:2px;")
    lines.append("    classDef database fill:#d1ecf1,stroke:#0c5460,stroke-width:2px;")
    lines.append("    classDef cache fill:#d4edda,stroke:#155724,stroke-width:2px;")
    lines.append("    classDef messageQueue fill:#f8d7da,stroke:#721c24,stroke-width:2px;")

    return "\n".join(lines)


def sanitize_node_id(name):
    """Sanitize a name for use as a Mermaid node ID."""
    safe = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if safe and safe[0].isdigit():
        safe = "N_" + safe
    return safe


def generate_markdown_report(project_name, service_deps, middleware_deps, datasources,
                              mermaid_diagram, modules):
    """Generate a Markdown report with embedded Mermaid."""
    lines = []
    lines.append(f"# {project_name} - Dependency Topology Report")
    lines.append("")
    lines.append("## 1. Topology Overview")
    lines.append("")
    lines.append("```mermaid")
    lines.append(mermaid_diagram)
    lines.append("```")
    lines.append("")

    # Service Dependencies Table
    lines.append("## 2. Service-to-Service Dependencies")
    lines.append("")
    if service_deps:
        lines.append("| Source Module | Source Class | Target Service | Protocol | Call Type |")
        lines.append("|---------------|-------------|-----------------|----------|-----------|")
        for dep in service_deps:
            lines.append(
                f"| {dep['source_module']} | {dep['source_class']} | "
                f"{dep['target_service']} | {dep['protocol']} | {dep['call_type']} |"
            )
    else:
        lines.append("_No inter-service dependencies detected._")
    lines.append("")

    # Middleware Dependencies Table
    lines.append("## 3. External Middleware Dependencies")
    lines.append("")
    if middleware_deps:
        lines.append("| Middleware | Type | Evidence |")
        lines.append("|-----------|------|----------|")
        for mw in middleware_deps:
            evidence_str = "; ".join(mw["evidence"][:3])
            lines.append(f"| {mw['middleware']} | {mw['type']} | {evidence_str} |")
    else:
        lines.append("_No external middleware dependencies detected._")
    lines.append("")

    # Datasource details
    lines.append("## 4. Datasource Details")
    lines.append("")
    if datasources:
        lines.append("| Datasource Name | Database Type | Host | Port | Database |")
        lines.append("|-----------------|--------------|------|------|----------|")
        for ds in datasources:
            lines.append(
                f"| {ds['name']} | {ds['type']} | {ds['host']} | {ds['port']} | {ds['database']} |"
            )
    else:
        lines.append("_No datasource configurations detected._")
    lines.append("")

    # Module summary
    lines.append("## 5. Module Summary")
    lines.append("")
    lines.append("| Module | Artifact ID | Packaging | Dependency Count |")
    lines.append("|--------|-----------|----------|-----------------|")
    for mod in modules:
        dep_count = len(mod.get("dependencies", []))
        lines.append(
            f"| {mod['name']} | {mod.get('artifactId', mod['name'])} | "
            f"{mod.get('packaging', 'jar')} | {dep_count} |"
        )
    lines.append("")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def analyze_dependencies(project_root, module_filter=None, output_dir=None):
    """Main dependency analysis function."""
    project_root = Path(project_root).resolve()
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = project_root / "docs-output"

    module_filter_list = module_filter.split(",") if module_filter else None

    # Gather files
    java_files = find_java_files(project_root, module_filter_list)
    config_files = find_config_files(project_root, module_filter_list)
    pom_files = find_pom_files(project_root, module_filter_list)

    # Extract dependencies
    service_deps = extract_service_dependencies(java_files, project_root)
    middleware_deps = extract_middleware_dependencies(config_files, pom_files)
    datasources = extract_datasources(config_files)

    # Load module info for the report
    from xml.etree import ElementTree as ET
    modules = []
    root_pom = project_root / "pom.xml"
    if root_pom.exists():
        try:
            tree = ET.parse(root_pom)
            root = tree.getroot()
            ns = "{http://maven.apache.org/POM/4.0.0}"
            for mod_elem in root.findall(f"{ns}modules/{ns}module"):
                if mod_elem.text:
                    modules.append({"name": mod_elem.text.strip(), "artifactId": mod_elem.text.strip(), "packaging": "jar", "dependencies": []})
        except Exception:
            pass

    project_name = project_root.name

    # Generate Mermaid topology
    mermaid = generate_mermaid_topology(project_name, service_deps, middleware_deps, datasources, modules)

    # Generate Markdown report
    markdown = generate_markdown_report(project_name, service_deps, middleware_deps, datasources, mermaid, modules)

    # Write outputs
    outputs = {
        "service-dependencies.json": service_deps,
        "middleware-dependencies.json": {
            "detected_middleware": middleware_deps,
            "datasources": datasources,
            "total_count": len(middleware_deps),
        },
        "dependency-topology.mmd": mermaid,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            if isinstance(data, str):
                f.write(data)
            else:
                json.dump(data, f, ensure_ascii=False, indent=2)

    md_path = output_dir / "dependency-topology.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"[analyze_dependencies] Analysis complete. Output directory: {output_dir}")
    print(f"  Service dependencies: {len(service_deps)}")
    print(f"  Middleware detected: {len(middleware_deps)}")
    print(f"  Datasources: {len(datasources)}")
    print(f"  Mermaid diagram: {output_dir / 'dependency-topology.mmd'}")
    print(f"  Markdown report: {md_path}")

    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze service and middleware dependencies")
    parser.add_argument("project_root", help="Root directory of the project")
    parser.add_argument("--modules", default=None, help="Comma-separated module names to filter")
    parser.add_argument("--output", default=None, help="Output directory")
    args = parser.parse_args()

    analyze_dependencies(args.project_root, args.modules, args.output)

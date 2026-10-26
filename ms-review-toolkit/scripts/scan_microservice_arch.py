#!/usr/bin/env python3
"""
Microservice Architecture Scanner — 微服务架构检查脚本
扫描微服务工程，构建服务清单与调用图，执行 M-01~M-10 架构检查规则。

用法:
    python scan_microservice_arch.py <project-root> --scan --output <dir>   # 工程扫描
    python scan_microservice_arch.py <project-root> --check --output <dir>  # 架构检查（需先 scan）
    python scan_microservice_arch.py <project-root> --scan --check --output <dir>  # 一步到位

产出文件:
    service-inventory.json   — 服务清单
    service-call-graph.json  — 服务间调用关系图
    arch-issues.json         — 架构问题列表
"""

import os
import re
import json
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict, deque


# ============================================================
# 可调阈值（服务拆分合理性 M-01）
# ============================================================
SERVICE_FILE_COUNT_MAX = 200        # 单服务文件数上限
SERVICE_FILE_COUNT_MIN = 5          # 单服务文件数下限
SERVICE_LINE_COUNT_MAX = 30000      # 单服务代码行数上限
CALL_CHAIN_DEPTH_THRESHOLD = 3      # 同步调用链路深度阈值
DUP_BLOCK_LINES = 6                 # 重复代码块行数阈值
DUP_SIMILARITY = 0.8                # 重复相似度阈值


def strip_ns(tag):
    if "}" in tag:
        return tag.split("}")[1]
    return tag


def parse_pom(pom_path):
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except ET.ParseError:
        return None
    result = {"groupId": None, "artifactId": None, "version": None,
              "packaging": "jar", "modules": [], "dependencies": [], "parent": None}
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
    pom_files = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ("target", ".git", "node_modules")]
        if "pom.xml" in files:
            pom_files.append(os.path.join(root, "pom.xml"))
    return pom_files


def parse_java_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except IOError:
        return None
    lines = content.split("\n")
    info = {
        "filePath": filepath.replace("\\", "/"),
        "fileName": os.path.basename(filepath),
        "packageName": None, "className": None, "isInterface": False,
        "annotations": [], "imports": [], "lineCount": len(lines),
        "methods": [], "content": content,
    }
    for line in lines:
        m = re.match(r"\s*package\s+([\w.]+)\s*;", line)
        if m:
            info["packageName"] = m.group(1)
            break
    for line in lines:
        m = re.match(r"\s*import\s+(?:static\s+)?([\w.*]+)\s*;", line)
        if m:
            info["imports"].append(m.group(1))
    for line in lines:
        ann_match = re.findall(r"@(\w+)", line)
        info["annotations"].extend(ann_match)
    class_match = re.search(r"\b(public\s+)?(abstract\s+)?(class|interface|enum)\s+(\w+)", content)
    if class_match:
        info["className"] = class_match.group(4)
        info["isInterface"] = class_match.group(3) == "interface"
    # 提取方法名（粗略）
    for m in re.finditer(r"(public|protected|private)?\s*(?:static\s+)?[\w<>\[\],\s]+\s+(\w+)\s*\(", content):
        info["methods"].append(m.group(2))
    return info


def parse_yaml_config(config_path):
    """简单解析 application.yml/properties 提取 datasource/url 等"""
    config = {}
    if not os.path.isfile(config_path):
        return config
    try:
        with open(config_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except IOError:
        return config
    if config_path.endswith(".properties"):
        for line in text.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip()
    else:
        # yml 粗解析：抓取 url/password/secret 等关键行
        for line in text.split("\n"):
            stripped = line.strip()
            if ":" in stripped and not stripped.startswith("#"):
                k, v = stripped.split(":", 1)
                k = k.strip()
                v = v.strip().strip("\"'")
                if v:
                    config[k] = v
    return config


def find_config_files(service_dir):
    """查找服务的配置文件"""
    configs = []
    for root, dirs, files in os.walk(service_dir):
        dirs[:] = [d for d in dirs if d not in ("target", ".git")]
        for f in files:
            if f.endswith((".yml", ".yaml", ".properties")) and ("application" in f or "bootstrap" in f):
                configs.append(os.path.join(root, f))
    return configs


# ============================================================
# 服务清单与调用图构建
# ============================================================

def identify_services(project_root, modules):
    """识别独立服务：含 @SpringBootApplication 的模块"""
    services = []
    for module_name, module_info in modules.items():
        for jf in module_info.get("javaFiles", []):
            if "@SpringBootApplication" in jf.get("annotations", []):
                # 提取端口与配置
                configs = find_config_files(module_info["path"])
                merged_cfg = {}
                for cp in configs:
                    merged_cfg.update(parse_yaml_config(cp))
                # 提取 datasource url
                ds_url = (merged_cfg.get("url")
                          or merged_cfg.get("spring.datasource.url")
                          or merged_cfg.get("datasource.url")
                          or "")
                port = merged_cfg.get("server.port", "unknown")
                services.append({
                    "serviceName": module_name,
                    "artifactId": module_name,
                    "path": module_info["path"],
                    "mainClass": jf["className"],
                    "mainClassFile": jf["filePath"],
                    "port": port,
                    "javaFileCount": module_info["javaFileCount"],
                    "totalLines": sum(j["lineCount"] for j in module_info["javaFiles"]),
                    "database": ds_url,
                    "configFiles": [c.replace("\\", "/") for c in configs],
                    "javaFiles": module_info["javaFiles"],
                    "packages": sorted(set(j["packageName"] for j in module_info["javaFiles"] if j["packageName"])),
                })
                break
    return services


def extract_call_edges(services):
    """从各服务源码提取服务间调用边（Feign/Dubbo/RestTemplate）"""
    edges = []
    service_names = {s["serviceName"] for s in services}
    # 兼容服务名变体：order-app -> order / order-service
    name_variants = {}
    for s in services:
        base = s["serviceName"]
        name_variants[base] = s["serviceName"]
        # 生成常见变体
        for suffix in ("-app", "-service", "-api", "-biz", "-server", "-web", "-provider", "-starter"):
            if base.endswith(suffix):
                short = base[:-len(suffix)]
                name_variants[short] = s["serviceName"]
        name_variants[base.replace("-", "")] = s["serviceName"]

    for svc in services:
        for jf in svc["javaFiles"]:
            content = jf.get("content", "")
            # Feign: @FeignClient(name="x") 或 contextId
            for m in re.finditer(r'@FeignClient\s*\([^)]*(?:name|contextId|value)\s*=\s*"([^"]+)"', content):
                target = m.group(1)
                target_svc = name_variants.get(target, target)
                has_fallback = "fallback" in content[m.start():m.start()+300] or "fallbackFactory" in content[m.start():m.start()+300]
                edges.append({"from": svc["serviceName"], "to": target_svc, "type": "feign",
                              "hasFallback": has_fallback, "file": jf["filePath"]})
            # Dubbo: @DubboReference / @Reference (interfaceClass 包名推断归属)
            for m in re.finditer(r'@(?:DubboReference|Reference)\s*\(', content):
                # 取后续 import 或 interfaceClass
                seg = content[m.start():m.start()+500]
                target_svc = "unknown(dubbo)"
                edges.append({"from": svc["serviceName"], "to": target_svc, "type": "dubbo",
                              "hasFallback": False, "file": jf["filePath"]})
            # RestTemplate/WebClient 直连服务名
            for m in re.finditer(r'(?:restTemplate|webClient|RestTemplate|WebClient)[\w.]*\.(?:get|post|put|delete)\w*\s*\(\s*"https?://([\w-]+)', content):
                target = m.group(1)
                target_svc = name_variants.get(target, target)
                edges.append({"from": svc["serviceName"], "to": target_svc, "type": "rest",
                              "hasFallback": False, "file": jf["filePath"]})
            # 硬编码 IP 调用（M-07 线索）
            for m in re.finditer(r'(?:restTemplate|RestTemplate|webClient|HttpClient)[\w.]*\.(?:get|post|put|delete)\w*\s*\(\s*"https?://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', content):
                edges.append({"from": svc["serviceName"], "to": f"hardcoded:{m.group(1)}", "type": "rest-hardcoded",
                              "hasFallback": False, "file": jf["filePath"]})
    return edges, name_variants


def build_call_graph(services, edges):
    nodes = [s["serviceName"] for s in services]
    # 计算最长路径（DFS）与环路检测
    adj = defaultdict(list)
    for e in edges:
        adj[e["from"]].append(e["to"])

    def max_depth(node, visited):
        visited.add(node)
        children = [t for t in adj.get(node, []) if t not in visited and not t.startswith("hardcoded") and t != "unknown(dubbo)"]
        if not children:
            return 0
        return 1 + max(max_depth(c, visited.copy()) for c in children)

    max_d = 0
    for n in nodes:
        max_d = max(max_d, max_depth(n, set()))

    # 环路检测
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for nb in adj.get(node, []):
            if nb.startswith("hardcoded") or nb == "unknown(dubbo)":
                continue
            if color[nb] == GRAY:
                idx = path.index(nb) if nb in path else 0
                cycles.append(path[idx:] + [nb])
            elif color[nb] == WHITE:
                dfs(nb, path)
        path.pop()
        color[node] = BLACK

    for n in nodes:
        if color[n] == WHITE:
            dfs(n, [])

    return {"nodes": nodes, "edges": edges, "maxDepth": max_d, "cycles": cycles}


# ============================================================
# 架构检查规则 M-01 ~ M-10
# ============================================================

def issue(rule_id, severity, desc, suggestion, confidence="high", **extra):
    d = {
        "ruleId": rule_id, "severity": severity, "category": "architecture",
        "confidence": confidence, "status": "confirmed" if confidence == "high" else "pending",
        "description": desc, "suggestion": suggestion,
    }
    d.update(extra)
    return d


def check_service_split(services):
    """M-01 服务拆分合理性"""
    issues = []
    for s in services:
        if s["javaFileCount"] > SERVICE_FILE_COUNT_MAX:
            issues.append(issue("M-01", "Critical", "pending",
                f"服务 {s['serviceName']} 文件数 {s['javaFileCount']} 超阈值 {SERVICE_FILE_COUNT_MAX}，疑似拆分不充分（伪微服务/单体）",
                "按 DDD 限界上下文拆分，识别内部领域边界拆为独立服务", confidence="medium",
                serviceName=s["serviceName"], filePath=s["path"], lineNumber=0))
        if s["javaFileCount"] < SERVICE_FILE_COUNT_MIN and s["javaFileCount"] > 0:
            issues.append(issue("M-01", "Critical", "pending",
                f"服务 {s['serviceName']} 文件数 {s['javaFileCount']} 过少，疑似过度拆分（纳米服务）",
                "合并同子域过细服务，减少运维与通信成本", confidence="medium",
                serviceName=s["serviceName"], filePath=s["path"], lineNumber=0))
        if s["totalLines"] > SERVICE_LINE_COUNT_MAX:
            issues.append(issue("M-01", "Critical", "pending",
                f"服务 {s['serviceName']} 代码行数 {s['totalLines']} 超阈值 {SERVICE_LINE_COUNT_MAX}",
                "评估领域边界，按子域拆分", confidence="medium",
                serviceName=s["serviceName"], filePath=s["path"], lineNumber=0))
        # 多业务上下文混杂
        domains = set()
        for pkg in s["packages"]:
            m = re.search(r'\.(order|payment|inventory|user|account|product|marketing|coupon|logistics|finance|member|cart|search)\b', pkg)
            if m:
                domains.add(m.group(1))
        if len(domains) > 2:
            issues.append(issue("M-01", "Critical", "pending",
                f"服务 {s['serviceName']} 内出现多个不相关业务上下文: {', '.join(sorted(domains))}，领域边界不清",
                "按业务领域重新划分服务边界，一个服务对应一个业务子域", confidence="medium",
                serviceName=s["serviceName"], filePath=s["path"], lineNumber=0))
    return issues


def check_communication(call_graph):
    """M-02 服务间通信效率"""
    issues = []
    if call_graph["maxDepth"] >= CALL_CHAIN_DEPTH_THRESHOLD:
        issues.append(issue("M-02", "Major",
            f"同步调用链路深度 {call_graph['maxDepth']} 跳 ≥ {CALL_CHAIN_DEPTH_THRESHOLD}，链路过长",
            "引入聚合服务/BFF，串行改并行；通知类依赖改消息异步解耦",
            serviceName="跨服务", filePath="service-call-graph.json", lineNumber=0))
    for cycle in call_graph["cycles"]:
        issues.append(issue("M-02", "Critical",
            f"服务间循环调用: {' -> '.join(cycle)}",
            "重构服务边界消除环依赖，或引入事件驱动解耦",
            serviceName=",".join(cycle), filePath="service-call-graph.json", lineNumber=0))
    return issues


def check_shared_database(services):
    """M-03 共享业务库"""
    issues = []
    # 按 host+port+dbname 分组
    db_map = defaultdict(list)
    for s in services:
        url = s.get("database", "")
        if not url:
            continue
        m = re.search(r'//([^/]+)/([\w-]+)', url)
        key = m.group(1) + "/" + m.group(2) if m else url
        db_map[key].append(s["serviceName"])
    for key, svc_list in db_map.items():
        if len(svc_list) > 1:
            issues.append(issue("M-03", "Blocker",
                f"多服务共享同一业务数据库 {key}: {', '.join(svc_list)}，破坏服务自治",
                "每个服务独占数据库，跨服务数据通过 API 获取；共享配置库除外",
                serviceName=",".join(svc_list), filePath="application.yml", lineNumber=0,
                impact="服务耦合，无法独立部署/扩缩容，故障连锁"))
    # 跨服务直接 import Mapper
    service_pkgs = {}
    for s in services:
        for pkg in s["packages"]:
            for jf in s["javaFiles"]:
                for imp in jf.get("imports", []):
                    mm = re.search(r'\.(order|payment|inventory|user|product)\.(?:mapper|repository|dao)\.\w+', imp)
                    if mm:
                        domain = mm.group(1)
                        if domain not in [p.split(".")[-2] if "." in p else "" for p in s["packages"]]:
                            issues.append(issue("M-03", "Blocker",
                                f"服务 {s['serviceName']} 直接 import 其他服务 Mapper: {imp}",
                                "跨服务数据通过 API 获取，禁止直接访问其他服务 DAO",
                                serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
    return issues


def check_distributed_transaction(services, call_graph, edges, tech_stack=None):
    """M-04 分布式事务缺失"""
    issues = []
    # 是否有跨服务写调用（非只读）
    has_cross_write = False
    write_keywords = ("create", "save", "update", "delete", "insert", "deduct", "pay", "submit", "confirm")
    for e in edges:
        if e["type"] in ("feign", "dubbo") and not e["to"].startswith("hardcoded"):
            # 检查调用方法名是否含写语义
            for s in services:
                if s["serviceName"] == e["from"]:
                    for jf in s["javaFiles"]:
                        content = jf.get("content", "")
                        if e["file"] == jf["filePath"]:
                            if any(kw in content.lower() for kw in write_keywords):
                                has_cross_write = True
    # 是否有分布式事务方案
    has_tx_solution = False
    tx_features = ("@GlobalTransactional", "@TwoPhaseBusinessAction", "@RocketMQTransactionListener",
                   "@LcnTransaction", "TransactionMessage", "LocalMessage")
    for s in services:
        for jf in s["javaFiles"]:
            content = jf.get("content", "")
            if any(feat in content for feat in tx_features):
                has_tx_solution = True
                break

    # 检查 @Transactional 方法内跨服务调用
    for s in services:
        for jf in s["javaFiles"]:
            content = jf.get("content", "")
            if "@Transactional" in content:
                if ("@FeignClient" in content or "@DubboReference" in content or "@Reference" in content):
                    # 粗判：同文件内既有事务又调用远程
                    issues.append(issue("M-04", "Critical",
                        f"{s['serviceName']} 中 @Transactional 方法存在跨服务调用，本地事务无法覆盖远程调用",
                        "强一致用 Seata @GlobalTransactional；最终一致用事务消息+本地消息表+消费幂等",
                        serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))

    if has_cross_write and not has_tx_solution and len(services) > 1:
        issues.append(issue("M-04", "Critical", "pending",
            "存在跨服务写操作但未识别到分布式事务方案（TCC/Saga/Seata/事务消息）",
            "强一致引入 Seata AT/TCC；最终一致用事务消息+本地消息表+幂等", confidence="medium",
            serviceName="跨服务", filePath="N/A", lineNumber=0,
            impact="跨服务写失败导致数据不一致"))
    return issues


def check_circuit_breaker(services, edges, tech_stack=None):
    """M-05 容错熔断缺失"""
    issues = []
    has_hystrix = any(fw["name"] == "Hystrix" for fw in (tech_stack or {}).get("frameworks", [])) if tech_stack else False
    has_sentinel = any(fw["name"] == "Sentinel" for fw in (tech_stack or {}).get("frameworks", [])) if tech_stack else False
    has_resilience4j = any(fw["name"] == "Resilience4j" for fw in (tech_stack or {}).get("frameworks", [])) if tech_stack else False

    # 检查每个 Feign/Dubbo 调用是否有 fallback
    for s in services:
        for jf in s["javaFiles"]:
            content = jf.get("content", "")
            # Feign 无 fallback
            for m in re.finditer(r'@FeignClient\s*\(([^)]*)\)', content, re.DOTALL):
                params = m.group(1)
                if "fallback" not in params and "fallbackFactory" not in params:
                    name_match = re.search(r'(?:name|contextId|value)\s*=\s*"([^"]+)"', params)
                    target = name_match.group(1) if name_match else "unknown"
                    issues.append(issue("M-05", "Critical",
                        f"Feign 客户端调用 {target} 未配置 fallback/fallbackFactory",
                        "配置 fallbackFactory 获取异常原因并提供降级返回值",
                        serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
            # Dubbo 无 timeout/mock
            for m in re.finditer(r'@(?:DubboReference|Reference)\s*\(([^)]*)\)', content, re.DOTALL):
                params = m.group(1)
                if "timeout" not in params:
                    issues.append(issue("M-05", "Critical",
                        "Dubbo 引用未配置 timeout，默认超时可能导致线程阻塞",
                        "配置 timeout 与 retries；写接口 retries=0",
                        serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
                if "mock" not in params:
                    issues.append(issue("M-05", "Major", "pending",
                        "Dubbo 引用未配置 mock 降级",
                        "配置 mock 实现降级", confidence="medium",
                        serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
    # 有跨服务调用但无任何熔断框架
    has_cross_call = any(e["type"] in ("feign", "dubbo") for e in edges)
    if has_cross_call and not (has_hystrix or has_sentinel or has_resilience4j):
        issues.append(issue("M-05", "Critical",
            "存在跨服务调用但未引入任何熔断框架（Hystrix/Sentinel/Resilience4j）",
            "引入 Sentinel/Resilience4j，配置熔断降级规则",
            serviceName="跨服务", filePath="N/A", lineNumber=0))
    return issues


def check_api_gateway(services, tech_stack=None):
    """M-06 API 网关配置"""
    issues = []
    has_gateway = any(fw["name"] in ("Spring Cloud Gateway", "Zuul") for fw in (tech_stack or {}).get("frameworks", [])) if tech_stack else False
    if not has_gateway:
        return issues  # 无网关则不报本规则
    for s in services:
        for cfg_path in s["configFiles"]:
            # 检查网关服务的路由配置
            if any(kw in s["serviceName"].lower() for kw in ("gateway", "zuul", "gateway-service")):
                configs = {}
                try:
                    with open(cfg_path, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                except IOError:
                    continue
                if "RequestRateLimiter" not in text and "Sentinel" not in text and "rateLimit" not in text.lower():
                    issues.append(issue("M-06", "Major", "pending",
                        "网关未配置限流（RequestRateLimiter/Sentinel 网关流控）",
                        "全局限流：Sentinel 网关流控或 RequestRateLimiter+Redis", confidence="medium",
                        serviceName=s["serviceName"], filePath=cfg_path, lineNumber=0))
                if "CORS" not in text.upper() and "cors" not in text.lower() and "allowedOrigins" not in text:
                    issues.append(issue("M-06", "Major", "pending",
                        "网关未配置 CORS 或需检查是否为 * 通配",
                        "CORS 白名单明确来源，禁止 *", confidence="medium",
                        serviceName=s["serviceName"], filePath=cfg_path, lineNumber=0))
                if "GlobalFilter" not in "".join(jf.get("content", "") for jf in s["javaFiles"]):
                    issues.append(issue("M-06", "Major", "pending",
                        "网关未实现 GlobalFilter 鉴权（内部服务可能裸暴露）",
                        "实现 GlobalFilter 校验 JWT/Token", confidence="medium",
                        serviceName=s["serviceName"], filePath=s["path"], lineNumber=0))
    return issues


def check_hardcoded_address(services):
    """M-07 硬编码地址调用"""
    issues = []
    for s in services:
        for jf in s["javaFiles"]:
            content = jf.get("content", "")
            for m in re.finditer(r'"https?://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?', content):
                ip = m.group(1)
                if ip in ("127.0.0.1", "localhost", "0.0.0.0"):
                    continue
                # 排除本地 profile 文件
                if "local" in jf["filePath"].lower() or "dev" in jf["filePath"].lower():
                    continue
                issues.append(issue("M-07", "Major",
                    f"硬编码 IP 调用 {ip}，未通过注册中心发现",
                    "内部服务调用走注册中心服务名，RestTemplate 加 @LoadBalanced",
                    serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
            # 密钥硬编码（M-08）
            for m in re.finditer(r'(?:password|secret|accessKey|apiKey|token)\s*[=:]\s*["\']([^"\']{6,})["\']', content, re.IGNORECASE):
                val = m.group(1)
                if val in ("changeme", "xxx", "test", "none", "example", "${", "TODO"):
                    continue
                issues.append(issue("M-08", "Blocker",
                    f"源码硬编码密钥/凭据: {m.group(0)[:40]}...",
                    "密钥走配置中心/环境变量/KMS，源码零明文",
                    serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
    # 配置文件明文密码
    for s in services:
        for cfg_path in s["configFiles"]:
            if "local" in cfg_path.lower() or "dev" in cfg_path.lower():
                continue
            try:
                with open(cfg_path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except IOError:
                continue
            for m in re.finditer(r'(?:password|secret|access-key|accessKey)\s*[:=]\s*([^\s${][^\s]{4,})', text, re.IGNORECASE):
                val = m.group(1).strip("\"'")
                if val in ("changeme", "xxx", "test", "none", "example"):
                    continue
                if "${" in val:
                    continue
                issues.append(issue("M-08", "Major",
                    f"配置文件明文密码: {cfg_path}",
                    "用 ${ENV_VAR} 占位引用，密钥走配置中心/KMS",
                    serviceName=s["serviceName"], filePath=cfg_path, lineNumber=0))
    return issues


def check_idempotency(services):
    """M-09 接口幂等性"""
    issues = []
    for s in services:
        for jf in s["javaFiles"]:
            content = jf.get("content", "")
            # 写接口
            for m in re.finditer(r'@(?:PostMapping|PutMapping|RequestMapping)\s*\([^)]*(?:method\s*=\s*RequestMethod\.(?:POST|PUT))?', content):
                # 检查是否有幂等标识
                has_idempotent = ("@Idempotent" in content or "requestId" in content.lower()
                                  or "idempotent" in content.lower() or "distributedLock" in content
                                  or "@DistributedLock" in content or "RedisLock" in content)
                if not has_idempotent:
                    issues.append(issue("M-09", "Critical", "pending",
                        f"写接口疑似未做幂等设计: {jf['filePath']}",
                        "加幂等键（requestId + Redis SETNX）/唯一约束/分布式锁防重", confidence="low",
                        serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
    return issues


def check_api_versioning(services):
    """M-10 API 版本管理"""
    issues = []
    for s in services:
        for jf in s["javaFiles"]:
            content = jf.get("content", "")
            # 查找对外 Controller 路径无版本号
            for m in re.finditer(r'@(?:RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping)\s*\(\s*(?:value\s*=\s*)?"(/[^"]*)"', content):
                path = m.group(1)
                if not re.search(r'/v\d+/', path) and not path.startswith("/v"):
                    # 排除内部接口
                    if any(kw in jf["filePath"].lower() for kw in ("internal", "inner", "admin")):
                        continue
                    issues.append(issue("M-10", "Minor", "pending",
                        f"对外 API 路径无版本号: {path}",
                        "对外 API 路径带版本号 /api/v1/xxx，破坏性变更新增版本", confidence="low",
                        serviceName=s["serviceName"], filePath=jf["filePath"], lineNumber=0))
    return issues


def run_all_checks(services, call_graph, edges, tech_stack=None):
    issues = []
    issues += check_service_split(services)
    issues += check_communication(call_graph)
    issues += check_shared_database(services)
    issues += check_distributed_transaction(services, call_graph, edges, tech_stack)
    issues += check_circuit_breaker(services, edges, tech_stack)
    issues += check_api_gateway(services, tech_stack)
    issues += check_hardcoded_address(services)
    issues += check_idempotency(services)
    issues += check_api_versioning(services)
    return issues


# ============================================================
# 主流程
# ============================================================

def scan_and_check(project_root, output_dir, do_scan, do_check):
    project_root = os.path.abspath(project_root)
    print(f"[INFO] Scanning project: {project_root}")

    # 1. 解析模块
    pom_files = find_pom_files(project_root)
    modules = {}
    for pom_file in pom_files:
        pom_info = parse_pom(pom_file)
        if not pom_info or not pom_info["artifactId"]:
            continue
        module_dir = os.path.dirname(pom_file)
        java_files = []
        java_src = os.path.join(module_dir, "src", "main", "java")
        if os.path.isdir(java_src):
            for root, dirs, files in os.walk(java_src):
                for f in files:
                    if f.endswith(".java"):
                        ji = parse_java_file(os.path.join(root, f))
                        if ji:
                            java_files.append(ji)
        modules[pom_info["artifactId"]] = {
            "pom": pom_info, "path": module_dir.replace("\\", "/"),
            "javaFiles": java_files, "javaFileCount": len(java_files),
        }

    # 2. 识别服务
    services = identify_services(project_root, modules)
    print(f"[INFO] Identified {len(services)} services")
    for s in services:
        print(f"  - {s['serviceName']} (files={s['javaFileCount']}, lines={s['totalLines']})")

    # 3. 构建调用图
    edges, name_variants = extract_call_edges(services)
    call_graph = build_call_graph(services, edges)
    print(f"[INFO] Call edges: {len(edges)}, max depth: {call_graph['maxDepth']}, cycles: {len(call_graph['cycles'])}")

    # 4. 读取技术栈（若存在）
    tech_stack = None
    tech_path = os.path.join(output_dir, "tech-stack.json") if output_dir else None
    if tech_path and os.path.isfile(tech_path):
        with open(tech_path, "r", encoding="utf-8") as f:
            tech_stack = json.load(f)

    # 5. 输出扫描结果
    if do_scan and output_dir:
        os.makedirs(output_dir, exist_ok=True)
        service_inventory = [{
            "serviceName": s["serviceName"], "artifactId": s["artifactId"], "path": s["path"],
            "port": s["port"], "mainClass": s["mainClass"], "javaFileCount": s["javaFileCount"],
            "totalLines": s["totalLines"], "database": s["database"], "packages": s["packages"],
        } for s in services]
        write_json(os.path.join(output_dir, "service-inventory.json"), service_inventory)
        write_json(os.path.join(output_dir, "service-call-graph.json"), call_graph)

    # 6. 架构检查
    if do_check:
        print("[INFO] Running architecture checks...")
        issues = run_all_checks(services, call_graph, edges, tech_stack)
        # 非微服务工程跳过 M 系列（仅当 tech_stack 明确 isMicroservice=false）
        if tech_stack and not tech_stack.get("isMicroservice", True):
            issues = [i for i in issues if i.get("category") != "architecture"]
            print("[INFO] Non-microservice project, architecture (M) checks skipped to avoid false positives.")
        if output_dir:
            write_json(os.path.join(output_dir, "arch-issues.json"), issues)
        print(f"[INFO] Found {len(issues)} architecture issues")
        for i in issues:
            print(f"  [{i['severity']}|{i['confidence']}] {i['ruleId']}: {i['description'][:80]}")
    print("[INFO] Done.")
    return {"services": services, "callGraph": call_graph, "issues": issues if do_check else []}


def write_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Written: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Microservice Architecture Scanner")
    parser.add_argument("project_root", help="Path to project root")
    parser.add_argument("--scan", action="store_true", help="Scan project structure")
    parser.add_argument("--check", action="store_true", help="Run architecture checks")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    args = parser.parse_args()
    if not os.path.isdir(args.project_root):
        print(f"[ERROR] Project root not found: {args.project_root}")
        return
    if not args.scan and not args.check:
        args.scan = True
        args.check = True
    scan_and_check(args.project_root, args.output, args.scan, args.check)


if __name__ == "__main__":
    main()

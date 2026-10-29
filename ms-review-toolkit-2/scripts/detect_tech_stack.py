#!/usr/bin/env python3
"""
Tech Stack Detector — 微服务技术栈识别脚本
识别 Spring Cloud / Dubbo 等主流微服务技术栈，为后续检查提供技术栈上下文，避免对非微服务工程误报。

用法:
    python detect_tech_stack.py <project-root> [--output <dir>]

产出文件:
    tech-stack.json — 工程级技术栈识别结果（含是否微服务、框架列表、能力缺口）
"""

import os
import re
import json
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET


# ============================================================
# 技术栈识别特征（对应 references/springcloud-dubbo-patterns.md）
# ============================================================

TECH_STACK_SIGNATURES = [
    # --- Spring Cloud Netflix ---
    {"name": "Eureka Server", "category": "discovery", "pom": ["spring-cloud-starter-netflix-eureka-server"], "code": ["@EnableEurekaServer"]},
    {"name": "Eureka Client", "category": "discovery", "pom": ["spring-cloud-starter-netflix-eureka-client"], "code": ["@EnableEurekaClient"]},
    {"name": "Hystrix", "category": "circuit-breaker", "pom": ["spring-cloud-starter-netflix-hystrix"], "code": ["@HystrixCommand", "@EnableCircuitBreaker"], "deprecated": True},
    {"name": "Zuul", "category": "gateway", "pom": ["spring-cloud-starter-netflix-zuul"], "code": ["@EnableZuulProxy"], "deprecated": True},
    {"name": "Ribbon", "category": "loadbalancer", "pom": ["spring-cloud-starter-netflix-ribbon"], "code": ["@LoadBalanced"], "deprecated": True},
    {"name": "OpenFeign", "category": "communication", "pom": ["spring-cloud-starter-openfeign"], "code": ["@FeignClient", "@EnableFeignClients"]},

    # --- Spring Cloud Alibaba ---
    {"name": "Nacos Discovery", "category": "discovery", "pom": ["spring-cloud-starter-alibaba-nacos-discovery"], "code": ["@EnableDiscoveryClient"]},
    {"name": "Nacos Config", "category": "config", "pom": ["spring-cloud-starter-alibaba-nacos-config"], "code": []},
    {"name": "Sentinel", "category": "circuit-breaker", "pom": ["spring-cloud-starter-alibaba-sentinel"], "code": ["@SentinelResource"]},
    {"name": "Seata", "category": "transaction", "pom": ["spring-cloud-starter-alibaba-seata"], "code": ["@GlobalTransactional"]},
    {"name": "RocketMQ", "category": "message", "pom": ["spring-cloud-starter-stream-rocketmq", "rocketmq-spring-boot-starter"], "code": ["@RocketMQMessageListener", "@RocketMQTransactionListener"]},

    # --- Spring Cloud 通用 ---
    {"name": "Spring Cloud Gateway", "category": "gateway", "pom": ["spring-cloud-starter-gateway"], "code": []},
    {"name": "Spring Cloud Config", "category": "config", "pom": ["spring-cloud-config-server", "spring-cloud-starter-config"], "code": ["@EnableConfigServer"]},
    {"name": "Resilience4j", "category": "circuit-breaker", "pom": ["resilience4j-spring-boot2", "resilience4j-spring-cloud"], "code": ["@CircuitBreaker", "@Retry", "@RateLimiter"]},

    # --- Apache Dubbo ---
    {"name": "Dubbo3", "category": "communication", "pom": ["dubbo-spring-boot-starter"], "code": ["@DubboService", "@DubboReference"]},
    {"name": "Dubbo2", "category": "communication", "pom": ["dubbo"], "code": ["@Reference"], "hint": "需配合 dubbo 包名判断"},

    # --- 基础设施 ---
    {"name": "Spring Boot", "category": "framework", "pom": ["spring-boot-starter"], "code": ["@SpringBootApplication"]},
    {"name": "MyBatis", "category": "orm", "pom": ["mybatis-spring-boot-starter", "mybatis-spring-boot3-starter"], "code": ["@Mapper", "@MapperScan"]},
    {"name": "JPA/Hibernate", "category": "orm", "pom": ["spring-boot-starter-data-jpa"], "code": ["@Entity", "@Repository"]},
    {"name": "Redis", "category": "cache", "pom": ["spring-boot-starter-data-redis"], "code": ["RedisTemplate", "RedissonClient"]},
    {"name": "Kafka", "category": "message", "pom": ["spring-kafka"], "code": ["@KafkaListener"]},
    {"name": "RabbitMQ", "category": "message", "pom": ["spring-boot-starter-amqp"], "code": ["@RabbitListener"]},
]

# 微服务能力类别（用于判断是否微服务工程及能力缺口）
MICROSERVICE_CAPABILITIES = {
    "discovery": "服务注册发现",
    "communication": "服务间通信",
    "circuit-breaker": "容错熔断",
    "config": "配置管理",
    "gateway": "API网关",
    "transaction": "分布式事务",
    "message": "消息中间件",
}

# 判定为微服务工程的最小特征（满足任一即视为微服务）
MICROSERVICE_INDICATORS = ["OpenFeign", "Dubbo3", "Dubbo2", "Nacos Discovery", "Eureka Server", "Eureka Client",
                           "Spring Cloud Gateway", "Zuul", "Sentinel", "Hystrix"]


def strip_ns(tag):
    if "}" in tag:
        return tag.split("}")[1]
    return tag


def parse_pom_dependencies(pom_path):
    """解析 POM 提取依赖 artifactId 列表"""
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except ET.ParseError:
        return []

    artifacts = []
    for child in root:
        if strip_ns(child.tag) == "dependencies":
            for dep in child:
                if strip_ns(dep.tag) == "dependency":
                    for d in dep:
                        if strip_ns(d.tag) == "artifactId":
                            if d.text:
                                artifacts.append(d.text.strip())
        # dependencyManagement 里的也要收
        if strip_ns(child.tag) == "dependencyManagement":
            for dep_mgmt in child:
                if strip_ns(dep_mgmt.tag) == "dependencies":
                    for dep in dep_mgmt:
                        if strip_ns(dep.tag) == "dependency":
                            for d in dep:
                                if strip_ns(d.tag) == "artifactId":
                                    if d.text:
                                        artifacts.append(d.text.strip())
    return artifacts


def find_pom_files(project_root):
    pom_files = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ("target", ".git", "node_modules")]
        if "pom.xml" in files:
            pom_files.append(os.path.join(root, "pom.xml"))
    return pom_files


def collect_all_dependencies(project_root):
    """汇总工程所有 POM 的依赖 artifactId"""
    all_artifacts = set()
    for pom in find_pom_files(project_root):
        for art in parse_pom_dependencies(pom):
            all_artifacts.add(art)
    return all_artifacts


def find_java_files(project_root):
    """收集所有 java 文件路径"""
    java_files = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ("target", ".git", "node_modules")]
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(root, f))
    return java_files


def scan_code_features(java_files, sample_limit=2000):
    """扫描源码注解/特征（采样以提升性能）"""
    code_features = set()
    files_to_scan = java_files[:sample_limit] if len(java_files) > sample_limit else java_files
    for fp in files_to_scan:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            for sig in TECH_STACK_SIGNATURES:
                for code in sig.get("code", []):
                    if code in content:
                        code_features.add(code)
        except IOError:
            continue
    return code_features


def detect_tech_stack(project_root):
    """识别工程技术栈"""
    all_deps = collect_all_dependencies(project_root)
    java_files = find_java_files(project_root)
    code_features = scan_code_features(java_files)

    detected = []
    for sig in TECH_STACK_SIGNATURES:
        pom_match = any(p in all_deps for p in sig.get("pom", []))
        code_match = any(c in code_features for c in sig.get("code", []))
        if pom_match or code_match:
            detected.append({
                "name": sig["name"],
                "category": sig["category"],
                "evidence": {
                    "pom": pom_match,
                    "code": code_match,
                },
                "deprecated": sig.get("deprecated", False),
            })

    # 判断是否微服务工程
    detected_names = {d["name"] for d in detected}
    is_microservice = any(name in detected_names for name in MICROSERVICE_INDICATORS)

    # 能力缺口分析
    present_categories = {d["category"] for d in detected}
    gaps = []
    for cat, desc in MICROSERVICE_CAPABILITIES.items():
        if cat not in present_categories:
            gaps.append(desc)

    # 微服务工程相关缺口（仅微服务工程才报关键缺口）
    ms_gaps = []
    if is_microservice:
        if "circuit-breaker" not in present_categories:
            ms_gaps.append("未识别到容错熔断方案（Hystrix/Sentinel/Resilience4j）")
        if "transaction" not in present_categories and "message" not in present_categories:
            ms_gaps.append("未识别到分布式事务方案（Seata）或消息最终一致性方案")

    return {
        "isMicroservice": is_microservice,
        "frameworks": detected,
        "presentCategories": sorted(present_categories),
        "gaps": ms_gaps,
        "allDependencies": sorted(all_deps),
        "javaFileCount": len(java_files),
    }


def main():
    parser = argparse.ArgumentParser(description="Microservice Tech Stack Detector")
    parser.add_argument("project_root", help="Path to project root")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    args = parser.parse_args()

    if not os.path.isdir(args.project_root):
        print(f"[ERROR] Project root not found: {args.project_root}")
        return

    print(f"[INFO] Detecting tech stack: {args.project_root}")
    result = detect_tech_stack(args.project_root)

    print(f"[INFO] Is microservice: {result['isMicroservice']}")
    print(f"[INFO] Frameworks detected: {len(result['frameworks'])}")
    for fw in result["frameworks"]:
        dep_tag = " (deprecated)" if fw["deprecated"] else ""
        print(f"  - {fw['name']} [{fw['category']}]{dep_tag}")
    if result["gaps"]:
        print("[INFO] Capability gaps:")
        for g in result["gaps"]:
            print(f"  - {g}")

    if args.output:
        os.makedirs(args.output, exist_ok=True)
        out_path = os.path.join(args.output, "tech-stack.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Written: {out_path}")


if __name__ == "__main__":
    main()

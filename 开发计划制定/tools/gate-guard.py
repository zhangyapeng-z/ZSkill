#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate-guard.py — 研发专家团段门校验脚本（v2.4.0，hzero-copilot 借鉴）

借鉴 hzero-spec 0.3.5 sdd-change-close-guard.py 的"脚本强制门禁"设计：
主理人在段门前调用本脚本做只读校验，任一检查不通过 → 拒绝过段。

用法:
    python gate-guard.py --artifacts-dir <artifacts目录> --gate <part2|part3|finish>

输出: JSON { gate, passed, checks: [{id, name, passed, detail}] }
退出码: 0 = 全部通过; 1 = 存在不通过项; 2 = 参数/环境错误

校验逻辑（只读，不修改任何文件）:
  part2  (进入设计段前): 需求段产物齐全 + 评审结论含基线冻结 + pipeline-state 1.1~1.5 全 DONE
  part3  (进入实现段前): 技术方案(含数据库类型) + dev-plan + 评审结论存在 + pipeline-state 2.1~2.3 全 DONE
  finish (实现段收尾前): 代码清单 + review-report + 验收走查存在 + pipeline-state 3.1~3.4 全 DONE
状态对账: pipeline-state 标 DONE 但产物缺失 → 以产物为准，该步骤按未通过处理（对齐 v2.3 §5.3）
"""
import argparse
import json
import sys
from pathlib import Path

def find_file(directory: Path, *patterns):
    """按多个 glob 模式查找第一个存在的文件（仅当前目录，不递归）。"""
    for pattern in patterns:
        hits = sorted(directory.glob(pattern))
        # 过滤目录，只留文件
        hits = [h for h in hits if h.is_file()]
        if hits:
            return hits[0]
    return None

def load_pipeline_state(artifacts_dir: Path):
    ps = artifacts_dir / "pipeline-state.json"
    if not ps.is_file():
        return None, f"pipeline-state.json 不存在: {ps}"
    try:
        return json.loads(ps.read_text(encoding="utf-8")), None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return None, f"pipeline-state.json 解析失败: {e}"

def build_step_index(state: dict):
    """按步骤 id 建索引: {id: {status, gateResult, ...}}"""
    idx = {}
    for step in state.get("steps", []):
        sid = str(step.get("id", ""))
        idx[sid] = step
    return idx

def check(name: str, passed: bool, detail: str):
    return {"id": "", "name": name, "passed": bool(passed), "detail": detail}

def file_content_marker(path: Path, *keywords):
    """文件存在且包含全部关键词（按出现顺序无所谓，做子串匹配）。返回 (ok, detail)。"""
    if path is None or not Path(path).is_file():
        return False, f"文件不存在: {path}"
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return False, f"读取失败 {path}: {e}"
    missing = [k for k in keywords if k not in text]
    if missing:
        return False, f"{path.name} 缺少关键标记: {', '.join(missing)}"
    return True, f"{path.name} 含全部关键标记"

def gate_checks(artifacts_dir: Path, gate: str):
    checks = []

    if gate == "part2":
        req_dir = artifacts_dir / "01-需求段"
        req_spec = find_file(req_dir, "requirement-spec.md", "requirement-spec.json")
        checks.append(check("req-spec-exists", req_spec is not None,
                            f"需求规格: {req_spec}" if req_spec else "01-需求段/ 下未找到 requirement-spec.md/.json"))
        proto = find_file(req_dir, "prototype", "prototype*", "prototype/index.html")
        checks.append(check("prototype-exists", proto is not None,
                            f"原型: {proto}" if proto else "01-需求段/ 下未找到 prototype/ 原型目录或文件"))
        review = find_file(req_dir, "requirement-review.md")
        ok, detail = (False, "requirement-review.md 不存在")
        if review is not None:
            ok, detail = file_content_marker(review, "基线冻结")
        checks.append(check("req-review-frozen", ok, detail))
        pm_review = find_file(req_dir, "pm-review-01.md")
        checks.append(check("pm-review-01-exists", pm_review is not None,
                            f"产品经理评审: {pm_review}" if pm_review else "pm-review-01.md 不存在"))
        expect_steps = ["1.1", "1.2", "1.3", "1.4", "1.5"]

    elif gate == "part3":
        design_dir = artifacts_dir / "02-设计段"
        tech = find_file(design_dir, "tech-design.md")
        ok, detail = (False, "tech-design.md 不存在")
        if tech is not None:
            ok, detail = file_content_marker(tech, "数据库")
        checks.append(check("tech-design-db-confirmed", ok, detail))
        dev_plan = find_file(design_dir, "dev-plan.md", "dev-plan.json", "dev-plan.xlsx")
        checks.append(check("dev-plan-exists", dev_plan is not None,
                            f"开发计划: {dev_plan}" if dev_plan else "02-设计段/ 下未找到 dev-plan.md/.json/.xlsx"))
        review = find_file(design_dir, "design-review.md")
        checks.append(check("design-review-exists", review is not None,
                            f"方案评审结论: {review}" if review else "design-review.md 不存在"))
        pm_review = find_file(design_dir, "pm-review-02.md")
        checks.append(check("pm-review-02-exists", pm_review is not None,
                            f"产品经理评审: {pm_review}" if pm_review else "pm-review-02.md 不存在"))
        expect_steps = ["2.1", "2.2", "2.3"]

    elif gate == "finish":
        code_dir = artifacts_dir / "03-实现段"
        manifest = find_file(code_dir, "code-manifest.json")
        checks.append(check("code-manifest-exists", manifest is not None,
                            f"代码清单: {manifest}" if manifest else "03-实现段/ 下未找到 code-manifest.json"))
        review_report = find_file(code_dir, "review-report.json")
        checks.append(check("review-report-exists", review_report is not None,
                            f"审查报告: {review_report}" if review_report else "review-report.json 不存在"))
        acceptance = find_file(code_dir, "acceptance-walkthrough.md")
        checks.append(check("acceptance-exists", acceptance is not None,
                            f"验收走查单: {acceptance}" if acceptance else "acceptance-walkthrough.md 不存在"))
        pm_review = find_file(code_dir, "pm-review-03.md")
        checks.append(check("pm-review-03-exists", pm_review is not None,
                            f"产品经理评审: {pm_review}" if pm_review else "pm-review-03.md 不存在"))
        # 追溯矩阵（全程产物）
        trace = find_file(artifacts_dir, "traceability-matrix.md", "**/traceability-matrix.md")
        checks.append(check("traceability-exists", trace is not None,
                            f"追溯矩阵: {trace}" if trace else "traceability-matrix.md 不存在"))
        expect_steps = ["3.1", "3.2", "3.3", "3.4"]
    else:
        raise ValueError(f"未知段门: {gate}")

    return checks, expect_steps

def state_checks(state: dict, expect_steps):
    checks = []
    if state is None:
        checks.append(check("pipeline-state-readable", False,
                            "pipeline-state.json 缺失或不可解析，步骤状态对账跳过（按不通过处理）"))
        return checks
    idx = build_step_index(state)
    for sid in expect_steps:
        step = idx.get(sid)
        if step is None:
            checks.append(check(f"step-{sid}-in-state", False, f"步骤 {sid} 未登记于 pipeline-state.json"))
            continue
        status = str(step.get("status", "PENDING")).upper()
        artifacts = step.get("artifacts") or []
        missing_artifacts = []
        # 状态对账：DONE 但声明产物路径不存在 → 按未通过
        if status == "DONE" and artifacts:
            base = Path(state.get("_artifacts_dir", "."))
            for a in artifacts:
                p = Path(a)
                if not p.is_absolute():
                    p = base / a
                if not p.exists():
                    missing_artifacts.append(a)
        if status != "DONE":
            checks.append(check(f"step-{sid}-done", False, f"步骤 {sid} 状态为 {status}，需 DONE"))
        elif missing_artifacts:
            checks.append(check(f"step-{sid}-done", False,
                                f"步骤 {sid} 标 DONE 但产物缺失(以产物为准，回退): {', '.join(missing_artifacts)}"))
        else:
            checks.append(check(f"step-{sid}-done", True, f"步骤 {sid} DONE 且产物对账通过"))
    return checks

def main():
    parser = argparse.ArgumentParser(description="研发专家团段门校验（只读）")
    parser.add_argument("--artifacts-dir", required=True, help="artifacts 目录绝对路径")
    parser.add_argument("--gate", required=True, choices=["part2", "part3", "finish"],
                        help="段门: part2=进设计段前, part3=进实现段前, finish=实现段收尾前")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir).resolve()
    if not artifacts_dir.is_dir():
        print(json.dumps({"gate": args.gate, "passed": False,
                          "checks": [check("artifacts-dir", False, f"目录不存在: {artifacts_dir}")]},
                         ensure_ascii=False, indent=2))
        sys.exit(2)

    state, err = load_pipeline_state(artifacts_dir)
    if err:
        # 状态文件问题不直接终止：文件检查仍执行，状态对账按不通过处理
        state = None
        state_err = err
    else:
        state_err = None
        if isinstance(state, dict):
            state["_artifacts_dir"] = str(artifacts_dir)

    checks, expect_steps = gate_checks(artifacts_dir, args.gate)
    checks += state_checks(state, expect_steps)
    if state_err:
        checks.append(check("pipeline-state-readable", False, state_err))

    passed = all(c["passed"] for c in checks)
    for i, c in enumerate(checks, 1):
        c["id"] = f"{args.gate}-{i:02d}"

    print(json.dumps({"gate": args.gate, "artifactsDir": str(artifacts_dir),
                      "passed": passed, "checks": checks},
                     ensure_ascii=False, indent=2))
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()

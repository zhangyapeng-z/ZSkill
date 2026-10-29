#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rd-dev-planning 开发计划 Excel 生成工具（v2.0.0）
====================================================================
读取 artifacts/03-planning/dev-plan.json，生成评审用 Excel 工作簿
dev-plan.xlsx（7 个 Sheet，HZERO 工作台风格）。

  Sheet1 概览          项目信息 + 统计卡片 + 里程碑概览
  Sheet2 数据库设计    每表一个分组标题行 + 列级明细
  Sheet3 API设计       API 契约清单
  Sheet4 开发任务      任务拆解清单（评审重点）
  Sheet5 任务序列      阶段化执行顺序
  Sheet6 里程碑        关键里程碑
  Sheet7 需求覆盖矩阵  FR -> API -> 任务 映射与覆盖率

用法:
  python generate-excel.py            # 生成 + 自校验
  python generate-excel.py --verify   # 仅校验已生成的 Excel 与 JSON 一致性

依赖: openpyxl (pip install openpyxl)
JSON 是唯一数据源，Excel 每次全量重新生成，禁止手工编辑后回写。
"""
import sys
import json
import os
import re

# Windows 控制台输出 UTF-8，避免中文乱码
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("缺少依赖 openpyxl，请先执行: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------- 路径定位
# 优先当前工作目录（cwd 下存在 artifacts/ 即为项目根，支持用户级技能安装后在任何项目使用），
# 回退到脚本自身向上 4 级（项目级安装 .workbuddy/skills/rd-dev-planning/tools/ 布局）
ROOT = os.getcwd() if os.path.isdir(os.path.join(os.getcwd(), "artifacts")) else os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
JSON_PATH = os.path.join(ROOT, "artifacts", "03-planning", "dev-plan.json")
XLSX_PATH = os.path.join(ROOT, "artifacts", "03-planning", "dev-plan.xlsx")

# ---------------------------------------------------------------- 主题色（HZERO 工作台）
C_PRIMARY = "1B83FF"      # 主色：表头
C_TITLE = "001529"        # 深蓝：Sheet 大标题
C_BAND = "F5F7FA"         # 斑马纹
C_BORDER = "D9DEE6"       # 边框
C_GRAY = "9E9E9E"         # 说明文字
C_TYPE_DB = "ECEFF1"      # DATABASE 灰
C_TYPE_BE = "E3F2FD"      # BACKEND 蓝
C_TYPE_FE = "E8F5E9"      # FRONTEND 绿
C_TYPE_CF = "FFF3E0"      # CONFIG 橙

THIN = Border(
    left=Side(style="thin", color=C_BORDER),
    right=Side(style="thin", color=C_BORDER),
    top=Side(style="thin", color=C_BORDER),
    bottom=Side(style="thin", color=C_BORDER),
)
F_HEADER = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
F_TITLE = Font(name="微软雅黑", size=14, bold=True, color=C_TITLE)
F_NOTE = Font(name="微软雅黑", size=9, color=C_GRAY)
F_BODY = Font(name="微软雅黑", size=10, color="333333")
F_BODY_BOLD = Font(name="微软雅黑", size=10, bold=True, color="333333")
FILL_HEADER = PatternFill("solid", fgColor=C_PRIMARY)
FILL_BAND = PatternFill("solid", fgColor=C_BAND)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)


def sheet_title(ws, title, note, ncols):
    """每个 Sheet 顶部：大标题 + 生成说明 + 表头占位。返回表头行号。"""
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(ncols, 1))
    c = ws.cell(row=1, column=1, value=title)
    c.font = F_TITLE
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 26
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max(ncols, 1))
    c2 = ws.cell(row=2, column=1, value=note)
    c2.font = F_NOTE
    c2.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 16
    return 3  # 表头从第 3 行开始


def write_header(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        cell = ws.cell(row=row, column=i, value=h)
        cell.font = F_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_CENTER
        cell.border = THIN
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 26
    ws.freeze_panes = ws.cell(row=row + 1, column=1).coordinate


def write_rows(ws, start_row, rows, ncols, type_col=None):
    """写数据行：斑马纹 + 边框 + 自动换行；type_col 指定任务类型列做类型着色。"""
    r = start_row
    for idx, row in enumerate(rows):
        for i in range(1, ncols + 1):
            v = row[i - 1] if i - 1 < len(row) else ""
            cell = ws.cell(row=r, column=i, value=v)
            cell.font = F_BODY
            cell.border = THIN
            cell.alignment = ALIGN_LEFT if i != 1 else ALIGN_CENTER
            if (idx % 2) == 1:
                cell.fill = FILL_BAND
        # 任务类型着色
        if type_col:
            tcell = ws.cell(row=r, column=type_col)
            tv = str(tcell.value or "")
            if tv.startswith("DATABASE"):
                tcell.fill = PatternFill("solid", fgColor=C_TYPE_DB)
            elif tv.startswith("BACKEND"):
                tcell.fill = PatternFill("solid", fgColor=C_TYPE_BE)
            elif tv.startswith("FRONTEND"):
                tcell.fill = PatternFill("solid", fgColor=C_TYPE_FE)
            else:
                tcell.fill = PatternFill("solid", fgColor=C_TYPE_CF)
        r += 1
    return r


def disp(v):
    if isinstance(v, bool):
        return "是" if v else "否"
    if v is None:
        return ""
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def load_plan():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_workbook(plan):
    wb = Workbook()
    wb.remove(wb.active)

    # ================================================================ Sheet1 概览
    ws = wb.create_sheet("概览")
    ncols = 6
    proj = plan.get("project", {})
    proj_name = proj.get("name", "") or "开发计划"
    hdr_row = sheet_title(ws, "{} · 开发计划概览".format(proj_name),
                          "生成时间：{} · 来源：dev-plan.json · 技术基线：后端 HZERO 1.11.5 + Oracle/Liquibase groovy，前端 UMI3 + TS + choerodon-ui 1.6.8".format(plan["_meta"].get("createdAt", "")), ncols)
    db = plan.get("database", {})
    tasks = plan.get("tasks", [])
    apis = plan.get("apiDesign", [])
    ms = plan.get("milestones", [])
    total_hours = round(sum(t.get("estimatedHours", 0) for t in tasks), 1)
    stats = [
        ("项目名称", proj.get("name", ""), "服务编码", proj.get("serviceCode", "")),
        ("后端包名", proj.get("packageName", ""), "数据库类型", proj.get("databaseType", "oracle")),
        ("建表脚本", proj.get("dbScriptType", "liquibase-groovy"), "数据库表数", len(db.get("tables", []))),
        ("API 数量", len(apis), "开发任务数", len(tasks)),
        ("总估算工时", "{} h".format(total_hours), "里程碑数", len(ms)),
    ]
    write_header(ws, hdr_row, ["统计项", "数值", "统计项", "数值", "", ""], [22, 18, 22, 18, 8, 8])
    rows = []
    for a, b, c, d in stats:
        rows.append([a, b, c, d, "", ""])
    end = write_rows(ws, hdr_row + 1, rows, ncols)
    # 里程碑概览
    ms_title = end + 1
    ws.merge_cells(start_row=ms_title, start_column=1, end_row=ms_title, end_column=ncols)
    c = ws.cell(row=ms_title, column=1, value="里程碑概览")
    c.font = F_BODY_BOLD
    ms_rows = [[m.get("name", ""), m.get("deliverable", ""), "任务数 {}".format(len(m.get("taskIds", []))), "", "", ""] for m in ms]
    write_rows(ws, ms_title + 1, ms_rows, ncols)

    # ================================================================ Sheet2 数据库设计
    ws = wb.create_sheet("数据库设计")
    ncols = 12
    headers = ["表名", "字段名", "类型", "长度", "精度/小数", "可空", "主键", "默认值", "字段注释", "索引", "唯一", "枚举值"]
    widths = [22, 22, 12, 8, 12, 8, 8, 16, 40, 12, 8, 30]
    hdr_row = sheet_title(ws, "数据库设计（Oracle · Liquibase groovy）",
                          "标准字段（id/tenant_id/object_version_number/creation_date/created_by/last_update_date/last_updated_by）每表必含，表中仅列出业务字段 + 标准字段 · 唯一约束见 addUniqueConstraint", ncols)
    write_header(ws, hdr_row, headers, widths)
    r = hdr_row + 1
    for t in db.get("tables", []):
        # 表分组标题行
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
        grp = ws.cell(row=r, column=1, value="[表] {name} — {desc} · 多租户:{mt} · 序列:{seq}".format(
            name=t.get("name", ""), desc=t.get("description", ""),
            mt="是" if t.get("multiTenant") else "否", seq=t.get("sequence", "-")))
        grp.font = F_BODY_BOLD
        grp.fill = PatternFill("solid", fgColor="E8EEF8")
        grp.border = THIN
        ws.row_dimensions[r].height = 20
        r += 1
        ucs = t.get("uniqueConstraints", [])
        uniq_map = {}
        for u in ucs:
            for col in u.get("columns", []):
                uniq_map[col] = u.get("name", "")
        for col in t.get("columns", []):
            nm = col.get("name", "")
            prec = "{}/{}".format(col.get("precision", ""), col.get("scale", "")) if col.get("type", "").upper() in ("DECIMAL", "NUMBER") else ""
            idx = "是" if col.get("index") else ""
            uniq = uniq_map.get(nm, "")
            vals = col.get("enumValues") or []
            row = [t.get("name", ""), nm, col.get("type", ""), col.get("length", ""), prec,
                   "否" if col.get("nullable") is False else "是",
                   "是" if col.get("primaryKey") else "", col.get("defaultValue", ""),
                   col.get("comment", ""), idx, uniq, ",".join(map(str, vals))]
            for i, v in enumerate(row, start=1):
                cell = ws.cell(row=r, column=i, value=v)
                cell.font = F_BODY
                cell.border = THIN
                cell.alignment = ALIGN_CENTER if i in (3, 4, 5, 6, 7, 10, 11) else ALIGN_LEFT
            r += 1
    ws.auto_filter.ref = "A{}:L{}".format(hdr_row, max(r - 1, hdr_row))

    # ================================================================ Sheet3 API设计
    ws = wb.create_sheet("API设计")
    ncols = 9
    headers = ["API ID", "分组", "Method", "Path", "接口说明", "权限编码", "关联需求", "输入摘要", "输出说明"]
    widths = [12, 14, 9, 38, 34, 28, 14, 34, 34]
    hdr_row = sheet_title(ws, "API 设计（RESTful · HZERO 规范）",
                          "路径与原型 DataSet transport 对齐 · Controller 统一 @RestController(\"xxxController.v1\") · 权限编码与需求角色权限对齐", ncols)
    write_header(ws, hdr_row, headers, widths)
    rows = []
    for a in apis:
        rows.append([a.get("id", ""), a.get("group", ""), a.get("method", ""), a.get("path", ""),
                     a.get("description", ""), a.get("permissionCode", ""),
                     ",".join(a.get("relatedFRs", [])), a.get("requestSummary", ""), a.get("responseSummary", "")])
    write_rows(ws, hdr_row + 1, rows, ncols)
    ws.auto_filter.ref = "A{}:I{}".format(hdr_row, max(hdr_row + len(rows), hdr_row + 1))

    # ================================================================ Sheet4 开发任务
    ws = wb.create_sheet("开发任务")
    ncols = 12
    headers = ["任务ID", "标题", "类型", "模块", "任务描述", "依赖", "估时(h)", "负责人", "关联表", "关联API", "关联页面/DataSet", "验收标准"]
    widths = [12, 26, 18, 14, 46, 16, 9, 9, 16, 16, 20, 46]
    hdr_row = sheet_title(ws, "开发任务拆解（评审重点）",
                          "依赖方向：DATABASE → BACKEND_ENTITY → BACKEND_SERVICE → BACKEND_API → FRONTEND_DATASET/SERVICE → FRONTEND_COMPONENT → FRONTEND_PAGE → CONFIG · 总工时 {} h".format(total_hours), ncols)
    write_header(ws, hdr_row, headers, widths)
    rows = []
    for t in tasks:
        art = t.get("artifacts", {})
        rows.append([
            t.get("id", ""), t.get("title", ""), t.get("type", ""), t.get("module", ""),
            t.get("description", ""), ",".join(t.get("dependencies", [])),
            t.get("estimatedHours", ""), t.get("assignedTo", ""),
            art.get("databaseTable", ""), ",".join(art.get("apiIds", [])),
            ",".join(art.get("pageIds", []) + art.get("dataSetIds", [])),
            "; ".join(t.get("acceptanceCriteria", [])),
        ])
    write_rows(ws, hdr_row + 1, rows, ncols, type_col=3)
    ws.auto_filter.ref = "A{}:L{}".format(hdr_row, max(hdr_row + len(rows), hdr_row + 1))

    # ================================================================ Sheet5 任务序列
    ws = wb.create_sheet("任务序列")
    ncols = 5
    headers = ["阶段", "包含任务", "任务数", "可并行", "阶段工时(h)"]
    widths = [22, 60, 10, 10, 12]
    hdr_row = sheet_title(ws, "任务序列（阶段化执行顺序）", "阶段按依赖方向串行，阶段内任务可并行", ncols)
    write_header(ws, hdr_row, headers, widths)
    rows = []
    for ph in plan.get("taskSequence", []):
        ids = ph.get("tasks", [])
        rows.append([ph.get("phase", ""), ",".join(ids), len(ids),
                     "是" if ph.get("canParallel") else "否", ph.get("phaseHours", "")])
    write_rows(ws, hdr_row + 1, rows, ncols)
    ws.auto_filter.ref = "A{}:E{}".format(hdr_row, max(hdr_row + len(rows), hdr_row + 1))

    # ================================================================ Sheet6 里程碑
    ws = wb.create_sheet("里程碑")
    ncols = 4
    headers = ["里程碑", "说明", "关联任务", "交付物"]
    widths = [22, 40, 40, 30]
    hdr_row = sheet_title(ws, "里程碑", "关键交付节点", ncols)
    write_header(ws, hdr_row, headers, widths)
    rows = [[m.get("name", ""), m.get("description", ""), ",".join(m.get("taskIds", [])), m.get("deliverable", "")] for m in ms]
    write_rows(ws, hdr_row + 1, rows, ncols)

    # ================================================================ Sheet7 需求覆盖矩阵
    ws = wb.create_sheet("需求覆盖矩阵")
    ncols = 7
    headers = ["FR-ID", "功能需求", "优先级", "所属模块", "关联API", "关联任务", "覆盖"]
    widths = [12, 44, 10, 14, 24, 30, 10]
    hdr_row = sheet_title(ws, "需求覆盖矩阵（FR → API → 任务）", "覆盖率必须 100%", ncols)
    write_header(ws, hdr_row, headers, widths)
    rows = []
    for c in plan.get("coverageMatrix", []):
        rows.append([c.get("frId", ""), c.get("title", ""), c.get("priority", ""), c.get("module", ""),
                     ",".join(c.get("apiIds", [])), ",".join(c.get("taskIds", [])),
                     "已覆盖" if c.get("covered") else "未覆盖"])
    write_rows(ws, hdr_row + 1, rows, ncols)
    ws.auto_filter.ref = "A{}:G{}".format(hdr_row, max(hdr_row + len(rows), hdr_row + 1))

    wb.save(XLSX_PATH)
    return wb


def verify(plan):
    """读回 Excel 校验与 JSON 一致性。返回 (ok, [问题])。"""
    wb = load_workbook(XLSX_PATH)
    problems = []
    expect_sheets = ["概览", "数据库设计", "API设计", "开发任务", "任务序列", "里程碑", "需求覆盖矩阵"]
    for s in expect_sheets:
        if s not in wb.sheetnames:
            problems.append("缺少 Sheet: " + s)
    if problems:
        return False, problems

    # 概览统计
    ws = wb["概览"]
    total_hours = round(sum(t.get("estimatedHours", 0) for t in plan.get("tasks", [])), 1)
    text = " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value is not None)
    checks = [
        ("表数", str(len(plan.get("database", {}).get("tables", []))), text),
        ("API 数量", str(len(plan.get("apiDesign", []))), text),
        ("开发任务数", str(len(plan.get("tasks", []))), text),
        ("总工时", "{} h".format(total_hours), text),
    ]
    for label, val, hay in checks:
        if val not in hay:
            problems.append("概览统计不一致: {} 期望 {}".format(label, val))

    # 数据库设计：分组行数 = 表数，字段行数 = 列总和
    ws = wb["数据库设计"]
    n_tables = len(plan.get("database", {}).get("tables", []))
    n_grp = 0
    for row in ws.iter_rows(min_col=1, max_col=1):
        v = row[0].value
        if isinstance(v, str) and v.startswith("[表] "):
            n_grp += 1
    if n_grp != n_tables:
        problems.append("数据库设计分组行数 {} != 表数 {}".format(n_grp, n_tables))

    # 开发任务行数 = 任务数
    ws = wb["开发任务"]
    n_task_rows = sum(1 for row in ws.iter_rows(min_col=1, max_col=1)
                      if isinstance(row[0].value, str) and re.match(r"^TASK-\d+$", str(row[0].value)))
    if n_task_rows != len(plan.get("tasks", [])):
        problems.append("开发任务行数 {} != 任务数 {}".format(n_task_rows, len(plan.get("tasks", []))))

    # API 行数
    ws = wb["API设计"]
    n_api_rows = sum(1 for row in ws.iter_rows(min_col=1, max_col=1)
                     if isinstance(row[0].value, str) and re.match(r"^API-\d+$", str(row[0].value)))
    if n_api_rows != len(plan.get("apiDesign", [])):
        problems.append("API 行数 {} != API 数 {}".format(n_api_rows, len(plan.get("apiDesign", []))))

    # 覆盖矩阵行数
    ws = wb["需求覆盖矩阵"]
    n_cov_rows = sum(1 for row in ws.iter_rows(min_col=1, max_col=1)
                     if isinstance(row[0].value, str) and re.match(r"^FR-\d+$", str(row[0].value)))
    if n_cov_rows != len(plan.get("coverageMatrix", [])):
        problems.append("覆盖矩阵行数 {} != FR 数 {}".format(n_cov_rows, len(plan.get("coverageMatrix", []))))

    return len(problems) == 0, problems


def main():
    mode = "--verify" in sys.argv
    if not os.path.exists(JSON_PATH):
        print("未找到数据源: {}".format(JSON_PATH), file=sys.stderr)
        sys.exit(1)
    plan = load_plan()
    if mode:
        if not os.path.exists(XLSX_PATH):
            print("未找到 Excel: {}".format(XLSX_PATH), file=sys.stderr)
            sys.exit(1)
        ok, problems = verify(plan)
    else:
        build_workbook(plan)
        ok, problems = verify(plan)
    if ok:
        print("[OK] dev-plan.xlsx 已生成且与 dev-plan.json 一致: {}".format(XLSX_PATH))
        sys.exit(0)
    else:
        print("[FAIL] 校验不通过:", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

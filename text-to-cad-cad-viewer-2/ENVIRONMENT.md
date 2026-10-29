# text-to-cad 技能集 · 本机环境约定（必读）

本目录下的 `text-to-cad-*` 8 个技能来自 [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)（MIT）v0.6.6，已针对本机适配并验证。

## 共享运行时（所有技能通用）

运行时**已预装**，不要重新 pip install：

```
VENV = D:/deskbook/桌面文件夹/WorkBuddy/text-to-cad-main/.venv/Scripts/python.exe
```

- `$VENV -m cadgen.cli <cmd>` 等价 `cadgen <cmd>`
- `$VENV -m cadgen.cli doctor <skill-dir>` 环境自检
- OCP CAD 内核 46MB 大包已装，重装成本高

## 技能清单与触发词

| 技能 | 用途 | 典型触发 |
| --- | --- | --- |
| text-to-cad-cad | 3D 参数化建模，STEP/STL/3MF/GLB 导出，几何测量 | 建模/3D模型/零件/法兰/支架 |
| text-to-cad-cad-viewer | 启动浏览器交互预览 | 预览模型/查看3D |
| text-to-cad-dxf | 2D DXF 图纸（激光/等离子切割轮廓） | DXF/2D图纸/切割轮廓 |
| text-to-cad-engineering-drawing | 工程制图 PDF（正交视图+标注+标题栏） | 工程图/零件图/2D视图 |
| text-to-cad-urdf | 机器人 URDF 描述编写与校验 | URDF/机器人模型 |
| text-to-cad-srdf | MoveIt2 SRDF 规划组 | SRDF/MoveIt |
| text-to-cad-sdf | Gazebo SDF 仿真模型 | SDF/Gazebo |
| text-to-cad-step-parts | 搜索 step.parts 标准件库（螺栓/轴承/电机） | 标准件/外购件/step.parts |

**未安装**（依赖硬件或窄场景）：gcode（需 OrcaSlicer）、bambu-labs（需 Bambu 打印机）、dfm/dfam-check（需 trimesh 分析栈）、sendcutsend（绑定商家）。需要时从上游仓库 `skills/` 目录补装。

## 已验证能力（2026-09-22 实测）

- 法兰盘建模（布尔+环形阵列）→ 四格式一次导出，5.9s
- 几何测量：体积误差 0.000%，bbox 精确
- URDF 校验：二连杆机械臂通过
- STEP→PNG 快照渲染（需 chromium headless-shell 1243，已装）
- CAD Viewer 交互预览 + 已发布线上版 https://cad-model-viewer.app.workbuddy.host/

## 踩坑记录（Windows）

1. Smart App Control 拦截 OCP 未签名 DLL → 关闭之（设置→隐私和安全→Windows 安全中心→应用和浏览器控制）
2. 沙箱内 node 子进程 EBUSY → 禁用沙箱跑 bundle
3. playwright chromium 版本错位（缓存 1244 vs 需要 1243）→ `$VENV -m playwright install chromium --only-shell`
4. build123d 0.11 无 `bd.Math` → 用标准库 math
5. 装饰器名是 `@threemf` 不是 `@three_mf`

## 跨工具使用（DataClaw / Cursor / Claude Code 等）

本技能集采用标准 SKILL.md 规范（frontmatter: name/description + references/），其他工具接入方式：

- **DataClaw / 任意支持 SKILL.md 的 agent**：把 `text-to-cad-*/` 目录整个复制/链接到该工具的技能目录即可；技能内命令都走绝对路径 venv 解释器，无 PATH 依赖
- **Claude Code**：`~/.claude/skills/` 下做目录链接：`mklink /D %USERPROFILE%\.claude\skills\text-to-cad-cad C:\Users\PC\.workbuddy\skills\text-to-cad-cad`
- **上游官方安装器**：`scripts/install/install-skills.sh --agent <codex|claude|gemini|universal>`（在 text-to-cad-main 仓库内执行，注意它装的是上游原版，不含本机适配）
- 共享前置条件只有两个：venv 存在 + Smart App Control 关闭

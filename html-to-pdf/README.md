# HTML to PDF Skill

使用 Playwright 将 HTML 文件转换为高质量 PDF 的 OpenClaw 技能。

## 🎯 功能特性

- ✅ 支持中文（UTF-8 编码）
- ✅ 保留 CSS 样式（颜色、字体、布局）
- ✅ 自动分页（避免表格/卡片被切断）
- ✅ A4 页面尺寸（可自定义）
- ✅ 打印优化（移除背景、优化字体）
- ✅ 支持本地文件和网络 URL

## 📦 安装

### 1. 安装 Python 依赖

```bash
pip3 install playwright
```

### 2. 安装浏览器（只需一次）

```bash
python3 -m playwright install chromium
```

### 3. 下载技能

```bash
# 选项 A：从技能市场安装（如果已发布）
openclaw skill install html-to-pdf

# 选项 B：手动下载到 ~/.qclaw/skills/
git clone https://github.com/your-repo/html-to-pdf ~/.qclaw/skills/html-to-pdf
```

## 🚀 使用方法

### 命令行使用

```bash
# 基本用法
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf

# 指定页面尺寸
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --format A3

# 自定义边距
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --margin-top 30mm

# 横向打印
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --landscape

# 不打印背景
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --no-background
```

### 在 OpenClaw 中使用

直接在对话中要求：

- "将 report.html 转换为 PDF"
- "把这个 HTML 文件转成 PDF"
- "生成 PDF 版本"

AI 会自动调用此技能。

### Python 代码调用

```python
from playwright.sync_api import sync_playwright
import os

def html_to_pdf(html_path, pdf_path):
    """将 HTML 文件转换为 PDF"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 加载 HTML
        html_abs = os.path.abspath(html_path)
        page.goto(f"file://{html_abs}", wait_until="networkidle")
        
        # 生成 PDF
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "20mm",
                "right": "15mm",
                "bottom": "20mm",
                "left": "15mm"
            }
        )
        
        browser.close()
```

## 📋 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | (必填) | 输入 HTML 文件路径 |
| `output` | (必填) | 输出 PDF 文件路径 |
| `--format` | A4 | 页面尺寸：A4, A3, Letter, Legal 等 |
| `--margin-top` | 20mm | 上边距 |
| `--margin-bottom` | 20mm | 下边距 |
| `--margin-left` | 15mm | 左边距 |
| `--margin-right` | 15mm | 右边距 |
| `--print-background` | true | 是否打印背景色/背景图 |
| `--landscape` | false | 是否横向打印 |
| `--scale` | 1.0 | 缩放比例 (0.1-2.0) |

## 🔧 故障排查

### 错误 1：`OSError: cannot load library 'libgobject-2.0'`

**原因：** 系统缺少 GTK 库（尝试使用 weasyprint 时出现）  
**解决：** 本技能使用 Playwright，不会出现此错误。请确认使用的是正确的脚本。

### 错误 2：`TimeoutError: waiting for selector "body" failed`

**原因：** HTML 文件加载超时  
**解决：** 增加超时时间，或检查 HTML 文件是否存在语法错误。

### 错误 3：`PermissionError: [Errno 13] Permission denied`

**原因：** 输出文件被占用或无写入权限  
**解决：** 关闭 PDF 阅读器，或换一个输出路径。

### 错误 4：`playwright command not found`

**原因：** Playwright 未安装或未在 PATH 中  
**解决：** 使用 `python3 -m playwright install chromium` 安装浏览器。

## 📸 示例

### 示例 1：转换本地 HTML 文件

```bash
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py \
    ~/Desktop/report.html \
    ~/Desktop/report.pdf
```

### 示例 2：批量转换

```bash
for html in ~/Desktop/*.html; do
    pdf="${html%.html}.pdf"
    python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py "$html" "$pdf"
done
```

### 示例 3：生成 A3 横向 PDF

```bash
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py \
    input.html \
    output.pdf \
    --format A3 \
    --landscape \
    --margin-top 10mm
```

## 🛠️ 技术细节

### 为什么选择 Playwright？

我们测试了多种 HTML-to-PDF 方案：

| 方案 | 中文支持 | CSS 支持 | 稳定性 | 速度 | 推荐度 |
|------|----------|----------|--------|------|--------|
| **Playwright** | ✅ 完美 | ✅ 完美 | ✅ 高 | ⚡ 中 | ⭐⭐⭐⭐⭐ |
| weasyprint | ✅ 完美 | 🟡 部分 | 🟡 中 | ⚡⚡ 快 | ⭐⭐⭐ |
| wkhtmltopdf | 🟡 需配置 | 🟡 部分 | 🟡 中 | ⚡⚡ 快 | ⭐⭐ |
| xhtml2pdf | 🟡 需配置 | ❌ 差 | ❌ 低 | ⚡⚡⚡ 最快 | ⭐ |

**结论：** Playwright 虽然需要下载浏览器（~180MB），但渲染效果最好，最适合生成专业报告。

### 依赖关系

```
html-to-pdf
├── python3
├── pip3
└── playwright (Python 包)
    └── chromium (浏览器, ~180MB)
```

## 📝 更新日志

- **v1.0.0** (2026-06-04): 初始版本
  - 支持 Playwright 转换
  - 支持命令行参数
  - 支持中文和 CSS 样式

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

- GitHub: https://github.com/openclaw/skills/html-to-pdf
- 技能市场: https://clawhub.com/skills/html-to-pdf

## 🙏 致谢

- Playwright 团队（提供优秀的浏览器自动化工具）
- OpenClaw 社区（提供技能开发框架）

---

**🎯 快速开始：**

```bash
# 1. 安装依赖
pip3 install playwright
python3 -m playwright install chromium

# 2. 使用技能
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf
```

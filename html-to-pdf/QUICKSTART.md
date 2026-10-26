# HTML to PDF Skill - 快速安装指南

## 🚀 5 分钟快速安装

### 步骤 1：安装 Python 依赖

```bash
pip3 install playwright
```

**预期输出：**
```
Successfully installed playwright-1.60.0 pyee-13.0.1 greenlet-3.5.1
```

---

### 步骤 2：安装 Chromium 浏览器

```bash
python3 -m playwright install chromium
```

**预期输出：**
```
Downloading Chrome for Testing 148.0.7778.96 ...
Chrome for Testing 148.0.7778.96 downloaded to /Users/xxx/Library/Caches/ms-playwright/chromium-1223
```

**注意：** 需要下载 ~180MB，耗时约 2-5 分钟（取决于网速）。

---

### 步骤 3：下载技能文件

#### 选项 A：从技能市场安装（推荐）

```bash
openclaw skill install html-to-pdf
```

#### 选项 B：手动下载

```bash
# 创建技能目录
mkdir -p ~/.qclaw/skills/html-to-pdf

# 下载技能文件（假设你已经创建了技能）
# 将以下文件放到 ~/.qclaw/skills/html-to-pdf/：
# - SKILL.md
# - README.md
# - USAGE.md
# - SUMMARY.md
# - _meta.json
# - html_to_pdf.py
# - test_skill.sh
# - example/test.html
```

---

### 步骤 4：运行测试

```bash
bash ~/.qclaw/skills/html-to-pdf/test_skill.sh
```

**预期输出：**
```
📄 HTML to PDF Skill - 安装测试
================================

1️⃣  检查 Python3...
✅ Python3 已安装: Python 3.14.3

2️⃣  检查 Playwright Python 包...
✅ Playwright 已安装

3️⃣  检查 Chromium 浏览器...
✅ Chromium 已安装

4️⃣  检查技能文件...
✅ 技能文件完整

5️⃣  运行转换测试...
正在转换测试文件...
✅ 转换成功！PDF 文件大小: 375.0 KB

6️⃣  清理测试文件...
✅ 测试文件已清理

================================
🎉 所有测试通过！HTML to PDF Skill 已成功安装。
```

---

### 步骤 5：首次转换

```bash
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py \
    ~/.qclaw/skills/html-to-pdf/example/test.html \
    ~/Desktop/test.pdf
```

**预期输出：**
```
📄 正在转换: /Users/xxx/.qclaw/skills/html-to-pdf/example/test.html
💾 输出到: /Users/xxx/Desktop/test.pdf
⚙️  参数: format=A4, margins=20mm/15mm/20mm/15mm
🚀 启动浏览器...
⏳ 加载 HTML 文件...
📸 生成 PDF...
✅ 转换成功！PDF 已保存到: /Users/xxx/Desktop/test.pdf
📊 文件大小: 375.0 KB
```

打开 `~/Desktop/test.pdf` 验证转换效果！

---

## 🔧 常见问题

### Q1：pip3 命令不存在？

**A：** 先安装 Python3。

- **macOS：** `brew install python3`
- **Ubuntu/Debian：** `sudo apt install python3 python3-pip`
- **Windows：** 从 https://www.python.org/downloads/ 下载

---

### Q2：Playwright 安装失败？

**A：** 尝试使用国内镜像源。

```bash
pip3 install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### Q3：Chromium 下载超时？

**A：** 设置代理或使用国内镜像。

```bash
# 方法 1：设置代理
export HTTPS_PROXY=http://proxy.example.com:8080
python3 -m playwright install chromium

# 方法 2：手动下载（然后放到缓存目录）
# 下载地址：https://cdn.playwright.dev/builds/cft/...
# 缓存目录：~/Library/Caches/ms-playwright/
```

---

### Q4：测试脚本报错 `command not found`？

**A：** 确认文件路径是否正确。

```bash
# 检查文件是否存在
ls -la ~/.qclaw/skills/html-to-pdf/test_skill.sh

# 如果不存在，重新下载技能
openclaw skill install html-to-pdf --force
```

---

### Q5：转换后的 PDF 中文显示不正常？

**A：** 在 HTML 的 CSS 中指定中文字体。

```css
body {
    font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif;
}
```

---

## 📚 更多资源

- **详细文档：** `~/.qclaw/skills/html-to-pdf/README.md`
- **使用示例：** `~/.qclaw/skills/html-to-pdf/USAGE.md`
- **技能总结：** `~/.qclaw/skills/html-to-pdf/SUMMARY.md`
- **官方文档：** https://playwright.dev/python/

---

## 🎯 下一步

安装成功后，你可以：

1. **转换自己的 HTML 文件：**
   ```bash
   python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf
   ```

2. **在 OpenClaw 中使用：**
   - 打开 OpenClaw 对话
   - 输入："将 `report.html` 转换为 PDF"
   - AI 会自动调用此技能

3. **集成到自己的 Python 项目：**
   ```python
   from playwright.sync_api import sync_playwright
   # 参考 USAGE.md 中的 Python API 示例
   ```

---

## 💡 技巧与最佳实践

### 技巧 1：批量转换

```bash
for html in *.html; do
    pdf="${html%.html}.pdf"
    python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py "$html" "$pdf"
done
```

### 技巧 2：优化 PDF 大小

```bash
# 不打印背景（减小文件大小）
python3 html_to_pdf.py input.html output.pdf --no-background

# 缩放 80%（减小文件大小）
python3 html_to_pdf.py input.html output.pdf --scale 0.8
```

### 技巧 3：自定义页面尺寸

```bash
# A3 横向打印（适合宽表格）
python3 html_to_pdf.py input.html output.pdf --format A3 --landscape
```

---

## 📞 获取帮助

- **GitHub Issues：** https://github.com/openclaw/skills/issues
- **技能市场：** https://clawhub.com/skills/html-to-pdf
- **官方文档：** https://docs.openclaw.ai/skills

---

**🎉 享受 HTML to PDF Skill 带来的便利吧！**

---

**文档版本：** 1.0.0  
**最后更新：** 2026-06-04  
**作者：** OpenClaw Community

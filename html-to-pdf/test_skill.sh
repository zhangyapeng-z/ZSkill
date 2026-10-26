#!/bin/bash
# HTML to PDF Skill - 快速测试脚本
# 用途：验证技能是否安装成功

set -e  # 遇到错误立即退出

echo "📄 HTML to PDF Skill - 安装测试"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 检查 Python3
echo "1️⃣  检查 Python3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✅ Python3 已安装: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 未安装，请先安装 Python3${NC}"
    exit 1
fi
echo ""

# 2. 检查 playwright Python 包
echo "2️⃣  检查 Playwright Python 包..."
if python3 -c "import playwright" 2>/dev/null; then
    echo -e "${GREEN}✅ Playwright 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  Playwright 未安装，正在安装...${NC}"
    pip3 install playwright
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Playwright 安装成功${NC}"
    else
        echo -e "${RED}❌ Playwright 安装失败${NC}"
        exit 1
    fi
fi
echo ""

# 3. 检查 Chromium 浏览器
echo "3️⃣  检查 Chromium 浏览器..."
PLAYWRIGHT_CACHE="$HOME/Library/Caches/ms-playwright"
if [ -d "$PLAYWRIGHT_CACHE/chromium-"* ]; then
    echo -e "${GREEN}✅ Chromium 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  Chromium 未安装，正在安装...${NC}"
    python3 -m playwright install chromium
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Chromium 安装成功${NC}"
    else
        echo -e "${RED}❌ Chromium 安装失败${NC}"
        exit 1
    fi
fi
echo ""

# 4. 检查技能文件
echo "4️⃣  检查技能文件..."
SKILL_DIR="$HOME/.qclaw/skills/html-to-pdf"
if [ -f "$SKILL_DIR/SKILL.md" ] && [ -f "$SKILL_DIR/html_to_pdf.py" ]; then
    echo -e "${GREEN}✅ 技能文件完整${NC}"
else
    echo -e "${RED}❌ 技能文件缺失，请重新安装技能${NC}"
    exit 1
fi
echo ""

# 5. 运行转换测试
echo "5️⃣  运行转换测试..."
TEST_HTML="$SKILL_DIR/example/test.html"
TEST_PDF="/tmp/html-to-pdf-test.pdf"

if [ ! -f "$TEST_HTML" ]; then
    echo -e "${YELLOW}⚠️  测试文件不存在，跳过转换测试${NC}"
else
    echo "正在转换测试文件..."
    python3 "$SKILL_DIR/html_to_pdf.py" "$TEST_HTML" "$TEST_PDF" --format A4
    
    if [ -f "$TEST_PDF" ]; then
        FILE_SIZE=$(ls -lh "$TEST_PDF" | awk '{print $5}')
        echo -e "${GREEN}✅ 转换成功！PDF 文件大小: $FILE_SIZE${NC}"
        echo "测试 PDF 已保存到: $TEST_PDF"
    else
        echo -e "${RED}❌ 转换失败${NC}"
        exit 1
    fi
fi
echo ""

# 6. 清理测试文件
echo "6️⃣  清理测试文件..."
if [ -f "$TEST_PDF" ]; then
    rm "$TEST_PDF"
    echo -e "${GREEN}✅ 测试文件已清理${NC}"
fi
echo ""

# 完成
echo "================================"
echo -e "${GREEN}🎉 所有测试通过！HTML to PDF Skill 已成功安装。${NC}"
echo ""
echo "📖 使用方法："
echo "  python3 $SKILL_DIR/html_to_pdf.py input.html output.pdf"
echo ""
echo "📘 查看更多信息："
echo "  cat $SKILL_DIR/README.md"
echo ""

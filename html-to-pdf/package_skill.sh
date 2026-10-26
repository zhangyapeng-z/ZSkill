#!/bin/bash
# HTML to PDF Skill - 打包脚本
# 用途：将技能打包为 ZIP 文件，方便分发

set -e

SKILL_NAME="html-to-pdf"
SKILL_DIR="$HOME/.qclaw/skills/$SKILL_NAME"
OUTPUT_DIR="$HOME/Desktop"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$OUTPUT_DIR/${SKILL_NAME}_${TIMESTAMP}.zip"

echo "📦 HTML to PDF Skill - 打包脚本"
echo "================================"
echo ""

# 1. 检查技能目录是否存在
echo "1️⃣  检查技能目录..."
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：技能目录不存在: $SKILL_DIR"
    exit 1
fi
echo "✅ 技能目录存在: $SKILL_DIR"
echo ""

# 2. 检查必要文件是否存在
echo "2️⃣  检查必要文件..."
REQUIRED_FILES=(
    "SKILL.md"
    "README.md"
    "USAGE.md"
    "SUMMARY.md"
    "QUICKSTART.md"
    "_meta.json"
    "html_to_pdf.py"
    "test_skill.sh"
    "example/test.html"
)

ALL_FILES_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$SKILL_DIR/$file" ]; then
        echo "❌ 缺失文件: $file"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    echo "❌ 部分必要文件缺失，请先创建这些文件"
    exit 1
fi
echo "✅ 所有必要文件存在"
echo ""

# 3. 运行测试（确保技能正常工作）
echo "3️⃣  运行技能测试..."
if bash "$SKILL_DIR/test_skill.sh" > /dev/null 2>&1; then
    echo "✅ 技能测试通过"
else
    echo "⚠️  技能测试失败，是否继续打包？(y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "❌ 打包已取消"
        exit 1
    fi
fi
echo ""

# 4. 创建 ZIP 包
echo "4️⃣  创建 ZIP 包..."
cd "$SKILL_DIR/.."
zip -r "$OUTPUT_FILE" "$SKILL_NAME/" -x "*.DS_Store" -x "__MACOSX/*"
if [ $? -eq 0 ]; then
    echo "✅ ZIP 包创建成功: $OUTPUT_FILE"
else
    echo "❌ ZIP 包创建失败"
    exit 1
fi
echo ""

# 5. 显示打包信息
echo "5️⃣  打包信息："
FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
FILE_COUNT=$(find "$SKILL_DIR" -type f | wc -l | tr -d ' ')
echo "   文件大小: $FILE_SIZE"
echo "   文件数量: $FILE_COUNT"
echo "   输出路径: $OUTPUT_FILE"
echo ""

# 6. 生成校验和
echo "6️⃣  生成校验和..."
if command -v shasum &> /dev/null; then
    shasum -a 256 "$OUTPUT_FILE" > "${OUTPUT_FILE}.sha256"
    echo "✅ SHA256 校验和已保存: ${OUTPUT_FILE}.sha256"
else
    echo "⚠️  shasum 命令不存在，跳过校验和生成"
fi
echo ""

# 完成
echo "================================"
echo "🎉 打包完成！"
echo ""
echo "📋 下一步："
echo "  1. 上传到技能市场: https://clawhub.com/upload"
echo "  2. 分享 ZIP 包给其他人安装"
echo "  3. 使用以下命令安装："
echo "     openclaw skill install $OUTPUT_FILE"
echo ""

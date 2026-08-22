#!/bin/bash

# 狮子英语 API 启动脚本

echo "================================"
echo "🦁 狮子英语 API 启动脚本"
echo "================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo ""

# 检查依赖
echo "📦 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  未安装Flask，正在安装依赖..."
    pip3 install Flask Flask-CORS python-dotenv
else
    echo "✅ 依赖已安装"
fi
echo ""

# 检查Dict词库
if [ ! -d "./dict/book" ]; then
    echo "⚠️  警告: dict/book 目录不存在"
    echo "   请确保Dict词库ZIP文件在 dict/book/ 目录下"
    echo ""
fi

# 启动服务
echo "🚀 启动API服务..."
echo "================================"
echo ""

python3 app.py

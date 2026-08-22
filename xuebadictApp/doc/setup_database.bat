@echo off
chcp 65001 >nul
echo ========================================
echo  狮子英语 - 数据库快速导入工具
echo ========================================
echo.

cd /d "%~dp0xuebaApi"

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)
echo ✅ Python环境正常

echo.
echo [2/3] 开始导入词库数据...
echo.

python -c "import os, json, zipfile, sqlite3, uuid; from datetime import datetime; BOOKS_METADATA = [{'id': 'PEPXiaoXue3_1', 'title': '人教版小学英语-三年级上册', 'wordCount': 64, 'category': '小学', 'grade': 3, 'term': 1}, {'id': 'PEPXiaoXue3_2', 'title': '人教版小学英语-三年级下册', 'wordCount': 72, 'category': '小学', 'grade': 3, 'term': 2}]; conn = sqlite3.connect('lioneng.db'); cursor = conn.cursor(); cursor.execute('CREATE TABLE IF NOT EXISTS dict_books (id TEXT PRIMARY KEY, book_id TEXT UNIQUE NOT NULL, title TEXT NOT NULL, word_count INTEGER DEFAULT 0, category TEXT, tag TEXT, grade INTEGER, term INTEGER, popularity INTEGER DEFAULT 0, icon TEXT, zip_file TEXT, file_size INTEGER DEFAULT 0, created_at TEXT, updated_at TEXT)'); cursor.execute('CREATE TABLE IF NOT EXISTS dict_words (id TEXT PRIMARY KEY, book_id TEXT NOT NULL, word_rank INTEGER NOT NULL, head_word TEXT NOT NULL, uk_phone TEXT, us_phone TEXT, uk_speech TEXT, us_speech TEXT, translations TEXT, sentences TEXT, phrases TEXT, synonyms TEXT, rel_words TEXT, exams TEXT, content TEXT, created_at TEXT, UNIQUE(book_id, word_rank))'); cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_id ON dict_books(book_id)'); cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON dict_books(category)'); cursor.execute('CREATE INDEX IF NOT EXISTS idx_words_book_id ON dict_words(book_id)'); cursor.execute('CREATE INDEX IF NOT EXISTS idx_head_word ON dict_words(head_word)'); conn.commit(); print('✅ 数据表创建成功'); conn.close()"

if %errorlevel% neq 0 (
    echo ❌ 数据表创建失败
    pause
    exit /b 1
)

echo.
echo [3/3] 验证数据库...
python -c "import sqlite3; conn=sqlite3.connect('lioneng.db'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM dict_books'); book_count=cursor.fetchone()[0]; cursor.execute('SELECT COUNT(*) FROM dict_words'); word_count=cursor.fetchone()[0]; print(f'\n📊 数据库统计:'); print(f'  词书总数: {book_count}'); print(f'  单词总数: {word_count}'); conn.close()"

echo.
echo ========================================
echo  ✅ 数据库初始化完成！
echo ========================================
echo.
echo 📝 后续步骤：
echo    1. 运行 start_dev.bat 启动后端服务
echo    2. 运行 Flutter 应用测试播放功能
echo.
pause

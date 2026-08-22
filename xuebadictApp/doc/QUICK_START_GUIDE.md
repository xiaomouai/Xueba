# 狮子英语 API 快速开始指南

## 🎯 目标

5分钟内启动狮子英语API服务，并完成Dict词库数据导入。

---

## 📋 前置要求

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+ (可选)

---

## 🚀 快速启动

### 步骤1: 安装依赖

```bash
cd xuebadictApp/lioneng-api

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤2: 配置数据库

```bash
# 创建数据库
mysql -u root -p
```

```sql
CREATE DATABASE lioneng_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 步骤3: 配置环境变量

```bash
# 复制环境变量示例
cp .env.example .env

# 编辑 .env 文件
# 修改数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=lioneng_db
```

### 步骤4: 导入Dict词库数据

```bash
cd ..  # 回到 xuebadictApp 目录

# 方式1: 导入小学全系列（推荐，快速测试）
python import_dict_to_db.py --category 小学

# 方式2: 导入指定词书
python import_dict_to_db.py --books PEPXiaoXue3_1,PEPXiaoXue3_2

# 方式3: 导入所有词书（需要较长时间）
python import_dict_to_db.py --all
```

**导入进度示例:**
```
✅ 数据库连接成功

📋 创建数据表...
  ✅ dict_books 表创建成功
  ✅ dict_words 表创建成功

🚀 开始导入 8 个词书...
⏰ 开始时间: 2026-02-03 10:00:00

📚 导入词书: 人教版小学英语-三年级上册 (PEPXiaoXue3_1)
  📦 ZIP文件: 1521164661774_PEPXiaoXue3_1.zip
  📖 读取到 64 个单词
  ✅ 词书记录已插入
  ⏳ 已导入 50/64 个单词...
  ✅ 导入完成: 成功 64 个，失败 0 个

📚 导入词书: 人教版小学英语-三年级下册 (PEPXiaoXue3_2)
  📦 ZIP文件: 1521164656604_PEPXiaoXue3_2.zip
  📖 读取到 72 个单词
  ✅ 词书记录已插入
  ⏳ 已导入 50/72 个单词...
  ✅ 导入完成: 成功 72 个，失败 0 个

...

============================================================
📊 导入统计:
  总词书数: 8
  成功: 8
  失败: 0
⏰ 结束时间: 2026-02-03 10:05:30
============================================================
```

### 步骤5: 启动API服务

```bash
cd lioneng-api

# 开发模式启动
python app.py

# 或使用 Flask CLI
flask run --host=0.0.0.0 --port=5000
```

**启动成功输出:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 步骤6: 测试API

```bash
# 测试健康检查
curl http://localhost:5000/health

# 获取教材列表
curl http://localhost:5000/api/v1/textbooks

# 获取三年级上册单词列表
curl http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=10
```

---

## 📚 核心API使用示例

### 1. 用户注册

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "code": "123456",
    "password": "password123",
    "role": "student"
  }'
```

**响应:**
```json
{
  "code": 200,
  "msg": "注册成功",
  "data": {
    "user_id": "user_001",
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "is_new_user": true
  }
}
```

### 2. 获取词书列表

```bash
curl -X GET "http://localhost:5000/api/v1/textbooks/PEP/books?grade=3&category=小学" \
  -H "Authorization: Bearer {token}"
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "textbook": {
      "id": "PEP",
      "name": "人教版",
      "grade": 3,
      "category": "小学"
    },
    "books": [
      {
        "id": "PEPXiaoXue3_1",
        "title": "人教版小学英语-三年级上册",
        "wordCount": 64,
        "grade": 3,
        "term": 1,
        "isLocked": false
      },
      {
        "id": "PEPXiaoXue3_2",
        "title": "人教版小学英语-三年级下册",
        "wordCount": 72,
        "grade": 3,
        "term": 2,
        "isLocked": false
      }
    ]
  }
}
```

### 3. 获取单词列表

```bash
curl -X GET "http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=5" \
  -H "Authorization: Bearer {token}"
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "book": {
      "id": "PEPXiaoXue3_1",
      "title": "人教版小学英语-三年级上册",
      "wordCount": 64
    },
    "words": [
      {
        "wordRank": 1,
        "headWord": "hello",
        "usphone": "həˈloʊ",
        "ukphone": "həˈləʊ",
        "translation": "int. 你好；喂",
        "usspeech": "https://dict.youdao.com/dictvoice?audio=hello&type=2",
        "isLearned": false,
        "masteryLevel": 0
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 5,
      "total": 64,
      "total_pages": 13
    }
  }
}
```

### 4. 获取单词详情

```bash
curl -X GET "http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1" \
  -H "Authorization: Bearer {token}"
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "bookId": "PEPXiaoXue3_1",
    "wordRank": 1,
    "word": "hello",
    "ukphone": "həˈləʊ",
    "usphone": "həˈloʊ",
    "ukspeech": "https://dict.youdao.com/dictvoice?audio=hello&type=1",
    "usspeech": "https://dict.youdao.com/dictvoice?audio=hello&type=2",
    "translations": [
      {
        "pos": "int",
        "tranCn": "你好；喂",
        "tranOther": "used as a greeting"
      }
    ],
    "sentences": [
      {
        "sContent": "Hello, how are you?",
        "sCn": "你好，你好吗？"
      }
    ],
    "phrases": [
      {
        "pContent": "say hello",
        "pCn": "打招呼；问好"
      }
    ]
  }
}
```

### 5. 开始闯关练习

```bash
curl -X GET "http://localhost:5000/api/v1/units/unit_001/challenges?mode=normal" \
  -H "Authorization: Bearer {token}"
```

### 6. 开始听写练习

```bash
curl -X POST "http://localhost:5000/api/v1/units/unit_001/dictation/start" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "word_count": 10,
    "mode": "random"
  }'
```

---

## 🔍 数据验证

### 查询导入的数据

```sql
-- 查看词书列表
SELECT book_id, title, word_count, category, grade, term 
FROM dict_books 
ORDER BY grade, term;

-- 查看单词数量统计
SELECT book_id, COUNT(*) as word_count 
FROM dict_words 
GROUP BY book_id;

-- 查看某个词书的单词
SELECT word_rank, head_word, uk_phone, us_phone 
FROM dict_words 
WHERE book_id = 'PEPXiaoXue3_1' 
ORDER BY word_rank 
LIMIT 10;

-- 搜索单词
SELECT book_id, word_rank, head_word 
FROM dict_words 
WHERE head_word LIKE '%hello%';
```

---

## 📊 性能测试

### 测试单词查询性能

```bash
# 安装 Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# 并发测试
ab -n 1000 -c 10 http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=20
```

### 测试数据库查询性能

```sql
-- 查看查询执行计划
EXPLAIN SELECT * FROM dict_words WHERE book_id = 'PEPXiaoXue3_1' AND word_rank = 1;

-- 查看索引使用情况
SHOW INDEX FROM dict_words;

-- 查看表大小
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES
WHERE table_schema = 'lioneng_db'
    AND table_name IN ('dict_books', 'dict_words');
```

---

## 🐛 常见问题

### 1. 数据库连接失败

**问题:** `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**解决:**
```bash
# 检查MySQL服务是否启动
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql

# Mac
brew services start mysql
```

### 2. ZIP文件未找到

**问题:** `❌ 未找到ZIP文件`

**解决:**
```bash
# 确认Dict词库路径
ls xuebaBackend/dict/book/

# 如果没有ZIP文件，需要先下载
cd xuebaBackend/dict
python download.py
```

### 3. 导入速度慢

**问题:** 导入大量单词时速度较慢

**解决:**
```python
# 修改 import_dict_to_db.py
# 使用批量插入代替单条插入

# 方法1: 使用 executemany
self.cursor.executemany(insert_word_sql, word_values)

# 方法2: 禁用自动提交，手动批量提交
self.conn.autocommit = False
# ... 插入数据
self.conn.commit()
```

### 4. JSON字段查询

**问题:** 如何查询JSON字段中的数据

**解决:**
```sql
-- 查询包含特定翻译的单词
SELECT head_word, translations 
FROM dict_words 
WHERE JSON_CONTAINS(translations, '"你好"', '$[0].tranCn');

-- 查询有例句的单词
SELECT head_word 
FROM dict_words 
WHERE JSON_LENGTH(sentences) > 0;
```

---

## 📖 下一步

1. **完善用户系统**: 实现注册、登录、JWT认证
2. **实现学习功能**: 单词学习、闯关、听写
3. **集成AI服务**: 发音评测、智能诊断
4. **开发前端应用**: Flutter App 或 Web 前端
5. **部署上线**: Docker + Nginx + MySQL

---

## 🔗 相关文档

- [API重构总结](./API_REFACTORING_SUMMARY.md)
- [API接口文档](./mark市场运营策略/3.API接口)
- [Dict词库README](./xuebaBackend/dict/README.md)
- [Lion English API README](./lioneng-api/README.md)

---

**最后更新**: 2026-02-03  
**版本**: V2.0.0

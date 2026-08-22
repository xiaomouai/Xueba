# 🚀 快速测试指南

## 1️⃣ 测试数据库

```bash
cd xuebadictApp/lioneng-api
python test_db_api.py
```

**预期输出：**
```
🎉 所有测试通过！数据库集成成功！
总计: 6/6 通过
```

---

## 2️⃣ 启动API服务

```bash
python app.py
```

**预期输出：**
```
 * Running on http://127.0.0.1:5000
```

---

## 3️⃣ 测试API接口

### 方法1: 使用curl（推荐）

```bash
# 1. 获取小学三年级词书
curl "http://localhost:5000/api/v1/textbooks/PEP/books?category=小学&grade=3"

# 2. 获取三年级上册单词列表（前5个）
curl "http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=5"

# 3. 获取第一个单词详情
curl "http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1"

# 4. 搜索单词
curl "http://localhost:5000/api/v1/words/search?keyword=hello"
```

### 方法2: 使用浏览器

直接在浏览器中打开：

```
http://localhost:5000/api/v1/textbooks/PEP/books?category=小学
http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=5
http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1
http://localhost:5000/api/v1/words/search?keyword=hello
```

### 方法3: 使用Python

```python
import requests

# 获取词书列表
response = requests.get('http://localhost:5000/api/v1/textbooks/PEP/books', 
                       params={'category': '小学', 'grade': 3})
print(response.json())

# 获取单词列表
response = requests.get('http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words',
                       params={'page': 1, 'page_size': 5})
print(response.json())

# 获取单词详情
response = requests.get('http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1')
print(response.json())

# 搜索单词
response = requests.get('http://localhost:5000/api/v1/words/search',
                       params={'keyword': 'hello'})
print(response.json())
```

---

## 4️⃣ 查看数据库

```bash
# 进入SQLite命令行
sqlite3 lioneng.db

# 查看所有词书
SELECT book_id, title, word_count, category, grade FROM dict_books;

# 查看三年级上册的前10个单词
SELECT word_rank, head_word, us_phone FROM dict_words 
WHERE book_id = 'PEPXiaoXue3_1' 
ORDER BY word_rank 
LIMIT 10;

# 搜索包含"hello"的单词
SELECT book_id, word_rank, head_word FROM dict_words 
WHERE head_word LIKE '%hello%';

# 统计信息
SELECT category, COUNT(*) as book_count, SUM(word_count) as total_words 
FROM dict_books 
GROUP BY category;

# 退出
.quit
```

---

## 5️⃣ 常见问题

### Q: 数据库文件在哪里？
A: `xuebadictApp/lioneng-api/lioneng.db`

### Q: 如何重新导入数据？
A: 
```bash
rm lioneng.db
python db_import.py
```

### Q: API返回404错误？
A: 检查服务是否启动，URL是否正确

### Q: 如何查看API日志？
A: 查看终端输出，Flask会显示所有请求日志

### Q: 如何添加更多词书？
A: 
1. 在 `db_import.py` 的 `BOOKS_METADATA` 中添加词书元数据
2. 确保对应的ZIP文件在 `dict/book/` 目录
3. 运行 `python db_import.py`

---

## 6️⃣ 性能测试

```bash
# 测试搜索性能
time curl "http://localhost:5000/api/v1/words/search?keyword=hello"

# 测试单词查询性能
time curl "http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1"

# 测试列表查询性能
time curl "http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=20"
```

**预期性能：**
- 搜索: <50ms
- 单词查询: <10ms
- 列表查询: <50ms

---

## 7️⃣ 完整测试流程

```bash
# 1. 进入项目目录
cd xuebadictApp/lioneng-api

# 2. 测试数据库
python test_db_api.py

# 3. 启动服务（新终端）
python app.py

# 4. 测试API（另一个新终端）
curl "http://localhost:5000/api/v1/textbooks/PEP/books?category=小学"
curl "http://localhost:5000/api/v1/books/PEPXiaoXue3_1/words?page=1&page_size=5"
curl "http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1"
curl "http://localhost:5000/api/v1/words/search?keyword=hello"

# 5. 查看数据库
sqlite3 lioneng.db
SELECT * FROM dict_books LIMIT 5;
.quit
```

---

## ✅ 成功标志

如果看到以下输出，说明一切正常：

1. **数据库测试**: `🎉 所有测试通过！数据库集成成功！`
2. **API响应**: `{"code": 200, "msg": "success", "data": {...}}`
3. **性能**: 响应时间 <50ms

---

**快速测试完成！开始使用狮子英语API吧！** 🦁

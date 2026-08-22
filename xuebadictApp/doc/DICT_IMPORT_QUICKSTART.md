# 词书数据导入 - 快速开始

## 🚀 5分钟快速上手

### 1️⃣ 安装依赖（第一次使用）

```bash
pip install mysql-connector-python python-dotenv
```

### 2️⃣ 配置数据库

编辑 `.env.dict_import` 文件：

```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=xuebadict
```

### 3️⃣ 创建数据库

打开MySQL命令行或工具：

```sql
CREATE DATABASE xuebadict CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4️⃣ 运行导入

双击 `import_dict_to_mysql.bat`

或命令行运行：
```bash
python import_dict_to_mysql.py
```

### 5️⃣ 验证导入

双击 `verify_dict_import.bat`

或命令行运行：
```bash
python verify_dict_import.py
```

## ✅ 预期结果

导入成功后应该看到：

- ✓ 词书总数: 81
- ✓ 单词总数: 约200,000+
- ✓ 例句总数: 约600,000+
- ✓ 短语总数: 约400,000+

## 📝 数据库表

导入完成后会创建以下表：

| 表名 | 说明 | 预计记录数 |
|------|------|-----------|
| word_books | 词书信息 | 81 |
| words | 单词基本信息 | 200,000+ |
| word_translations | 单词释义 | 300,000+ |
| word_sentences | 例句 | 600,000+ |
| word_phrases | 短语 | 400,000+ |
| word_synonyms | 近义词 | 300,000+ |
| word_related | 同根词 | 200,000+ |

## 🔍 快速查询示例

### 查询所有词书

```sql
SELECT id, title, word_num, tags 
FROM word_books 
ORDER BY word_num DESC;
```

### 查询四级词书的单词

```sql
SELECT w.word_rank, w.head_word, w.us_phone
FROM words w
WHERE w.book_id = 'CET4luan_1'
ORDER BY w.word_rank
LIMIT 20;
```

### 查询单词详情（以 cancel 为例）

```sql
-- 基本信息
SELECT * FROM words WHERE head_word = 'cancel' LIMIT 1;

-- 释义
SELECT pos, tran_cn FROM word_translations 
WHERE word_id = (SELECT word_id FROM words WHERE head_word = 'cancel' LIMIT 1);

-- 例句
SELECT s_content, s_cn FROM word_sentences 
WHERE word_id = (SELECT word_id FROM words WHERE head_word = 'cancel' LIMIT 1);
```

## ❓ 常见问题

### Q: 导入失败怎么办？

检查：
1. MySQL是否已启动
2. 数据库配置是否正确
3. Python依赖是否已安装

### Q: 导入时间太长？

正常情况下：
- 小型词书（< 1000词）：1-2分钟
- 大型词书（> 10000词）：5-10分钟
- 全部81个词书：20-30分钟

### Q: 如何重新导入？

可以直接重新运行脚本，会自动覆盖已有数据。

或删除数据库后重新导入：
```sql
DROP DATABASE xuebadict;
CREATE DATABASE xuebadict CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📚 详细文档

更多详细信息请查看：[DICT_IMPORT_GUIDE.md](./DICT_IMPORT_GUIDE.md)

## 🎯 下一步

导入完成后，可以：

1. 在应用中使用这些词书数据
2. 开发单词学习功能
3. 实现单词搜索
4. 统计学习进度

---

**祝您使用愉快！** 🎉

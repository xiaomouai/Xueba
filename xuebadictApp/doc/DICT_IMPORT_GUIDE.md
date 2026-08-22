# 词书数据导入MySQL数据库 - 使用说明

## 📋 功能说明

本工具可以将 `xuebaApi/dict/book/` 目录下的所有词书数据（81个词书，包含约20万单词）导入到MySQL数据库中。

### 数据来源
- **来源**: 有道背单词(app) 词书数据
- **词书数量**: 81个
- **覆盖范围**: 
  - 考试类：四级、六级、考研、专四、专八、雅思、托福、GRE、SAT、GMAT、BEC
  - 教材类：人教版小学/初中/高中、北师大版高中、外研社版初中
  - 其他：新东方系列、中考必备、高考必备

## 📊 数据库表结构

### 1. `word_books` - 词书表
存储词书的基本信息（标题、封面、单词数量、来源等）

### 2. `words` - 单词表
存储单词的基本信息（单词、音标、发音参数等）

### 3. `word_translations` - 单词释义表
存储单词的中英文释义和词性

### 4. `word_sentences` - 例句表
存储单词的英文例句和中文翻译

### 5. `word_phrases` - 短语表
存储单词相关的短语和翻译

### 6. `word_synonyms` - 近义词表
存储单词的近义词

### 7. `word_related` - 同根词表
存储单词的同根词

## 🚀 使用步骤

### 步骤1: 安装依赖

```bash
pip install mysql-connector-python python-dotenv
```

### 步骤2: 配置数据库

编辑 `.env.dict_import` 文件，填入你的MySQL数据库配置：

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here  # 修改为你的密码
DB_NAME=xuebadict
DB_CHARSET=utf8mb4
```

### 步骤3: 创建数据库

在MySQL中创建数据库（如果还没有创建）：

```sql
CREATE DATABASE xuebadict CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 步骤4: 运行导入

**方式一：使用批处理脚本（推荐）**

双击运行 `import_dict_to_mysql.bat`

**方式二：使用Python命令**

```bash
python import_dict_to_mysql.py
```

### 步骤5: 等待导入完成

导入过程可能需要 10-30 分钟（取决于电脑性能），请耐心等待。

## 📁 目录结构

```
xuebaApi/
└── dict/
    ├── bookLists.txt           # 词书列表（JSON格式）
    ├── book/                   # 词书数据目录
    │   ├── *.zip              # ZIP压缩的词书文件
    │   ├── */                 # 解压后的词书目录
    │   │   └── *.json        # 词书数据文件
    │   └── *.json             # 直接的JSON文件
    ├── README.md              # 原始说明文档
    └── download.py            # 下载脚本
```

## 🔍 导入逻辑

1. **读取词书列表**: 从 `bookLists.txt` 读取81个词书的元数据
2. **创建数据库表**: 自动创建7个相关表
3. **导入词书信息**: 将词书元数据插入 `word_books` 表
4. **查找词书数据**:
   - 先查找已解压的目录
   - 如果没有，自动解压ZIP文件
   - 查找JSON数据文件
5. **导入单词数据**: 解析JSON并插入到相关表中
   - 单词基本信息 → `words` 表
   - 释义 → `word_translations` 表
   - 例句 → `word_sentences` 表
   - 短语 → `word_phrases` 表
   - 近义词 → `word_synonyms` 表
   - 同根词 → `word_related` 表

## 📝 数据示例

### 词书数据示例

| id | title | word_num | tags |
|----|-------|----------|------|
| CET4luan_1 | 四级真题核心词（图片记忆） | 1162 | 四级,有道 |
| CET6luan_1 | 六级真题核心词（图片记忆） | 1228 | 六级,有道 |
| PEPXiaoXue3_1 | 人教版小学英语-三年级上册 | 64 | 人教版 |

### 单词数据示例

**单词**: cancel

**音标**: 
- 美音: 'kænsl
- 英音: 'kænsl

**释义**:
- vt. 取消，撤销；删去
- vi. 取消；相互抵销
- n. 取消，撤销

**例句**:
- Our flight was cancelled. (我们的航班取消了。)
- I'm afraid I'll have to cancel our meeting tomorrow. (恐怕我得取消我们明天的会议。)

**短语**:
- cancel button (取消按钮)
- cancel out (取消；抵销)

**近义词**:
- recall, call it off, withdrawal, revocation

## 🔧 查询示例

### 1. 查询所有词书

```sql
SELECT id, title, word_num, tags 
FROM word_books 
ORDER BY recite_user_num DESC;
```

### 2. 查询特定词书的所有单词

```sql
SELECT w.word_rank, w.head_word, w.us_phone, w.uk_phone
FROM words w
WHERE w.book_id = 'CET4luan_1'
ORDER BY w.word_rank;
```

### 3. 查询单词的完整信息

```sql
-- 查询单词基本信息
SELECT * FROM words WHERE head_word = 'cancel';

-- 查询释义
SELECT * FROM word_translations WHERE word_id = 'CET4_3_1';

-- 查询例句
SELECT * FROM word_sentences WHERE word_id = 'CET4_3_1';

-- 查询短语
SELECT * FROM word_phrases WHERE word_id = 'CET4_3_1';
```

### 4. 按标签查询词书

```sql
SELECT * FROM word_books WHERE tags LIKE '%四级%';
SELECT * FROM word_books WHERE tags LIKE '%人教版%';
```

### 5. 统计信息

```sql
-- 每个词书的单词数量统计
SELECT b.title, COUNT(w.id) as word_count
FROM word_books b
LEFT JOIN words w ON b.id = w.book_id
GROUP BY b.id, b.title;

-- 每个词书的例句数量统计
SELECT b.title, COUNT(s.id) as sentence_count
FROM word_books b
LEFT JOIN words w ON b.id = w.book_id
LEFT JOIN word_sentences s ON w.word_id = s.word_id
GROUP BY b.id, b.title;
```

## ⚠️ 注意事项

1. **数据库权限**: 确保MySQL用户有创建表和插入数据的权限
2. **磁盘空间**: 确保有足够的磁盘空间（建议至少2GB）
3. **内存**: 建议至少4GB可用内存
4. **导入时间**: 完整导入可能需要10-30分钟
5. **中断处理**: 如果导入中断，可以重新运行（使用 ON DUPLICATE KEY UPDATE）
6. **字符编码**: 数据库必须使用 utf8mb4 编码以支持所有Unicode字符

## 🐛 常见问题

### Q1: 导入时提示"Access denied"
**A**: 检查数据库用户名和密码是否正确，以及用户是否有足够权限。

### Q2: 导入很慢或卡住
**A**: 这是正常现象，因为数据量较大。可以观察日志输出判断是否在正常进行。

### Q3: 部分词书导入失败
**A**: 可能是ZIP文件损坏或JSON格式问题，查看错误日志定位具体问题。

### Q4: 如何重新导入
**A**: 可以直接重新运行脚本，脚本会自动覆盖已存在的数据。或者先删除数据库再重新导入：

```sql
DROP DATABASE xuebadict;
CREATE DATABASE xuebadict CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📈 性能优化建议

1. **批量插入**: 脚本已使用批量提交优化性能
2. **索引优化**: 表已创建必要的索引
3. **内存配置**: 可以临时增大MySQL的 `innodb_buffer_pool_size`
4. **禁用外键检查**: 导入时可以临时禁用外键检查加速

```sql
SET FOREIGN_KEY_CHECKS = 0;
-- 导入数据
SET FOREIGN_KEY_CHECKS = 1;
```

## 📚 数据统计（预期）

- **词书总数**: 81个
- **单词总数**: 约200,000+
- **例句总数**: 约600,000+
- **短语总数**: 约400,000+
- **近义词记录**: 约300,000+
- **数据库大小**: 约1-2GB

## 🎯 后续使用

导入完成后，可以在应用中：

1. **词书列表**: 从 `word_books` 表读取所有词书
2. **单词学习**: 从 `words` 表按 `word_rank` 顺序学习
3. **单词详情**: 联合查询多个表获取完整信息
4. **搜索功能**: 按单词、释义、例句搜索
5. **统计分析**: 学习进度、掌握情况等

## 📧 技术支持

如遇到问题，请检查：
1. MySQL服务是否正常运行
2. 数据库配置是否正确
3. Python依赖是否已安装
4. 词书文件是否完整

---

**注意**: 本数据来源于有道背单词App，仅供学习研究使用。

# 前后端完整集成指南

## 📋 项目概述

本项目是一个完整的英语单词学习应用，包含：
- **后端API**: Flask + SQLite，提供完整的RESTful API
- **前端APP**: Flutter，支持Android/iOS
- **词库资源**: Dict词库（81个词书，153,009个单词）

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────┐
│          Flutter 前端应用                │
├─────────────────────────────────────────┤
│  HomePage  │  LibraryPage  │  Settings  │
│  学习页面   │   词库管理    │  设置页面   │
└─────────────┬───────────────┴───────────┘
              │ HTTP/JSON
              │
┌─────────────▼───────────────────────────┐
│         Flask 后端 API (5000)            │
├─────────────────────────────────────────┤
│  /api/v1/textbooks  │  教材管理         │
│  /api/v1/books      │  词书查询         │
│  /api/v1/words      │  单词学习         │
│  /api/v1/challenges │  闯关练习         │
│  /api/v1/dictations │  听写练习         │
│  /api/v1/auth       │  用户认证         │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│         SQLite 数据库                    │
│  dict_books  │  dict_words │  users    │
└─────────────────────────────────────────┘
```

---

## 🔧 后端API接口

### 1. 教材管理 (Textbook)

#### 1.1 获取教材版本列表
```http
GET /api/v1/textbooks
Query: ?category=小学

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "textbooks": [
      {
        "id": "PEP",
        "name": "人教版",
        "publisher": "人民教育出版社",
        "grades": [3, 4, 5, 6, 7, 8, 9],
        "categories": ["小学", "初中", "高中"]
      }
    ],
    "statistics": {
      "totalTextbooks": 1,
      "totalBooks": 13,
      "totalWords": 3169
    }
  }
}
```

#### 1.2 获取所有词书列表
```http
GET /api/v1/books
Query: ?category=小学&grade=3

Response:
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": "PEPXiaoXue3_1",
      "bookId": "PEPXiaoXue3_1",
      "title": "人教版小学英语-三年级上册",
      "wordCount": 64,
      "grade": 3,
      "term": 1,
      "category": "小学",
      "tag": "人教版",
      "icon": ""
    }
  ]
}
```

#### 1.3 获取词书单词列表（分页）
```http
GET /api/v1/books/{book_id}/words
Query: ?page=1&page_size=20

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "book": {
      "id": "PEPXiaoXue3_1",
      "title": "人教版小学英语-三年级上册",
      "wordCount": 64
    },
    "words": [
      {
        "id": "...",
        "book_id": "PEPXiaoXue3_1",
        "word_rank": 1,
        "head_word": "hello",
        "uk_phone": "həˈləʊ",
        "us_phone": "həˈloʊ",
        "translations": [{"pos": "int", "tranCn": "你好"}]
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 64,
      "total_pages": 4
    }
  }
}
```

### 2. 单词学习 (Word)

#### 2.1 获取单词详情
```http
GET /api/v1/words/{book_id}/{word_rank}

Response:
{
  "code": 200,
  "msg": "success",
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
    ],
    "synonyms": [],
    "relWords": [],
    "exams": [],
    "userLearning": {
      "isLearned": false,
      "masteryLevel": 0,
      "learnCount": 0
    }
  }
}
```

#### 2.2 更新单词学习状态
```http
POST /api/v1/words/{book_id}/{word_rank}/learn
Content-Type: application/json

Body:
{
  "action": "practice",
  "duration": 30,
  "is_correct": true,
  "score": 100
}

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "wordRank": 1,
    "word": "hello",
    "masteryLevel": 1,
    "nextReviewAt": "2026-02-04T10:30:00Z",
    "points_earned": 10,
    "exp_earned": 5
  }
}
```

#### 2.3 搜索单词
```http
GET /api/v1/words/search
Query: ?keyword=hello&book_id=PEPXiaoXue3_1&limit=50

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "keyword": "hello",
    "results": [...],
    "total": 1,
    "searchTime": 0.05
  }
}
```

### 3. 闯关练习 (Challenge)

#### 3.1 获取闯关题目
```http
GET /api/v1/units/{unit_id}/challenges
Query: ?mode=normal&difficulty=medium

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "challenge_id": "ch_abc123",
    "unit_id": "unit_001",
    "mode": "normal",
    "total_questions": 10,
    "time_limit": 300,
    "questions": [
      {
        "id": "q_001",
        "type": "choice",
        "bookId": "PEPXiaoXue3_1",
        "wordRank": 1,
        "word": "hello",
        "question": "hello 的中文意思是？",
        "options": ["你好", "再见", "谢谢", "对不起"],
        "correct_index": 0,
        "time_limit": 15,
        "points": 10
      }
    ]
  }
}
```

#### 3.2 提交闯关结果
```http
POST /api/v1/challenges/{challenge_id}/submit
Content-Type: application/json

Body:
{
  "answers": [
    {
      "id": "q_001",
      "answer": 0,
      "time_spent": 5
    }
  ],
  "total_time": 120
}

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "challenge_id": "ch_abc123",
    "correct_count": 8,
    "total_count": 10,
    "accuracy": 80,
    "stars": 2,
    "points_earned": 40,
    "exp_earned": 24
  }
}
```

### 4. 听写练习 (Dictation)

#### 4.1 开始听写
```http
POST /api/v1/units/{unit_id}/dictation/start
Content-Type: application/json

Body:
{
  "word_count": 10,
  "mode": "random",
  "include_phrases": false
}

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "dictation_id": "dict_abc123",
    "unit_id": "unit_001",
    "mode": "random",
    "total_words": 10,
    "words": [
      {
        "id": "dw_001",
        "bookId": "PEPXiaoXue3_1",
        "wordRank": 1,
        "word": "hello",
        "audio_url": "https://dict.youdao.com/dictvoice?audio=hello&type=2",
        "play_count": 3,
        "hint": "h____",
        "translation": "你好"
      }
    ],
    "time_limit": 600
  }
}
```

#### 4.2 提交听写结果
```http
POST /api/v1/dictations/{dictation_id}/submit
Content-Type: application/json

Body:
{
  "answers": [
    {
      "id": "dw_001",
      "input": "hello",
      "play_count": 2,
      "time_spent": 10
    }
  ],
  "total_time": 120
}

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "dictation_id": "dict_abc123",
    "score": 90,
    "correct_count": 9,
    "total_count": 10,
    "accuracy": 90,
    "results": [...],
    "points_earned": 45
  }
}
```

### 5. 用户认证 (Auth)

#### 5.1 用户注册
```http
POST /api/v1/auth/register
Content-Type: application/json

Body:
{
  "phone": "13800138000",
  "code": "123456",
  "password": "password123",
  "invite_code": "WELCOME"
}

Response:
{
  "code": 200,
  "msg": "注册成功",
  "data": {
    "user_id": "210a856ac56e4ba9983f51b5",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "is_new_user": true
  }
}
```

#### 5.2 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

Body:
{
  "phone": "13800138000",
  "password": "password123"
}

Response:
{
  "code": 200,
  "msg": "登录成功",
  "data": {
    "user_id": "326848d91da9496db5766bf7",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_info": {
      "nickname": "小明",
      "avatar": "https://...",
      "role": "student"
    }
  }
}
```

---

## 🎯 前端Flutter集成

### 1. 服务层架构

```dart
lib/services/
├── api_service.dart              // 通用HTTP请求封装
├── backend_api_service.dart      // 后端API专用服务
├── auth_service.dart             // 认证服务
├── version_service.dart          // 版本管理
└── word_spelling_service.dart    // 单词拼读
```

### 2. 核心服务使用示例

#### 2.1 获取词书列表
```dart
import 'package:xueba_app/services/backend_api_service.dart';

// 获取所有词书
final books = await BackendApiService.getBooks();

// 按分类获取词书
final primaryBooks = await BackendApiService.getBooks(
  category: '小学',
);

// 获取词书详情
final bookDetail = await BackendApiService.getBookDetail('PEPXiaoXue3_1');
```

#### 2.2 获取单词数据
```dart
// 获取词书单词列表（分页）
final wordsData = await BackendApiService.getWords(
  'PEPXiaoXue3_1',
  page: 1,
  pageSize: 20,
);

final words = wordsData['words'] as List;

// 获取单词详情
final wordDetail = await BackendApiService.getWordDetail(
  'PEPXiaoXue3_1',
  1, // word_rank
);
```

#### 2.3 更新学习状态
```dart
await BackendApiService.updateWordLearning(
  bookId: 'PEPXiaoXue3_1',
  wordRank: 1,
  action: 'practice',
  duration: 30,
  isCorrect: true,
  score: 100,
);
```

#### 2.4 闯关练习
```dart
// 获取闯关题目
final challenge = await BackendApiService.getUnitChallenges(
  unitId: 'unit_001',
  mode: 'normal',
  difficulty: 'medium',
);

// 提交闯关结果
final result = await BackendApiService.submitChallenge(
  challengeId: challenge!['challenge_id'],
  answers: [
    {'id': 'q_001', 'answer': 0, 'time_spent': 5}
  ],
  totalTime: 120,
);
```

#### 2.5 听写练习
```dart
// 开始听写
final dictation = await BackendApiService.startDictation(
  unitId: 'unit_001',
  wordCount: 10,
  mode: 'random',
);

// 提交听写结果
final result = await BackendApiService.submitDictation(
  dictationId: dictation!['dictation_id'],
  answers: [
    {'id': 'dw_001', 'input': 'hello', 'time_spent': 10}
  ],
  totalTime: 120,
);
```

### 3. HomePage 单词学习集成

```dart
// 从后端API加载单词
Future<void> _loadWordsFromAPI() async {
  if (_currentBookId == null) return;
  
  try {
    // 获取词书单词
    final words = await BackendApiService.getBookWords(
      _currentBookId!,
      page: 1,
      pageSize: 100,
    );
    
    setState(() {
      _unitWords = words;
      _isLoadingUnitWords = false;
    });
    
    // 开始学习第一个单词
    if (_unitWords.isNotEmpty) {
      await _selectWordForLearning();
    }
  } catch (e) {
    print('加载单词失败: $e');
    setState(() {
      _isLoadingUnitWords = false;
    });
  }
}

// 记录单词学习
Future<void> _recordWordLearning(String action, bool isCorrect) async {
  if (_currentWord == null || _currentBookId == null) return;
  
  await BackendApiService.updateWordLearning(
    bookId: _currentBookId!,
    wordRank: _currentWord!.wordRank ?? 0,
    action: action,
    duration: 30,
    isCorrect: isCorrect,
  );
}
```

### 4. LibraryPage 词库管理集成

```dart
// 从后端API加载词库列表
Future<void> _loadWordBooks() async {
  try {
    setState(() {
      _isLoading = true;
    });
    
    // 从API获取词书
    final booksData = await BackendApiService.getBooks();
    final wordBooks = booksData.map((data) => WordBook.fromJson(data)).toList();
    
    setState(() {
      _allWordBookItems = wordBooks.map((book) => WordBookItem(
        wordBook: book,
        status: WordBookStatus.downloaded, // API模式下词书已"下载"
      )).toList();
      _isLoading = false;
    });
  } catch (e) {
    print('加载词书失败: $e');
    setState(() {
      _isLoading = false;
      _errorMessage = '加载失败：$e';
    });
  }
}
```

---

## 🔌 启动和测试

### 1. 启动后端API

```bash
# 进入后端目录
cd xuebaApi

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 访问API文档
http://localhost:5000/api/docs
```

### 2. 启动Flutter应用

```bash
# 进入前端目录
cd xuebaAPP

# 安装依赖
flutter pub get

# 运行应用
flutter run
```

### 3. 配置API地址

编辑 `lib/config/api_config.dart`:

```dart
class ApiConfig {
  // 开发环境 - 本地API
  static const String devBaseUrl = 'http://localhost:5000';
  
  // 生产环境 - 部署后的API
  static const String prodBaseUrl = 'https://your-domain.com';
  
  // 是否使用生产环境
  static const bool isProduction = false;
  
  static String get baseUrl => isProduction ? prodBaseUrl : devBaseUrl;
  static String get apiPath => '$baseUrl/api/v1';
}
```

### 4. 测试API接口

```bash
# 测试健康检查
curl http://localhost:5000/health

# 测试获取词书列表
curl http://localhost:5000/api/v1/books

# 测试获取单词详情
curl http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1

# 测试搜索单词
curl "http://localhost:5000/api/v1/words/search?keyword=hello"
```

---

## 📊 数据库设计

### 1. dict_books 词书表

```sql
CREATE TABLE dict_books (
    id VARCHAR(32) PRIMARY KEY,
    book_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(100) NOT NULL,
    word_count INT,
    category VARCHAR(20),
    tag VARCHAR(20),
    grade INT,
    term INT,
    icon VARCHAR(255),
    popularity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. dict_words 单词表

```sql
CREATE TABLE dict_words (
    id VARCHAR(32) PRIMARY KEY,
    book_id VARCHAR(50) NOT NULL,
    word_rank INT NOT NULL,
    head_word VARCHAR(100) NOT NULL,
    uk_phone VARCHAR(100),
    us_phone VARCHAR(100),
    uk_speech VARCHAR(255),
    us_speech VARCHAR(255),
    translations JSON,
    sentences JSON,
    phrases JSON,
    synonyms JSON,
    rel_words JSON,
    exams JSON,
    content JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_book_rank (book_id, word_rank),
    INDEX idx_head_word (head_word),
    INDEX idx_book_id (book_id)
);
```

---

## 🚀 功能实现进度

### ✅ 已完成
- [x] 后端API基础架构
- [x] 教材和词书管理接口
- [x] 单词查询和学习接口
- [x] 闯关练习接口
- [x] 听写练习接口
- [x] 用户认证接口
- [x] 前端API服务层
- [x] HomePage基础集成
- [x] LibraryPage基础集成
- [x] SQLite数据库集成

### 🔄 进行中
- [ ] 用户学习数据持久化
- [ ] AI发音评测功能
- [ ] 单词拼读模式优化
- [ ] 完整的用户认证流程

### 📅 计划中
- [ ] 会员系统和支付
- [ ] 家长中心功能
- [ ] 错题诊断分析
- [ ] 成就系统
- [ ] 社交分享功能
- [ ] 离线缓存优化

---

## 📝 开发建议

### 1. API调用最佳实践

```dart
// ✅ 推荐：使用 try-catch 处理异常
try {
  final words = await BackendApiService.getBookWords('PEPXiaoXue3_1');
  // 处理数据
} catch (e) {
  print('API调用失败: $e');
  // 显示错误提示
}

// ✅ 推荐：检查返回数据
final wordDetail = await BackendApiService.getWordDetail('PEPXiaoXue3_1', 1);
if (wordDetail != null) {
  // 使用数据
} else {
  // 处理失败情况
}

// ❌ 不推荐：直接使用可能为null的数据
final words = await BackendApiService.getBookWords('PEPXiaoXue3_1');
print(words[0]); // 可能抛出异常
```

### 2. 状态管理建议

```dart
// 使用 setState 更新UI
setState(() {
  _words = newWords;
  _isLoading = false;
});

// 异步操作后检查 mounted
if (mounted) {
  setState(() {
    _words = newWords;
  });
}
```

### 3. 性能优化建议

- 使用分页加载大量数据
- 实现本地缓存减少API调用
- 使用防抖(debounce)处理搜索
- 图片和音频资源使用CDN

---

## 🐛 常见问题

### Q1: API连接失败
**A:** 检查：
1. 后端服务是否已启动（http://localhost:5000）
2. 前端配置的API地址是否正确
3. 防火墙是否阻止了连接
4. 模拟器/真机能否访问本地网络

### Q2: 词书数据为空
**A:** 确保：
1. 数据库文件存在（lioneng.db）
2. 数据已正确导入
3. API接口返回正确的数据格式

### Q3: 音频播放失败
**A:** 检查：
1. 网络连接是否正常
2. 有道发音API是否可用
3. 音频URL格式是否正确

---

## 📧 联系方式

- 项目地址: [GitHub仓库]
- 技术支持: support@lioneng.com
- 文档更新: 2026-02-04

---

**祝开发顺利！** 🎉

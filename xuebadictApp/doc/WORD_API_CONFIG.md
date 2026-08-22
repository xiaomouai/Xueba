# 单词API配置迁移说明

## 📋 修改概述

已将前端单词API从第三方接口迁移到本地后端API，并统一管理API配置。

---

## ✅ 已完成的修改

### 1. **API配置中心化** (`lib/config/api_config.dart`)

新增了单词API相关的配置：

```dart
// 单词搜索接口
static String get wordSearchUrl => '$apiPath/words/search';

// 单词详情接口
static String wordDetailUrl(String bookId, int wordRank) => 
    '$apiPath/words/$bookId/$wordRank';

// 词书单词列表接口
static String bookWordsUrl(String bookId) => 
    '$apiPath/books/$bookId/words';

// 今日推荐单词接口
static String get dailyRecommendUrl => '$apiPath/words/daily-recommend';
```

**优势：**
- 统一管理所有API URL
- 支持开发/生产环境切换
- 易于维护和更新

---

### 2. **英语单词API服务** (`lib/utils/english_word_api_service.dart`)

#### 修改前：
```dart
// 使用第三方API
static const String _baseUrl = 'https://v2.xxapi.cn/api/englishwords';
```

#### 修改后：
```dart
// 使用本地后端API
import '../config/api_config.dart';

// 方法1: 通过单词名称搜索
static Future<WordDetailResponse?> getWordDetails(String word) async {
  final uri = Uri.parse('${ApiConfig.wordSearchUrl}?keyword=$word&limit=1');
  // ...
}

// 方法2: 通过词书ID和序号直接获取
static Future<WordDetailResponse?> getWordDetailByRank(String bookId, int wordRank) async {
  final uri = Uri.parse(ApiConfig.wordDetailUrl(bookId, wordRank));
  // ...
}
```

**改进点：**
1. ✅ 从配置文件读取API地址
2. ✅ 增强了数据模型兼容性
3. ✅ 支持多种数据格式（List/Map/嵌套格式）
4. ✅ 添加了详细的错误日志

---

### 3. **数据模型增强**

#### WordDetailResponse
- 新增 `wordRank` 字段
- 增强 JSON 解析逻辑，支持多种数据格式

#### WordTranslation
- 新增 `tranOther` 字段（英文释义）
- 兼容多种字段命名：`tranCn` / `tran_cn`

#### WordSentence & WordPhrase
- 兼容驼峰和下划线命名：`sContent` / `s_content`

---

## 🔧 后端API说明

### API 1: 单词搜索
```
GET /api/v1/words/search?keyword={word}&limit=1
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "keyword": "hello",
    "results": [
      {
        "wordRank": 1,
        "headWord": "hello",
        "bookId": "PEPXiaoXue3_1",
        "bookTitle": "人教版小学英语-三年级上册"
      }
    ],
    "total": 1
  }
}
```

### API 2: 单词详情
```
GET /api/v1/words/{bookId}/{wordRank}
```

**响应示例：**
```json
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
    "sentences": {
      "sentences": [
        {
          "sContent": "Hello, how are you?",
          "sCn": "你好，你怎么样？"
        }
      ]
    },
    "phrases": {
      "phrases": [
        {
          "pContent": "say hello to",
          "pCn": "向...问好"
        }
      ]
    }
  }
}
```

---

## 🌍 环境配置

### 开发环境
```dart
// lib/config/api_config.dart
static const String devBaseUrl = 'http://localhost:5000';
static const bool isProduction = false;
```

实际调用URL: `http://localhost:5000/api/v1/words/search`

### 生产环境
```dart
static const String prodBaseUrl = 'https://your-domain.com';
static const bool isProduction = true;
```

实际调用URL: `https://your-domain.com/api/v1/words/search`

---

## 📝 使用示例

```dart
// 在Flutter代码中使用
import 'package:xueba_app/utils/english_word_api_service.dart';

// 方式1: 通过单词名称搜索（推荐）
final wordDetail = await EnglishWordApiService.getWordDetails('hello');

if (wordDetail != null) {
  print('单词: ${wordDetail.word}');
  print('英音: ${wordDetail.ukPhone}');
  print('美音: ${wordDetail.usPhone}');
  print('翻译: ${wordDetail.translations.first.tranCn}');
}

// 方式2: 通过词书ID和序号直接获取
final wordDetail2 = await EnglishWordApiService.getWordDetailByRank(
  'PEPXiaoXue3_1', 
  1
);
```

---

## 🔄 迁移前后对比

| 特性 | 修改前 | 修改后 |
|------|--------|--------|
| API地址 | 硬编码第三方URL | 配置文件管理 |
| 环境切换 | 不支持 | 支持开发/生产环境 |
| 数据来源 | 第三方API | 本地后端数据库 |
| 数据格式 | 固定格式 | 兼容多种格式 |
| 错误处理 | 静默失败 | 详细日志输出 |
| 维护性 | 依赖第三方 | 完全自主控制 |
| 性能 | 外部网络请求 | 本地网络请求 |
| 数据一致性 | 可能不一致 | 与词书完全一致 |

---

## ✨ 优势总结

### 1. **数据自主可控**
- 所有单词数据来自本地MySQL数据库
- 与词书数据完全一致，无需担心第三方API数据不准确

### 2. **性能提升**
- 本地网络请求，响应速度更快
- 减少对外部服务的依赖

### 3. **维护便捷**
- 统一的API配置管理
- 易于切换开发/生产环境
- 代码结构更清晰

### 4. **扩展性强**
- 可轻松添加新的单词API接口
- 支持未来的功能扩展

---

## 🚀 后续建议

1. **完善错误处理**
   - 添加重试机制
   - 实现离线缓存

2. **性能优化**
   - 实现单词详情本地缓存
   - 批量查询优化

3. **功能增强**
   - 添加单词收藏功能
   - 实现单词学习历史记录

---

## 📞 技术支持

如有问题，请查看：
- 后端API文档: `xuebaApi/api/word.py`
- 前端配置文件: `xuebaAPP/lib/config/api_config.dart`
- API服务类: `xuebaAPP/lib/utils/english_word_api_service.dart`

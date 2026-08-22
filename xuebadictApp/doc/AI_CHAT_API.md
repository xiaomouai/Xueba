# AI聊天接口文档

## 概述

本API提供统一的AI聊天接口，支持**千问(Qwen)**和**DeepSeek**两个AI提供商，自动进行服务降级和切换。

## 基础信息

- **Base URL**: `http://localhost:5000/api/v1`
- **Content-Type**: `application/json`
- **编码**: UTF-8

## 接口列表

### 1. AI聊天接口

**端点**: `POST /ai/chat`

发送消息给AI并获取回复，支持自定义系统提示词和对话历史。

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| message | string | 是 | 用户消息内容 |
| provider | string | 否 | AI提供商（qwen/deepseek），不指定则自动选择 |
| system_prompt | string | 否 | 系统提示词，定义AI的角色和行为 |
| conversation_history | array | 否 | 对话历史，格式：[{role, content}] |
| temperature | number | 否 | 温度参数（0-1），默认0.7 |
| max_tokens | integer | 否 | 最大token数，默认2000 |

#### 请求示例

```json
{
  "message": "请用英语说：你好，很高兴认识你！",
  "provider": "qwen",
  "system_prompt": "你是一位友好的英语老师，帮助学生学习英语。",
  "temperature": 0.7,
  "max_tokens": 100
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "content": "Hello, nice to meet you!",
    "provider": "qwen",
    "model": "qwen-plus"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "消息内容不能为空",
  "data": null
}
```

---

### 2. 获取AI提供商列表

**端点**: `GET /ai/providers`

获取所有可用的AI提供商及其配置信息。

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "providers": [
      {
        "id": "qwen",
        "name": "通义千问",
        "model": "qwen-plus",
        "enabled": true,
        "priority": 1
      },
      {
        "id": "deepseek",
        "name": "DeepSeek",
        "model": "deepseek-chat",
        "enabled": true,
        "priority": 2
      }
    ]
  }
}
```

---

### 3. 测试AI提供商连接

**端点**: `GET /ai/test/{provider}`

测试指定AI提供商的连接状态和响应时间。

#### 路径参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| provider | string | AI提供商ID（qwen/deepseek） |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "provider": "qwen",
    "status": "ok",
    "response_time": 1.23,
    "test_response": "Hello! How can I help you today?..."
  }
}
```

---

### 4. 获取预设提示词

**端点**: `GET /ai/prompts`

获取AI学习助手的预设系统提示词。

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "prompts": {
      "general": "你是一位友好的英语老师Luna...",
      "speaking": "You are an English speaking tutor...",
      "grammar": "你是一位英语语法专家...",
      "writing": "你是一位英语写作指导老师...",
      "translate": "你是一位专业的中英翻译...",
      "qa": "你是一位博学的百科助手...",
      "planning": "你是一位学习规划顾问...",
      "vocabulary": "你是一位词汇拓展专家..."
    }
  }
}
```

---

## 使用场景

### 场景1：通用聊天（自动选择提供商）

```json
POST /ai/chat
{
  "message": "Hello! How are you?",
  "system_prompt": "你是一位友好的英语老师。"
}
```

后端会自动选择可用且优先级最高的提供商（千问）。

### 场景2：指定提供商

```json
POST /ai/chat
{
  "message": "解释一下现在完成时",
  "provider": "deepseek",
  "system_prompt": "你是一位英语语法专家。"
}
```

强制使用DeepSeek进行回复。

### 场景3：带对话历史的多轮对话

```json
POST /ai/chat
{
  "message": "那我们从打招呼开始吧",
  "system_prompt": "你是一位友好的英语老师。",
  "conversation_history": [
    {"role": "user", "content": "你好，我想学习英语"},
    {"role": "assistant", "content": "你好！我很高兴帮助你。"},
    {"role": "user", "content": "我想学习日常对话"}
  ]
}
```

AI会基于对话历史提供连贯的回复。

---

## 自动降级机制

当指定的提供商不可用时，系统会自动尝试其他提供商：

1. **优先使用指定的provider**（如果有）
2. 如果失败，按priority顺序尝试其他provider
3. 所有provider都失败时返回错误信息

示例流程：
- 请求指定`provider: "qwen"`
- 千问API失败 → 自动尝试DeepSeek
- DeepSeek成功 → 返回DeepSeek的响应

---

## 前端集成

### Flutter示例

```dart
import 'package:xuebaAPP/services/ai_service.dart';

// 发送消息
final response = await AIService.chat(
  message: '你好',
  provider: 'qwen', // 可选
  systemPrompt: '你是一位友好的老师',
);

if (response.success) {
  print('AI回复: ${response.content}');
  print('使用的模型: ${response.provider} - ${response.model}');
} else {
  print('错误: ${response.error}');
}

// 获取提供商列表
final providers = await AIService.getProviders();
for (var p in providers) {
  print('${p.name} (${p.id}): ${p.enabled}');
}

// 测试连接
final testResult = await AIService.testProvider('qwen');
if (testResult.success) {
  print('连接成功，响应时间: ${testResult.responseTime}秒');
}
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误（如消息为空、提供商不存在） |
| 500 | 服务器错误（如所有AI服务不可用） |

---

## 提示词预设

系统提供8种预设提示词，对应不同的AI学习功能：

| 类型 | chatType | 说明 |
|------|----------|------|
| 通用聊天 | general | Luna老师，中英双语交流 |
| 口语对练 | speaking | 英语口语练习 |
| 语法讲解 | grammar | 语法规则讲解 |
| AI写作 | writing | 作文指导和修改 |
| AI翻译 | translate | 中英文翻译 |
| 百科问答 | qa | 回答各种问题 |
| 学习规划 | planning | 制定学习计划 |
| 词汇拓展 | vocabulary | 扩展词汇量 |

---

## 注意事项

1. **对话历史限制**：系统自动保留最近10条对话历史
2. **超时设置**：API请求超时时间为30秒
3. **重试机制**：单个提供商失败时会重试2次
4. **自动降级**：所有提供商失败后返回详细错误信息

---

## 测试方法

运行测试脚本：

```bash
# Windows
test_ai_chat.bat

# 或直接运行Python脚本
cd xuebaApi
python test_ai_chat.py
```

测试脚本会验证：
- 获取提供商列表
- 获取预设提示词
- 测试千问和DeepSeek连接
- 自动选择提供商
- 指定提供商
- 带对话历史的多轮对话
- 各种错误情况

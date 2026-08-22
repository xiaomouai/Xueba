# 千问 / DeepSeek 模拟 Provider 接入记录

## 1. 目标

在没有外部模型密钥、没有公网访问或只想做 Flutter 页面联调时，让现有 `/api/v1/ai/chat` 仍能选择 `qwen` 或 `deepseek`，并返回工作英语页面可以解析的内容。

## 2. 配置

### 模拟模式

```bash
AI_MODE=simulation python app.py
```

或：

```bash
AI_SIMULATION=true python app.py
```

模拟模式会注册 `qwen` 和 `deepseek` 两个 provider，即使没有 API key；不会访问外部网络。

### 真实模式

不设置模拟开关时保持 `live` 模式。只有对应的 API key 和 base URL 同时存在，provider 才会注册：

- 千问：`QWEN_API_KEY`、`QWEN_BASE_URL`、`QWEN_MODEL`。
- DeepSeek：`DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`、`DEEPSEEK_MODEL`。

真实密钥只放在运行环境，不写入代码、研究记录或客户端。

## 3. 模拟输出契约

- 知识请求：识别系统提示词中的 JSON 知识卡要求，返回 `EnglishKnowledge.fromJson` 所需的目标词、推荐说法、组织顺序、起手式、搭配、例句、语法、场景、短文、演讲和 3 条中文口语提示。
- speaking 请求：首次反馈要求用户重说；检测到 `Training phase: retry after feedback` 时返回场景通过提示。
- 其他 chat 请求：返回明确的模拟文本，不冒充真实模型结果。
- `/api/v1/ai/providers` 会暴露 `mode=simulation`，前端已有 provider 解析会忽略额外字段，不破坏兼容性。

## 4. 当前边界

- 本 task 只模拟 AI Chat；`/api/v1/ai/speech` 仍依赖现有语音服务，未伪造音频转写结果。
- 模拟内容是确定性联调数据，不用于评估千问或 DeepSeek 的真实回答质量。
- 已完成 Python AST、配置加载和模拟 provider 内容契约检查；Flask 运行时需要安装项目依赖后再做真实 API 联调。

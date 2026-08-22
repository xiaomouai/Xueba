# GitHub 开源复用记录：千问 / DeepSeek

## 结论

本次直接复用两个官方 Python SDK 的公开调用入口，并把返回值收敛到现有 Flask 的 `ChatResponse`，不复制整仓库：

| 来源 | 用途 | 许可证 | 实际采用 |
| --- | --- | --- | --- |
| [dashscope/dashscope-sdk-python](https://github.com/dashscope/dashscope-sdk-python) | 千问文本生成、DashScope 响应对象 | Apache-2.0 | `Generation.call` |
| [openai/openai-python](https://github.com/openai/openai-python) | DeepSeek OpenAI-compatible Chat Completions | Apache-2.0 | `OpenAI().chat.completions.create` |
| [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) | 核对 Qwen DashScope/OpenAI-compatible 参数 | Apache-2.0 | 只采用协议事实，不引入 Agent 框架 |
| [chippeddog/english.now](https://github.com/chippeddog/english.now) | AI 英语训练交互参考 | 以仓库当前声明为准 | 不导入；TypeScript/Expo 与 Flutter/Dart 基座不匹配 |

## 接入方式

默认仍是当前 `requests` HTTP 适配器：

```text
AI_CLIENT=http
```

需要直接调用官方 SDK 时显式切换：

```text
AI_CLIENT=official_sdk
```

此模式仍沿用现有 `QWEN_API_KEY/QWEN_BASE_URL`、`DEEPSEEK_API_KEY/DEEPSEEK_BASE_URL` 配置，不在日志或代码中输出密钥。千问 SDK 会将现有 native generation endpoint 归一为 `/api/v1`；DeepSeek SDK 会将完整 `/v1/chat/completions` URL 归一为 OpenAI client 所需的 base URL。

## 边界

- `AI_MODE=simulation` 优先使用本地确定性 provider，不导入或调用官方 SDK；Flutter 无需改变调用协议。
- 本次未把 Qwen-Agent、english.now、Nia 或其他整套应用复制进 `xuebadictApp`。
- 真实 SDK 网络调用需要安装依赖和有效服务密钥；本地静态检查不能替代真实额度/网络联调。

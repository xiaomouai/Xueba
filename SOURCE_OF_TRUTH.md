# 项目真源

这份文件规定 Agent 在本仓库中“先相信什么、修改哪里、如何判断完成”。产品真源是
[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md)；代码真源是 `xuebadictApp`。

## 1. 唯一生产实现线

| 内容 | 当前真源 | 规则 |
| --- | --- | --- |
| 生产产品目标与验收 | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) | 以最新用户要求和本文件的状态边界为准 |
| Flutter/Dart 客户端 | `xuebadictApp/xuebaAPP` | 所有新客户端功能、页面、权限和生产构建任务默认修改这里 |
| Flask/Python API | `xuebadictApp/xuebaApi` | 所有新接口、AI、语音、词库、账户和数据任务默认修改这里 |
| API 真实路由 | `xuebadictApp/xuebaApi/api/`、`app.py` | 以实际路由和响应为证据，不以旧文档标题为证据 |
| Flutter API 配置 | `xuebadictApp/xuebaAPP/lib/config/api_config.dart` | 开发/生产地址和构建注入方式以代码为准 |
| 生产部署材料 | `xuebadictApp/xuebaApi/Dockerfile.prod`、`docker-compose.prod.yml`、`docker-compose.nginx.yml` | 只能证明存在部署材料，不能证明已经部署成功 |

## 2. 非生产基座内容

以下内容保留，但不再是当前产品的新功能基座：

| 路径 | 定位 | 使用规则 |
| --- | --- | --- |
| `apps/mobile` | Nia 衍生 Flutter 参考实现 | 只在 task 明确要求迁移、对比或提取能力时读取/修改 |
| `apps/api` | Nia 衍生 Go API 参考实现 | 不作为狮子英语生产 API |
| `contracts/openapi.yaml` | Nia API 契约 | 不自动代表 `xuebaApi` 的 Flask 契约 |
| 根 `docs/` | Nia 架构、Firebase、Cloud Run 和 WebRTC 参考材料 | 不用来证明狮子英语的生产状态 |
| `xuebadictApp/doc/` | 历史集成、部署、测试和操作文档 | 只能作为线索；与实际代码冲突时以代码和 task 证据为准 |

## 3. 事实判断顺序

1. 当前用户要求。
2. 根 `AGENTS.md` 的协作和记录规则。
3. 本文件的基座边界。
4. `PRODUCT_SPEC.md` 的产品目标和验收条件。
5. `xuebadictApp` 的实际代码、配置、路由和数据库模型。
6. 运行命令、接口响应、安装包和公网页面等可复核证据。
7. README、注释、历史总结和生成文档只作参考。

## 4. 当前中文到英文链路事实

- 页面：`xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart`。
- AI 请求：客户端通过 `AIService.chat` 请求 `/api/v1/ai/chat`。
- AI provider：默认 `live` 模式按 `QWEN_API_KEY/QWEN_BASE_URL`、`DEEPSEEK_API_KEY/DEEPSEEK_BASE_URL` 注册真实 provider；`AI_CLIENT=http` 使用现有 requests 适配器，`AI_CLIENT=official_sdk` 复用 DashScope/OpenAI 官方 Python SDK；显式设置 `AI_MODE=simulation` 或 `AI_SIMULATION=true` 时注册无网络的 qwen/deepseek 模拟 provider。
- 语音请求：客户端录音后请求 `/api/v1/ai/speech`。
- 工作英语记录：客户端通过 `WorkEnglishApiService` 请求 `/api/v1/work-english/sessions`，服务端复用 `study_logs` 的 `module=work_english` 和 `details` 保存快照，并按 JWT 用户隔离。
- API 蓝图：`xuebadictApp/xuebaApi/api/ai/routes.py`。
- 当前没有被代码证实的独立 `POST /api/v1/knowledge` 生产接口；文档不得再把它写成现有事实。
- 当前页面的训练状态主要在客户端内存中；训练快照已具备服务端保存/查询/删除接口，但真实环境联调、历史重新打开和复习能力仍需单独验收。

## 5. 工作区保护

当前仓库和 `xuebadictApp` 都可能有用户未提交改动。Agent 必须：

- 修改前读取目标文件和相邻调用方。
- 只改当前 task 授权的文件。
- 不使用 `git reset --hard`、`git checkout --` 或递归删除清理工作区。
- 不把旧实现默默复制到 `apps/` 或从 `apps/` 反向覆盖 `xuebadictApp`。
- 外部开源代码引入时，在 task 结果中记录来源、许可证和实际采用范围。

## 6. 文档维护

- 产品变化先改 `PRODUCT_SPEC.md`。
- 代码基座或接口边界变化先改本文件。
- 架构长期决策确认后再写入 `docs/adr/`，并注明它属于 `xuebadictApp` 还是历史 Nia 参考线。
- 以后只允许有一个生产产品真源；不要再创建第二份同义的 `PRODUCT_PROD.md` 或复制版规格书。

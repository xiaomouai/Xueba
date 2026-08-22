# 工作英语 API 与 Flutter 联调记录

## 1. 本轮结论

工作英语页面原本已经调用现有 AI/语音接口，但训练快照只保存在 `SharedPreferences`。本轮补上最小服务端记录闭环：

```text
Flutter 页面
  → WorkEnglishApiService
  → /api/v1/work-english/sessions
  → JWT 当前用户
  → study_logs(module=work_english, details=快照)
```

AI 知识生成和口语反馈仍使用 `/api/v1/ai/chat`，语音转写仍使用 `/api/v1/ai/speech`，没有复制一套新的 AI 路由。

## 2. 实际接口

| 方法 | 路径 | 作用 | 权限 |
| --- | --- | --- | --- |
| POST | `/api/v1/work-english/sessions` | 创建或按 `session_id` 更新训练快照 | JWT 必需 |
| GET | `/api/v1/work-english/sessions?limit=20` | 当前用户的已完成训练列表 | JWT 必需 |
| GET | `/api/v1/work-english/sessions/<session_id>` | 当前用户读取一条快照 | JWT 必需 |
| DELETE | `/api/v1/work-english/sessions/<session_id>` | 当前用户删除一条快照 | JWT 必需 |

POST 请求核心字段：

- `source_zh`：必填，最多 2000 字符。
- `role_id`、`role_zh`、`scenario_id`、`scenario_zh`：必填，服务端校验长度。
- `scene_index`：0 到 2；`completed`：布尔值。
- `turns`：最多 12 条，每条包含场景序号、阶段、英文回答和反馈，服务端重新裁剪并保存。
- `session_id`：首次省略由服务端生成 32 位十六进制 ID；后续提交该 ID 实现幂等更新。

列表只返回 `completed=true` 的记录；详情和删除始终同时过滤 `id + user_id + module`，不接受客户端传入的用户 ID。

## 3. 前端行为

- 登录用户：页面进入时先请求服务端已完成记录；请求失败才回退本地历史。
- 保存训练：先写本地，随后请求 API；API 失败不会丢失本地训练，并显示同步失败提示。
- 未登录用户：维持原有本地保存，不伪造服务端记录。
- AI 与语音链路保持原调用方式，未新增 pubspec 依赖。

## 4. 真实边界

- 复用 `study_logs`，本轮没有新增表或迁移文件；开发环境的表创建仍依赖现有 Flask/数据库配置。
- 已完成源码级契约检查和 Python 静态编译检查；若本机缺少数据库、JWT 测试用户或 Flutter 工具链，不把它们写成真实联调通过。
- 当前列表可以回看摘要和快照，但页面尚未实现从服务端记录重新打开为可继续训练的完整复习流程。

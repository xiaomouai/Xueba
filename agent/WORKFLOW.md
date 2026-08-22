# 多 Agent 工作流

## 标准链路

```text
Coordinator → Researcher → Implementer → Reviewer → Recorder
```

小任务可以合并角色，但不能省略 task、日志和结果收据。Recorder 通常由 Coordinator
兼任。

## 开始任务

1. Coordinator 分配 `TASK-YYYYMMDD-NNN`。
2. 创建三份文件，并在 registry 登记：
   - `tasks/TASK-*.md`：目标、范围、验收条件、状态。
   - `logs/TASK-*.md`：过程事实和交接记录。
   - `results/TASK-*.md`：完成收据；开始时先建空框架，结束时补齐。
3. 先写 `start` 日志，再委派或修改代码。

## 交接格式

每次交给下一个 Agent 时，必须提供：

```text
Task: TASK-...
Role: researcher | implementer | reviewer | recorder
Done: 已完成的事实
Files: 读过或改过的绝对/仓库相对路径
Evidence: 命令、响应、截图或明确的未验证项
Decision: 已做的选择及原因
Next: 下一 Agent 只需要做什么
Blocker: 没有则写 none
```

## 日志时机

- `start`：目标、负责人、范围和初始状态。
- `progress`：完成一个可独立复核的阶段。
- `decision`：发生基座、接口、范围或冲突选择时。
- `handoff`：交接给另一个 Agent 时。
- `blocker`：外部依赖、权限、环境或事实不足导致无法继续时。
- `finish`：验收结果、实际文件和未完成边界。

## 收口流程

Reviewer 按 task 的验收条件逐条给出证据。Coordinator 根据证据更新 task 和 registry，
Recorder 在 `results/` 写完成收据：

- 全部满足：`completed`。
- 仍有条件不满足：`blocked`，写清阻塞原因和重新启动条件。
- 不确定的检查不能写成通过。

## 命名与索引

- 任务：`tasks/TASK-YYYYMMDD-NNN.md`
- 日志：`logs/TASK-YYYYMMDD-NNN.md`
- 结果：`results/TASK-YYYYMMDD-NNN.md`
- 总索引：[`tasks/registry.md`](../tasks/registry.md)

每个新任务都复制对应模板：[`TASK_TEMPLATE.md`](TASK_TEMPLATE.md)、
[`LOG_TEMPLATE.md`](LOG_TEMPLATE.md)、[`COMPLETION_TEMPLATE.md`](COMPLETION_TEMPLATE.md)。

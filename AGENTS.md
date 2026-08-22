# AGENTS.md

本文件是本仓库所有 Agent 的工作规则。开始任何任务前，先读本文件和
[`SOURCE_OF_TRUTH.md`](SOURCE_OF_TRUTH.md)。

## 1. 任务规则

- 没有 task ID 不开始工作。每个任务必须同时有三份文件：
  `tasks/TASK-*.md`、`logs/TASK-*.md`、`results/TASK-*.md`。
- 任务由协调 Agent 创建并登记到 [`tasks/registry.md`](tasks/registry.md)。
  ID 格式为 `TASK-YYYYMMDD-NNN`，由协调 Agent 统一分配。
- 任务必须写清目标、范围、验收条件、负责人和当前状态；子任务使用独立 ID，
  并在父任务中建立链接。
- 状态只使用：`planned`、`in_progress`、`blocked`、`completed`。
- 任务完成后必须写结果收据，记录交付物、证据、未完成边界和下一步；没有结果收据，
  不得把状态改为 `completed`。

## 2. 多 Agent 分工

- **Coordinator**：拆分任务、分配 ID 和负责人、维护 registry、处理冲突、汇总结果。
- **Researcher**：只读调查，输出文件路径、事实、证据和建议；不直接修改实现文件。
- **Implementer**：只修改 task 范围内的文件；写入前先读相邻代码；不覆盖其他 Agent 的改动。
- **Reviewer**：按验收条件检查 diff 和证据；只报告问题，除非被明确分配修复任务。
- **Recorder**：维护日志和结果收据；可以由 Coordinator 兼任。

一个 Agent 可以承担多个角色，但一个文件同一时间只能有一个写入负责人。并行任务
不得同时修改同一文件；需要共享文件时，先由 Coordinator 排队并记录决定。

## 3. 记录规则

- 每个任务至少记录四个节点：`start`、`progress/decision`、`handoff/blocker`、`finish`。
- 日志只记可复核事实：做了什么、改了哪些文件、依据是什么、下一步是什么。
- 不把“代码已写”“脚本已运行”“测试通过”“已部署”混为一谈；每种结论都要有对应证据。
- 遇到阻塞要立即记录原因、已排查内容和需要谁提供什么；不能用猜测伪造完成。
- 保留用户已有改动；禁止使用破坏性回滚命令清理工作区。

## 4. 完成门槛

Coordinator 只有在以下条件全部满足时才能收口：

1. 验收条件逐项有 `done` 或明确的未完成说明。
2. 任务文件、日志文件、结果收据和 registry 状态一致。
3. 结果收据列出实际改动路径和验证证据。
4. 已知限制、未运行的验证、外部依赖和后续任务均已写明。

详细流程和模板见 [`agent/WORKFLOW.md`](agent/WORKFLOW.md)。

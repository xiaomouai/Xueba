# 工作英语临场训练首发 MVP 研究记录

更新时间：2026-08-22 Asia/Shanghai
对应任务：`TASK-20260822-005`

## 1. 首发用户视角

我把自己放在一个中文母语外贸销售的位置：我知道 `quote`、`reliable`、`delay` 这些词，邮件也能看懂，但客户突然问价格、交期或下一步时，我无法快速组织成一段自然英文。真正的损失不是“少背一个单词”，而是回复慢、说得不专业、无法推进对话。

所以首发产品不以“查词”作为主任务，而以“今天这句工作话怎么说、我现在能不能说出来”为主任务。

## 2. 首发角色与场景

### 角色

1. 外贸销售：客户报价、跟进、谈价、交期沟通。
2. 客户支持：道歉、澄清、方案和问题升级。
3. 外企项目协作：会议汇报、风险说明和行动请求。

### 场景

- 报价跟进
- 确认需求
- 价格和条款谈判
- 交期延误
- 会议汇报
- 升级问题

每个场景拆成“首次表达、补充细节、推进下一步”三个小场景。没有完成重说，不允许直接进入下一个小场景。

## 3. 已实现的最小商业闭环

当前 Flutter 页面路径：

`xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart`

流程：

1. 选择工作角色和场景。
2. 输入中文工作意图，可选 EchoType 英文聚焦词和例句。
3. AI 生成目标表达、中文组织顺序、起手式、搭配、例句、语法、场景、短文和演讲。
4. 用户用英文文字或录音作答。
5. AI 只指出一个主要问题，并要求重说。
6. 用户重说后进入下一个小场景；完成三次迁移后结束。
7. 本地保存训练草稿和最近 20 次完成摘要。

## 4. 代码复用判断

### 已复用

- 本地 `echo-type` 项目：`https://github.com/Talljack/echo-type`。本次只复用已审计的 `business-english.json` 和 `daily-vocab.json` 资产，通过 `EchoTypeWordBookService` 作为语境参考，不复制其前端或桌面实现。
- 当前 xuebadictApp：复用 `AIService.chat`、`AIService.speechToText`、`RecorderService`、`ChatInputBar`、现有会员页面和 `shared_preferences`。

### 只作参考、未移植

- [Nia](https://github.com/bielcarpi/nia)：已有 Flutter/Go 的语音练习、反馈和历史概念，BSD 3-Clause；但它的 API、Firebase/Cloud Run 结构与当前 Flask 基座不同，本 task 不复制。
- [Speak Up Flutter](https://github.com/witchfindertr/speak_up_flutter)：有对话、发音和本地学习模块，但需要其 Firebase、Google Cloud 和独立架构；本 task 不引入新的服务依赖。
- [Google Project Euphonia App](https://github.com/google/project-euphonia-app)：重点是收集语音和训练定制 ASR，不是当前首发的工作表达产品；本 task 保留现有服务端语音转写。

## 5. 商业化验证

### 销售假设

- 免费：让用户完整体验一次三场景闭环。
- 9.9 元：7 天真实工作沟通急救，验证“愿不愿意把真实工作场景带进来并付钱”。
- 约 59 元/月 Pro：无限训练、历史复习、自定义场景和错误表达回练；价格只是待验证假设，不是已配置的生产商品。

### 7 天 go/no-go

- 10 名目标用户；每人提交至少 1 个真实工作场景。
- 5 人完成三场景训练。
- 3 笔真实 9.9 元付款或定金。
- 若没有付款/定金，只保留客户端 MVP，不继续扩展课程、词库和复杂会员功能。

## 6. 明确边界

- 客户端本地记录不是服务端持久化；还没有用户隔离、跨设备同步、删除和隐私策略闭环。
- 现有会员页面只是商业入口；本 task 没有新增或验收支付接口，也没有服务端权益 enforcement。
- 当前环境没有可用的 `dart`/`flutter` 命令，未执行 Flutter 构建、静态分析或设备/API 联调。
- EchoType 根项目 MIT 不自动证明每个词库文件都可再分发；已接入资产的许可边界以 `research/ECHOTYPE_WORDBOOK_IMPORT_20260822.md` 为准。

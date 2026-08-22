# 狮子英语（xuebadictApp）

这是一个以中文为入口、以英文开口训练为结果的 Flutter 英语学习 App。

用户可以输入中文想法、中文句子或中文场景，系统建立英文知识，并引导用户完成：

```text
中文想法 → 英文知识 → 英文开口 → 语音转写/AI反馈 → 必须重说 → 场景迁移 → 复习
```

## 唯一业务基座

- Flutter/Dart 客户端：[xuebadictApp/xuebaAPP](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP)
- Flask/Python API：[xuebadictApp/xuebaApi](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaApi)
- 产品生产文档：[PRODUCT_SPEC.md](/Users/wangliyan/Documents/englistapp/PRODUCT_SPEC.md)
- Agent 协作规则：[AGENTS.md](/Users/wangliyan/Documents/englistapp/AGENTS.md)
- 代码真源边界：[SOURCE_OF_TRUTH.md](/Users/wangliyan/Documents/englistapp/SOURCE_OF_TRUTH.md)

## 当前已有的业务能力

`xuebadictApp` 已包含词书、单词详情、学习记录、闯关、听写、账户、AI Chat、录音和语音转文字等
业务模块。中文→英文入口位于：

```text
xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart
```

当前生产目标不是另起一个新 App，而是把这些已有能力收敛到第一条可验收的英文口语闭环。

## 本地启动入口

后端：

```bash
cd xuebadictApp/xuebaApi
python app.py
```

Flutter 客户端：

```bash
cd xuebadictApp/xuebaAPP
flutter pub get
flutter run
```

API 健康检查和 Swagger 入口由 Flask 提供：

```text
GET  /health
GET  /api/v1/health
GET  /api/docs
```

本地启动成功不等于公网生产完成。生产验收、移动端构建、用户数据持久化和真实语音链路必须按
[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) 的门槛单独记录证据。

## Nia 参考材料

`apps/mobile`、`apps/api`、`contracts/` 和根 `docs/` 保留为历史 Nia 基座的参考/迁移材料，
不作为狮子英语当前生产实现线。任何要从这些目录提取能力的工作，都必须新建 task，写明来源、
许可证、目标文件和迁移范围。

## 协作方式

每项工作先创建唯一 task，同时维护 task 文件、过程日志和完成收据；详见
[`tasks/registry.md`](tasks/registry.md) 和 [`agent/WORKFLOW.md`](agent/WORKFLOW.md)。

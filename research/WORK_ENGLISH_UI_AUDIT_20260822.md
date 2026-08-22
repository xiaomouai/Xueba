# 工作英语 UI 体检与 Flutter/Dart 参考记录

更新时间：2026-08-22 Asia/Shanghai
对应任务：`TASK-20260822-006`

## 1. 体检范围

目标页面：

`xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart`

对照读取：

- `xuebadictApp/xuebaAPP/lib/utils/app_theme.dart`
- `xuebadictApp/xuebaAPP/lib/utils/responsive_helper.dart`
- `xuebadictApp/xuebaAPP/lib/pages/home/tabs/ai_study_tab.dart`

## 2. 体检结论

### 高优先级

1. setup 页面把词库和会员信息放在主开始按钮之前，用户需要滚动很长距离才能开始训练。
2. practice 页面先展示完整知识卡，中文提示和真正的英文输入动作被放在后面；这会把“学习资料”误放成“训练主任务”。
3. 进度只用文字“第 N/3 场景”，缺少比例反馈；重说状态虽然有文案，但视觉权重不够。

### 中优先级

1. 页面原先固定使用 `0xFF00C897`、白色、黑色等颜色，与 `AppTheme` 的主题色和暗色模式不一致。
2. setup 和 practice 内容没有宽度上限，桌面/平板会出现过宽的输入框和知识文本。
3. 词库例句是辅助参考，却使用完整卡片展开，增加了首屏噪音。

### 保留问题

- 页面状态、提示词和 UI 仍在一个 State 类中，约 900 行；本 task 不做大规模拆分，避免改变训练状态机。后续若继续扩展错误复习和历史页面，再拆成 `WorkEnglishSessionController` 与独立 widgets。

## 3. GitHub / Dart 参考

- [flutter/samples](https://github.com/flutter/samples)：Flutter 官方示例仓库，包含 Material 3、导航和可运行样例；本次采用“原生 Material 组件、少量代码、行为不变”的原则。
- [Material 3 demo](https://github.com/chayanforyou/flutter_material_3_demo)：展示 Flutter Material 3 的主题色、Typography、Chip、Card 和 ProgressIndicator；本次采用 `ColorScheme`、选中 Chip 和进度条的组合，不复制项目代码。
- [Flutter responsive layout guidance](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-build-responsive-layout/SKILL.md)：建议用 `LayoutBuilder` 测量可用宽度、用 `ConstrainedBox` 约束文本/表单；本次页面增加最大宽度 760 的内容约束。

没有新增第三方 UI 依赖。当前基座已使用 Material 3 和现有响应式工具，继续复用比移植一个完整 UI kit 更安全。

## 4. 本次实际优化

- setup：新增工作英语首屏 Hero、角色分组、场景分组、全宽开始按钮；把词库改为可展开参考，把会员卡压缩到主 CTA 之后。
- practice：将当前场景、中文提示和开口动作放到知识卡之前；完整知识改为折叠内容，保留全部搭配、例句、语法、文章和演讲。
- 主题：AppBar、卡片、Chip、对话气泡、提示文字和按钮改用 `Theme.of(context).colorScheme`，不再固定白底/黑字/绿色。
- 响应式：用 `LayoutBuilder` + `ConstrainedBox` 把宽屏内容收束到 760，手机仍保留滚动和底部输入栏。
- 训练可见性：三场景进度增加 `LinearProgressIndicator`，重说状态使用不同的 Material 3 容器色。

## 5. 验证边界

- 已做源文件结构检查、关键 widget/状态字符串检查和任务文档检查。
- 当前环境没有可用 `dart`/`flutter` 命令，未运行 `flutter analyze`、构建、截图、真机或横竖屏联调。
- 因此本记录证明“改动已落到源码”，不证明页面已在所有设备上通过视觉验收。

# EchoType 词库接入记录

更新时间：2026-08-22 Asia/Shanghai  
对应任务：`TASK-20260822-004`

## 1. 审计结论

- 本地项目：`echo-type`，远程仓库为 `https://github.com/Talljack/echo-type`。
- 审计版本：`c33d6d324126e93a91ec238f35c4db31f1f9f547`。
- EchoType 项目根许可证：MIT（见 `echo-type/LICENSE`）。
- 词库文件实际结构：JSON 数组，每项只有 `word` 和 `sentence` 两个字段。
- 词库文件没有逐本声明上游数据许可证；因此不能把项目 MIT 直接解释为全部词库内容可再分发。

## 2. 本次接入范围

只把首发“工作/外贸/外企沟通”闭环所需的两本词库复制为 Flutter 本地资产：

| EchoType 文件 | App 名称 | 条目数 | SHA-256 |
| --- | --- | ---: | --- |
| `public/wordbooks/business-english.json` | 工作英语例句 | 100 | `c2a3dcde6583f192ee7d12561509c91d0d8eb2d08d499aaa0f53fc8c4181a51c` |
| `public/wordbooks/daily-vocab.json` | 日常英语例句 | 100 | `d889a4f7093910a49a52df0ff025da9ecfcabd0ee3a0c3ff0c483e7513bcd0c1` |

目标资产：

- `xuebadictApp/xuebaAPP/assets/wordbooks/echo_type/business-english.json`
- `xuebadictApp/xuebaAPP/assets/wordbooks/echo_type/daily-vocab.json`

没有复制 Oxford、COCA、考试和教材词库到当前产品包；它们保留在 EchoType 源项目中，待逐本确认上游许可后再决定。

## 3. 产品接入方式

`xuebadictApp/xuebaAPP/lib/services/echo_type_wordbook_service.dart`：

- 从 Flutter asset 加载词库，缓存当前会话的解析结果。
- 提供精确匹配和前缀匹配，将英文聚焦词映射到词库例句。
- 将条目转换为当前 `WordData`，保留 `bookId`、序号、例句和来源信息。

`xuebadictApp/xuebaAPP/lib/pages/library_page.dart`：

- 在现有 API 词库前增加两本本地 EchoType 词库。
- 点击下载时直接读本地资产，不覆盖 API/MySQL 词库。
- 兼容现有缓存、选中词库和单元学习流程。

`xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart`：

- 增加“EchoType 例句库”选择和例句预览。
- 词库例句作为 AI 知识生成的语境参考，不直接替代中文意图，也不强迫用户背原句。
- 口语反馈继续要求英文作答、中文解释一个主要问题并再次表达。

## 4. 边界

- 本次是 Flutter 本地资产接入，不是数据库迁移；没有修改现有 `word_books`、`words` 或用户学习记录表。
- 资产导入不代表已经完成 Flutter 构建、API 联调或生产发布。
- 许可证确认之前，当前范围适合本地开发/验证；对外分发前需要逐本补齐来源和授权判断。

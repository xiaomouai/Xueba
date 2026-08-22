# xuebadictAPP 功能全景地图

> 盘点日期：2026-08-22  
> 盘点范围：`xuebadictApp/xuebaAPP`、`xuebadictApp/xuebaApi` 及其已接入资产  
> 盘点方式：只读代码、路由、模型、配置和资源清单；本次没有执行构建、测试或真实接口联调。

## 1. 结论先行

当前产品不是一个单一功能的背词 App，而是由两条能力线组成：

```text
传统英语学习线：词书/单词 → 学/读/练/拼/写 → 复习/统计/闯关/听写

中文到英文口语线：中文想法 → 英文知识 → 英文回答 → 语音转写/AI反馈
             → 必须重说 → 三场景迁移 → 本地/服务端保存
```

当前唯一生产代码基座是：

| 层 | 路径 | 定位 |
| --- | --- | --- |
| Flutter 客户端 | [`xuebadictApp/xuebaAPP`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP) | 当前 App 主线 |
| Flask API | [`xuebadictApp/xuebaApi`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaApi) | 当前后端主线 |
| 产品规则 | [`PRODUCT_SPEC.md`](/Users/wangliyan/Documents/englistapp/PRODUCT_SPEC.md) | 产品目标与验收边界 |
| 代码真源 | [`SOURCE_OF_TRUTH.md`](/Users/wangliyan/Documents/englistapp/SOURCE_OF_TRUTH.md) | 生产/参考目录边界 |

静态规模：Flutter `lib` 下 99 个 Dart 文件，其中 39 个页面、14 个服务、22 个工具、9 个模型、10 个通用组件；Flask API 目录有 106 个路由声明，其中支付模块和独立语音评测模块没有被主应用注册，不能直接按“已上线接口”计算。

最终判断：

- 功能面很宽，词书、单词、AI、口语、会员、签到、闯关、听写和后台能力都已经有代码入口。
- 最符合当前产品定位的是“中文想法 → 工作英语开口训练”闭环，入口在 `AI 智学 → 中文想法→英文`。
- 传统词汇链路有多处真实接口、模拟数据和旧契约并存，不能把页面存在当成联调完成。
- 工作英语的重说和三场景状态目前主要由 Flutter 客户端控制，服务端快照接口会校验字段，但尚未在服务端强制训练状态和 Pro 权益。

## 2. 端到端产品流程

### 2.1 启动与进入首页

```text
App 启动
  → 渲染兼容性/缓存/性能初始化
  → 自动更新检查
  → 是否完成引导
  → 是否登录
  → 首页 HomePage
```

启动路由和登录保护集中在 [`xuebadictApp/xuebaAPP/lib/main.dart`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP/lib/main.dart)：

- 未完成引导：`/onboarding`。
- 未登录：`/login`。
- 已登录：`/home`。
- 登录后页面通过 `authGuard` 保护。
- 支持中文/英文本地化、浅色/深色/羊皮纸/奶油色主题、字体缩放、响应式手机/平板/桌面布局。

### 2.2 首页五个 Tab

[`home_page.dart`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP/lib/pages/home_page.dart) 使用 `IndexedStack` 保留五个 Tab 的状态：

| Tab | 主要功能 | 当前状态 |
| --- | --- | --- |
| 单词 | 当前词书、学习进度、单元学习、错题、生词本、语音、闯关、签到 | 主链路代码已接入 |
| 计划 | 今日目标、今日任务、学习统计 | UI 有，目标和统计有硬编码示例值 |
| AI 智学 | 中文想法→英文、AI 对话、语法、写作、翻译、百科、规划、词汇拓展 | 入口已接入；部分工具只是统一 Chat 提示词 |
| 学习中心 | 绘本、听力、口语、视频、词汇竞赛 | 口语/竞赛有入口，绘本/听力/视频有占位行为 |
| 我的 | 昵称、会员、统计、个人信息、设置、反馈、关于 | 页面已接入；部分数据仍为静态或待服务端完善 |

## 3. Flutter 客户端全部功能

### 3.1 账户、引导和权限

页面：

- `OnboardingPage`：产品介绍、三步学习说明、完成引导并进入登录。
- `LoginPage`：手机号密码登录、手机号验证码登录、验证码倒计时、登录态保存；忘记密码和第三方登录目前是占位入口。
- `RegisterPage`：手机号、验证码、密码、确认密码、用户协议/隐私政策同意、新用户礼包提示。
- `GradeSelectPage`：小学一年级至初中九年级年级选择，并尝试按年级匹配教材。
- `PrivacyPolicyPage`：读取 `assets/privacy/privacy.md` 展示隐私政策。
- `FeedbackPage`：提交问题/建议/联系方式到后端。

认证服务 [`auth_service.dart`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP/lib/services/auth_service.dart) 提供：

- 初始化本地 token 和用户信息。
- 注册、密码登录、验证码登录。
- 发送验证码、刷新 token、退出登录。
- 读取/更新昵称、头像、角色、会员等级等用户信息。
- 统一生成 Bearer 请求头。

服务端认证路由：

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/send-code
POST /api/v1/auth/refresh-token
POST /api/v1/auth/logout
POST /api/v1/auth/reset-password
```

当前风险：后端认证文件中短信验证码校验、短信服务和 token 黑名单仍有 TODO/简化实现；前端忘记密码和第三方登录没有完整业务流。

### 3.2 词库和教材

页面/服务：

- `LibraryPage`：从 API 获取分类和词书，支持搜索、分类筛选、分页/无限滚动、下载状态、失败重试、选择当前词书、查看已下载词书。
- `CacheService`：缓存词书列表、词书单词、当前选中的词书 ID/名称。
- `GithubApiService`：从 GitHub/Gitee Markdown/CSV 解析词书和单词，并带默认降级数据。
- `EchoTypeWordBookService`：读取 App 资产中的 EchoType 本地词库。
- `LessonContentService`：为课文/句子内容保留的旧服务接口。

当前已导入的 EchoType 词库：

| 词库 | 资产 | 数量 | 用途 |
| --- | --- | ---: | --- |
| 工作英语例句 | `assets/wordbooks/echo_type/business-english.json` | 100 | 工作/客户/项目表达参考 |
| 日常英语例句 | `assets/wordbooks/echo_type/daily-vocab.json` | 100 | 日常生活、出行、社交参考 |

EchoType 词库会和后端词书一起出现在词库选择页；本地词库不需要网络，选择后转成 `WordData`，训练页可以按聚焦词查找例句。

### 3.3 单词学习主链路

#### 单词首页和控制器

`HomeController` 与 `WordLearningController` 负责：

- 加载用户资料和当前词书。
- 加载单词队列、当前单词、学习数量和掌握数量。
- 获取音节拆分。
- 标记掌握/取消掌握。
- 收藏/取消收藏。
- 切换前后单词。
- 保存或同步学习记录。

#### 单元学习

`UnitWordListPage` → `UnitLearningPage` 是传统单词学习的核心训练页面。每个词有五步：

```text
学 → 读 → 练 → 拼 → 写
```

具体包括：

- 词形、中文释义、词性、英/美音标。
- 单词标准音频和例句音频。
- 自然拼读/音节拆分/音素序列展示。
- “读”：按住录音并显示发音评分入口。
- “练”：选择正确含义。
- “拼”：点击字母拼出单词。
- “写”：输入单词并检查。
- “收藏”“掌握”“AI 学”入口。
- 前一词、下一词、上一步、下一步。

代码中“练”的干扰项是临时生成的错误选项；“读”流程在 `UnitLearningPage` 中目前以固定 95 分写入学习状态，并不是完整真实录音评测，见第 8 节风险清单。

#### 单词详情和复习

- `WordDetailPage`：展示单词详情、翻译、例句、短语、学习次数、记忆等级、掌握度、复习间隔、复习历史时间线和掌握度计算说明。
- `EnhancedWordReviewPage`：按日期查看学习情况，生成每日数据、正确/错误/困难/简单统计、趋势图和算法效果分析。
- `LearningReportPage`：展示词书学习报告和统计图表。
- `ErrorWordsPage`：错词列表、错误次数、最后错误时间、强化训练入口、清空错词。
- `FavoritesPage`：生词本列表、收藏时间、释义、移除收藏、开始学习。
- `SpacedRepetitionService`：按到期时间、记忆等级、学习次数排序；根据 forgot/hard/good/easy 计算下一次复习时间、间隔和难度系数。
- `LearningDataService`：本地学习记录、全局词记录、跨词书继承、最近复习、推荐词、统计、CSV 导入导出、清空数据、后端同步。

### 3.4 发音、音标、拼读和音频

客户端能力：

- `WordAudioService`：单词英式/美式发音、例句 TTS、播放/停止/预加载。
- `RecorderService`：录音开始、停止、是否录音、释放录音资源。
- `WordSpellingDialog` + `WordSpellingService`：字母拼读、音节拼读、音素拼读、自然拼读、批量拼读、发音信息。
- `PhoneticsPracticePage`：26 个字母、48 个国际音标、英式/美式 TTS、语速/音高调节、视频播放。
- `PhoneticCoursePage`：视频课程、音标卡片、音标说明；音标数据在页面内是示例数据。
- `LessonStudyPage`：英文句子、中文翻译、TTS 跟读、句子进度、完成弹窗；语音评测当前为模拟分数。
- 后端 `audio` 模块：音频代理、音节拆分、上传音频评测、TTS。
- 后端 `syllable_service`：优先 CMU Pronouncing Dictionary，使用 `eng_to_ipa` 和规则引擎兜底。
- 后端 `pronunciation_service`：SpeechRecognition/Google Web Speech 识别后进行文本匹配和启发式评分；当前没有音素级真实识别。

### 3.5 AI 智学和通用 AI Chat

AI 智学页内置九个工具：


| 工具 | 处理方式 |
| --- | --- |
| 中文想法→英文 | 进入 `ChineseToEnglishPage`，结构化知识 + 口语训练 |
| 百科问答 | 进入 AI Chat |
| 口语对练 | 进入 AI Chat |
| 语法讲解 | 进入 AI Chat |
| AI 写作 | 进入 AI Chat |
| AI 翻译 | 进入 AI Chat |
| 十万个为什么 | 进入 AI Chat |
| 学习规划 | 进入 AI Chat |
| 词汇拓展 | 进入 AI Chat |

`AIService` 统一调用：

- AI 聊天：`POST /api/v1/ai/chat`。
- 获取 Provider：`GET /api/v1/ai/providers`。
- 获取场景：`GET /api/v1/ai/scenes`、`GET /api/v1/ai/scenes/<scene_id>`。
- Provider 健康检查：`GET /api/v1/ai/health/<provider_id>`。
- 语音转文字：`POST /api/v1/ai/speech`。
- 提示词热加载：`POST /api/v1/ai/prompts/reload`。

后端 AI 场景配置目前包含：

```text
general       综合英语助手
speaking      口语练习
grammar       语法专家
writing       写作指导
translate     翻译助手
qa            百科问答
planning      学习规划
vocabulary   词汇拓展
```

AI 提供商和模式：

- 千问 Qwen：HTTP 适配器或 DashScope 官方 SDK。
- DeepSeek：HTTP 适配器或 OpenAI 兼容官方 SDK。
- simulation：无网络模拟 provider，用于本地演示，不等于真实模型质量。
- provider manager：按优先级、指定 provider、重试和失败降级处理。
- 提示词配置：`services/prompts/prompts.yaml`，支持基础片段、场景、中文/英文输出约束和热加载。

客户端还保留一条旧的本地 DeepSeek API Key 链路：`DeepSeekApiService` 用于造句判断、示例句生成和旧版 AI Chat；这与当前服务端统一 AI 链路并存，后续需要收敛。

### 3.6 中文环境 → 英文工作场景训练

入口：[`xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart)。

#### 角色

1. 外贸销售：推进客户沟通、报价和下一步。
2. 客户支持：稳定客户、确认问题、给出方案。
3. 外企项目协作：会议、进度、风险和行动对齐。

#### 场景

1. 报价跟进。
2. 确认需求。
3. 价格和条款谈判。
4. 交期延误。
5. 会议汇报。
6. 升级问题。

每个场景又有三个小阶段，例如首次表达、补充细节、推进下一步。

#### 知识卡输出

用户输入中文工作意图，可选输入英文聚焦词，AI 通过 `general` Chat 请求 JSON，页面解析并展示：

- 目标词。
- 中文释义。
- 词性。
- 音标。
- 直接可以说的推荐表达。
- 中文组织顺序。
- 开口起手式。
- 备用说法。
- 常用搭配。
- 例句。
- 语法提醒。
- 英文场景。
- 三个中文口语提示。
- 80–120 词短文。
- 60–90 秒演讲练习。

生成前会尝试从 EchoType 词库取一条例句作为参考，但提示词要求判断语境是否适合，不能机械复制。

#### 训练过程

```text
输入中文 → 选角色/场景 → 生成知识
  → 先按中文提示用英文回答
  → 文本回答或录音
  → 录音上传 /api/v1/ai/speech 转写
  → speaking Chat 返回鼓励、一个主要问题、一个自然修正
  → 必须重说并补充细节
  → 进入下一个场景
  → 三个场景完成后保存
```

页面当前已实现：

- “先说，再看完整知识”的界面顺序。
- 反馈后显示“请重说一次”。
- 未完成重说不能进入下一场景。
- 三场景进度和完成状态。
- 文字回答和录音转写后自动提交。
- 训练草稿写入 `SharedPreferences`。
- 已完成记录在本地最多保留最近 20 次。
- 登录后向服务端保存训练快照；失败时保留本地并提示稍后重试。
- Pro 入口复用 `MembershipPage`。

当前未完全具备：

- 服务端没有独立知识生成契约，知识仍复用 Chat + JSON 提示词。
- 服务端只保存快照字段，不判断“是否先回答、是否已重说、是否完成三个场景”。
- 服务端训练记录接口没有接入 Pro 权益检查。
- 历史列表可以读取摘要，但页面没有完整的历史训练重新打开/回练体验。

### 3.7 闯关、听写和趣味练习

#### 闯关

客户端：

- `ChallengeMainPage`：加载统计、历史、题型、难度、词书，创建挑战。
- `ChallengeGamePage`：选择题、拼写题、听音选择、计时、逐题提交、完成结算。
- 结算展示得分、正确题数、积分、是否通过。

服务端：

- 创建挑战。
- 提交答案。
- 完成挑战。
- 历史、统计。
- 题型和难度配置。
- 数据模型包含挑战、挑战记录、答题记录。

#### 听写

服务端 `DictationService` 支持：

- 创建听写任务。
- 逐题提交。
- 完成听写。
- 详情、历史、统计、错词本、听写模式。
- 模式包括 sequential、random、wrong_words。
- 会员中间件可限制非会员听写数量。

Flutter `BackendApiService` 也保留了听写调用方法，但当前主要首页入口没有完整的听写页面闭环，且存在路径契约风险。

### 3.8 会员、支付、签到和邀请

#### 会员

`MembershipPage` 和 `MembershipService` 支持：

- 获取套餐。
- 套餐选择。
- 创建订单。
- 查询订单状态。
- 激活码兑换。
- 刷新会员状态。
- 检查功能权益。
- 复用现有会员页作为工作英语 Pro 入口。

服务端会员模型同时存在两套结构：

- `membership_models.py`：会员、套餐、会员订单、权益、激活码。
- `payment.py`：另一套支付订单、VIP 会员、金币模型。

#### 支付

`api/payment.py` 写有微信/支付宝创建订单、查询、关闭、回调、用户订单、VIP 状态、金币和商品列表接口，但该文件没有在 `api/__init__.py` 中导入注册，当前不能把它当成 `/api/v1` 主线已发布模块。

#### 签到

`CheckinPage` + `CheckinService` 支持：

- 今日签到。
- 连续签到天数。
- 签到日历。
- 积分。
- 用户等级。
- 连续签到奖励。
- 升级提示和奖励弹窗。

#### 邀请

`InvitePage` 有邀请码复制、分享、邀请奖励、积分进度和规则说明；代码中明确标注邀请统计仍使用模拟数据，后端没有对应的完整邀请路由。

### 3.9 设置、数据和更新

`SettingsPage` 支持：

- 自动播放发音。
- 显示单词动画。
- 快速记忆/深入学习模式。
- 深入学习模式的 DeepSeek API Key 配置和连接测试。
- 英式/美式发音选择。
- 字体缩放。
- 主题模式。
- 切换词书时自动继承学习记录。
- SuperMemo、Anki、自适应算法设置入口。
- 学习数据 CSV 导出。
- CSV 导入，支持“数据更新”和“全部覆盖”两种模式。
- 增强学习分析。
- 重置学习进度。
- 隐私政策、版本信息、退出登录。

更新能力：

- `VersionService`：API 版本、App 最新版本、更新检查、兼容性检查。
- `AutoUpdateService` / `EnhancedUpdateService`：启动/恢复/手动检查更新、下载、跳过版本、强制更新提示。
- `UpdateManager`：Android APK 下载、权限、安装、进度和取消。

## 4. Flask 后端功能地图

后端入口 [`xuebadictApp/xuebaApi/app.py`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaApi/app.py) 使用 Flask App Factory，接入：

- Flask-CORS。
- SQLAlchemy、Flask-Migrate。
- Flask-JWT-Extended。
- Flasgger/Swagger。
- 全局错误响应。
- `/health`、`/api/v1/health`。
- `/api/docs`、`/apispec.json`。

### 4.1 实际主蓝图模块

主蓝图在 `api/__init__.py` 注册到 `/api/v1`。下表是代码声明的功能边界；具体是否能在目标环境工作，还要看依赖、数据库和外部服务配置。

| 模块 | 路由能力 |
| --- | --- |
| auth | 注册、密码登录、验证码登录、发送验证码、刷新 token、退出、重置密码 |
| user | 资料、学习记录读取/同步、统计、签到、改密码、绑定教材、设置、单词状态、收藏/取消收藏 |
| textbook | 教材列表、分类、词书列表、教材下词书、词书单词、词书单元、单元单词 |
| word | 单词详情、学习行为、批量查询、搜索、每日推荐 |
| audio | 音频代理、音节拆分、上传发音评测、TTS |
| ai | Chat、provider 列表、provider 健康、场景、场景详情、提示词重载、语音转文字 |
| work_english | 训练快照创建/更新、列表、详情、删除 |
| membership | 状态、权益检查、创建订单、订单状态、测试支付、套餐、激活会员 |
| challenge | 创建、答题、完成、历史、统计、题型、难度 |
| dictation | 创建、答题、完成、详情、历史、统计、错词、模式 |
| spelling | 单词拼读、全部拼读模式、批量拼读、发音信息 |
| checkin | 签到、签到页数据 |
| version | API 版本、App 最新版本、更新检查、兼容性 |
| admin | 管理员登录、仪表盘、用户、订单、版本、增长/收入报表、用户/订单状态、激活码 |
| activation | 激活码激活、测试激活码生成 |
| feedback | 提交反馈 |

### 4.2 重要路由清单

#### 认证和用户

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/send-code
POST /api/v1/auth/refresh-token
POST /api/v1/auth/logout
POST /api/v1/auth/reset-password

GET  /api/v1/user/profile
PUT  /api/v1/user/profile
GET  /api/v1/user/learning_records
POST /api/v1/user/learning_records/sync
GET  /api/v1/user/statistics
POST /api/v1/user/checkin
POST /api/v1/user/change-password
POST /api/v1/user/bind-textbook
GET  /api/v1/user/settings
PUT  /api/v1/user/settings
GET  /api/v1/user/word_status/<book_id>/<word_rank>
POST /api/v1/user/favorites
DELETE /api/v1/user/favorites
```

#### 教材、词书和单词

```text
GET  /api/v1/textbooks
GET  /api/v1/categories
GET  /api/v1/books
GET  /api/v1/textbooks/<textbook_id>/books
GET  /api/v1/books/<book_id>/words
GET  /api/v1/books/<book_id>/units
GET  /api/v1/units/<unit_id>/words

GET  /api/v1/words/<book_id>/<word_rank>
POST /api/v1/words/<book_id>/<word_rank>/learn
POST /api/v1/words/batch
GET  /api/v1/words/search
GET  /api/v1/words/daily-recommend
```

#### AI、音频和工作英语

```text
POST /api/v1/ai/chat
GET  /api/v1/ai/providers
GET  /api/v1/ai/health/<provider_id>
GET  /api/v1/ai/scenes
GET  /api/v1/ai/scenes/<scene_id>
POST /api/v1/ai/prompts/reload
POST /api/v1/ai/speech

GET  /api/v1/audio/proxy
GET  /api/v1/audio/syllables/<word>
POST /api/v1/audio/evaluate
GET  /api/v1/audio/tts

POST   /api/v1/work-english/sessions
GET    /api/v1/work-english/sessions
GET    /api/v1/work-english/sessions/<session_id>
DELETE /api/v1/work-english/sessions/<session_id>
```

#### 会员、闯关、听写、签到、版本和后台

```text
GET        /api/v1/membership/status
POST     /api/v1/membership/check-feature
POST     /api/v1/membership/order/create
GET      /api/v1/membership/order/status
POST     /api/v1/membership/order/test-pay
GET      /api/v1/membership/plans
POST     /api/v1/membership/activate

POST /api/v1/challenge/create
POST /api/v1/challenge/<challenge_id>/submit
POST /api/v1/challenge/<challenge_id>/finish
GET  /api/v1/challenge/history
GET  /api/v1/challenge/stats
GET  /api/v1/challenge/types
GET  /api/v1/challenge/difficulties

POST /api/v1/dictation/create
POST /api/v1/dictation/<dictation_id>/submit
POST /api/v1/dictation/<dictation_id>/finish
GET  /api/v1/dictation/<dictation_id>
GET  /api/v1/dictation/history
GET  /api/v1/dictation/stats
GET  /api/v1/dictation/wrong-words
GET  /api/v1/dictation/modes

POST /api/v1/checkin
GET  /api/v1/checkin/page

GET  /api/v1/version/api
GET  /api/v1/version/app/latest
POST /api/v1/version/app/check
POST /api/v1/version/compatibility
```

### 4.3 未纳入主蓝图的后端模块

以下代码存在，但 `api/__init__.py` 没有把它们注册到主应用：

| 文件 | 代码能力 | 当前判断 |
| --- | --- | --- |
| `api/payment.py` | 微信/支付宝支付订单、回调、VIP、金币、商品 | 后端代码存在，主蓝图未注册 |
| `api/speech_evaluator.py` | `/api/evaluate`、`/api/health` 独立评测服务 | 使用 `app.route`，没有被 `create_app` 导入注册 |

## 5. 数据模型和持久化

### 5.1 服务端数据库模型

| 模型组 | 主要数据 |
| --- | --- |
| 用户 | 用户资料、等级、积分、签到、邀请码、家长关系 |
| 词书 | 教材、单元、词书、单词、翻译、例句、短语、同义词、相关词 |
| 学习 | 学习日志、错题、发音记录、挑战、挑战答题、听写、听写答题 |
| 工作英语 | 复用 `study_logs`，`module=work_english`，`details` 保存训练快照 JSON |
| 会员 | 套餐、会员、权益、用户权益、订单、激活码、激活日志 |
| 签到 | 签到记录、等级、连续奖励、积分流水、用户奖励 |
| AI/反馈/版本 | AI 消息 DTO、反馈、App 版本、API 版本 |

### 5.2 当前存在的并行数据结构

这些不是同一套模型的不同命名，而是代码中确实存在的并行结构，后续维护要特别小心：

- `models/user.py` 的轻量 `User/UserStorage` 与 `models/user_models.py` 的 SQLAlchemy 用户模型并存。
- `models/dict_models.py` 的字典数据结构与 `models/word_models.py` 的 SQLAlchemy 词书/单词模型并存。
- `models/membership_models.py` 与 `models/payment.py` 各自有会员/订单/支付结构。
- `xuebaApi/services/dict_service.py` 还支持从 `dict/book/*.zip` 读取词库内容，和数据库词书链路并存。

### 5.3 客户端本地保存

- `SharedPreferences`：登录信息、设置、选中词书、缓存索引、工作英语草稿和最近 20 次已完成训练摘要。
- App 资产：隐私政策、EchoType 两本 JSON 例句词库、图像、字体。
- 文件系统：学习数据 CSV 导入/导出、Android 下载/安装包。
- 内存状态：当前 Tab、当前单词、工作英语当前场景、AI 对话消息和当前训练回合。
- 服务端同步：传统学习记录和工作英语训练快照均有同步代码，但不等于跨设备恢复已经验收。

## 6. 前后端联调边界和已发现风险

### 6.1 可以确认“代码已连上”的链路

- Flutter 生产 API 配置由 [`lib/config/api_config.dart`](/Users/wangliyan/Documents/englistapp/xuebadictApp/xuebaAPP/lib/config/api_config.dart) 控制，生产可通过 `APP_PRODUCTION`、`API_BASE_URL` 注入。
- AI 智学和工作英语统一调用 `/api/v1/ai/chat`。
- 工作英语录音使用 `RecorderService`，再调用 `/api/v1/ai/speech`。
- 工作英语保存使用 `/api/v1/work-english/sessions`，服务端使用 JWT 和用户 ID 隔离。
- 词库页面会优先 API，失败后使用缓存；EchoType 本地词库不依赖 API。
- 会员页调用会员状态、套餐、创建订单、查询订单和激活码接口。

### 6.2 代码存在但契约可能不一致的链路

下列是按客户端字符串和后端路由静态对照发现的风险，不是本次运行测试结论：

| 客户端调用 | 后端现有路由/问题 |
| --- | --- |
| `BackendApiService.getRecommendedWords` 调用 `/words/recommended` | 后端声明的是 `/words/daily-recommend` |
| `BackendApiService.getBookDetail` 调用 `/books/<id>` | 后端路由清单没有对应的词书详情路由 |
| `BackendApiService.searchWords` 调用 `/search` | 后端声明的是 `/words/search` |
| `BackendApiService.getPronunciationUrl` 调用 `/pronunciation` | 后端对应能力在 `/audio/tts` 或 `/spelling/pronunciation` |
| `getUnitChallenges`、`submitChallenge`、旧听写方法 | 与当前 challenge/dictation 路由命名不完全一致 |
| `LessonContentService` 调用 `/api/lesson/*`、`/api/learning/*` | `xuebaApi/api` 没有对应生产路由；且它通过 `BackendApiService` 还会叠加 `/api/v1` |
| `WordSpellingService` 使用 `ApiConfig.baseUrl` 而非 `apiPath` | 客户端调用路径没有 `/api/v1/spelling` 前缀，需重新对齐 |
| dictation Blueprint 自带 `/api/dictation`，又被父蓝图以 `/dictation` 注册 | 存在重复前缀风险，需以 Flask `url_map` 最终确认 |

### 6.3 已明确的模拟/占位行为

- `PlanTab` 的今日目标、完成率、坚持天数和累计词量是页面示例值。
- `ProfileTab` 的部分统计是静态 `0`，会员有效期文案包含固定日期。
- `InvitePage` 邀请统计明确使用模拟数据。
- `UnitLearningPage` 的“读”步骤当前写入固定 95 分。
- `LessonStudyPage` 的流畅度/准确度/完整度使用固定 85/92/88 分。
- `PhoneticCoursePage` 使用页面内示例音标数据和固定视频地址。
- `StudyCenterTab` 的听力和视频入口只提示“开发中”，绘本入口暂时跳到词库。
- 登录页忘记密码、第三方登录为占位入口。
- 后端用户学习记录、设置、部分单元和推荐逻辑仍有 TODO 或模拟返回。
- 会员测试支付、测试激活码生成必须在生产环境禁用或受管理员权限保护。

## 7. 依赖和外部服务

### 7.1 Flutter 主要依赖用途

- 网络：`http`、`dio`、`http_parser`。
- 本地：`shared_preferences`、`path_provider`、`file_picker`、`permission_handler`。
- 音频/语音：`audioplayers`、`just_audio`、`record`、`audio_waveforms`、`audio_service`、`flutter_tts`。
- 视频：`video_player`。
- UI：`provider`、`flutter_smart_dialog`、`awesome_dialog`、`flutter_markdown`、`animated_text_kit`、`fl_chart`。
- 系统/更新：`package_info_plus`、`device_info_plus`、`open_filex`、`url_launcher`。
- 数据和工具：`intl`、`uuid`、`collection`、`go_router`。

当前主路由在 `main.dart` 使用 `MaterialApp.routes`，`go_router` 是否仍有使用需要后续依赖审计确认。

### 7.2 外部依赖

- 千问、DeepSeek：AI Chat 真实模式。
- `SPEECH_API_URL/SPEECH_API_KEY`：服务端通用语音转文字。
- Google Web Speech：服务端发音评测中的识别实现。
- 有道词典音频：移动端单词发音；Web 通过后端音频代理。
- Google TTS：后端句子 TTS 备用接口。
- GitHub/Gitee：词库 Markdown/CSV 资源来源。
- Iconify：AI 老师图像。
- 外部视频 CDN：音标课程视频。
- 微信/支付宝：支付代码已经存在，但 `payment.py` 当前未接入主蓝图。

## 8. 当前功能分层

| 分层 | 含义 | 当前模块 |
| --- | --- | --- |
| A：主线代码已接入 | UI 能进入，且有对应服务/路由或本地数据 | 中文到英文训练、AI Chat、EchoType 词库、词书选择、单词学习、登录、会员页、签到、闯关入口 |
| B：入口存在但仍是示例/占位 | 页面可见，但数据或动作还不是生产实现 | 计划统计、课文评测、单词读音评分、邀请统计、听力、视频、绘本、忘记密码、第三方登录 |
| C：后端有代码但需联调/契约修复 | 服务端路由/模型存在，但客户端路径、注册或外部依赖未确认 | 听写、旧课文服务、拼读服务、部分推荐/搜索/发音调用、支付模块 |
| D：历史/参考线 | 保留供迁移和研究，不代表当前 App 生产功能 | `apps/mobile`、`apps/api`、`contracts/`、根 `docs/`、嵌套 `echo-type` 项目 |

## 9. 面向当前商业产品的优先级判断

### P0：当前最值得收敛的产品主线

```text
工作角色/场景
  → 中文真实工作意图
  → 结构化英文知识
  → 英文文字或录音回答
  → 一个主要问题反馈
  → 必须重说
  → 三场景迁移
  → 历史回练
```

这条线已有最多关键代码，应该作为首发产品的唯一主流程；词库作为知识参考，会员作为 Pro 入口，传统背词能力作为复习补充。

### P0 还缺的验收项

1. 服务端强制训练状态机，而不只保存客户端提交的状态。
2. 服务端对 Pro 训练次数、历史、场景和自定义场景做权益判断。
3. 对齐真实 Flutter/Flask 路由契约，清理旧服务调用路径。
4. 配置真实语音识别后，验证录音格式、超时、空文本和失败时本地保存。
5. 完成历史训练重新打开、复习和再次开口。
6. 解决 AI JSON 结构稳定性，逐步把知识卡从 Chat 提示词迁移为服务端契约。

### P1：P0 稳定后再做

- OCR 拍照识别单词/句子。
- 音素级发音评分、重音和流利度。
- 错误表达间隔复习。
- 从历史训练和词库反向生成个性化工作场景。
- 文章、演讲的收藏、导出和复述训练。

### 当前不应继续扩张

- 无真实用户训练和付费证据前，不再平铺更多课程、视频、绘本和运营功能。
- 不把支付代码存在、会员页面存在或模拟支付成功当成商业化完成。
- 不把模拟 AI provider 当成真实千问/DeepSeek 接入完成。

## 10. 证据索引

- Flutter 入口和路由：`xuebadictApp/xuebaAPP/lib/main.dart`
- 首页容器：`xuebadictApp/xuebaAPP/lib/pages/home_page.dart`
- 单词首页：`xuebadictApp/xuebaAPP/lib/pages/home/tabs/word_tab.dart`
- AI 智学：`xuebadictApp/xuebaAPP/lib/pages/home/tabs/ai_study_tab.dart`
- 中文到英文工作英语：`xuebadictApp/xuebaAPP/lib/pages/chinese_to_english_page.dart`
- 客户端 API 聚合：`xuebadictApp/xuebaAPP/lib/services/backend_api_service.dart`
- AI 客户端：`xuebadictApp/xuebaAPP/lib/services/ai_service.dart`
- 工作英语同步：`xuebadictApp/xuebaAPP/lib/services/work_english_api_service.dart`
- 本地 EchoType 词库：`xuebadictApp/xuebaAPP/lib/services/echo_type_wordbook_service.dart`
- Flask 主应用：`xuebadictApp/xuebaApi/app.py`
- Flask 蓝图注册：`xuebadictApp/xuebaApi/api/__init__.py`
- AI 路由：`xuebadictApp/xuebaApi/api/ai/routes.py`
- 工作英语路由：`xuebadictApp/xuebaApi/api/work_english.py`
- AI provider：`xuebadictApp/xuebaApi/services/providers/`
- 工作英语持久化模型：`xuebadictApp/xuebaApi/models/study_models.py`

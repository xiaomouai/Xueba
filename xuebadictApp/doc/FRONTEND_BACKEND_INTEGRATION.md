# 前后端联动集成文档

## 概述

本文档描述了 WordFlow 应用的前后端联动架构，包括版本管理、用户认证和API集成。

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Flutter 前端应用                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  登录/注册页  │  │  版本管理     │  │  API服务     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  认证服务     │  │  更新对话框   │  │  拼读服务     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                     Flask 后端 API                           │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  认证API      │  │  版本API     │  │  拼读API     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  词库API      │  │  学习API     │  │  用户API     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 功能模块

### 1. 版本管理系统

#### 后端 API

**获取API版本**
```http
GET /api/v1/version/api
```

响应示例：
```json
{
  "success": true,
  "data": {
    "version": "2.0.0",
    "build": 20260204,
    "release_date": "2026-02-04",
    "min_app_version": "1.0.0",
    "features": [
      "单词拼读API",
      "语音评测API",
      "智能学习算法",
      "词库管理系统"
    ]
  }
}
```

**检查应用更新**
```http
POST /api/v1/version/app/check
Content-Type: application/json

{
  "current_version": "1.0.0",
  "build_number": 10,
  "platform": "android"
}
```

响应示例：
```json
{
  "success": true,
  "data": {
    "has_update": true,
    "current_version": "1.0.0",
    "latest_version": "1.2.0",
    "force_update": false,
    "update_info": {
      "version": "1.2.0",
      "build_number": 12,
      "download_url": "https://...",
      "changelog": ["新增功能", "修复问题"],
      "file_size": "25.6 MB"
    }
  }
}
```

**检查兼容性**
```http
POST /api/v1/version/compatibility
Content-Type: application/json

{
  "app_version": "1.2.0"
}
```

#### 前端服务

**VersionService** (`lib/services/version_service.dart`)
- `getCurrentVersion()` - 获取当前应用版本
- `getApiVersion()` - 获取API版本信息
- `checkUpdate()` - 检查应用更新
- `checkCompatibility()` - 检查前后端兼容性

**EnhancedUpdateService** (`lib/utils/enhanced_update_service.dart`)
- `checkOnAppStart()` - 应用启动时检查更新
- `checkOnAppResume()` - 应用恢复时检查更新
- `checkUpdate()` - 手动检查更新

**UpdateDialog** (`lib/widgets/update_dialog.dart`)
- 显示更新提示对话框
- 支持强制更新和可选更新
- 显示更新日志和文件大小

### 2. 用户认证系统

#### 后端 API

**用户注册**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "phone": "13800138000",
  "code": "123456",
  "password": "password123",
  "invite_code": "WELCOME"
}
```

响应示例：
```json
{
  "success": true,
  "message": "注册成功",
  "data": {
    "user_id": "210a856ac56e4ba9983f51b5",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "is_new_user": true,
    "gifts": [
      {
        "type": "vip_trial",
        "days": 7
      }
    ]
  }
}
```

**用户登录（密码）**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "password": "password123"
}
```

**用户登录（验证码）**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "code": "123456"
}
```

响应示例：
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "user_id": "326848d91da9496db5766bf7",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_info": {
      "nickname": "小明",
      "avatar": "https://cdn.lioneng.com/avatars/default.png",
      "role": "student",
      "vip_level": "free",
      "vip_expire_at": null
    }
  }
}
```

**发送验证码**
```http
POST /api/v1/auth/send-code
Content-Type: application/json

{
  "phone": "13800138000",
  "type": "register"
}
```

**刷新Token**
```http
POST /api/v1/auth/refresh-token
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 前端服务

**AuthService** (`lib/services/auth_service.dart`)
- `initialize()` - 初始化服务，加载本地token
- `register()` - 用户注册
- `loginWithPassword()` - 密码登录
- `loginWithCode()` - 验证码登录
- `sendCode()` - 发送验证码
- `refreshToken()` - 刷新token
- `logout()` - 登出
- `isLoggedIn` - 是否已登录
- `getAuthHeaders()` - 获取认证请求头

**LoginPage** (`lib/pages/login_page.dart`)
- 支持密码登录和验证码登录
- 验证码倒计时功能
- 密码可见性切换
- 第三方登录入口（微信、Apple）

**RegisterPage** (`lib/pages/register_page.dart`)
- 手机号注册
- 验证码验证
- 密码设置和确认
- 邀请码输入
- 用户协议勾选
- 新用户礼包展示

### 3. 单词拼读系统

#### 后端 API

**单词拼读**
```http
GET /api/v1/spelling/spell?word=computer&mode=syllable
```

响应示例：
```json
{
  "success": true,
  "data": {
    "word": "computer",
    "mode": "syllable",
    "parts": ["com", "put", "er"],
    "display": "com - put - er",
    "speak_text": "com ... put ... er",
    "ipa": null
  }
}
```

**获取所有拼读模式**
```http
GET /api/v1/spelling/spell/all?word=cat
```

**批量拼读**
```http
POST /api/v1/spelling/batch
Content-Type: application/json

{
  "words": ["cat", "dog", "computer"],
  "mode": "phoneme"
}
```

**获取发音信息**
```http
GET /api/v1/spelling/pronunciation?word=beautiful
```

#### 前端服务

**WordSpellingService** (`lib/services/word_spelling_service.dart`)
- 与后端拼读API对接
- 支持四种拼读模式：letter、syllable、phoneme、phonics
- 批量拼读功能
- 发音信息获取

### 4. 统一API服务

**ApiService** (`lib/services/api_service.dart`)
- 统一的HTTP请求封装
- 支持GET、POST、PUT、DELETE方法
- 自动处理请求头和响应
- 错误处理和超时控制

## 配置说明

### 前端配置

**API配置** (`lib/config/api_config.dart`)
```dart
class ApiConfig {
  static const String devBaseUrl = 'http://localhost:5000';
  static const String prodBaseUrl = 'https://your-domain.com';
  static const bool isProduction = false;
  static String get baseUrl => isProduction ? prodBaseUrl : devBaseUrl;
  static const Duration timeout = Duration(seconds: 10);
  static const bool enableAutoUpdateCheck = true;
  static const int versionCheckInterval = 24; // 小时
}
```

### 后端配置

**环境配置** (`xuebaApi/.env.development`)
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

**应用配置** (`xuebaApi/config.py`)
- 数据库配置
- Redis配置
- JWT配置
- 文件上传配置

## 数据流程

### 用户注册流程

```
1. 用户输入手机号
2. 点击"发送验证码"
   → POST /api/v1/auth/send-code
   ← 验证码已发送
3. 输入验证码和密码
4. 点击"注册"
   → POST /api/v1/auth/register
   ← 返回token和用户信息
5. 保存token到本地
6. 跳转到首页
```

### 用户登录流程

```
1. 用户输入手机号和密码/验证码
2. 点击"登录"
   → POST /api/v1/auth/login
   ← 返回token和用户信息
3. 保存token到本地
4. 跳转到首页
```

### 版本更新流程

```
1. 应用启动/恢复
2. 检查是否需要更新检查（24小时间隔）
3. 如果需要：
   → POST /api/v1/version/app/check
   ← 返回更新信息
4. 如果有更新：
   - 显示更新对话框
   - 用户选择"立即更新"或"稍后"
5. 如果强制更新：
   - 不允许关闭对话框
   - 必须更新才能继续使用
```

## 安全考虑

### Token管理
- Token存储在SharedPreferences中
- 每次请求自动添加Authorization头
- Token过期自动刷新
- 登出时清除所有认证信息

### 密码安全
- 前端不存储明文密码
- 后端使用SHA256加密
- 建议使用更强的加密算法（如bcrypt）

### API安全
- 使用HTTPS加密传输
- 实现请求签名验证
- 添加请求频率限制
- 实现IP白名单

## 测试

### 后端测试

```bash
# 测试版本管理API
python xuebaApi/test_version_api.py

# 测试认证API
python xuebaApi/test_auth_api.py

# 测试拼读API
python xuebaApi/test_spelling_api.py
```

### 前端测试

```bash
# 运行Flutter应用
cd xuebaAPP
flutter run

# 测试登录页面
# 导航到 /login

# 测试注册页面
# 导航到 /register
```

## 部署建议

### 后端部署
1. 使用Gunicorn或uWSGI作为WSGI服务器
2. 使用Nginx作为反向代理
3. 配置SSL证书
4. 使用Redis缓存
5. 使用MySQL/PostgreSQL数据库

### 前端部署
1. 构建Release版本
2. 配置生产环境API地址
3. 启用代码混淆
4. 配置应用签名
5. 上传到应用商店

## 常见问题

### Q: 如何切换开发/生产环境？
A: 修改 `lib/config/api_config.dart` 中的 `isProduction` 值

### Q: Token过期怎么办？
A: AuthService会自动调用refreshToken()刷新token

### Q: 如何禁用自动更新检查？
A: 设置 `ApiConfig.enableAutoUpdateCheck = false`

### Q: 如何自定义更新检查间隔？
A: 修改 `ApiConfig.versionCheckInterval` 值（单位：小时）

## 下一步计划

- [ ] 实现数据库持久化
- [ ] 接入真实短信服务
- [ ] 实现JWT token加密
- [ ] 添加第三方登录（微信、Apple）
- [ ] 实现应用内更新下载
- [ ] 添加更多API接口
- [ ] 完善错误处理和日志
- [ ] 添加单元测试和集成测试

## 联系方式

如有问题，请联系开发团队。

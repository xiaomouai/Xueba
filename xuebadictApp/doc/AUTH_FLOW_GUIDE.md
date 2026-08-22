# 用户认证流程指南

## 概述

本文档详细说明了 WordFlow 应用的完整用户认证流程，包括注册、登录、信息保存和自动跳转。

## 认证流程图

```
┌─────────────────────────────────────────────────────────────┐
│                     应用启动                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              初始化 AuthService                              │
│         从本地加载 token 和用户信息                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────┴───────┐
                    │               │
            已完成引导页？          否
                    │               │
                   是               ↓
                    │         ┌──────────┐
                    │         │ 引导页    │
                    │         └──────────┘
                    │               ↓
                    │         完成引导
                    │               ↓
                    └───────┬───────┘
                            ↓
                    ┌───────┴───────┐
                    │               │
                已登录？            否
                    │               │
                   是               ↓
                    │         ┌──────────┐
                    │         │ 登录页    │
                    │         └──────────┘
                    │               ↓
                    │         登录成功
                    │               ↓
                    └───────┬───────┘
                            ↓
                    ┌──────────┐
                    │  首页     │
                    │显示用户信息│
                    └──────────┘
```

## 详细流程

### 1. 应用启动流程

**文件**: `lib/main.dart`

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 初始化认证服务（从本地加载token和用户信息）
  await AuthService.instance.initialize();
  
  runApp(const WordFlowApp());
}
```

**AppInitializer** 决定显示哪个页面：

```dart
Future<AppStartupRoute> _determineStartupRoute() async {
  // 1. 检查是否完成引导页
  final onboardingCompleted = await _checkOnboardingStatus();
  if (!onboardingCompleted) {
    return AppStartupRoute.onboarding;
  }
  
  // 2. 检查是否已登录
  final isLoggedIn = AuthService.instance.isLoggedIn;
  if (!isLoggedIn) {
    return AppStartupRoute.login;
  }
  
  // 3. 已登录，进入首页
  return AppStartupRoute.home;
}
```

### 2. 用户注册流程

**页面**: `lib/pages/register_page.dart`

**步骤**:
1. 用户输入手机号
2. 点击"发送验证码"
   - 调用 `AuthService.sendCode(phone: phone, type: 'register')`
   - 后端发送验证码到手机
3. 用户输入验证码、密码、确认密码
4. 可选输入邀请码
5. 勾选用户协议
6. 点击"注册"
   - 调用 `AuthService.register()`
   - 后端验证并创建账号
   - 返回 token、refresh_token、user_id、user_info
7. 保存认证信息到本地
   ```dart
   SharedPreferences:
   - auth_token
   - refresh_token
   - user_id
   - user_nickname
   - user_avatar
   - user_role
   - user_vip_level
   ```
8. 显示新用户礼包（如果有）
9. 跳转到首页（清除所有路由栈）

### 3. 用户登录流程

**页面**: `lib/pages/login_page.dart`

**支持两种登录方式**:

#### 3.1 密码登录
1. 用户输入手机号和密码
2. 点击"登录"
3. 调用 `AuthService.loginWithPassword()`
4. 后端验证凭证
5. 返回 token 和用户信息
6. 保存到本地
7. 跳转到首页

#### 3.2 验证码登录
1. 用户输入手机号
2. 点击"发送验证码"
3. 输入收到的验证码
4. 点击"登录"
5. 调用 `AuthService.loginWithCode()`
6. 后端验证验证码
7. 返回 token 和用户信息
8. 保存到本地
9. 跳转到首页

### 4. 首页用户信息显示

**页面**: `lib/pages/home_page.dart`

**加载流程**:

```dart
@override
void initState() {
  super.initState();
  _loadUserInfo();  // 首先加载用户信息
  // ... 其他初始化
}

Future<void> _loadUserInfo() async {
  // 检查是否已登录
  if (!AuthService.instance.isLoggedIn) {
    // 未登录，跳转到登录页
    Navigator.of(context).pushNamedAndRemoveUntil('/login', (route) => false);
    return;
  }

  // 加载用户信息
  setState(() {
    _userName = AuthService.instance.getUserNickname();
    _userAvatar = AuthService.instance.getUserAvatar();
    _isLoadingUserInfo = false;
  });
}
```

**显示内容**:
- 用户头像（网络图片或默认头像）
- 用户昵称
- VIP标识（如果是VIP用户）

### 5. 用户登出流程

**页面**: `lib/pages/settings_page.dart`

**步骤**:
1. 用户在设置页点击"退出登录"
2. 显示确认对话框
3. 用户确认后：
   - 调用 `AuthService.logout()`
   - 清除本地所有认证信息
   - 显示"已退出登录"提示
   - 跳转到登录页（清除所有路由栈）

### 6. 路由守卫

**文件**: `lib/utils/auth_guard.dart`

所有需要登录的页面都使用 `authGuard` 包装：

```dart
routes: {
  '/login': (context) => const LoginPage(),
  '/register': (context) => const RegisterPage(),
  // 需要登录的页面
  '/home': (context) => authGuard(const HomePage()),
  '/library': (context) => authGuard(const LibraryPage()),
  '/settings': (context) => authGuard(const SettingsPage()),
}
```

**工作原理**:
- 检查 `AuthService.instance.isLoggedIn`
- 如果未登录，自动跳转到登录页
- 如果已登录，显示目标页面

## 本地存储结构

### SharedPreferences 存储的数据

| Key | 类型 | 说明 |
|-----|------|------|
| `auth_token` | String | 访问令牌（JWT） |
| `refresh_token` | String | 刷新令牌 |
| `user_id` | String | 用户ID |
| `user_nickname` | String | 用户昵称 |
| `user_avatar` | String | 用户头像URL |
| `user_role` | String | 用户角色（student/teacher/parent） |
| `user_vip_level` | String | VIP等级（free/basic/premium） |
| `onboarding_completed` | bool | 是否完成引导页 |

## API 接口

### 注册接口
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

**响应**:
```json
{
  "success": true,
  "message": "注册成功",
  "data": {
    "user_id": "abc123",
    "token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "is_new_user": true,
    "gifts": [
      {"type": "vip_trial", "days": 7}
    ]
  }
}
```

### 登录接口
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "password": "password123"
}
```

**响应**:
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "user_id": "abc123",
    "token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "user_info": {
      "nickname": "小明",
      "avatar": "https://cdn.example.com/avatar.jpg",
      "role": "student",
      "vip_level": "free",
      "vip_expire_at": null
    }
  }
}
```

## 用户头像显示逻辑

### 1. 网络头像
如果用户设置了头像URL，从网络加载：
```dart
Image.network(
  _userAvatar,
  fit: BoxFit.cover,
  errorBuilder: (context, error, stackTrace) {
    return _buildDefaultAvatar();
  },
)
```

### 2. 默认头像
如果没有头像或加载失败，显示默认头像：
- 根据用户名生成背景颜色（6种颜色循环）
- 显示用户名首字母
- 圆形容器

```dart
Widget _buildDefaultAvatar() {
  final colors = [
    Color(0xFF00C897), Color(0xFF00E676),
    Color(0xFF64B5F6), Color(0xFFFFB74D),
    Color(0xFFE57373), Color(0xFFBA68C8),
  ];
  final colorIndex = _userName.hashCode.abs() % colors.length;
  final initial = _userName[0].toUpperCase();
  
  return Container(
    decoration: BoxDecoration(
      color: colors[colorIndex],
      shape: BoxShape.circle,
    ),
    child: Center(
      child: Text(initial, style: TextStyle(
        color: Colors.white,
        fontSize: 18,
        fontWeight: FontWeight.bold,
      )),
    ),
  );
}
```

## 测试场景

### 场景1: 首次使用
1. 启动应用
2. 显示引导页
3. 完成引导页
4. 跳转到登录页
5. 注册新账号
6. 进入首页，显示用户信息

### 场景2: 已登录用户
1. 启动应用
2. 从本地加载token和用户信息
3. 验证token有效
4. 直接进入首页
5. 显示用户昵称和头像

### 场景3: Token过期
1. 启动应用
2. 加载本地token
3. Token已过期
4. 自动使用refresh_token刷新
5. 获取新token
6. 进入首页

### 场景4: 用户登出
1. 在设置页点击"退出登录"
2. 确认退出
3. 清除本地所有认证信息
4. 跳转到登录页
5. 下次启动需要重新登录

## 安全考虑

### 1. Token 管理
- Token 存储在 SharedPreferences（加密存储）
- 每次请求自动添加 Authorization 头
- Token 过期自动刷新
- 登出时清除所有 token

### 2. 密码安全
- 前端不存储明文密码
- 传输使用 HTTPS 加密
- 后端使用 SHA256 加密（建议升级到 bcrypt）

### 3. 验证码
- 60秒倒计时防止频繁发送
- 验证码5分钟有效期
- 后端限制发送频率

## 常见问题

### Q: 如何判断用户是否已登录？
A: 使用 `AuthService.instance.isLoggedIn`，它会检查是否有有效的 token 和 user_id

### Q: 用户信息存储在哪里？
A: 存储在 SharedPreferences 中，包括 token、user_id、nickname、avatar 等

### Q: 如何更新用户信息？
A: 调用后端API更新，然后调用 `AuthService._saveUserInfo()` 保存到本地

### Q: Token 过期怎么办？
A: AuthService 会自动调用 `refreshToken()` 刷新 token

### Q: 如何实现"记住我"功能？
A: 默认已实现，token 保存在本地，下次启动自动登录

### Q: 如何强制用户重新登录？
A: 调用 `AuthService.logout()` 清除所有认证信息

## 下一步优化

- [ ] 实现生物识别登录（指纹/面容）
- [ ] 添加第三方登录（微信、Apple）
- [ ] 实现多设备登录管理
- [ ] 添加登录日志和安全提醒
- [ ] 实现账号注销功能
- [ ] 添加密码强度检测
- [ ] 实现找回密码功能
- [ ] 添加账号绑定（邮箱、手机）

## 相关文件

- `lib/services/auth_service.dart` - 认证服务
- `lib/pages/login_page.dart` - 登录页面
- `lib/pages/register_page.dart` - 注册页面
- `lib/pages/home_page.dart` - 首页（用户信息显示）
- `lib/pages/settings_page.dart` - 设置页面（登出功能）
- `lib/utils/auth_guard.dart` - 路由守卫
- `lib/main.dart` - 应用入口和路由配置
- `xuebaApi/api/auth.py` - 后端认证API
- `xuebaApi/models/user.py` - 用户模型
- `xuebaApi/utils/jwt_helper.py` - JWT工具类

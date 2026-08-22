# 狮子英语 API 后端系统

基于 Python + Flask + MySQL 构建的完整后端API系统

## 📋 项目结构

```
lioneng-api/
├── app.py                      # 应用入口
├── config.py                   # 配置文件
├── requirements.txt            # 依赖包
├── .env.example               # 环境变量示例
├── models/                     # 数据库模型
│   ├── __init__.py
│   ├── user.py                # 用户模型
│   ├── textbook.py            # 教材模型
│   ├── word.py                # 单词模型
│   ├── learning.py            # 学习记录模型
│   ├── order.py               # 订单模型
│   └── growth.py              # 成长系统模型
├── api/                        # API路由
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py            # 认证接口
│   │   ├── user.py            # 用户接口
│   │   ├── textbook.py        # 教材接口
│   │   ├── learning.py        # 学习接口
│   │   ├── pronunciation.py   # 发音接口
│   │   ├── diagnosis.py       # 诊断接口
│   │   ├── parent.py          # 家长接口
│   │   ├── growth.py          # 成长接口
│   │   ├── membership.py      # 会员接口
│   │   └── order.py           # 订单接口
├── services/                   # 业务逻辑层
│   ├── __init__.py
│   ├── auth_service.py        # 认证服务
│   ├── sms_service.py         # 短信服务
│   ├── payment_service.py     # 支付服务
│   ├── ai_service.py          # AI服务
│   └── oss_service.py         # 对象存储服务
├── utils/                      # 工具函数
│   ├── __init__.py
│   ├── response.py            # 响应封装
│   ├── decorators.py          # 装饰器
│   ├── validators.py          # 验证器
│   └── helpers.py             # 辅助函数
├── tasks/                      # 异步任务
│   ├── __init__.py
│   ├── celery_app.py          # Celery配置
│   └── tasks.py               # 任务定义
├── migrations/                 # 数据库迁移
├── tests/                      # 测试文件
├── logs/                       # 日志文件
└── docs/                       # 文档
    ├── API.md                 # API文档
    ├── DATABASE.md            # 数据库文档
    └── DEPLOYMENT.md          # 部署文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入实际配置
```

### 4. 初始化数据库

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE lioneng_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 运行数据库迁移
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. 启动服务

```bash
# 开发模式
python app.py

# 生产模式
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

服务将在 `http://localhost:5000` 启动

### 6. 启动Celery（可选）

```bash
# 启动Worker
celery -A tasks.celery_app worker --loglevel=info

# 启动Flower监控
celery -A tasks.celery_app flower
```

## 📚 API文档

### 基础信息

- **Base URL**: `http://localhost:5000/api/v1`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

### 通用响应格式

```json
{
  "code": 200,
  "msg": "success",
  "data": {},
  "request_id": "abc123..."
}
```

### 核心接口

#### 1. 用户认证

```bash
# 注册
POST /api/v1/auth/register
Content-Type: application/json

{
  "phone": "13800138000",
  "code": "123456",
  "password": "password123",
  "role": "student"
}

# 登录
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "password": "password123"
}

# 获取用户信息
GET /api/v1/user/profile
Authorization: Bearer {token}
```

#### 2. 教材和单词

```bash
# 获取教材列表
GET /api/v1/textbooks

# 获取单元列表
GET /api/v1/textbooks/{textbook_id}/grades/{grade}/terms/{term}/units

# 获取单词列表
GET /api/v1/units/{unit_id}/words

# 获取单词详情
GET /api/v1/words/{word_id}
```

#### 3. 学习功能

```bash
# 开始学习
POST /api/v1/words/{word_id}/learn

# 获取闯关题目
GET /api/v1/units/{unit_id}/challenges

# 提交闯关结果
POST /api/v1/challenges/{challenge_id}/submit

# 开始听写
POST /api/v1/units/{unit_id}/dictation/start

# 提交听写结果
POST /api/v1/dictations/{dictation_id}/submit
```

#### 4. AI发音评测

```bash
# 发音评测
POST /api/v1/pronunciation/evaluate
Content-Type: multipart/form-data

audio: file
text: string
word_id: string
type: word|sentence

# 获取发音诊断报告
GET /api/v1/pronunciation/diagnosis?period=week
```

#### 5. 会员和支付

```bash
# 获取会员套餐
GET /api/v1/membership/plans

# 创建订单
POST /api/v1/orders/create
{
  "plan_id": "plan_ai",
  "payment_method": "wechat"
}

# 查询订单状态
GET /api/v1/orders/{order_id}/status
```

完整API文档请查看: [docs/API.md](docs/API.md)

## 🗄️ 数据库设计

### 核心表

- **users** - 用户表
- **memberships** - 会员表
- **textbooks** - 教材表
- **units** - 单元表
- **words** - 单词表
- **user_words** - 用户单词学习记录
- **wrong_records** - 错题记录
- **pronunciation_records** - 发音评测记录
- **study_logs** - 学习日志
- **orders** - 订单表
- **parent_child** - 家长孩子关联表

详细设计请查看: [docs/DATABASE.md](docs/DATABASE.md)

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_auth.py

# 生成覆盖率报告
pytest --cov=. --cov-report=html
```

## 📦 部署

### Docker部署

```bash
# 构建镜像
docker build -t lioneng-api .

# 运行容器
docker run -d -p 5000:5000 --name lioneng-api lioneng-api
```

### 使用Docker Compose

```bash
docker-compose up -d
```

详细部署文档请查看: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 🔧 开发指南

### 添加新接口

1. 在 `models/` 中定义数据模型
2. 在 `api/v1/` 中创建路由文件
3. 在 `services/` 中实现业务逻辑
4. 编写单元测试
5. 更新API文档

### 代码规范

- 遵循 PEP 8 规范
- 使用类型提示
- 编写文档字符串
- 保持函数简洁

## 📊 监控和日志

### 日志

日志文件位于 `logs/` 目录：
- `app.log` - 应用日志
- `error.log` - 错误日志
- `access.log` - 访问日志

### 监控

- Prometheus metrics: `http://localhost:5000/metrics`
- Flower (Celery): `http://localhost:5555`

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- 项目地址: https://github.com/your-org/lioneng-api
- 技术支持: support@lioneng.com

---

**最后更新**: 2026-02-03

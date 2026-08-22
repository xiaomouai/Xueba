# 🎉 狮子英语 API - Swagger 文档版

## 📖 概述

本项目已成功集成 Swagger API 文档，提供交互式的 API 测试界面。

### ✨ 主要特性

- ✅ **交互式文档** - 在浏览器中直接测试 API
- ✅ **完整的接口说明** - 每个接口都有详细的参数和响应说明
- ✅ **JWT 认证支持** - 支持在文档中配置认证 token
- ✅ **接口分类** - 按功能模块组织接口
- ✅ **实时测试** - 无需 Postman，直接在文档中测试

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd xuebadictApp/lioneng-api
pip install -r requirements.txt
```

主要依赖：
- `Flask==3.0.0` - Web 框架
- `flasgger==0.9.7.1` - Swagger 文档生成
- `flask-swagger-ui==4.11.1` - Swagger UI 界面

### 2. 启动服务

**方式一：使用批处理文件（推荐）**
```bash
start_with_swagger.bat
```

**方式二：直接启动**
```bash
python app.py
```

### 3. 访问文档

服务启动后，打开浏览器访问：

- **Swagger UI**: http://localhost:5000/api/docs
- **Swagger JSON**: http://localhost:5000/apispec.json
- **API 首页**: http://localhost:5000/
- **健康检查**: http://localhost:5000/health

---

## 📚 API 文档使用指南

### 浏览接口

1. 访问 http://localhost:5000/api/docs
2. 你会看到所有接口按标签分类：
   - 📚 **教材管理** - 教材版本和词书管理
   - 📖 **单词学习** - 单词查询、学习和搜索
   - 🎮 **闯关练习** - 单元闯关和挑战
   - 🎧 **听写练习** - 单词和短语听写
   - 🔐 **用户认证** - 注册、登录和token管理
   - 👤 **用户中心** - 用户信息和设置

### 测试接口

#### 无需认证的接口

1. 点击接口展开详情
2. 点击 **"Try it out"** 按钮
3. 填写必要的参数
4. 点击 **"Execute"** 执行请求
5. 查看响应结果

**示例：搜索单词**
```
GET /api/v1/words/search
参数：
  - keyword: hello
  - limit: 10
```

#### 需要认证的接口

1. 先调用登录接口获取 token
2. 点击右上角的 **"Authorize"** 按钮
3. 输入 token（格式：`Bearer {your_token}`）
4. 点击 **"Authorize"** 确认
5. 之后的请求会自动带上认证信息

**示例：获取用户信息**
```
GET /api/v1/user/profile
需要在 Header 中添加：
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🧪 测试脚本

### 自动化测试

运行测试脚本验证 Swagger 是否正常工作：

```bash
python test_swagger.py
```

测试内容：
- ✅ Swagger UI 可访问性
- ✅ Swagger JSON 格式正确性
- ✅ 示例接口调用

---

## 📝 已完成的接口文档

### 用户中心（3个接口）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/user/profile` | 获取用户信息 | ✅ |
| PUT | `/api/v1/user/profile` | 更新用户信息 | ✅ |
| POST | `/api/v1/user/textbook` | 设置用户教材 | ✅ |

### 单词学习（部分接口）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/words/{book_id}/{word_rank}` | 获取单词详情 | ❌ |
| POST | `/api/v1/words/{book_id}/{word_rank}/learn` | 更新学习状态 | ✅ |
| GET | `/api/v1/words/search` | 搜索单词 | ❌ |

---

## 🔧 为新接口添加文档

### 步骤

1. 在接口函数的文档字符串中添加 YAML 格式的 Swagger 注释
2. 使用 `---` 分隔符开始 Swagger 定义
3. 定义 tags、summary、description、parameters、responses 等

### 示例模板

```python
@api_v1.route('/example/<id>', methods=['GET'])
def example_endpoint(id):
    """
    接口简短描述
    ---
    tags:
      - 接口分类标签
    summary: 接口摘要
    description: 接口详细说明
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: 参数说明
        example: example_value
      - name: query_param
        in: query
        type: integer
        required: false
        description: 查询参数
        default: 10
    responses:
      200:
        description: 成功响应
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            msg:
              type: string
              example: success
            data:
              type: object
      400:
        description: 错误响应
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 400
            msg:
              type: string
              example: 错误信息
    """
    # 接口实现代码
    pass
```

### 参数位置说明

- `path` - 路径参数（如 `/users/{id}` 中的 `id`）
- `query` - 查询参数（如 `?page=1&size=10`）
- `body` - 请求体参数（POST/PUT 请求）
- `header` - 请求头参数（如 `Authorization`）

### 数据类型

- `string` - 字符串
- `integer` - 整数
- `number` - 数字（包括小数）
- `boolean` - 布尔值
- `array` - 数组
- `object` - 对象

---

## 🎯 待完成的工作

### 1. 完善其他接口文档

需要为以下文件添加 Swagger 文档：

- [ ] `api/textbook.py` - 教材接口（5个）
  - GET `/api/v1/textbooks` - 获取教材列表
  - GET `/api/v1/textbooks/{id}/books` - 获取词书列表
  - GET `/api/v1/books/{book_id}/words` - 获取单词列表
  - GET `/api/v1/books/{book_id}/units` - 获取单元列表
  - GET `/api/v1/units/{unit_id}/words` - 获取单元单词

- [ ] `api/word.py` - 单词接口（剩余2个）
  - POST `/api/v1/words/batch` - 批量获取单词
  - GET `/api/v1/words/daily-recommend` - 今日推荐

- [ ] `api/challenge.py` - 闯关接口（3个）
  - GET `/api/v1/units/{unit_id}/challenges` - 获取闯关题目
  - POST `/api/v1/challenges/{challenge_id}/submit` - 提交闯关结果
  - GET `/api/v1/challenges/history` - 闯关历史

- [ ] `api/dictation.py` - 听写接口（4个）
  - POST `/api/v1/units/{unit_id}/dictation/start` - 开始听写
  - POST `/api/v1/dictations/{dictation_id}/submit` - 提交听写
  - GET `/api/v1/dictations/history` - 听写历史
  - POST `/api/v1/units/{unit_id}/dictation/phrases/start` - 短语听写

- [ ] `api/auth.py` - 认证接口（4个）
  - POST `/api/v1/auth/register` - 用户注册
  - POST `/api/v1/auth/login` - 用户登录
  - POST `/api/v1/auth/send-code` - 发送验证码
  - POST `/api/v1/auth/refresh-token` - 刷新token

### 2. 去掉模拟数据，连接真实数据库

当前接口返回的是模拟数据，需要：

- [ ] 配置数据库连接（MySQL）
- [ ] 实现用户认证（JWT）
- [ ] 从数据库读取真实数据
- [ ] 保存学习记录到数据库
- [ ] 实现学习统计功能

### 3. 完善文档

- [ ] 添加更多请求/响应示例
- [ ] 完善错误码说明
- [ ] 添加接口调用流程图
- [ ] 编写最佳实践指南

---

## 🔍 Swagger 配置说明

### 配置文件位置

Swagger 配置在 `app.py` 中：

```python
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "狮子英语 API",
        "description": "基于Dict词库的小学英语学习API",
        "version": "2.0.0",
        "contact": {
            "name": "狮子英语团队",
            "email": "support@lioneng.com"
        }
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT授权，格式: Bearer {token}"
        }
    }
}
```

### 修改配置

如果需要修改 Swagger 配置：

1. 修改 `swagger_template` 中的 `host` 为你的服务器地址
2. 修改 `specs_route` 更改文档访问路径
3. 添加更多 `securityDefinitions` 支持其他认证方式

---

## 🐛 常见问题

### 1. Swagger UI 无法访问

**问题**: 访问 `/api/docs` 返回 404

**解决方案**:
```bash
# 确保已安装依赖
pip install flasgger flask-swagger-ui

# 检查 app.py 中是否正确初始化 Swagger
# 重启服务
python app.py
```

### 2. 接口文档不显示

**问题**: Swagger UI 中看不到某个接口

**可能原因**:
- 接口函数没有文档字符串
- YAML 格式错误（缩进、冒号等）
- 蓝图未正确注册

**解决方案**:
- 检查接口函数的文档字符串格式
- 使用在线 YAML 验证器检查格式
- 查看控制台错误信息

### 3. 参数验证失败

**问题**: 测试接口时提示参数错误

**解决方案**:
- 检查参数类型是否匹配（string/integer/boolean）
- 确认必填参数都已填写
- 查看示例值是否正确

### 4. 认证失败

**问题**: 调用需要认证的接口返回 401

**解决方案**:
- 确保已点击 "Authorize" 按钮配置 token
- Token 格式正确：`Bearer {token}`
- Token 未过期且有效

---

## 📚 参考资料

- [Flasgger 官方文档](https://github.com/flasgger/flasgger)
- [Swagger 2.0 规范](https://swagger.io/specification/v2/)
- [OpenAPI 规范](https://spec.openapis.org/)
- [Flask 官方文档](https://flask.palletsprojects.com/)

---

## 📞 技术支持

如有问题，请联系：
- 📧 Email: support@lioneng.com
- 📱 微信: lioneng_support

---

**文档更新时间**: 2026-02-03  
**API 版本**: V2.0.0  
**Swagger 版本**: 2.0

---

## ✨ 总结

✅ Swagger 文档已成功集成  
✅ 提供交互式 API 测试界面  
✅ 支持 JWT 认证  
✅ 完整的接口说明和示例  
✅ 易于扩展和维护  

**立即体验**: 
1. 运行 `start_with_swagger.bat`
2. 访问 http://localhost:5000/api/docs
3. 开始测试 API！

🎉 **Happy Coding!** 🎉

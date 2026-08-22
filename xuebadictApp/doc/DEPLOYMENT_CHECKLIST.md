# ✅ 部署检查清单

## 第一步：数据库准备

### 1.1 创建数据表
```bash
cd xuebaApi
mysql -u root -p xuebadict < add_new_tables.sql
```

**验证**: 运行后应该看到：
```
✅ 数据表创建完成！
```

### 1.2 初始化会员数据
```bash
mysql -u root -p xuebadict < init_membership_data.sql
```

**验证**: 应该看到4个会员套餐和12种权益的数据。

---

## 第二步：代码文件检查

### 2.1 模型文件
- ✅ `xuebaApi/models/study_models.py` - 包含 Challenge, Dictation 等模型
- ✅ `xuebaApi/models/membership_models.py` - 包含 MembershipPlan 等模型
- ✅ `xuebaApi/models/__init__.py` - 正确导出所有模型

### 2.2 服务文件
- ✅ `xuebaApi/services/membership_service.py` - 会员服务
- ✅ `xuebaApi/services/challenge_service.py` - 闯关服务
- ✅ `xuebaApi/services/dictation_service.py` - 听写服务

### 2.3 API文件
- ✅ `xuebaApi/api/membership.py` - 会员API
- ✅ `xuebaApi/api/challenge.py` - 闯关API
- ✅ `xuebaApi/api/dictation.py` - 听写API
- ✅ `xuebaApi/api/__init__.py` - 正确导入模块

### 2.4 中间件
- ✅ `xuebaApi/middleware/membership_middleware.py` - 会员权限中间件

---

## 第三步：启动服务

### 3.1 检查环境配置
确保 `.env` 文件存在且配置正确：
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=xuebadict
JWT_SECRET_KEY=你的密钥
```

### 3.2 启动服务
```bash
cd xuebaApi
python app.py
```

### 3.3 验证启动成功
应该看到：
```
🦁 狮子英语 API 服务启动中...
🌐 服务地址: http://localhost:5000
📖 API文档: http://localhost:5000/api/docs
```

---

## 第四步：功能测试

### 4.1 健康检查
访问：http://localhost:5000/health

应该返回：
```json
{
  "code": 200,
  "data": {
    "status": "healthy",
    "message": "API is running"
  }
}
```

### 4.2 API文档
访问：http://localhost:5000/api/docs

应该能看到 Swagger 文档界面。

### 4.3 运行测试脚本
```bash
# Windows
test_new_features.bat

# 或直接运行
cd xuebaApi
python test_new_features.py
```

---

## 常见问题排查

### Q1: 找不到 mysql 命令
**解决方案**：
- 添加 MySQL bin 目录到系统 PATH
- 或使用完整路径：
  ```bash
  "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
  ```

### Q2: 数据库连接失败
**检查项**：
- [ ] MySQL 服务是否运行
- [ ] `.env` 文件配置是否正确
- [ ] 数据库 `xuebadict` 是否已创建
- [ ] 用户名密码是否正确

### Q3: 导入错误
**检查项**：
- [ ] 所有模型文件是否存在
- [ ] `__init__.py` 是否正确导入
- [ ] 是否有语法错误

### Q4: 表已存在
**不用担心**：SQL脚本使用了 `CREATE TABLE IF NOT EXISTS`，不会重复创建。

---

## 文件清单

### 必需文件
- ✅ `xuebaApi/app.py` - 主应用文件
- ✅ `xuebaApi/config.py` - 配置文件
- ✅ `xuebaApi/extensions.py` - 扩展初始化
- ✅ `xuebaApi/.env` - 环境配置

### 数据库脚本
- ✅ `xuebaApi/add_new_tables.sql` - 创建数据表
- ✅ `xuebaApi/init_membership_data.sql` - 初始化会员数据

### 模型文件（11个模型）
- ✅ `models/study_models.py` - 6个模型
- ✅ `models/membership_models.py` - 5个模型
- ✅ `models/word_models.py`
- ✅ `models/user_models.py`

### 服务文件
- ✅ `services/membership_service.py`
- ✅ `services/challenge_service.py`
- ✅ `services/dictation_service.py`
- ✅ `services/word_service.py`
- ✅ `services/user_service.py`

### API文件
- ✅ `api/membership.py`
- ✅ `api/challenge.py`
- ✅ `api/dictation.py`
- ✅ `api/textbook.py`
- ✅ `api/word.py`
- ✅ `api/auth.py`
- ✅ `api/user.py`

### 测试文件
- ✅ `test_new_features.py`
- ✅ `test_new_features.bat`

---

## 快速命令

### 完整部署流程（一键）
```bash
# 1. 创建表并初始化数据
cd xuebaApi
mysql -u root -p xuebadict < add_new_tables.sql
mysql -u root -p xuebadict < init_membership_data.sql

# 2. 启动服务
python app.py
```

### 或使用批处理
```bash
setup_and_start.bat
```

---

## 成功标志

当你看到以下所有条件满足时，说明部署成功：

1. ✅ 数据表创建成功（11个新表）
2. ✅ 会员数据初始化成功（4个套餐，12种权益）
3. ✅ API 服务启动成功（无错误信息）
4. ✅ 健康检查通过
5. ✅ API 文档可访问
6. ✅ 测试脚本运行成功

---

## 下一步

服务启动成功后：
1. 查看 API 文档：http://localhost:5000/api/docs
2. 运行功能测试：`test_new_features.bat`
3. 开始前端对接开发

---

**祝部署顺利！** 🎉

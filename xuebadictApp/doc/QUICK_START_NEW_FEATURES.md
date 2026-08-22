# 快速启动指南 - 会员系统、闯关和听写模块

## 🚀 5分钟快速上手

### 第一步：初始化会员数据

```bash
# 导入会员套餐和权益数据
mysql -u root -p xuebadict < xuebaApi/init_membership_data.sql
```

这将创建4个会员套餐和12种会员权益。

### 第二步：启动API服务

```bash
cd xuebaApi
python app.py
```

看到以下输出表示启动成功：
```
🦁 狮子英语 API 服务启动中...
🌐 服务地址: http://localhost:5000
📖 API文档: http://localhost:5000/api/docs
```

### 第三步：测试新功能

**方式1：使用测试脚本（推荐）**
```bash
# Windows
test_new_features.bat

# Linux/Mac
cd xuebaApi
python test_new_features.py
```

**方式2：使用API文档**
访问 http://localhost:5000/api/docs

---

## 📋 完整功能清单

### ✅ 会员系统
- [x] 查看会员套餐
- [x] 创建会员订单
- [x] 激活会员（模拟支付）
- [x] 查看我的会员信息
- [x] 查看订单历史
- [x] 查看会员权益

### ✅ 闯关模块
- [x] 创建闯关（4种题型）
- [x] 3种难度等级
- [x] 提交答案
- [x] 查看闯关结果
- [x] 闯关历史查询
- [x] 闯关统计数据

### ✅ 听写模块
- [x] 创建听写（3种模式）
- [x] 提交听写答案
- [x] 自动判断正误
- [x] 查看听写结果
- [x] 错词本管理
- [x] 听写历史和统计

---

## 🎯 核心API一览

### 会员系统
```bash
# 获取会员套餐
GET http://localhost:5000/api/membership/plans

# 创建订单
POST http://localhost:5000/api/membership/create-order
Authorization: Bearer {token}
Content-Type: application/json
{
  "plan_id": 1,
  "payment_method": "alipay"
}

# 查看我的会员
GET http://localhost:5000/api/membership/my-membership
Authorization: Bearer {token}
```

### 闯关模块
```bash
# 创建闯关
POST http://localhost:5000/api/challenge/create
Authorization: Bearer {token}
Content-Type: application/json
{
  "word_book_id": 1,
  "difficulty": "easy",
  "question_type": "choose_meaning"
}

# 提交答案
POST http://localhost:5000/api/challenge/{challenge_id}/submit
Authorization: Bearer {token}
Content-Type: application/json
{
  "word_id": 123,
  "user_answer": "A",
  "is_correct": true,
  "time_spent": 5
}
```

### 听写模块
```bash
# 创建听写
POST http://localhost:5000/api/dictation/create
Authorization: Bearer {token}
Content-Type: application/json
{
  "word_book_id": 1,
  "mode": "random",
  "word_count": 20
}

# 提交听写
POST http://localhost:5000/api/dictation/{dictation_id}/submit
Authorization: Bearer {token}
Content-Type: application/json
{
  "word_id": 123,
  "user_answer": "hello"
}

# 查看错词本
GET http://localhost:5000/api/dictation/wrong-words
Authorization: Bearer {token}
```

---

## 💡 使用技巧

### 1. 测试流程建议
```
注册/登录 → 购买会员 → 创建闯关 → 创建听写 → 查看统计
```

### 2. 获取Token
所有需要登录的接口都需要在请求头中添加：
```
Authorization: Bearer {你的token}
```

登录成功后会返回token，保存后使用。

### 3. 会员功能测试
```python
# 先购买会员（使用模拟支付）
1. 创建订单 → 获取 order_id
2. 调用支付回调 → 传入 order_id
3. 查看会员信息 → 确认激活成功
```

### 4. 闯关题型说明
- `choose_meaning`: 给单词选词义
- `choose_word`: 给词义选单词  
- `spell_word`: 拼写单词
- `listen_choose`: 听音选词

### 5. 听写模式说明
- `sequential`: 顺序听写
- `random`: 随机听写
- `wrong_words`: 错词专项

---

## 🔧 常见问题

### Q1: API服务启动失败？
**A**: 检查数据库连接配置（.env文件）和数据库是否已创建。

### Q2: Token过期怎么办？
**A**: 重新调用登录接口获取新token。

### Q3: 非会员能玩什么？
**A**: 非会员可以体验简单难度闯关和每日20个单词听写。

### Q4: 如何清空测试数据？
**A**: 
```sql
-- 清空用户数据（保留套餐）
TRUNCATE TABLE users;
TRUNCATE TABLE user_membership;
TRUNCATE TABLE membership_orders;
TRUNCATE TABLE challenges;
TRUNCATE TABLE dictations;
```

---

## 📚 文档索引

- **完整功能文档**: `COMPLETE_FEATURES.md`
- **API重构说明**: `REFACTOR_SUMMARY.md`
- **测试脚本**: `test_new_features.py`
- **在线API文档**: http://localhost:5000/api/docs

---

## 🎉 开始使用

现在运行：
```bash
test_new_features.bat
```

查看所有功能的完整测试流程！

---

**祝您使用愉快！** 🎊

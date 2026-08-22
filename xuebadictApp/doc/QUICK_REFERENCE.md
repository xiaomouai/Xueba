# 🚀 快速参考卡片

## 一键启动

```bash
cd xuebadictApp/lioneng-api
start_with_swagger.bat
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 🌐 API 首页 | http://localhost:5000/ |
| 📖 Swagger 文档 | http://localhost:5000/api/docs |
| 📋 Swagger JSON | http://localhost:5000/apispec.json |
| 💚 健康检查 | http://localhost:5000/health |

## 测试命令

```bash
# 测试 Swagger
python test_swagger.py

# 测试 API
python test_db_api.py
```

## 已完成的接口文档

### 用户中心
- ✅ GET `/api/v1/user/profile` - 获取用户信息
- ✅ PUT `/api/v1/user/profile` - 更新用户信息
- ✅ POST `/api/v1/user/textbook` - 设置用户教材

### 单词学习
- ✅ GET `/api/v1/words/{book_id}/{word_rank}` - 获取单词详情
- ✅ POST `/api/v1/words/{book_id}/{word_rank}/learn` - 更新学习状态
- ✅ GET `/api/v1/words/search` - 搜索单词

## 快速测试示例

### 1. 搜索单词
```bash
curl "http://localhost:5000/api/v1/words/search?keyword=hello&limit=5"
```

### 2. 获取单词详情
```bash
curl "http://localhost:5000/api/v1/words/PEPXiaoXue3_1/1"
```

### 3. 获取用户信息
```bash
curl "http://localhost:5000/api/v1/user/profile"
```

## 在 Swagger UI 中测试

1. 访问 http://localhost:5000/api/docs
2. 点击接口展开
3. 点击 "Try it out"
4. 填写参数
5. 点击 "Execute"
6. 查看响应

## 添加认证

对于需要认证的接口：
1. 点击右上角 "Authorize" 按钮
2. 输入：`Bearer {your_token}`
3. 点击 "Authorize"

## 下一步

- [ ] 完善其他接口文档（18个待完成）
- [ ] 连接真实数据库
- [ ] 实现 JWT 认证

## 相关文档

- [完整使用手册](./README_SWAGGER.md)
- [配置指南](./SWAGGER_SETUP.md)
- [完成总结](./SWAGGER_INTEGRATION_COMPLETE.md)

---

**版本**: V2.0.0 | **更新**: 2026-02-03

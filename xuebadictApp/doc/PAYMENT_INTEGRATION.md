# 支付系统集成文档

## 📱 支付功能概述

狮子英语已完整集成微信支付和支付宝支付功能，支持VIP会员购买和金币充值。

## 🎯 支持的支付方式

### 微信支付
- ✅ **扫码支付 (NATIVE)** - PC网站扫码支付
- ✅ **公众号支付 (JSAPI)** - 微信公众号/小程序支付
- ✅ **APP支付** - 移动应用内支付
- ✅ **H5支付 (MWEB)** - 移动网页支付

### 支付宝支付
- ✅ **APP支付** - 移动应用内支付
- ✅ **手机网站支付 (WAP)** - 移动浏览器支付
- ✅ **PC网站支付** - 电脑浏览器支付

## 🛍️ 商品列表

### VIP会员商品

| 商品ID | 商品名称 | 价格 | 时长 | 折扣 |
|--------|---------|------|------|------|
| vip_month | VIP月卡 | ¥19 | 30天 | - |
| vip_season | VIP季卡 | ¥49 | 90天 | 8.6折 |
| vip_year | VIP年卡 | ¥99 | 365天 | 4.3折 |

### 金币商品

| 商品ID | 商品名称 | 价格 | 金币数 |
|--------|---------|------|--------|
| coins_100 | 100金币 | ¥1 | 100 |
| coins_500 | 500金币 | ¥5 | 500 |
| coins_1000 | 1000金币 | ¥10 | 1000 |

## 📡 API接口文档

### 基础URL
```
http://localhost:5000/api/v1/payment
```

### 1. 创建支付订单

**接口地址**: `POST /create`

**请求参数**:
```json
{
  "user_id": 1,
  "product_type": "vip_month",
  "payment_method": "wechat",
  "payment_scene": "NATIVE",
  "openid": "oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"
}
```

**参数说明**:
- `user_id`: 用户ID (必填)
- `product_type`: 商品类型，如 `vip_month`, `coins_100` (必填)
- `payment_method`: 支付方式，`wechat` 或 `alipay` (必填)
- `payment_scene`: 支付场景
  - 微信: `NATIVE`/`JSAPI`/`APP`/`MWEB`
  - 支付宝: `app`/`wap`/`pc`
- `openid`: 微信用户openid (JSAPI支付必填)

**响应示例**:
```json
{
  "code": 200,
  "message": "订单创建成功",
  "data": {
    "order_no": "LEWX1738627200000",
    "order_id": 1,
    "payment_method": "wechat",
    "total_amount": 1900,
    "expired_at": "2024-02-04T10:30:00",
    "payment_data": {
      "code_url": "weixin://wxpay/bizpayurl?pr=xxxxx",
      "prepay_id": "wx04103443447015..."
    }
  }
}
```

### 2. 查询订单状态

**接口地址**: `GET /query/{order_no}`

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "order": {
      "id": 1,
      "order_no": "LEWX1738627200000",
      "trade_no": "4200001234567890",
      "status": 1,
      "status_name": "已支付",
      "total_amount": 1900,
      "paid_amount": 1900,
      "created_at": "2024-02-04T10:00:00",
      "paid_at": "2024-02-04T10:05:30"
    },
    "payment_status": {
      "trade_state": "SUCCESS",
      "trade_state_desc": "支付成功",
      "transaction_id": "4200001234567890"
    }
  }
}
```

### 3. 关闭订单

**接口地址**: `POST /close/{order_no}`

**响应示例**:
```json
{
  "code": 200,
  "message": "订单已关闭",
  "data": null
}
```

### 4. 获取用户订单列表

**接口地址**: `GET /orders/user/{user_id}`

**查询参数**:
- `page`: 页码，默认1
- `per_page`: 每页数量，默认10
- `status`: 订单状态筛选 (可选)

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "orders": [
      {
        "id": 1,
        "order_no": "LEWX1738627200000",
        "product_name": "狮子英语VIP月卡",
        "total_amount": 1900,
        "status": 1,
        "status_name": "已支付",
        "created_at": "2024-02-04T10:00:00"
      }
    ],
    "total": 10,
    "page": 1,
    "per_page": 10,
    "pages": 1
  }
}
```

### 5. 获取VIP状态

**接口地址**: `GET /vip/{user_id}`

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "is_vip": true,
    "vip_info": {
      "id": 1,
      "user_id": 1,
      "vip_type": "month",
      "is_active": true,
      "is_valid": true,
      "start_date": "2024-02-04T10:05:30",
      "end_date": "2024-03-04T10:05:30"
    }
  }
}
```

### 6. 获取用户金币

**接口地址**: `GET /coins/{user_id}`

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "coins": {
      "user_id": 1,
      "total_coins": 1000,
      "used_coins": 200,
      "available_coins": 800
    }
  }
}
```

### 7. 获取商品列表

**接口地址**: `GET /products`

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "products": {
      "vip_products": [
        {
          "id": "vip_month",
          "name": "VIP月卡",
          "desc": "畅享所有VIP功能30天",
          "price": 1900,
          "price_yuan": 19.0,
          "duration": "30天",
          "type": "vip"
        }
      ],
      "coin_products": [
        {
          "id": "coins_100",
          "name": "100金币",
          "desc": "可用于兑换学习资源",
          "price": 100,
          "price_yuan": 1.0,
          "coins": 100,
          "type": "coins"
        }
      ]
    }
  }
}
```

### 8. 支付回调接口

#### 微信支付回调
**接口地址**: `POST /wechat/notify`

**响应**: 
```json
{"code": "SUCCESS", "message": "成功"}
```

#### 支付宝支付回调
**接口地址**: `POST /alipay/notify`

**响应**: 
```
success
```

## 📊 订单状态说明

| 状态码 | 状态名称 | 说明 |
|--------|---------|------|
| 0 | 待支付 | 订单已创建，等待支付 |
| 1 | 已支付 | 支付成功 |
| 2 | 已取消 | 订单已取消 |
| 3 | 退款中 | 正在退款 |
| 4 | 已退款 | 退款完成 |
| 5 | 支付失败 | 支付失败 |

## 🔧 配置说明

### 1. 安装依赖

```bash
pip install wechatpay-python alipay-sdk-python cryptography
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填入真实配置：

```bash
# 微信支付配置
WECHAT_APP_ID=your_app_id
WECHAT_MCH_ID=your_mch_id
WECHAT_MCH_KEY=your_api_key
WECHAT_MCH_SERIAL_NO=your_cert_serial_no
WECHAT_NOTIFY_URL=https://yourdomain.com/api/v1/payment/wechat/notify

# 支付宝配置
ALIPAY_APP_ID=your_app_id
ALIPAY_GATEWAY=https://openapi.alipaydev.com/gateway.do
ALIPAY_APP_PRIVATE_KEY=your_private_key
ALIPAY_PUBLIC_KEY=your_alipay_public_key
ALIPAY_NOTIFY_URL=https://yourdomain.com/api/v1/payment/alipay/notify
```

### 3. 配置证书文件

将微信支付证书放到 `certs/` 目录下：
```
certs/
  ├── apiclient_cert.pem
  └── apiclient_key.pem
```

### 4. 初始化数据库

```bash
flask db init
flask db migrate -m "Add payment tables"
flask db upgrade
```

## 💻 使用示例

### Python示例

```python
import requests

# 创建订单
response = requests.post('http://localhost:5000/api/v1/payment/create', json={
    'user_id': 1,
    'product_type': 'vip_month',
    'payment_method': 'wechat',
    'payment_scene': 'NATIVE'
})

data = response.json()
order_no = data['data']['order_no']
code_url = data['data']['payment_data']['code_url']

# 生成二维码供用户扫描
# ...

# 查询订单状态
response = requests.get(f'http://localhost:5000/api/v1/payment/query/{order_no}')
print(response.json())
```

### Flutter示例

```dart
// 创建订单
final response = await http.post(
  Uri.parse('http://localhost:5000/api/v1/payment/create'),
  headers: {'Content-Type': 'application/json'},
  body: json.encode({
    'user_id': 1,
    'product_type': 'vip_month',
    'payment_method': 'alipay',
    'payment_scene': 'app',
  }),
);

final data = json.decode(response.body);
final orderString = data['data']['payment_data']['order_string'];

// 调用支付宝SDK
// ...
```

## 🔐 安全注意事项

1. **回调地址安全**
   - 回调地址必须使用HTTPS
   - 必须验证回调签名
   - 防止重复通知

2. **订单金额校验**
   - 回调时验证订单金额
   - 防止金额篡改

3. **订单状态管理**
   - 使用数据库事务
   - 防止并发问题
   - 记录详细日志

4. **证书和密钥管理**
   - 妥善保管私钥
   - 不要提交到代码仓库
   - 定期更新证书

## 🧪 测试说明

### 沙箱测试

1. **微信支付沙箱**
   - 申请微信支付沙箱账号
   - 使用沙箱环境测试

2. **支付宝沙箱**
   - 使用支付宝开放平台沙箱环境
   - 网关: `https://openapi.alipaydev.com/gateway.do`
   - 使用沙箱账号测试

### 测试脚本

运行测试脚本：
```bash
python test_payment.py
```

## 📝 数据库表结构

### payment_orders (支付订单表)
- `id`: 主键
- `order_no`: 订单号 (唯一)
- `trade_no`: 第三方交易号
- `user_id`: 用户ID
- `payment_method`: 支付方式
- `payment_scene`: 支付场景
- `product_name`: 商品名称
- `total_amount`: 订单金额 (分)
- `paid_amount`: 实付金额 (分)
- `status`: 订单状态
- `created_at`: 创建时间
- `paid_at`: 支付时间
- `expired_at`: 过期时间

### vip_memberships (VIP会员表)
- `id`: 主键
- `user_id`: 用户ID
- `vip_type`: 会员类型
- `is_active`: 是否激活
- `start_date`: 开始时间
- `end_date`: 结束时间

### user_coins (用户金币表)
- `id`: 主键
- `user_id`: 用户ID
- `total_coins`: 总金币
- `used_coins`: 已使用
- `available_coins`: 可用金币

## 🚀 部署建议

1. **使用正式环境配置**
   - 更新为正式的APP_ID和密钥
   - 使用正式网关地址

2. **配置HTTPS**
   - 回调地址必须使用HTTPS
   - 配置SSL证书

3. **配置域名**
   - 在微信/支付宝后台配置回调域名
   - 确保域名可公网访问

4. **监控和日志**
   - 配置日志系统
   - 监控支付成功率
   - 设置异常告警

## 📞 技术支持

如有问题，请参考：
- 微信支付官方文档: https://pay.weixin.qq.com/wiki/doc/api/
- 支付宝开放平台: https://opendocs.alipay.com/

---

**更新时间**: 2024-02-04  
**版本**: v1.0.0

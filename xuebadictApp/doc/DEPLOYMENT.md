# 🚀 部署指南

本文档详细说明如何将猫头鹰记单词应用部署到生产环境。

---

## 📋 部署架构

### 推荐架构

```
               Internet
                  ↓
            [Cloudflare CDN]
                  ↓
           [Nginx (SSL/443)]
                  ↓
        [Gunicorn (5000) × 4]
                  ↓
           [Flask应用]
                  ↓
         [SQLite数据库]
                  ↓
          [Dict词库资源]
```

### 备选架构

```
       [Docker容器]
            ↓
    [Flask + Gunicorn]
            ↓
      [SQLite Volume]
```

---

## 🖥️ 后端部署

### 方案一：传统部署（推荐生产环境）

#### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install python3 python3-pip python3-venv nginx -y

# 创建应用目录
sudo mkdir -p /var/www/lioneng-api
cd /var/www/lioneng-api
```

#### 2. 部署应用

```bash
# 克隆代码
git clone https://github.com/your-org/xuebadictapp.git .

# 进入后端目录
cd xuebaApi

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn
```

#### 3. 配置环境变量

创建 `.env` 文件：

```bash
# .env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
DATABASE_URI=sqlite:///lioneng.db
```

#### 4. 配置Gunicorn

创建 `gunicorn_config.py`：

```python
# gunicorn_config.py
import multiprocessing

# 服务器socket
bind = "127.0.0.1:5000"
backlog = 2048

# Worker进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# 日志
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

# 进程命名
proc_name = 'lioneng-api'

# 服务器机制
daemon = False
pidfile = '/var/run/gunicorn.pid'
```

创建日志目录：

```bash
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
```

#### 5. 配置systemd服务

创建 `/etc/systemd/system/lioneng-api.service`：

```ini
[Unit]
Description=LionEng API Gunicorn Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/lioneng-api/xuebaApi
Environment="PATH=/var/www/lioneng-api/xuebaApi/venv/bin"
ExecStart=/var/www/lioneng-api/xuebaApi/venv/bin/gunicorn \
    --config gunicorn_config.py \
    app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 重新加载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start lioneng-api

# 设置开机自启
sudo systemctl enable lioneng-api

# 查看状态
sudo systemctl status lioneng-api
```

#### 6. 配置Nginx

创建 `/etc/nginx/sites-available/lioneng-api`：

```nginx
upstream lioneng_api {
    server 127.0.0.1:5000 fail_timeout=0;
}

server {
    listen 80;
    server_name api.lioneng.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.lioneng.com;
    
    # SSL证书配置
    ssl_certificate /etc/ssl/certs/lioneng.crt;
    ssl_certificate_key /etc/ssl/private/lioneng.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # 日志
    access_log /var/log/nginx/lioneng-api.access.log;
    error_log /var/log/nginx/lioneng-api.error.log;
    
    # 请求体大小限制
    client_max_body_size 10M;
    
    # API代理
    location / {
        proxy_pass http://lioneng_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 缓冲设置
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
    
    # 静态资源
    location /static {
        alias /var/www/lioneng-api/xuebaApi/static;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
    
    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

启用站点：

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/lioneng-api /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

#### 7. 配置SSL证书

使用Let's Encrypt免费证书：

```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx -y

# 自动配置SSL
sudo certbot --nginx -d api.lioneng.com

# 自动续期
sudo certbot renew --dry-run
```

#### 8. 配置防火墙

```bash
# 允许HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

### 方案二：Docker部署

#### 1. 创建Dockerfile

`xuebaApi/Dockerfile`:

```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./xuebaApi
      dockerfile: Dockerfile
    container_name: lioneng-api
    restart: always
    ports:
      - "5000:5000"
    volumes:
      - ./xuebaApi/lioneng.db:/app/lioneng.db
      - ./xuebaApi/dict:/app/dict
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - lioneng-network

  nginx:
    image: nginx:alpine
    container_name: lioneng-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl/certs:ro
    depends_on:
      - api
    networks:
      - lioneng-network

networks:
  lioneng-network:
    driver: bridge
```

#### 3. 启动容器

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps
```

---

## 📱 前端部署

### Android APK打包

#### 1. 配置签名

创建 `android/key.properties`:

```properties
storePassword=your-store-password
keyPassword=your-key-password
keyAlias=lioneng
storeFile=/path/to/keystore.jks
```

#### 2. 生成签名密钥

```bash
keytool -genkey -v -keystore ~/lioneng-keystore.jks \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias lioneng
```

#### 3. 配置build.gradle

编辑 `android/app/build.gradle`:

```gradle
android {
    ...
    
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
        }
    }
}
```

#### 4. 打包APK

```bash
# 进入前端目录
cd xuebaAPP

# 配置生产环境API
# 编辑 lib/config/api_config.dart
# 将 isProduction 设置为 true

# 清理缓存
flutter clean

# 获取依赖
flutter pub get

# 打包APK
flutter build apk --release

# 打包App Bundle（推荐Google Play）
flutter build appbundle --release
```

生成的文件：
- APK: `build/app/outputs/flutter-apk/app-release.apk`
- AAB: `build/app/outputs/bundle/release/app-release.aab`

### iOS IPA打包

#### 1. 配置签名

在Xcode中配置：
1. 打开 `ios/Runner.xcworkspace`
2. 选择 Runner target
3. 配置 Signing & Capabilities
4. 选择你的开发团队

#### 2. 打包IPA

```bash
# 清理缓存
flutter clean

# 获取依赖
flutter pub get

# 打包iOS
flutter build ios --release

# 在Xcode中打包
# Product -> Archive -> Distribute App
```

---

## 🗄️ 数据库管理

### 备份数据库

```bash
# 备份SQLite数据库
cp lioneng.db lioneng.db.backup.$(date +%Y%m%d)

# 定时备份（crontab）
0 2 * * * cp /var/www/lioneng-api/xuebaApi/lioneng.db \
    /var/backups/lioneng-db/lioneng.db.$(date +\%Y\%m\%d)
```

### 恢复数据库

```bash
# 停止服务
sudo systemctl stop lioneng-api

# 恢复数据库
cp lioneng.db.backup.20260204 lioneng.db

# 启动服务
sudo systemctl start lioneng-api
```

### 数据库优化

```bash
# SQLite优化
sqlite3 lioneng.db "VACUUM;"
sqlite3 lioneng.db "ANALYZE;"
```

---

## 📊 监控和日志

### 应用日志

```bash
# 查看Gunicorn日志
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log

# 查看Nginx日志
tail -f /var/log/nginx/lioneng-api.access.log
tail -f /var/log/nginx/lioneng-api.error.log

# 查看systemd日志
sudo journalctl -u lioneng-api -f
```

### 性能监控

安装监控工具：

```bash
# 安装htop
sudo apt install htop

# 安装netdata（推荐）
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

### 健康检查

```bash
# 检查API健康状态
curl http://localhost:5000/health

# 检查API版本
curl http://localhost:5000/api/v1/version/api
```

---

## 🔒 安全配置

### 1. 修改默认密钥

```bash
# 生成随机密钥
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2. 配置CORS

编辑 `app.py`:

```python
from flask_cors import CORS

# 生产环境限制CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 3. 限流配置

安装Flask-Limiter：

```bash
pip install flask-limiter
```

配置限流：

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/v1/words/search')
@limiter.limit("10 per minute")
def search_words():
    pass
```

### 4. 防火墙规则

```bash
# 仅允许特定IP访问SSH
sudo ufw limit from 你的IP地址 to any port 22

# 限制API访问频率
sudo apt install fail2ban
```

---

## 🚀 CDN配置（可选）

### 使用Cloudflare

1. 注册Cloudflare账号
2. 添加域名
3. 配置DNS记录
4. 开启CDN代理
5. 配置缓存规则

### 静态资源CDN

```nginx
# Nginx配置
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 365d;
    add_header Cache-Control "public, immutable";
}
```

---

## 📈 性能优化

### 1. 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_word_rank ON dict_words(word_rank);
CREATE INDEX idx_book_id ON dict_words(book_id);
CREATE INDEX idx_head_word ON dict_words(head_word);

-- 优化查询
VACUUM;
ANALYZE;
```

### 2. 应用优化

```python
# 使用缓存
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/v1/books')
@cache.cached(timeout=3600)
def get_books():
    pass
```

### 3. Nginx优化

```nginx
# 开启gzip压缩
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;

# 开启HTTP/2
listen 443 ssl http2;

# 配置缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g;
```

---

## 🔄 更新和维护

### 更新应用

```bash
# 拉取最新代码
cd /var/www/lioneng-api
git pull origin main

# 激活虚拟环境
source xuebaApi/venv/bin/activate

# 更新依赖
pip install -r xuebaApi/requirements.txt

# 重启服务
sudo systemctl restart lioneng-api
```

### 零停机更新

```bash
# 使用Gunicorn的热重载
sudo systemctl reload lioneng-api

# 或使用Nginx的灰度发布
# 配置多个upstream，逐步切换流量
```

---

## 🐛 故障排查

### 服务无法启动

```bash
# 查看服务状态
sudo systemctl status lioneng-api

# 查看详细日志
sudo journalctl -u lioneng-api -n 100 --no-pager
```

### API响应缓慢

```bash
# 检查进程资源使用
htop

# 检查数据库性能
sqlite3 lioneng.db ".timer on" "SELECT COUNT(*) FROM dict_words;"

# 检查Nginx日志
tail -f /var/log/nginx/lioneng-api.access.log | grep "request_time"
```

### 数据库锁定

```bash
# 检查数据库连接
lsof | grep lioneng.db

# 重建数据库索引
sqlite3 lioneng.db "REINDEX;"
```

---

## 📞 技术支持

部署遇到问题？

- 📧 邮箱: devops@lioneng.com
- 📝 Issues: https://github.com/your-org/xuebadictapp/issues
- 📖 文档: https://docs.lioneng.com

---

**部署愉快！** 🚀

最后更新: 2026-02-04

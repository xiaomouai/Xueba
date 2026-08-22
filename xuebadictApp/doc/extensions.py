"""
Flask扩展实例
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# 数据库
db = SQLAlchemy()

# 数据库迁移
migrate = Migrate()

# JWT认证
jwt = JWTManager()

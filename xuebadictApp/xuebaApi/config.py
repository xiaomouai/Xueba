"""
配置文件
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# 获取项目根目录的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """基础配置"""
    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 数据库基本配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
    DB_NAME = os.getenv('DB_NAME', 'xuebadict')

    # 动态构建数据库URI
    # 1. 优先使用完整的SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # 2. 其次使用DATABASE_URL
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # 3. 最后根据分片配置构建MySQL URI
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 3600
    
    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}" if REDIS_PASSWORD else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Celery配置
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4'}
    
    # 分页配置
    PAGINATION_PAGE_SIZE = int(os.getenv('PAGINATION_PAGE_SIZE', 20))
    
    # 阿里云配置
    ALIYUN_ACCESS_KEY_ID = os.getenv('ALIYUN_ACCESS_KEY_ID', '')
    ALIYUN_ACCESS_KEY_SECRET = os.getenv('ALIYUN_ACCESS_KEY_SECRET', '')
    ALIYUN_SMS_SIGN_NAME = os.getenv('ALIYUN_SMS_SIGN_NAME', '狮子英语')
    ALIYUN_SMS_TEMPLATE_CODE = os.getenv('ALIYUN_SMS_TEMPLATE_CODE', '')
    
    # OSS配置
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', '')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', '')
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', '')
    
    # 微信支付配置
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', '')
    WECHAT_MCH_ID = os.getenv('WECH_ID', '')
    WECHAT_API_KEY = os.getenv('WECHAT_API_KEY', '')
    WECHAT_NOTIFY_URL = os.getenv('WECHAT_NOTIFY_URL', '')
    
    # 支付宝配置
    ALIPAY_APP_ID = os.getenv('ALIPAY_APP_ID', '')
    ALIPAY_PRIVATE_KEY_PATH = os.getenv('ALIPAY_PRIVATE_KEY_PATH', '')
    ALIPAY_PUBLIC_KEY_PATH = os.getenv('ALIPAY_PUBLIC_KEY_PATH', '')
    ALIPAY_NOTIFY_URL = os.getenv('ALIPAY_NOTIFY_URL', '')
    
    # 讯飞AI配置
    XUNFEI_APP_ID = os.getenv('XUNFEI_APP_ID', '')
    XUNFEI_API_KEY = os.getenv('XUNFEI_API_KEY', '')
    XUNFEI_API_SECRET = os.getenv('XUNFEI_API_SECRET', '')
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

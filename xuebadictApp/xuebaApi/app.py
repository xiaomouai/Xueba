"""
狮子英语 API 主应用
"""
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flasgger import Swagger
import os
from datetime import datetime

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from flask import Flask
    app = Flask(__name__)
    
    # 启用CORS - 允许所有来源访问，并支持凭据
    # 指定常见的开发环境来源，确保跨域请求成功
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://127.0.0.1:8080", "http://localhost:8080", "http://localhost:5000"]}})
    
    # 加载配置
    from config import config as app_config
    app.config.from_object(app_config.get(config_name, app_config['development']))
    
    # 基础配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_AS_ASCII'] = False
    
    # 初始化扩展
    from extensions import db, migrate, jwt
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # 导入模型以确保 db.create_all() 能识别到表结构
    with app.app_context():
        import models
    
    # 自动创建数据库表（开发环境下）
    if app.config.get('DEBUG'):
        with app.app_context():
            try:
                db.create_all()
                print("✅ 数据库表自动创建/验证完成")
            except Exception as e:
                print(f"⚠️ 数据库表创建失败 (可能是MySQL未启动或数据库不存在): {e}")
    
    # Swagger配置
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
            "description": "基于Dict词库的小学英语学习API - 完整的RESTful接口文档",
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
        },
        "tags": [
            {"name": "教材管理", "description": "教材版本和词书管理"},
            {"name": "单词学习", "description": "单词查询、学习和搜索"},
            {"name": "闯关练习", "description": "单元闯关和挑战"},
            {"name": "听写练习", "description": "单词和短语听写"},
            {"name": "用户认证", "description": "注册、登录和token管理"},
            {"name": "用户中心", "description": "用户信息和设置"}
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # 注册蓝图
    register_blueprints(app)

    # 注册后台管理静态页面路由
    @app.route('/xuebaApi/admin/')
    @app.route('/xuebaApi/admin/<path:path>')
    def serve_admin(path='index.html'):
        admin_path = os.path.join(os.path.dirname(app.root_path), 'admin')
        return send_from_directory(admin_path, path)
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app


def register_blueprints(app):
    """注册蓝图 - 统一使用 /api/v1 前缀"""
    from api import api_v1
    
    # 注册主蓝图（包含所有路由）- 统一前缀 /api/v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    print("\n" + "="*60)
    print("📋 API 路由注册完成")
    print("="*60)
    
    @app.route('/')
    def index():
        return jsonify({
            'name': '狮子英语 API',
            'version': '2.0.0',
            'status': 'running',
            'description': '基于Dict词库的小学英语学习API',
            'documentation': '/api/docs',
            'base_url': '/api/v1',
            'modules': {
                'textbook': '教材管理',
                'word': '单词学习',
                'auth': '用户认证',
                'user': '用户中心',
                'membership': '会员系统',
                'payment': '支付系统',
                'speech': '独立发音评测',
                'challenge': '闯关练习',
                'dictation': '听写练习'
            },
            'key_endpoints': {
                'health': '/api/v1/health',
                'textbooks': '/api/v1/textbooks',
                'books': '/api/v1/books',
                'words': '/api/v1/words/{book_id}/{word_rank}',
                'membership': '/api/v1/membership/status',
                'challenge': '/api/v1/challenge/create',
                'dictation': '/api/v1/dictation/create',
                'payment': '/api/v1/payment/create',
                'speech': '/api/v1/speech/evaluate'
            }
        })
    
    @app.route('/health')
    @app.route('/api/v1/health')
    def health():
        """健康检查接口"""
        from utils.response import success_response
        return success_response({
            'status': 'healthy', 
            'message': 'API is running',
            'version': '2.0.0',
            'timestamp': datetime.now().isoformat()
        })


def register_error_handlers(app):
    """注册错误处理器"""
    from utils.response import error_response
    
    @app.errorhandler(400)
    def bad_request(error):
        return error_response(400, '请求参数错误')
    
    @app.errorhandler(401)
    def unauthorized(error):
        return error_response(401, '未授权，请先登录')
    
    @app.errorhandler(403)
    def forbidden(error):
        return error_response(403, '禁止访问')
    
    @app.errorhandler(404)
    def not_found(error):
        return error_response(404, '资源不存在')
    
    @app.errorhandler(500)
    def internal_error(error):
        return error_response(500, '服务器内部错误')


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    print("="*60)
    print("🦁 狮子英语 API 服务启动中...")
    print("="*60)
    print(f"📚 Dict词库路径: ./dict/book/")
    print(f"🌐 服务地址: http://localhost:5000")
    print(f"💚 健康检查: http://localhost:5000/health")
    print(f"📖 API文档: http://localhost:5000/api/docs")
    print(f"📋 Swagger JSON: http://localhost:5000/apispec.json")
    print("="*60)
    print("\n✨ 核心接口:")
    print("  GET  /api/v1/textbooks")
    print("  GET  /api/v1/textbooks/PEP/books?grade=3&category=小学")
    print("  GET  /api/v1/books/PEPXiaoXue3_1/words")
    print("  GET  /api/v1/words/PEPXiaoXue3_1/1")
    print("  GET  /api/v1/words/search?keyword=hello")
    print("  GET  /api/v1/units/unit_001/challenges")
    print("  POST /api/v1/units/unit_001/dictation/start")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

"""
API路由包 - 统一管理所有API路由
"""
from flask import Blueprint
from flask_cors import CORS

# 创建API v1蓝图
api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1) # 为蓝图开启跨域支持

# ========== 核心模块 ==========
# 导入使用 api_v1 的旧模块
from . import textbook, word, auth, user, feedback, work_english

# ========== 新增模块 ==========
# 导入会员、闯关、听写模块（这些模块使用子蓝图）
try:
    from .membership import bp as membership_bp
    api_v1.register_blueprint(membership_bp, url_prefix='/membership')
    print("✅ Membership module loaded")
except ImportError as e:
    print(f"⚠️  Could not import membership: {e}")

try:
    from .challenge import bp as challenge_bp
    api_v1.register_blueprint(challenge_bp, url_prefix='/challenge')
    print("✅ Challenge module loaded")
except ImportError as e:
    print(f"⚠️  Could not import challenge: {e}")

try:
    from .dictation import bp as dictation_bp
    api_v1.register_blueprint(dictation_bp, url_prefix='/dictation')
    print("✅ Dictation module loaded")
except ImportError as e:
    print(f"⚠️  Could not import dictation: {e}")

# ========== 可选模块 ==========
try:
    from . import audio
    print("✅ Audio module loaded")
except ImportError as e:
    print(f"⚠️  Could not import audio: {e}")

try:
    # 注册 AI 模块（重构后）
    from .ai import ai_bp
    api_v1.register_blueprint(ai_bp, url_prefix='/ai')
    print("✅ AI module (refactored) loaded")
except ImportError as e:
    print(f"⚠️  Could not import ai module: {e}")

# ========== 子蓝图 ==========
try:
# 注册版本管理模块
    from .version import version_bp
    api_v1.register_blueprint(version_bp, url_prefix='/version')
    print("✅ Version module loaded")

    # 注册后台管理模块
    from .admin import admin_bp
    api_v1.register_blueprint(admin_bp, url_prefix='/admin')
    print("✅ Admin module loaded")
except ImportError as e:
    print(f"⚠️  Could not import version blueprint: {e}")

try:
    from .word_spelling import spelling_bp
    api_v1.register_blueprint(spelling_bp, url_prefix='/spelling')
    print("✅ Spelling module loaded")
except ImportError as e:
    print(f"⚠️  Could not import spelling blueprint: {e}")

# ========== 激活码模块 ==========
try:
    from .activation import activation_bp
    api_v1.register_blueprint(activation_bp, url_prefix='/activation')
    print("✅ Activation module loaded")
except ImportError as e:
    print(f"⚠️  Could not import activation: {e}")

# ========== 签到模块 ==========
try:
    from .checkin import checkin_bp
    api_v1.register_blueprint(checkin_bp, url_prefix='/checkin')
    print("✅ Checkin module loaded")
except ImportError as e:
    print(f"⚠️  Could not import checkin: {e}")

# ========== 支付与独立语音评测模块 ==========
try:
    from .payment import payment_bp
    api_v1.register_blueprint(payment_bp, url_prefix='/payment')
    print("✅ Payment module loaded")
except ImportError as e:
    print(f"⚠️  Could not import payment: {e}")

try:
    from .speech_evaluator import speech_bp
    api_v1.register_blueprint(speech_bp, url_prefix='/speech')
    print("✅ Speech evaluator module loaded")
except ImportError as e:
    print(f"⚠️  Could not import speech evaluator: {e}")

__all__ = ['api_v1']

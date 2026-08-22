"""
创建初始管理员账号
"""
import sys
import os

# 确保 xuebaApi 目录在 python 路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(current_dir, 'xuebaApi')

if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

# 必须使用与 app.py 一致的导入方式（不带 xuebaApi. 前缀）
# 否则会导致 SQLAlchemy 报 "Table 'users' is already defined" 错误
from app import create_app
from extensions import db
from models.user_models import User
from services.user_service import UserService

def create_admin(phone, password, nickname="系统管理员"):
    app = create_app('development')
    with app.app_context():
        # 尝试更新表结构，确保 admin 角色存在
        try:
            from sqlalchemy import text
            db.session.execute(text("ALTER TABLE users MODIFY COLUMN role ENUM('student', 'parent', 'admin') NOT NULL"))
            db.session.commit()
            print("✅ 数据库表结构已同步 (role enum)")
        except Exception as e:
            db.session.rollback()
            # 如果失败可能是列已经更新或环境不支持 ALTER，忽略错误继续
            pass

        # 检查是否已存在
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            print(f"用户 {phone} 已存在，正在更新为管理员角色...")
            existing_user.role = 'admin'
            existing_user.password_hash = UserService.hash_password(password)
            db.session.commit()
            print("更新成功！")
            return

        # 创建新管理员
        admin = User(
            id=UserService.generate_user_id(),
            phone=phone,
            password_hash=UserService.hash_password(password),
            nickname=nickname,
            role='admin',
            status='active',
            invite_code=UserService.generate_invite_code()
        )
        
        db.session.add(admin)
        db.session.commit()
        print(f"管理员账号创建成功！\n手机号: {phone}\n密码: {password}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="创建猫头鹰词典管理员账号")
    parser.add_argument("--phone", required=True, help="管理员手机号")
    parser.add_argument("--password", required=True, help="管理员密码")
    parser.add_argument("--nickname", default="系统管理员", help="管理员昵称")
    
    args = parser.parse_args()
    create_admin(args.phone, args.password, args.nickname)

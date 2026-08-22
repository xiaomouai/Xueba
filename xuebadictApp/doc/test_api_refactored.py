"""
API测试脚本
用于测试重构后的API接口
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/v1"


def print_response(title, response):
    """打印响应结果"""
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_textbooks():
    """测试教材相关接口"""
    print("\n🧪 测试教材相关API")
    
    # 1. 获取教材列表
    response = requests.get(f"{BASE_URL}/textbooks")
    print_response("获取教材列表", response)
    
    # 2. 获取词书列表
    response = requests.get(f"{BASE_URL}/books?category=小学&grade=3")
    print_response("获取词书列表", response)
    
    # 3. 获取单词列表
    response = requests.get(f"{BASE_URL}/books/PEPXiaoXue3_1/words?page=1&page_size=5")
    print_response("获取单词列表（分页）", response)


def test_words():
    """测试单词相关接口"""
    print("\n🧪 测试单词相关API")
    
    # 1. 获取单词详情
    response = requests.get(f"{BASE_URL}/words/PEPXiaoXue3_1/1")
    print_response("获取单词详情", response)
    
    # 2. 搜索单词
    response = requests.get(f"{BASE_URL}/words/search?keyword=hello&limit=5")
    print_response("搜索单词", response)
    
    # 3. 批量获取单词
    payload = {
        "words": [
            {"bookId": "PEPXiaoXue3_1", "wordRank": 1},
            {"bookId": "PEPXiaoXue3_1", "wordRank": 2}
        ]
    }
    response = requests.post(f"{BASE_URL}/words/batch", json=payload)
    print_response("批量获取单词", response)


def test_auth():
    """测试认证相关接口"""
    print("\n🧪 测试认证相关API")
    
    # 1. 注册用户
    register_data = {
        "phone": "13800138000",
        "code": "123456",
        "password": "test123456",
        "role": "student",
        "nickname": "测试用户",
        "grade": 3
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response("用户注册", response)
    
    # 如果注册成功，保存token
    if response.status_code == 200:
        data = response.json()
        token = data.get('data', {}).get('token')
        return token
    
    # 2. 如果注册失败（可能已存在），尝试登录
    login_data = {
        "phone": "13800138000",
        "password": "test123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("用户登录", response)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('data', {}).get('token')
        return token
    
    return None


def test_user(token):
    """测试用户相关接口"""
    if not token:
        print("\n⚠️  跳过用户API测试（没有token）")
        return
    
    print("\n🧪 测试用户相关API")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. 获取用户信息
    response = requests.get(f"{BASE_URL}/user/profile", headers=headers)
    print_response("获取用户信息", response)
    
    # 2. 更新用户信息
    update_data = {
        "nickname": "测试用户-已更新",
        "gender": "male"
    }
    response = requests.put(f"{BASE_URL}/user/profile", json=update_data, headers=headers)
    print_response("更新用户信息", response)
    
    # 3. 用户签到
    response = requests.post(f"{BASE_URL}/user/checkin", headers=headers)
    print_response("用户签到", response)
    
    # 4. 获取用户统计
    response = requests.get(f"{BASE_URL}/user/statistics", headers=headers)
    print_response("获取用户统计", response)


def test_word_learning(token):
    """测试单词学习接口"""
    if not token:
        print("\n⚠️  跳过单词学习API测试（没有token）")
        return
    
    print("\n🧪 测试单词学习API")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 更新学习记录
    learn_data = {
        "action": "practice",
        "duration": 30,
        "is_correct": True,
        "score": 95
    }
    response = requests.post(
        f"{BASE_URL}/words/PEPXiaoXue3_1/1/learn",
        json=learn_data,
        headers=headers
    )
    print_response("更新单词学习状态", response)


def main():
    """主测试函数"""
    print("="*60)
    print("🚀 狮子英语 API 测试")
    print("="*60)
    print(f"📡 测试服务器: {BASE_URL}")
    print("="*60)
    
    try:
        # 测试健康检查
        response = requests.get("http://localhost:5000/health")
        print_response("健康检查", response)
        
        # 测试教材和单词接口（不需要认证）
        test_textbooks()
        test_words()
        
        # 测试认证和用户接口（需要认证）
        token = test_auth()
        test_user(token)
        test_word_learning(token)
        
        print("\n" + "="*60)
        print("✅ 测试完成")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("请确保API服务已启动: python app.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

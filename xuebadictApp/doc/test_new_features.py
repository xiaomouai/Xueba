"""
会员系统、闯关和听写模块测试脚本
"""
import requests
import json
from typing import Dict

BASE_URL = 'http://localhost:5000'

class APITester:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.challenge_id = None
        self.dictation_id = None
    
    def print_result(self, title: str, response):
        """打印测试结果"""
        print(f"\n{'='*60}")
        print(f"📝 {title}")
        print(f"{'='*60}")
        print(f"状态码: {response.status_code}")
        try:
            data = response.json()
            print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        except:
            print(f"响应: {response.text}")
        print(f"{'='*60}\n")
    
    def test_register_and_login(self):
        """测试注册和登录"""
        print("\n🔐 【步骤1】用户认证测试")
        
        # 注册
        register_data = {
            'username': f'test_user_{int(requests.get(f"{BASE_URL}/health").elapsed.total_seconds()*1000)}',
            'password': 'Test123456',
            'phone': '13800138000'
        }
        
        response = requests.post(f'{BASE_URL}/api/auth/register', json=register_data)
        self.print_result('用户注册', response)
        
        # 登录
        login_data = {
            'username': register_data['username'],
            'password': register_data['password']
        }
        
        response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        self.print_result('用户登录', response)
        
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                self.token = data['data']['token']
                self.user_id = data['data']['user_id']
                print(f"✅ 登录成功! Token: {self.token[:20]}...")
    
    def get_headers(self) -> Dict:
        """获取请求头"""
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def test_membership_plans(self):
        """测试会员套餐"""
        print("\n💎 【步骤2】会员系统测试")
        
        # 获取会员套餐列表
        response = requests.get(f'{BASE_URL}/api/membership/plans')
        self.print_result('获取会员套餐列表', response)
        
        # 获取我的会员信息
        response = requests.get(
            f'{BASE_URL}/api/membership/my-membership',
            headers=self.get_headers()
        )
        self.print_result('获取我的会员信息', response)
    
    def test_create_order(self):
        """测试创建订单"""
        print("\n💳 【步骤3】订单创建测试")
        
        # 创建会员订单
        order_data = {
            'plan_id': 1,  # 月度会员
            'payment_method': 'alipay'
        }
        
        response = requests.post(
            f'{BASE_URL}/api/membership/create-order',
            json=order_data,
            headers=self.get_headers()
        )
        self.print_result('创建会员订单', response)
        
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                order_id = data['data']['order_id']
                
                # 模拟支付回调
                callback_data = {'order_id': order_id}
                response = requests.post(
                    f'{BASE_URL}/api/membership/pay/callback',
                    json=callback_data
                )
                self.print_result('支付回调（激活会员）', response)
        
        # 获取订单列表
        response = requests.get(
            f'{BASE_URL}/api/membership/orders',
            headers=self.get_headers()
        )
        self.print_result('获取订单列表', response)
        
        # 获取会员权益
        response = requests.get(
            f'{BASE_URL}/api/membership/benefits',
            headers=self.get_headers()
        )
        self.print_result('获取会员权益', response)
    
    def test_challenge(self):
        """测试闯关功能"""
        print("\n🎯 【步骤4】闯关模块测试")
        
        # 获取难度列表
        response = requests.get(f'{BASE_URL}/api/challenge/difficulties')
        self.print_result('获取难度列表', response)
        
        # 获取题型列表
        response = requests.get(f'{BASE_URL}/api/challenge/types')
        self.print_result('获取题型列表', response)
        
        # 创建闯关
        challenge_data = {
            'word_book_id': 1,
            'difficulty': 'easy',
            'question_type': 'choose_meaning'
        }
        
        response = requests.post(
            f'{BASE_URL}/api/challenge/create',
            json=challenge_data,
            headers=self.get_headers()
        )
        self.print_result('创建闯关', response)
        
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                self.challenge_id = data['data']['challenge_id']
                questions = data['data']['questions']
                
                # 模拟答题
                if questions:
                    first_question = questions[0]
                    # 找到正确答案
                    correct_option = next((opt for opt in first_question['options'] if opt['is_correct']), None)
                    
                    answer_data = {
                        'word_id': first_question['word_id'],
                        'user_answer': correct_option['option'] if correct_option else 'A',
                        'is_correct': True,
                        'time_spent': 5
                    }
                    
                    response = requests.post(
                        f'{BASE_URL}/api/challenge/{self.challenge_id}/submit',
                        json=answer_data,
                        headers=self.get_headers()
                    )
                    self.print_result('提交答案', response)
                
                # 完成闯关
                response = requests.post(
                    f'{BASE_URL}/api/challenge/{self.challenge_id}/finish',
                    headers=self.get_headers()
                )
                self.print_result('完成闯关', response)
        
        # 获取闯关历史
        response = requests.get(
            f'{BASE_URL}/api/challenge/history',
            headers=self.get_headers()
        )
        self.print_result('获取闯关历史', response)
        
        # 获取闯关统计
        response = requests.get(
            f'{BASE_URL}/api/challenge/stats',
            headers=self.get_headers()
        )
        self.print_result('获取闯关统计', response)
    
    def test_dictation(self):
        """测试听写功能"""
        print("\n✍️ 【步骤5】听写模块测试")
        
        # 获取听写模式列表
        response = requests.get(f'{BASE_URL}/api/dictation/modes')
        self.print_result('获取听写模式列表', response)
        
        # 创建听写
        dictation_data = {
            'word_book_id': 1,
            'mode': 'random',
            'word_count': 5
        }
        
        response = requests.post(
            f'{BASE_URL}/api/dictation/create',
            json=dictation_data,
            headers=self.get_headers()
        )
        self.print_result('创建听写', response)
        
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                self.dictation_id = data['data']['dictation_id']
                words = data['data']['words']
                
                # 模拟听写答题
                if words:
                    for word in words[:3]:  # 只测试前3个
                        answer_data = {
                            'word_id': word['word_id'],
                            'user_answer': word['word']  # 正确答案
                        }
                        
                        response = requests.post(
                            f'{BASE_URL}/api/dictation/{self.dictation_id}/submit',
                            json=answer_data,
                            headers=self.get_headers()
                        )
                        self.print_result(f'提交听写答案 - {word["word"]}', response)
                
                # 完成听写
                response = requests.post(
                    f'{BASE_URL}/api/dictation/{self.dictation_id}/finish',
                    headers=self.get_headers()
                )
                self.print_result('完成听写', response)
        
        # 获取听写详情
        if self.dictation_id:
            response = requests.get(
                f'{BASE_URL}/api/dictation/{self.dictation_id}',
                headers=self.get_headers()
            )
            self.print_result('获取听写详情', response)
        
        # 获取听写历史
        response = requests.get(
            f'{BASE_URL}/api/dictation/history',
            headers=self.get_headers()
        )
        self.print_result('获取听写历史', response)
        
        # 获取听写统计
        response = requests.get(
            f'{BASE_URL}/api/dictation/stats',
            headers=self.get_headers()
        )
        self.print_result('获取听写统计', response)
        
        # 获取错词本
        response = requests.get(
            f'{BASE_URL}/api/dictation/wrong-words',
            headers=self.get_headers()
        )
        self.print_result('获取错词本', response)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🚀 开始测试会员系统、闯关和听写模块")
        print("="*60)
        
        try:
            self.test_register_and_login()
            
            if not self.token:
                print("\n❌ 登录失败，无法继续测试")
                return
            
            self.test_membership_plans()
            self.test_create_order()
            self.test_challenge()
            self.test_dictation()
            
            print("\n" + "="*60)
            print("✅ 所有测试完成!")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ 测试出错: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()

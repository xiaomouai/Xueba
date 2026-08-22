import requests
import json

def test_login_api():
    url = "http://localhost:5000/api/v1/auth/login"
    
    # 1. Test OPTIONS request (Preflight)
    print("--- Testing OPTIONS (Preflight) ---")
    headers_options = {
        "Origin": "http://127.0.0.1:8080",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    resp_options = requests.options(url, headers=headers_options)
    print(f"Status: {resp_options.status_code}")
    for k, v in resp_options.headers.items():
        if "Access-Control" in k or "Vary" in k:
            print(f"{k}: {v}")

    # 2. Test POST request (Actual Login)
    print("\n--- Testing POST (Login) ---")
    headers_post = {
        "Origin": "http://127.0.0.1:8080",
        "Content-Type": "application/json"
    }
    data = {
        "phone": "13800138000",
        "password": "wrong_password"
    }
    resp_post = requests.post(url, headers=headers_post, data=json.dumps(data))
    print(f"Status: {resp_post.status_code}")
    print(f"Body: {resp_post.text}")
    for k, v in resp_post.headers.items():
        if "Access-Control" in k or "Vary" in k:
            print(f"{k}: {v}")

if __name__ == "__main__":
    test_login_api()

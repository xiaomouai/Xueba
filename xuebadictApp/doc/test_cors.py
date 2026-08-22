import requests

def test_cors():
    url = "http://localhost:5000/api/v1/auth/login"
    headers = {
        "Origin": "http://127.0.0.1:8080",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    
    print(f"Testing OPTIONS request to {url}")
    try:
        response = requests.options(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Headers:")
        for key, value in response.headers.items():
            if key.startswith("Access-Control"):
                print(f"  {key}: {value}")
        
        if "Access-Control-Allow-Origin" in response.headers:
            print("\nSUCCESS: CORS headers are present!")
        else:
            print("\nFAILURE: CORS headers are missing!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cors()

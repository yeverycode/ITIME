import requests

url = "http://127.0.0.1:8000/users/signup"
data = {
    "email": "test@gmail.com",
    "name": "빈코더",
    "phone": "01020304050",
    "nickname": "빈코더",
    "password": "123456781"
}

response = requests.post(url, data=data)

# 상태 코드 출력
print(f"Status Code: {response.status_code}")

try:
    response_data = response.json()
    print(response_data)
except requests.exceptions.JSONDecodeError:
    print("Response content is not in JSON format.")
    print(response.text)

import requests

data = {
    "code": "116713"
}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3V1aWQiOiJkMmI3YzM1NC0xZTM4LTQyZGYtYjMyZi1hMzUxYmYwODEwZjIiLCJjcmVhdGVkX2F0IjoiMjAyNC0wNC0xNFQxNDo1NjoxNy40MzY5MzIiLCJleHAiOjE3MTMxMDY2MzcsInN1YiI6ImFjY2VzcyJ9.eJjqzJv8SY1lBfMyGa5xNrsDJhhBDw4iq6osogPhzAw"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}
resp = requests.post("http://localhost:8080/api/auth/login/access-token", json=data, headers=headers)
print(resp.text, resp.status_code, resp.headers)
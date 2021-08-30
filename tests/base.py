from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

user_data = {"username" : "test@evoke.com", "password" : "12345", "scope":"admin"}
user_id = 0
category_id = 0
product_id = 0

def jwt_token():
    data = {"username" : user_data['username'], "password" : user_data['password'], "scope":user_data['scope']}
    response = client.post("/login", data=data)
    return response

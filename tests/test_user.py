from fastapi.testclient import TestClient
import json
from main import app
from . import base

client = TestClient(app)

jwt_token = base.jwt_token()

def test_register_user():
    data = {
        "firstname": "pradeep",
        "lastname": "kumar",
        "email": base.user_data['username'],
        "password": base.user_data['password'],
        "mobile": "99999999",
        "address": "kaikalur",
        "role_id": 1
    }

    response = client.post("/user/register", data=json.dumps(data))
    assert response.status_code == 201
    
    base.user_id = response.json()['id']

def test_users():
    response = client.get("/users")
    assert response.status_code == 401

    response = client.get("/users", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_show_user():
    response = client.get("/user/999")
    assert response.status_code == 401

    response = client.get("/user/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 999 not found"

    response = client.get(f"/user/{base.user_id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_user():
    data = {
        "firstname": "pradeep",
        "lastname": "kumar",
        "email": base.user_data['username'],
        "mobile": "1234567890",
        "address": "kaikalur"
        }

    response = client.put(f"/user/{base.user_id}", data = json.dumps(data))
    assert response.status_code == 401

    response = client.put(f"/user/{base.user_id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 202



     

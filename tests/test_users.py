from fastapi.testclient import TestClient
import json
from main import app

client = TestClient(app)

id = 0

def get_jwt_token():
    data = {"username" : "p@evoke.com", "password" : "12345"}
    response = client.post("/login", data=data)
    return response

def test_users():
    response = client.get("/users")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.get("/users", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_register_user():
    data = {
        "firstname": "pradeep",
        "lastname": "kumar",
        "password": "12345",
        "email": "p@evoke.com",
        "mobile": "99999999",
        "address": "kaikalur"
        }
    response = client.post("/user/register")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.post("/user/register", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 201
    global id 
    id = response.json()['id']

def test_show_user():
    response = client.get("/user/999")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.get("/user/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 999 not found"

    response = client.get("/user/%s"%(id) , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_user():
    data = {
        "firstname": "pradeep",
        "lastname": "kumar",
        "password": "12345",
        "email": "p@evoke.com",
        "mobile": "00000000",
        "address": "kaikalur"
        }
    response = client.put("/user/id")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.put(f"/user/{id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 202

def test_delete():
    response = client.delete("/user/999")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.delete("/user/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 999 not found"
    
    response = client.delete("/user/%s"%(id) , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204

     

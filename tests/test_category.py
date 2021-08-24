from fastapi.testclient import TestClient
import json
from main import app

client = TestClient(app)

id = 0

def get_jwt_token():
    data = {"username" : "p@evoke.com", "password" : "12345"}
    response = client.post("/login", data=data)
    return response

def test_categories():
    response = client.get("/categories")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.get("/categories", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_create_category():
    response = client.post("/category/add")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    data = {}
    response = client.post("/category/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 422

    data = {
        "name": "furniture"
    }

    response = client.post("/category/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 201

    global id 
    id = response.json()['id']

def test_show_category():
    response = client.get("/category/999")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.get("/category/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Category with id 999 not found"

    response = client.get(f"/category/{id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_category():
    
    data = {
        "name": "mobiles"
    }

    response = client.put(f"/category/{id}", data=json.dumps(data))
    assert response.status_code == 401

    jwt_token = get_jwt_token()

    response = client.put(f"/category/{id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 202

def test_delete():
    response = client.delete("/category/999")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.delete("/category/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Category with id 999 not found"
    
    response = client.delete(f"/category/{id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204

     

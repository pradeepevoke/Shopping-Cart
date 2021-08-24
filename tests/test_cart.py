from fastapi.testclient import TestClient
import json
from main import app

client = TestClient(app)

id = 0

def get_jwt_token():
    data = {"username" : "p@evoke.com", "password" : "12345"}
    response = client.post("/login", data=data)
    return response

def test_add_cart():
    data = {
        "user_id": 0,
        "product_id": 0,
        "quantity": 0
    }
    response = client.post("/cart/add")
    assert response.status_code == 401

    jwt_token = get_jwt_token()

    response = client.post("/cart/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 400

    data = {
        "user_id": 0,
        "product_id": 0,
        "quantity": 1
    }

    response = client.post("/cart/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 500

    data = {
        "user_id": 7,
        "product_id": 3,
        "quantity" : 2
    }

    response = client.post("/cart/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 201
    global id 
    id = response.json()['id']

def test_get_carts():
    response = client.get("/cart", data={"user_id": id})
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    data = {"user_id": id}
    response = client.get(f"/cart?user_id={id}", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_cart():
    data = {
        "user_id": 0,
        "product_id": 0,
        "quantity": 0
    }
    response = client.put(f"/cart/{id}")
    assert response.status_code == 401

    jwt_token = get_jwt_token()

    response = client.put(f"/cart/{id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 400

    data = {
        "user_id": 0,
        "product_id": 0,
        "quantity": 1
    }

    response = client.put(f"/cart/{id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 500

    data = {
        "user_id": 7,
        "product_id": 4,
        "quantity" : 2
    }

    response = client.put(f"/cart/{id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 202

def test_delete_cart():
    response = client.delete(f"/cart/{id}")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.delete("/cart/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart with id 999 not found"
    
    response = client.delete(f"/cart/{id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204

     

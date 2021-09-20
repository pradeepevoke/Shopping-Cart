from fastapi.testclient import TestClient
import json
from main import app
from . import base

client = TestClient(app)
jwt_token = base.jwt_token()

def test_categories():
    response = client.get("/categories")
    assert response.status_code == 401

    response = client.get("/categories", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_create_category():
    response = client.post("/category/add")
    assert response.status_code == 401

    data = {}
    response = client.post("/category/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 422

    data = {
        "name": "furniture", 
        "description" : "For testing"
    }

    response = client.post("/category/add", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 201

    base.category_id = response.json()['id']

def test_show_category():
    response = client.get("/category/999")
    assert response.status_code == 401

    response = client.get("/category/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Category with id 999 not found"

    response = client.get(f"/category/{base.category_id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_category():
    
    data = {
        "name": "mobiles",
        "description" : "For testing"
    }

    response = client.put(f"/category/{base.category_id}", data=json.dumps(data))
    assert response.status_code == 401

    response = client.put(f"/category/{base.category_id}", data=json.dumps(data), headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 202


     

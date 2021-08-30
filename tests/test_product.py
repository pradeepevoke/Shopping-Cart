from fastapi.testclient import TestClient
import json
from main import app
from . import base

client = TestClient(app)
jwt_token = base.jwt_token()

def test_product():
    response = client.get("/products")
    assert response.status_code == 401

    response = client.get("/products", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_create_product():
    response = client.post("/product/add")
    assert response.status_code == 401

    data = {}
    response = client.post("/product/add", data=data, headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token'], "Content_Type":"multipart/form-data"})
    assert response.status_code == 422

    data = {
        "name" : "test", 
        "category_id" : base.category_id, 
        "description" : "Testcase Description", 
        "price" : 3000, 
    }
    uploaded_file = {
        "image" : ("gloves.jpg", open('images/gloves.jpg', 'rb'), "image/jpeg")
    }
    
    response = client.post("/product/add", data=data, files=uploaded_file, headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token'], "Content_Type":"multipart/form-data"})
    assert response.status_code == 201

    base.product_id = response.json()['id']

def test_show_product():
    response = client.get("/product/999")
    assert response.status_code == 401

    response = client.get("/product/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 999 not found"

    response = client.get(f"/product/{base.product_id}", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_product():
    data = {
        "name" : "testcase", 
        "category_id" : base.category_id, 
        "description" : "Testcase Description", 
        "price" : 3000, 
    }
    uploaded_file = {
        "image" : ("gloves.jpg", open('images/gloves.jpg', 'rb'), "image/jpeg")
    }

    response = client.put(f"/product/{base.product_id}", data=data)
    assert response.status_code == 401

    response = client.put(f"/product/{base.product_id}", data=data, files=uploaded_file, headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token'], "Content_Type":"multipart/form-data"})
    assert response.status_code == 202

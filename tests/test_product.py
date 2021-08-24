from fastapi.testclient import TestClient
import json
from main import app

client = TestClient(app)

id = 0

def get_jwt_token():
    data = {"username" : "p@evoke.com", "password" : "12345"}
    response = client.post("/login", data=data)
    return response

def test_product():
    response = client.get("/products")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.get("/products", headers={"Authorization": "Bearer "+jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_create_product():
    response = client.post("/product/add")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    data = {}
    response = client.post("/product/add", data=data, headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 422

    data = {
        "name" : "testcase", 
        "category_id" : 3, 
        "description" : "Testcase Description", 
        "price" : 3000, 
    }
    uploaded_file = {
        "image" : ("gloves", open('C:/Users/pghantasala/Downloads/gloves.jpg', 'rb'), "image/jpg")
    }
    
    response = client.post("/product/add", data=data, files=uploaded_file, headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token'], "Content_Type":"multipart/form-data"})
    assert response.status_code == 201

    global id 
    id = response.json()['id']

def test_show_product():
    response = client.get("/product/999")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.get("/product/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 999 not found"

    response = client.get(f"/product/{id}", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 200

def test_update_product():
    data = {
        "name" : "testcase", 
        "category_id" : 3, 
        "description" : "Testcase Description", 
        "price" : 3000, 
    }
    uploaded_file = {
        "image" : ("gloves", open('C:/Users/pghantasala/Downloads/gloves.jpg', 'rb'), "image/jpg")
    }

    response = client.put(f"/product/{id}", data=data)
    assert response.status_code == 401

    jwt_token = get_jwt_token()

    response = client.put(f"/product/{id}", data=data, files=uploaded_file, headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token'], "Content_Type":"multipart/form-data"})
    assert response.status_code == 202

def test_delete():
    response = client.delete("/product/999")
    assert response.status_code == 401

    jwt_token = get_jwt_token()
    response = client.delete("/product/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 999 not found"
    
    response = client.delete(f"/product/{id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204

     

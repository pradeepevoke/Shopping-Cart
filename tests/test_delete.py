from fastapi.testclient import TestClient
from main import app
from . import base

client = TestClient(app)
jwt_token = base.jwt_token()

def test_delete_product():
    response = client.delete("/product/999")
    assert response.status_code == 401

    response = client.delete("/product/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 999 not found"
    
    response = client.delete(f"/product/{base.product_id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204

def test_delete_category():
    response = client.delete("/category/999")
    assert response.status_code == 401

    response = client.delete("/category/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "Category with id 999 not found"
    
    response = client.delete(f"/category/{base.category_id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204

def test_delete_user():
    response = client.delete("/user/999")
    assert response.status_code == 401

    response = client.delete("/user/999", headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 999 not found"
    
    response = client.delete(f"/user/{base.user_id}" , headers = {"Authorization": "Bearer "+ jwt_token.json()['access_token']})
    assert response.status_code == 204
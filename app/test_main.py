from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


client = TestClient(app)
product_id = None

def get_token():
    response = client.post(
        "/v1/auth/token",
        json={"username": settings.client_id, "password": settings.client_secret}
    )
    return response.json()["access_token"]

def test_auth_token():
    # Valid credentials
    response = client.post(
        "/v1/auth/token",
        json={"username": settings.client_id, "password": settings.client_secret}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    # Invalid credentials
    response = client.post(
        "/v1/auth/token",
        json={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 401

def test_read_products():
    # Invalid parameters
    page = 0
    limit = 2000
    response = client.get(f"/v1/products?page={page}&limit={limit}")
    assert response.status_code == 422
    # Valid parameters
    page = 1
    limit = 10
    response = client.get(f"/v1/products?page={page}&limit={limit}")
    assert response.status_code == 200

def test_create_product():
    data = {
        "name": "Product 11",
        "price": 11.99,
        "quantity": 110
    }
    # Forbidden
    response = client.post(
        "/v1/products",
        json=data,
    )
    assert response.status_code == 403
    # Valid
    token = get_token()
    response = client.post(
        "/v1/products",
        json=data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    created_product = response.json()
    assert created_product["name"] == "Product 11"
    assert created_product["price"] == 11.99
    assert created_product["quantity"] == 110
    global product_id
    product_id = created_product["id"]

def test_read_product():
    global product_id
    token = get_token()
    # Not found
    response = client.get("/v1/products/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    # Found
    response = client.get(f"/v1/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Product 11"
    assert data["price"] == 11.99
    assert data["quantity"] == 110


def test_update_product():
    global product_id
    token = get_token()
    data = {
        "name": "Product 11 Updated",
        "price": 12.99,
        "quantity": 111
    }
    # Not found
    response = client.put(
        "/v1/products/999",
        json=data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    # Found
    token = get_token()
    response = client.put(
        f"/v1/products/{product_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["name"] == "Product 11 Updated"
    assert updated_data["price"] == 12.99
    assert updated_data["quantity"] == 111

def test_delete_product():
    global product_id
    token = get_token()
    # Not found
    response = client.delete("/v1/products/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    # Found
    token = get_token()
    response = client.delete(
        f"/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
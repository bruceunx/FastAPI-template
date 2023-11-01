import pytest


@pytest.fixture()
def auth_token(client):
    payload = {"username": "test", "password": "test123"}
    response = client.post("/v1/user/token", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


@pytest.fixture()
def auth_admin(client):
    payload = {"username": "admin", "password": "admin123#"}
    response = client.post("/v1/user/token", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


def test_protected_endpoint(auth_token, client):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/v1/product/products/?page=1&limit=10",
                          headers=headers)
    assert response.status_code == 200
    assert "total_num" in response.json()
    assert "products" in response.json()


def test_protected_create(auth_token, client):
    headers = {"Authorization": f"Bearer {auth_token}"}
    product = {"name": "new_product"}
    response = client.post("/v1/product/product",
                           headers=headers,
                           json=product)
    assert response.status_code == 403


def test_admin_create(auth_admin, client):
    headers = {"Authorization": f"Bearer {auth_admin}"}
    product = {"name": "new_product_from_admin55"}
    response = client.post("/v1/product/product",
                           headers=headers,
                           json=product)
    assert response.status_code == 201

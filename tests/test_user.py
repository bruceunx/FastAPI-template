def test_token(client):
    payload = {"username": "test", "password": "test123"}
    response = client.post("/v1/user/token", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_failed_token(client):
    payload = {"username": "test", "password": "test"}
    response = client.post("/v1/user/token", data=payload)
    assert response.status_code == 401


def test_refresh_token(client):
    payload = {"username": "test", "password": "test123"}
    response = client.post("/v1/user/token", data=payload)
    payload = {"refresh_token": response.json()['refresh_token']}
    response = client.post("/v1/user/refresh-token", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" not in response.json()

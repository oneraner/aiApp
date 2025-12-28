def test_create_user(client):
    res = client.post("/api/v1/users/", json={"email": "a@test.com"})
    assert res.status_code == 200
    assert res.json()["email"] == "a@test.com"
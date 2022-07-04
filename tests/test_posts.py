def test_create_a_post(authorized_client):
    response = authorized_client.post()
    pass


def test_all_posts(authorized_client):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200

def test_vote_on_post_by_auth_user(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 201

def test_vote_on_post_twice_by_auth_user(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 409

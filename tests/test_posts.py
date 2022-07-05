import schemas as _schemas


def test_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    # print(response.json())
    def validate(post):
        return _schemas.ShowPostVote(**post)

    post_map = map(validate, response.json())
    post_list = list(post_map)

    # assert post_list[0].Post.id == test_posts[0].id
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_authorized_user_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 200


def test_authorized_user_get_non_existed_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/123")

    assert response.status_code == 404

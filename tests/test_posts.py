import schemas as _schemas


def test_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    # print(response.json())
    def validate(post):
        return _schemas.ShowPostVote(post)

    post_map = map(validate, test_posts)
    post_list = list(post_map)

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

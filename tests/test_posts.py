import schemas as _schemas
from pytest import mark


def test_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

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

    post = _schemas.ShowPostVote(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == "first title"
    assert post.Post.content == "first content"


def test_authorized_user_get_non_existed_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/123")

    assert response.status_code == 404


@mark.parametrize(
    "title,content,published",
    [
        ("first title", "first content", True),
        ("2nd title", "2nd content", False),
        ("3rd title", "3rd content", True),
    ],
)
def test_create_post_by_authorized_user(
    authorized_client, test_user, title, content, published
):
    response = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )
    created_post = _schemas.ShowPost(**response.json())
    assert response.status_code == 201

    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

def test_create_post_with_deafult_published_by_authorized_user(
    authorized_client, test_user):
    response = authorized_client.post(
        "/posts/", json={"title": "test title", "content": "test content"}
    )
    created_post = _schemas.ShowPost(**response.json())
    assert response.status_code == 201

    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

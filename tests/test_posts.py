import schemas as _schemas
from pytest import mark


@mark.posts
def test_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return _schemas.ShowPostVote(**post)

    post_map = map(validate, response.json())
    post_list = list(post_map)

    # assert post_list[0].Post.id == test_posts[0].id
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


@mark.posts
def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401


@mark.posts
def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401

@mark.posts
def test_authorized_user_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = _schemas.ShowPostVote(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == "first title"
    assert post.Post.content == "first content"

@mark.posts
def test_authorized_user_get_non_existed_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/123")

    assert response.status_code == 404

@mark.posts
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


def test_create_post_with_default_published_by_authorized_user(
    authorized_client, test_user
):
    response = authorized_client.post(
        "/posts/", json={"title": "test title", "content": "test content"}
    )
    created_post = _schemas.ShowPost(**response.json())
    assert response.status_code == 201

    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_posts):
    response = client.post(
        "/posts/", json={"title": "test title", "content": "test content"}
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_a_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_authorized_user_delete_a_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_authorized_user_delete_nonexisted_post(authorized_client):
    response = authorized_client.delete(f"/posts/123")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


def test_update_post_with_authorized_user(authorized_client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = _schemas.ShowPost(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert response.status_code == 403


def test_unauthenticated_user_update_post(client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id,
    }
    response = client.put(f"/posts/{test_posts[3].id}", json=data)

    assert response.status_code == 401


def test_authenticated_user_update_nonexisted_post(authorized_client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/posts/12", json=data)

    assert response.status_code == 404

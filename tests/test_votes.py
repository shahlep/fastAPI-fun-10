from pytest import fixture
import models as _models


@fixture(scope="function")
def test_vote(session, test_user, test_posts):
    new_vote = _models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post_by_auth_user(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 201


def test_vote_on_post_twice_by_auth_user(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 409


def test_vote_on_post_by_unauthorized_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == 401


def test_vote_on_nonexisted_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": 12, "dir": 1})
    assert response.status_code == 404


def test_remove_vote_on_not_given_vote_on_post_by_auth_user(
    authorized_client, test_posts
):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == 404


def test_remove_vote_on_post_by_auth_user(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == 201

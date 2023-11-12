import pytest
import json
from http import HTTPStatus


@pytest.mark.parametrize(
    "status_code, data",
    [
        (HTTPStatus.OK, {"name": "John", "content": "something"}),
        (HTTPStatus.OK, {"name": "Alice", "content": "anything"}),
        (HTTPStatus.BAD_REQUEST, {}),
        (HTTPStatus.BAD_REQUEST, {"name": 1, "content": "something"}),
        (HTTPStatus.BAD_REQUEST, {"name": None, "content": "something"}),
        (HTTPStatus.BAD_REQUEST, {"Invalid": "John", "content": "something"}),
        (HTTPStatus.BAD_REQUEST, {"name": "John", "Invalid": "something"}),
    ],
)
def test_post_post(api_client, headers, status_code, data):
    url = "/api/post/create"
    resp = api_client.post(url, data=json.dumps(data), headers=headers)
    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "status_code, post_id",
    [
        (HTTPStatus.OK, 1),
        (HTTPStatus.OK, 2),
        (HTTPStatus.NOT_FOUND, 3),
    ],
)
def test_post_item_get(api_client, headers, status_code, post_id):
    url = f"/api/post/{post_id}"
    resp = api_client.get(url, headers=headers)
    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "status_code, post_id, data",
    [
        (HTTPStatus.NO_CONTENT, 1, {"name": "newName"}),
        (HTTPStatus.NO_CONTENT, 1, {"content": "newContent"}),
    ],
)
def test_post_item_put(api_client, headers, status_code, post_id, data):
    url = f"/api/post/{post_id}"
    resp = api_client.put(url, headers=headers, data=json.dumps(data))
    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "status_code, post_id",
    [
        (HTTPStatus.NO_CONTENT, 1),
        (HTTPStatus.NO_CONTENT, 2),
        (HTTPStatus.NOT_FOUND, 3),
    ],
)
def test_post_item_delete(api_client, headers, status_code, post_id):
    url = f"/api/post/{post_id}"
    resp = api_client.delete(url, headers=headers)
    assert resp.status_code == status_code

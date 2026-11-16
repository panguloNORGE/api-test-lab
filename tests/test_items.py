import pytest
import requests


def test_health(base_url):
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_item(base_url):
    response = requests.post(f"{base_url}/items", json={"name": "buy milk"})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "buy milk"
    assert body["done"] is False
    assert isinstance(body["id"], int)


def test_get_item(base_url, new_item):
    response = requests.get(f"{base_url}/items/{new_item['id']}")
    assert response.status_code == 200
    assert response.json() == new_item


def test_list_contains_item(base_url, new_item):
    response = requests.get(f"{base_url}/items")
    assert response.status_code == 200
    assert new_item in response.json()


def test_update_item(base_url, new_item):
    response = requests.put(f"{base_url}/items/{new_item['id']}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_delete_item(base_url, new_item):
    response = requests.delete(f"{base_url}/items/{new_item['id']}")
    assert response.status_code == 204
    assert requests.get(f"{base_url}/items/{new_item['id']}").status_code == 404


@pytest.mark.parametrize("payload", [{}, {"name": ""}, {"name": "   "}, {"name": 123}])
def test_create_item_invalid_name(base_url, payload):
    response = requests.post(f"{base_url}/items", json=payload)
    assert response.status_code == 400


def test_get_missing_item(base_url):
    response = requests.get(f"{base_url}/items/999999")
    assert response.status_code == 404


def test_wrong_method_not_allowed(base_url):
    response = requests.patch(f"{base_url}/items")
    assert response.status_code == 405
import os
import time

import pytest
import requests

BASE_URL = os.environ.get("API_URL", "http://localhost:5000")


@pytest.fixture(scope="session")
def base_url():
    # Wait up to 30 seconds for the API to start
    for _ in range(30):
        try:
            if requests.get(f"{BASE_URL}/health", timeout=1).status_code == 200:
                return BASE_URL
        except requests.ConnectionError:
            pass
        time.sleep(1)
    pytest.fail(f"API at {BASE_URL} did not start")


@pytest.fixture
def new_item(base_url):
    # Create an item for a test, and delete it afterwards
    response = requests.post(f"{base_url}/items", json={"name": "test item"})
    item = response.json()
    yield item
    requests.delete(f"{base_url}/items/{item['id']}")
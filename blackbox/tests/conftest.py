import pytest
import requests

@pytest.fixture
def base_url():
    return "http://localhost:8080"

@pytest.fixture
def default_headers():
    return {
        "X-Roll-Number": "123456",
        "X-User-ID": "1"
    }

@pytest.fixture
def admin_headers():
    return {
        "X-Roll-Number": "123456"
    }

def get_db_state(base_url, admin_headers):
    """Helper to inspect full state if needed."""
    users = requests.get(f"{base_url}/api/v1/admin/users", headers=admin_headers)
    orders = requests.get(f"{base_url}/api/v1/admin/orders", headers=admin_headers)
    return users.json() if users.status_code == 200 else [], orders.json() if orders.status_code == 200 else []

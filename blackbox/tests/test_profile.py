import requests

def test_get_profile_valid(base_url, default_headers):
    # Valid Request
    response = requests.get(f"{base_url}/api/v1/profile", headers=default_headers)
    assert response.status_code == 200, "Should return 200 for valid profile fetch"

def test_get_profile_missing_roll_no(base_url):
    # Missing Field
    headers = {"X-User-ID": "1"}
    response = requests.get(f"{base_url}/api/v1/profile", headers=headers)
    assert response.status_code == 401, "Should return 401 when X-Roll-Number is missing"

def test_get_profile_invalid_roll_no(base_url):
    # Wrong data types
    headers = {"X-Roll-Number": "abc", "X-User-ID": "1"}
    response = requests.get(f"{base_url}/api/v1/profile", headers=headers)
    assert response.status_code == 400, "Should return 400 when X-Roll-Number is valid integer"

def test_put_profile_valid(base_url, default_headers):
    # Valid Request
    data = {"name": "Test User", "phone": "1234567890"}
    response = requests.put(f"{base_url}/api/v1/profile", json=data, headers=default_headers)
    assert response.status_code == 200, "Should return 200 for valid profile update"

def test_put_profile_invalid_name_boundary(base_url, default_headers):
    # Boundary Value (name < 2 chars)
    data = {"name": "A", "phone": "1234567890"}
    response = requests.put(f"{base_url}/api/v1/profile", json=data, headers=default_headers)
    assert response.status_code == 400, "Should return 400 for name < 2 chars"

def test_put_profile_invalid_phone_boundary(base_url, default_headers):
    # Invalid Inputs / Boundary
    data = {"name": "Test", "phone": "123456789"} # 9 digits
    response = requests.put(f"{base_url}/api/v1/profile", json=data, headers=default_headers)
    assert response.status_code == 400, "Should return 400 for phone != 10 digits"

def test_put_profile_missing_fields(base_url, default_headers):
    # Missing fields
    data = {"name": "Test"}
    response = requests.put(f"{base_url}/api/v1/profile", json=data, headers=default_headers)
    assert response.status_code == 400, "Should return 400 for missing phone"

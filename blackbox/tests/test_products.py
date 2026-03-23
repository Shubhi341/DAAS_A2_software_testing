import requests

def test_get_products(base_url, default_headers):
    response = requests.get(f"{base_url}/api/v1/products", headers=default_headers)
    assert response.status_code == 200
    # Should only return active products

def test_get_product_not_exist(base_url, default_headers):
    response = requests.get(f"{base_url}/api/v1/products/999999", headers=default_headers)
    assert response.status_code == 404

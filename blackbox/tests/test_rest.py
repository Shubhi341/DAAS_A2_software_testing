import requests

def test_add_cart_valid(base_url, default_headers):
    # Quantity at least 1
    data = {"product_id": 1, "quantity": 1}
    response = requests.post(f"{base_url}/api/v1/cart/add", json=data, headers=default_headers)
    assert response.status_code == 200

def test_add_cart_invalid_quantity(base_url, default_headers):
    data = {"product_id": 1, "quantity": 0}
    response = requests.post(f"{base_url}/api/v1/cart/add", json=data, headers=default_headers)
    assert response.status_code == 400

def test_add_cart_invalid_product(base_url, default_headers):
    data = {"product_id": 999999, "quantity": 1}
    response = requests.post(f"{base_url}/api/v1/cart/add", json=data, headers=default_headers)
    assert response.status_code == 404

def test_checkout_empty_cart(base_url, default_headers):
    # First clear the cart
    requests.delete(f"{base_url}/api/v1/cart/clear", headers=default_headers)
    data = {"payment_method": "COD"}
    response = requests.post(f"{base_url}/api/v1/checkout", json=data, headers=default_headers)
    assert response.status_code == 400

def test_checkout_invalid_payment_method(base_url, default_headers):
    data = {"payment_method": "INVALID"}
    response = requests.post(f"{base_url}/api/v1/checkout", json=data, headers=default_headers)
    assert response.status_code == 400

def test_add_wallet_invalid_amount(base_url, default_headers):
    data = {"amount": 0}
    response = requests.post(f"{base_url}/api/v1/wallet/add", json=data, headers=default_headers)
    assert response.status_code == 400
    
    data = {"amount": 100001}
    response = requests.post(f"{base_url}/api/v1/wallet/add", json=data, headers=default_headers)
    assert response.status_code == 400

def test_review_invalid_rating(base_url, default_headers):
    data = {"rating": 6, "comment": "Great product!"}
    response = requests.post(f"{base_url}/api/v1/products/1/reviews", json=data, headers=default_headers)
    assert response.status_code == 400
    
    data = {"rating": 0, "comment": "Bad product!"}
    response = requests.post(f"{base_url}/api/v1/products/1/reviews", json=data, headers=default_headers)
    assert response.status_code == 400

def test_support_ticket_invalid_subject(base_url, default_headers):
    data = {"subject": "abc", "message": "Help!"}
    response = requests.post(f"{base_url}/api/v1/support/ticket", json=data, headers=default_headers)
    assert response.status_code == 400

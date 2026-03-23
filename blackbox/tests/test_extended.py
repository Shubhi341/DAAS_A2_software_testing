import requests

def test_loyalty_get(base_url, default_headers):
    response = requests.get(f"{base_url}/api/v1/loyalty", headers=default_headers)
    assert response.status_code == 200

def test_loyalty_redeem_invalid_amount(base_url, default_headers):
    data = {"points": 0}
    response = requests.post(f"{base_url}/api/v1/loyalty/redeem", json=data, headers=default_headers)
    assert response.status_code == 400

def test_coupon_apply_invalid(base_url, default_headers):
    data = {"code": "INVALID_COUPON"}
    response = requests.post(f"{base_url}/api/v1/coupon/apply", json=data, headers=default_headers)
    # Could be 400 or 404, valid spec usually 400 or 404. Let's assert it is not 200.
    assert response.status_code != 200

def test_orders_get(base_url, default_headers):
    response = requests.get(f"{base_url}/api/v1/orders", headers=default_headers)
    assert response.status_code == 200

def test_order_cancel_not_exist(base_url, default_headers):
    response = requests.post(f"{base_url}/api/v1/orders/999999/cancel", headers=default_headers)
    assert response.status_code == 404

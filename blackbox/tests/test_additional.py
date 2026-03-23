import pytest
import requests


def test_get_products_schema(base_url, default_headers):
    response = requests.get(f"{base_url}/api/v1/products", headers=default_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) == 0:
        pytest.skip("No products available to validate schema")
    item = data[0]
    assert "id" in item and isinstance(item["id"], int)
    assert "name" in item and isinstance(item["name"], str)
    assert "price" in item and (isinstance(item["price"], int) or isinstance(item["price"], float))


def test_get_product_detail_schema(base_url, default_headers):
    response = requests.get(f"{base_url}/api/v1/products", headers=default_headers)
    assert response.status_code == 200
    products = response.json()
    if not products:
        pytest.skip("No products to inspect detail endpoint")
    pid = products[0]["id"]
    resp = requests.get(f"{base_url}/api/v1/products/{pid}", headers=default_headers)
    assert resp.status_code == 200
    detail = resp.json()
    assert "id" in detail and detail["id"] == pid
    assert "name" in detail and isinstance(detail["name"], str)
    assert "description" in detail


def test_add_and_get_cart_item(base_url, default_headers):
    # pick a product
    resp = requests.get(f"{base_url}/api/v1/products", headers=default_headers)
    assert resp.status_code == 200
    products = resp.json()
    if not products:
        pytest.skip("No products to add to cart")
    pid = products[0]["id"]

    # clear cart then add
    requests.delete(f"{base_url}/api/v1/cart/clear", headers=default_headers)
    data = {"product_id": pid, "quantity": 2}
    r = requests.post(f"{base_url}/api/v1/cart/add", json=data, headers=default_headers)
    assert r.status_code == 200

    # verify via GET /cart
    g = requests.get(f"{base_url}/api/v1/cart", headers=default_headers)
    assert g.status_code == 200
    cart = g.json()
    assert isinstance(cart, dict)
    items = cart.get("items", []) if isinstance(cart, dict) else []
    assert any(i.get("product_id") == pid and i.get("quantity") == 2 for i in items), "Cart must contain added product with correct quantity"


def test_checkout_success_creates_order(base_url, default_headers):
    resp = requests.get(f"{base_url}/api/v1/products", headers=default_headers)
    assert resp.status_code == 200
    products = resp.json()
    if not products:
        pytest.skip("No products to checkout")
    pid = products[0]["id"]

    # ensure cart has item
    requests.delete(f"{base_url}/api/v1/cart/clear", headers=default_headers)
    requests.post(f"{base_url}/api/v1/cart/add", json={"product_id": pid, "quantity": 1}, headers=default_headers)

    r = requests.post(f"{base_url}/api/v1/checkout", json={"payment_method": "COD"}, headers=default_headers)
    assert r.status_code == 200
    j = r.json()
    assert isinstance(j, dict)
    assert "order_id" in j


def test_post_address_update_immutable_verified(base_url, default_headers):
    # create address
    data = {"label": "HOME", "street": "123 Test St", "city": "Test City", "pincode": "123456", "is_default": False}
    r = requests.post(f"{base_url}/api/v1/addresses", json=data, headers=default_headers)
    assert r.status_code == 200
    res = r.json()
    addr_id = res.get("address_id")
    if not addr_id:
        pytest.skip("Address create did not return address_id; cannot verify update behavior")

    # attempt to change immutable fields
    update = {"label": "INVALID_CHANGE", "city": "New City", "pincode": "654321", "street": "New St", "is_default": True}
    u = requests.put(f"{base_url}/api/v1/addresses/{addr_id}", json=update, headers=default_headers)
    assert u.status_code in (200, 400)

    # fetch addresses and ensure label/city/pincode didn't change to disallowed values
    g = requests.get(f"{base_url}/api/v1/addresses", headers=default_headers)
    assert g.status_code == 200
    found = None
    for a in g.json() if isinstance(g.json(), list) else []:
        if a.get("address_id") == addr_id:
            found = a
            break
    assert found is not None
    assert found.get("label") in ("HOME",), "Label must not be changed by update"
    assert found.get("pincode") == "123456", "Pincode must not be changed by update"


def test_review_and_support_ticket_success(base_url, default_headers):
    # review
    resp = requests.post(f"{base_url}/api/v1/products/1/reviews", json={"rating": 5, "comment": "Excellent"}, headers=default_headers)
    assert resp.status_code in (200, 201)

    # support ticket
    s = requests.post(f"{base_url}/api/v1/support/ticket", json={"subject": "Help", "message": "Need assistance"}, headers=default_headers)
    assert s.status_code in (200, 201)
    js = s.json() if s.status_code in (200, 201) else {}
    assert s.status_code in (200, 201)
    if js:
        assert "ticket_id" in js or "id" in js

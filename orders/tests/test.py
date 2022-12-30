# from orders.wsgi import *
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from web_service.models import Shop, Category, Product, ProductInfo


# ---------Fixtures and factories block

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def host_url():
    url = "http://127.0.0.1:8000/api/v1/"
    return url


@pytest.fixture()
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)

    return factory


@pytest.fixture()
def shop_status_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)

    return factory


@pytest.fixture()
def category_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)

    return factory


@pytest.fixture()
def product_factory():
    def factory(*args, **kwargs):
        return baker.make(Product, *args, **kwargs)

    return factory


@pytest.fixture()
def productinfo_factory():
    def factory(*args, **kwargs):
        return baker.make(ProductInfo, *args, **kwargs)

    return factory


# -----------Tests block

# Example test
def test_example():
    assert True, "It's just test example!"


# Test_1
@pytest.mark.django_db
def test_orders_1(client, shop_factory, host_url, quantity=1):
    # Arrange
    _ = shop_factory(_quantity=quantity)
    # Act
    response = client.get(f"{host_url}shops/")
    # Assert
    assert response.status_code == 200
    assert response.status_text == "OK"
    assert response.data["count"] == 1


# Test_2
@pytest.mark.django_db
def test_orders_2(client, category_factory, host_url, quantity=3):
    # Arrange
    _ = category_factory(_quantity=quantity)
    # Act
    response = client.get(f"{host_url}categories/")
    # Assert
    assert response.status_code == 200
    assert response.status_text == "OK"
    assert len(response.data["results"]) == 3


# Test_3
@pytest.mark.django_db
def test_orders_3(client, shop_status_factory, host_url):
    # Arrange
    _ = shop_status_factory()
    # Act
    response = client.get(f"{host_url}shops/")
    # Assert
    assert response.status_code == 200
    assert response.status_text == "OK"
    assert response.data["results"][0]["id"] == 2
    assert response.data["results"][0]["state"] == True


# Test 4
@pytest.mark.django_db
def test_orders_4(client, category_factory, host_url):
    # Arrange
    _ = category_factory()
    # Act
    response = client.get(f"{host_url}categories/")
    # Assert
    assert response.status_code == 200
    assert response.status_text == "OK"
    assert response.data["next"] == None
    assert response.data["previous"] == None


# Test_5
@pytest.mark.django_db
def test_orders_5(client, productinfo_factory, host_url, quantity=1, product_id=5, shop_id=1):
    # Arrange
    _ = productinfo_factory(quantity=quantity, product_id=product_id, shop_id=shop_id)
    # Act
    response = client.get(f"{host_url}products/")
    # Assert
    assert response.status_code == 200
    assert response.status_text == "OK"

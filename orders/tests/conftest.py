import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def shop_factory():
    def factory(**kwargs):
        return baker.make('Shop', **kwargs)

    return factory


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)

    return factory


@pytest.fixture
def product_info_factory():
    def factory(**kwargs):
        return baker.make('ProductInfo', **kwargs)

    return factory


@pytest.fixture
def category_factory():
    def factory(**kwargs):
        return baker.make('Category', **kwargs)

    return factory

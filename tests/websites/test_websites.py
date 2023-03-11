from itertools import chain
from typing import List, Type

import pytest

from src.websites.magalu import Magalu
from src.websites.pichau import Pichau
from src.websites.website import Product, Website
from tests.products import (
    MAGALU_I5,
    MAGALU_I5_2,
    MAGALU_RTX,
    PICHAU_I9,
    PICHAU_RTX,
)

PICHAU_PARAMS = [
    pytest.param(Pichau, PICHAU_I9, id="Pichau - i9"),
    pytest.param(Pichau, PICHAU_RTX, id="Pichau - RTX"),
]


MAGALU_PARAMS = [
    pytest.param(Magalu, MAGALU_I5, id="Magalu - i5"),
    pytest.param(Magalu, MAGALU_RTX, id="Magalu - RTX"),
]

DIFFERENT_PRODUCTS_PARAMS = list(chain(PICHAU_PARAMS, MAGALU_PARAMS))


@pytest.mark.parametrize(
    "website", [Pichau, Magalu], ids=lambda val: val.__class__.__name__
)
def test_get_product_no_item(website: Type[Website]):
    assert website().get_product("") is None


@pytest.mark.parametrize(["website", "product"], DIFFERENT_PRODUCTS_PARAMS)
def test_get_product_one_item(website: Type[Website], product: Product):
    assert website().get_product(product.search_term) == product


@pytest.mark.parametrize(["website", "product"], DIFFERENT_PRODUCTS_PARAMS)
def test_get_different_products_one_item(
    website: Type[Website], product: Product
):
    assert website().get_different_products([product.search_term]) == [product]


@pytest.mark.parametrize(
    ["website", "products"],
    [
        pytest.param(Pichau, [PICHAU_I9, PICHAU_RTX], id="Pichau - i9 + RTX"),
        pytest.param(Magalu, [MAGALU_I5, MAGALU_RTX], id="Magalu - i5 + RTX"),
    ],
)
def test_get_different_products_multiples_item(
    website: Type[Website], products: List[Product]
):
    products_found = website().get_different_products(
        [product.search_term for product in products]
    )
    for product_found in products_found:
        assert product_found in products


PARAMS = [
    pytest.param(Magalu, [MAGALU_I5, MAGALU_I5_2], id="Magalu - i5"),
]


@pytest.mark.parametrize(["website", "products"], PARAMS)
def test_get_products_one_item(
    website: Type[Website], products: List[Product]
):
    result = website().get_products(products[0].search_term)
    for product in products:
        assert product in result

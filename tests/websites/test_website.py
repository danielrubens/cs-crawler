from typing import Optional

import pytest

from src.websites.website import List, Product, Website


class MockedWebsite(Website):
    def _get_search_page_with_search_results(self, _: str) -> str:
        return "html"

    def _get_products_html(self, name: str) -> List[str]:
        return ["html"] if name else []

    def _get_product_name(self, product_html: str) -> Optional[str]:
        return "name" if product_html else None

    def _get_product_url(self, product_html: str) -> Optional[str]:
        return "url" if product_html else None

    def _get_product_price(self, product_html: str) -> Optional[float]:
        return 1.1 if product_html else None


@pytest.fixture
def website() -> MockedWebsite:
    return MockedWebsite()


def test_get_product_okay_with_one_product(website: MockedWebsite):
    assert website.get_product("term") == Product("term", "name", 1.1, "url")


@pytest.mark.parametrize(
    ["product_names", "expected_products"],
    [
        pytest.param([], [], id="empty list"),
        pytest.param(
            ["term1"], [Product("term1", "name", 1.1, "url")], id="find first"
        ),
        pytest.param(
            ["term2"], [Product("term2", "name", 1.1, "url")], id="find second"
        ),
        pytest.param(
            ["term1", "term2"],
            [
                Product("term1", "name", 1.1, "url"),
                Product("term2", "name", 1.1, "url"),
            ],
            id="find both",
        ),
    ],
)
def test_get_different_products_okay_with_two_products(
    website: MockedWebsite,
    expected_products: List[Product],
    product_names: List[str],
):
    given_products = website.get_different_products(product_names)

    assert len(expected_products) == len(given_products)
    for product in given_products:
        assert product in given_products

import itertools
from typing import Dict, NamedTuple, Type

import pytest
from bs4 import BeautifulSoup

from src.websites import Magalu, Pichau, Website


class ProductInfo(NamedTuple):
    website_class: Type[Website]
    product_name: str
    expected_products_return: int

    @property
    def company_name(self):
        return self.website_class.__name__.lower()


def id_function(val: ProductInfo):
    return f"{val.company_name} - {val.product_name}"


@pytest.mark.parametrize(
    "product",
    [
        ProductInfo(Magalu, "i5 11400f", 60),
        ProductInfo(Pichau, "i9 12900ks", 36),
    ],
    ids=id_function,
)
def test_get_products_html_okay(content: Dict[str, str], product: ProductInfo):
    website = product.website_class()

    given_contents = website._get_products_html(product.product_name)
    assert len(given_contents) == product.expected_products_return

    given_contents = [
        BeautifulSoup(content, "html.parser") for content in given_contents
    ]

    for item in itertools.count(start=1):
        expected_content = content.get(
            f"{product.company_name} - {product.product_name}{item}.html"
        )
        if expected_content is None:
            break

        expected = BeautifulSoup(expected_content, "html.parser")
        assert expected in given_contents

    assert item == product.expected_products_return + 1

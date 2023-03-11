from typing import Dict, NamedTuple, Type

import pytest
from bs4 import BeautifulSoup

from src.websites import Magalu, Pichau, Website


class ProductInfo(NamedTuple):
    website_class: Type[Website]
    product_name: str

    @property
    def company_name(self):
        return self.website_class.__name__.lower()


def id_function(val: ProductInfo):
    return f"{val.company_name} - {val.product_name}"


@pytest.mark.parametrize(
    "product",
    [
        ProductInfo(Magalu, "i5 11400f"),
        ProductInfo(Magalu, "rtx 3080"),
        ProductInfo(Pichau, "i9 12900ks"),
        ProductInfo(Pichau, "rtx 3080"),
    ],
    ids=id_function,
)
def test_get_product_html_okay(content: Dict[str, str], product: ProductInfo):
    website = product.website_class()

    given_content = website._get_product_html(product.product_name)
    if given_content is None:
        assert False, "Invalid return"

    given = BeautifulSoup(given_content, "html.parser")

    expected_content = content.get(
        f"{product.company_name} - {product.product_name}.html"
    )
    if expected_content is None:
        raise ValueError("Invalid test mock")

    expected = BeautifulSoup(expected_content, "html.parser")
    assert given == expected

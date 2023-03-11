from typing import Dict, NamedTuple, Type

import pytest

from src.websites import Magalu, Pichau, Website


class ProductInfo(NamedTuple):
    website_class: Type[Website]
    search_term: str
    expected_product_url: str

    @property
    def company_name(self):
        return self.website_class.__name__.lower()


PARAMS = [
    ProductInfo(
        Magalu,
        "i5 11400f",
        "https://www.magazineluiza.com.br/processador-intel-core-i5-11400f-"
        "lga1200-2-6ghz-bx8070811400f/p/gj88ag6k9f/in/pepc/",
    ),
    ProductInfo(
        Magalu,
        "rtx 3080",
        "https://www.magazineluiza.com.br/placa-de-video-galax-rtx-3080-"
        "10gbsg-gddr6x-320bits-lhr-38nwm3md99rg/p/cb8bgjgahe/in/pcvd/",
    ),
    ProductInfo(
        Pichau,
        "i9 12900ks",
        "https://www.pichau.com.br/processador-intel-core-i9-12900ks-16-core-"
        "24-threads-3-4ghz-5-5ghz-turbo-cache-30mb-lga1700-bx8071512900ks",
    ),
    ProductInfo(
        Pichau,
        "rtx 3080",
        "https://www.pichau.com.br/placa-de-video-galax-geforce-rtx-3080-sg-1-"
        "click-oc-lhr-10gb-gddr6x-320-bit-38nwm3md99rg-nac",
    ),
]


def id_function(value: ProductInfo):
    return f"{value.company_name} - {value.search_term}"


@pytest.mark.parametrize("product", PARAMS, ids=id_function)
def test_get_product_url_okay(content: Dict[str, str], product: ProductInfo):
    website = product.website_class()

    file_name = f"{product.company_name} - {product.search_term}.html"
    result = website._get_product_url(content.get(file_name, ""))

    assert result == product.expected_product_url

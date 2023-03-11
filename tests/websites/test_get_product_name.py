from typing import Dict, NamedTuple, Type

import pytest

from src.websites import Magalu, Pichau, Website


class ProductInfo(NamedTuple):
    website_class: Type[Website]
    search_term: str
    expected_product_name: str

    @property
    def company_name(self):
        return self.website_class.__name__.lower()


PARAMETERS = [
    ProductInfo(
        Pichau,
        "i9 12900ks",
        "Processador Intel Core i9-12900KS, 16-Core, 24-Threads, 3.4GHz "
        "(5.5GHz Turbo), Cache 30MB, LGA1700, BX8071512900KS",
    ),
    ProductInfo(
        Pichau,
        "rtx 3080",
        "Placa de Video Galax Geforce RTX 3080 SG 1-Click"
        " OC, LHR, 10GB, GDDR6X, 320-bit, 38NWM3MD99RG-NAC",
    ),
    ProductInfo(
        Magalu,
        "i5 11400f",
        "Processador Intel Core i5-11400F (LGA1200 - 2.6GHz) - BX8070811400F",
    ),
    ProductInfo(
        Magalu,
        "rtx 3080",
        "Placa De Vídeo Galax Rtx 3080 10gbsg Gddr6x 320bits Lhr 38nwm3md99rg",
    ),
]


def id_function(value: ProductInfo):
    return f"{value.company_name} - {value.search_term}"


@pytest.mark.parametrize("product", PARAMETERS, ids=id_function)
def test_get_product_name_okay(content: Dict[str, str], product: ProductInfo):
    website = product.website_class()

    file_name = f"{product.company_name} - {product.search_term}.html"
    result = website._get_product_name(content.get(file_name, ""))

    assert result == product.expected_product_name

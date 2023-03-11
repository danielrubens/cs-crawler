from copy import deepcopy
from typing import List, NamedTuple

import pytest

from src.aggregator import get_products_from_many_sites
from tests.products import (
    MAGALU_I5,
    MAGALU_RTX,
    PICHAU_I9,
    PICHAU_RTX,
    Product,
)


class Information(NamedTuple):
    search_term: str
    expected_products: List[Product]


FAKE_I5 = deepcopy(MAGALU_I5)
FAKE_I5.search_term = "i5"

PARAMETERS = [
    Information("rtx 3080", [MAGALU_RTX, PICHAU_RTX]),
    Information("i5 11400f", [MAGALU_I5]),
    Information("i9 12900ks", [PICHAU_I9]),
    Information("i5", [FAKE_I5]),
    Information("invalid string", []),
]


@pytest.mark.parametrize("info", PARAMETERS, ids=lambda info: info.search_term)
def test_get_products_from_many_sites_okay(info: Information):
    result = get_products_from_many_sites(info.search_term)
    for expected_product in info.expected_products:
        assert expected_product in result

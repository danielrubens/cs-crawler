import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Type

from .product import Product
from .websites import WEBSITE_CLASSES, Website

max_workers = max(1, min(os.cpu_count() or 1, len(WEBSITE_CLASSES)))


def get_products_from_many_sites(search_term: str) -> List[Product]:
    def get_product(website_class: Type[Website]) -> Optional[Product]:
        return website_class().get_product(search_term=search_term)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return [
            product
            for product in executor.map(get_product, WEBSITE_CLASSES)
            if product is not None
        ]


def get_many_products_from_many_sites(
    search_term: str, quantity: int
) -> List[Product]:
    if quantity == 1:
        return get_products_from_many_sites(search_term)

    def get_products(website_class: Type[Website]) -> List[Product]:
        products: List[Product] = []
        generator = website_class().get_products(search_term=search_term)
        for i in range(quantity):
            try:
                products.append(next(generator))
            except StopIteration:
                break
        return products

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return [
            product
            for products in executor.map(get_products, WEBSITE_CLASSES)
            for product in products
            if product is not None
        ]

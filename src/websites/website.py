import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Iterable, List, Optional

from src.product import Product

HTML = str


class Website(ABC):
    def get_different_products(
        self, product_names: Iterable[str]
    ) -> List[Product]:
        """Get different `Product`s at once

        Calls `get_product` for many products in a single function call, with
        multithread support.

        Parameters
        ----------
        product_names : Iterable[str]
            Preferable a list of strings with the names of the products to be
            searched
        """

        names = set(product_names)
        max_workers = max(1, min(os.cpu_count() or 1, len(names)))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return [
                product
                for product in executor.map(self.get_product, names)
                if product is not None
            ]

    def get_products(self, search_term: str) -> Generator[Product, None, None]:
        """Get all `Product`s found in the first search page

        The `Product` is only considered if all information fields (`name`,
        `url` and `price`) are found in the page.

        Parameters
        ----------
        search_term : str
            The term to be used to search for the product in the website

        Yields
        ------
        Generator[Product, None, None]
            A generator of `Product`s
        """

        return (
            Product(search_term, name, price, url)
            for product_html in self._get_products_html(search_term)
            if (name := self._get_product_name(product_html)) is not None
            and (price := self._get_product_price(product_html)) is not None
            and (url := self._get_product_url(product_html)) is not None
        )

    def get_product(self, search_term: str) -> Optional[Product]:
        """Get the first `Product` found in the search page or `None`

        If some information about the product is not found, such as price, url
        or name, `None` is returned.

        Parameters
        ----------
        search_term : str
            The term to be used to search for the product in the website
        """

        if (
            not search_term
            or (product_html := self._get_product_html(search_term)) is None
            or (name := self._get_product_name(product_html)) is None
            or (price := self._get_product_price(product_html)) is None
            or (url := self._get_product_url(product_html)) is None
        ):
            return None

        return Product(search_term, name, price, url)

    @abstractmethod
    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        """Request the search page and return it's HTML"""

    @abstractmethod
    def _get_products_html(self, name: str) -> List[HTML]:
        """Get the HTML content of all products in the search page

        Should call `_get_search_page_with_search_results`
        """

    def _get_product_html(self, name: str) -> Optional[str]:
        """Get the HTML content of the first product in the search page"""
        try:
            return self._get_products_html(name)[0]
        except IndexError:
            return None

    @abstractmethod
    def _get_product_name(self, product_html: str) -> Optional[str]:
        """Get the product's full name as displayed in the search results"""

    @abstractmethod
    def _get_product_price(self, product_html: str) -> Optional[float]:
        """Get the product's price"""

    @abstractmethod
    def _get_product_url(self, product_html: str) -> Optional[str]:
        """Get the url to the product's page in the website"""

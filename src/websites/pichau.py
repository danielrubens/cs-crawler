import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from src.utils import PRICE_REGEX
from src.websites.website import HTML, Website
from .services import get_constants, soup_finder, get_product_info

class Pichau(Website):
    PRODUCTS, PRICE, PRODUCT_TITLE = get_product_info("pichau")
    BASE_URL, BASE_SEARCH_URL, HEADERS = get_constants("pichau")

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        kwargs = {'headers': self.HEADERS, 'params': {"q": product_name.lower()}}
        return requests.get(self.BASE_SEARCH_URL, **kwargs).text

    def _get_products_html(self, product_name: str) -> List[HTML]:
        content = self._get_search_page_with_search_results(product_name)
        products = soup_finder(content, "find_all", self.PRODUCTS)
        return [str(product) for product in products]
    
    def _get_product_price(self, product_html: str) -> Optional[float]:
        price_div = soup_finder(product_html, "find", self.PRICE)
        price_str = PRICE_REGEX.search(price_div.text)
        return None if not price_str else float(price_str.group(0).replace(",", ""))

    def _get_product_name(self, product_html: str) -> Optional[str]:
        return BeautifulSoup(product_html, "html.parser").h2.text
    
    def _get_product_url(self, product_html: str) -> Optional[str]:
        url = BeautifulSoup(product_html, "html.parser").a.get("href")
        product_path = url[0] if isinstance(url, list) else url
        return f"{self.BASE_URL}{product_path}"
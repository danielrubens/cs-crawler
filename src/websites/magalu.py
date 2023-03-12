import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from src.utils import PRICE_REGEX
from src.websites.website import HTML, Website
from .services import get_constants, soup_finder, get_product_info

class Magalu(Website):
    PRODUCTS, PRICE, PRODUCT_TITLE = get_product_info("magalu")
    BASE_URL, BASE_SEARCH_URL, HEADERS = get_constants("magazineluiza")

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        url = product_name.lower().replace(" ", "+")
        return requests.get(f"{self.BASE_SEARCH_URL}/{url}", headers=self.HEADERS).text
    
    def _get_products_html(self, product_name: str) -> List[HTML]:
        content = self._get_search_page_with_search_results(product_name)
        products = soup_finder(content, "find_all", self.PRODUCTS)
        return [str(product) for product in products if products]
    
    def _get_product_price(self, product_html: str) -> Optional[float]:
        price_div = soup_finder(product_html, "find", self.PRICE)
        price_str = PRICE_REGEX.search(price_div.text)
        return None if not price_str else float(price_str.group(0).replace(".", "").replace(",", "."))

    def _get_product_name(self, product_html: str) -> Optional[str]:
        return soup_finder(product_html, "find", self.PRODUCT_TITLE).text
    
    def _get_product_url(self, product_html: str) -> Optional[str]:
        url = BeautifulSoup(product_html, "html.parser").a.get("href")
        product_path = url[0] if isinstance(url, list) else url
        return f"{self.BASE_URL}{product_path}"
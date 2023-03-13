import requests
from bs4 import BeautifulSoup
from typing import Optional
from src.websites.website import HTML
from .parent import WebsiteWithSearchResults
from .services import get_constants, get_product_info


class Pichau(WebsiteWithSearchResults):
    PRODUCTS, PRICE, PRODUCT_TITLE = get_product_info("pichau")
    BASE_URL, BASE_SEARCH_URL, HEADERS = get_constants("pichau")

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        kwargs = {'headers': self.HEADERS, 'params': {"q": product_name.lower()}}
        return requests.get(self.BASE_SEARCH_URL, **kwargs).text
    
    def _get_product_name(self, product_html: str) -> Optional[str]:
        return BeautifulSoup(product_html, "html.parser").h2.text
    
    def _get_product_price(self, product_html: str) -> Optional[float]:
        price_str = WebsiteWithSearchResults.base_price(self, product_html)
        return None if not price_str else float(price_str.group(0).replace(",", ""))
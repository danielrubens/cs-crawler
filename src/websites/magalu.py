import requests
from typing import Optional
from src.websites.website import HTML
from .parent import WebsiteWithSearchResults
from .services import get_constants, get_product_info, soup_finder

class Magalu(WebsiteWithSearchResults):
    PRODUCTS, PRICE, PRODUCT_TITLE = get_product_info("magalu")
    BASE_URL, BASE_SEARCH_URL, HEADERS = get_constants("magazineluiza")

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        url = product_name.lower().replace(" ", "+")
        return requests.get(f"{self.BASE_SEARCH_URL}/{url}", headers=self.HEADERS).text
    
    def _get_product_name(self, product_html: str) -> Optional[str]:
        return soup_finder(product_html, "find", self.PRODUCT_TITLE).text
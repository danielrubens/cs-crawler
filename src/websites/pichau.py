import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from src.utils import PRICE_REGEX
from src.websites.website import Website
from src.websites.website import HTML

class Pichau(Website):
    BASE_URL = "https://www.pichau.com.br"
    BASE_SEARCH_URL = f"{BASE_URL}/search"
    HEADERS = {
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
            "Safari/537.36"
        ),
    }

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        return requests.get(self.BASE_URL, headers=self.HEADERS, params={"q": product_name.lower()}).text

    def _get_products_html(self, product_name: str) -> List[HTML]:
        content = self._get_search_page_with_search_results(product_name)
        soup = BeautifulSoup(content, "html.parser")
        products = soup.find_all("a", {"data-cy": "list-product"})
        return (str(product) for product in products)
    
    def _get_product_price(self, product_html: str) -> Optional[float]:
        soup = BeautifulSoup(product_html, "html.parser")
        price_div = soup.find("div", {"class": "jss83"})
        try:
            price_str = PRICE_REGEX.search(price_div.text)
        except AttributeError:
            return None
        try:
            content = price_str.group(0).replace(",", "")
            return float(content)
        except (ValueError, AttributeError):
            return None

    def _get_product_name(self, product_html: str) -> Optional[str]:
        soup = BeautifulSoup(product_html, "html.parser")
        return soup.h2.text
    
    
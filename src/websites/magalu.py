import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from src.utils import PRICE_REGEX
from src.websites.website import HTML, Website
from .services import get_constantes, soup_finder

class Magalu(Website):
    BASE_URL, BASE_SEARCH_URL, HEADERS = get_constantes("magazineluiza")

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        urlify_product_name = product_name.lower().replace(" ", "+")
        return requests.get(
            f"{self.BASE_SEARCH_URL}/{urlify_product_name}", headers=self.HEADERS).text
    
    def _get_products_html(self, product_name: str) -> List[HTML]:
        content = self._get_search_page_with_search_results(product_name)
        products = soup_finder(content, "find_all", ("li", {"class": "sc-fCBrnK hYPKVt"}))
        return [str(product) for product in products if products]
    
    def _get_product_price(self, product_html: str) -> Optional[float]:
        price_div = soup_finder(product_html, "find", ("p", {"data-testid": "price-value"}))
        try:
            content = PRICE_REGEX.search(price_div.text).group(0).replace(".", "").replace(",", ".")
            return float(content)
        except (AttributeError, ValueError, ArithmeticError):
            return None

    
    def _get_product_name(self, product_html: str) -> Optional[str]:
        soup = BeautifulSoup(product_html, "html.parser")
        return soup.find("h2", {"data-testid": "product-title"}).text
    
    def _get_product_url(self, product_html: str) -> Optional[str]:
        soup = BeautifulSoup(product_html, "html.parser")
        url = soup.a.get("href")
        product_path = url[0] if isinstance(url, list) else url
        return f"{self.BASE_URL}{product_path}"
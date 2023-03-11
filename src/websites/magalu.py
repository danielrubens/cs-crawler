import requests
from typing import List
from bs4 import BeautifulSoup
from src.websites.website import HTML, Website


class Magalu(Website):
    BASE_URL = "https://www.magazineluiza.com.br"
    BASE_SEARCH_URL = f'{BASE_URL}/busca'
    HEADERS = {
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
            "Safari/537.36"
        ),
    }

    def _get_search_page_with_search_results(self, product_name: str) -> HTML:
        urlify_product_name = product_name.lower().replace(" ", "+")
        return requests.get(
            f"{self.BASE_SEARCH_URL}/{urlify_product_name}", headers=self.HEADERS).text
    
    def _get_products_html(self, product_name: str) -> List[HTML]:
        content = self._get_search_page_with_search_results(product_name)
        soup = BeautifulSoup(content, "html.parser")
        products = soup.find_all("li", {"class": "sc-fCBrnK hYPKVt"})
        return [str(product) for product in products if products]
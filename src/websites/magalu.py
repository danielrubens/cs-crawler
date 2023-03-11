import requests
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
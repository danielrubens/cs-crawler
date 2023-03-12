from src.websites.website import Website
import requests
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

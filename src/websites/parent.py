from bs4 import BeautifulSoup
from typing import List, Optional
from src.utils import PRICE_REGEX
from src.websites.website import HTML, Website
from .services import soup_finder

class WebsiteWithSearchResults(Website):
    def _get_products_html(self, product_name: str) -> List[HTML]:
        content = self._get_search_page_with_search_results(product_name)
        products = soup_finder(content, "find_all", self.PRODUCTS)
        return [str(product) for product in products if products]
    
    def _get_product_price(self, product_html: str) -> Optional[float]:
        price_div = soup_finder(product_html, "find", self.PRICE)
        price_str = PRICE_REGEX.search(price_div.text)
        return None if not price_str else float(price_str.group(0).replace(".", "").replace(",", "."))
    
    def base_price(self, product_html: str):
        price_div = soup_finder(product_html, "find", self.PRICE)
        return PRICE_REGEX.search(price_div.text)
    
    def _get_product_url(self, product_html: str) -> Optional[str]:
        url = BeautifulSoup(product_html, "html.parser").a.get("href")
        product_path = url[0] if isinstance(url, list) else url
        return f"{self.BASE_URL}{product_path}"

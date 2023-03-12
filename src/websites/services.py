import json
from bs4 import BeautifulSoup

def get_product_info(arg):
    with open('src/websites/constants.json') as f:
        file = json.load(f)
    return (file[arg][key] for key in ['PRODUCTS', 'PRICE', 'PRODUCT_TITLE'])

def get_constants(website: str):
    BASE_URL = f"https://www.{website}.com.br"
    BASE_SEARCH_URL = f"{BASE_URL}/search"
    HEADERS = {"user-agent": """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) 
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"""}
    return (BASE_URL, BASE_SEARCH_URL, HEADERS)

def soup_finder(content, method, finder):
    soup = BeautifulSoup(content, "html.parser")
    methods = {"find_all": soup.find_all, "find": soup.find}
    return methods[method](*finder)

def get_constantes(website: str):
    websites ={'pichau': ['pichau', 'search'], 'magazineluiza': ['magazineluiza', 'search']}
    BASE_URL = f"https://www.{websites[website][0]}.com.br"
    BASE_SEARCH_URL = f'{BASE_URL}/{websites[website][1]}'
    HEADERS = {
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
            "Safari/537.36"
        ),
    }
    return (BASE_URL, BASE_SEARCH_URL, HEADERS)
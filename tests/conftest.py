from pathlib import Path
from typing import Dict

import pytest
import requests


class MockResponse:
    def __init__(self, *args, **kwargs):
        url: str = args[0]
        if not url:
            raise ValueError

        if "pichau" in url:
            self.store = "pichau"
            if not (params := kwargs.get("params")) or not (
                product_name := params.get("q")
            ):
                raise ValueError("Invalid product name")
        elif "magazineluiza" in url:
            self.store = "magalu"
            try:
                product_name = url.split("/")[-1]
            except IndexError:
                raise ValueError("Invalid product name or url")
        else:
            raise ValueError("Invalid store")

        self.name = product_name

    @property
    def product(self):
        if "i9" in self.name:
            return "i9 12900ks"
        if "rtx" in self.name:
            return "rtx 3080"
        if "i5" in self.name:
            return "i5 11400f"
        return ""

    @property
    def content(self):
        return self

    def decode(self):
        try:
            with open(
                f"tests/websites/mocks/{self.store} - {self.product} full.html"
            ) as file:
                return file.read()
        except FileNotFoundError:
            return ""

    @property
    def text(self):
        return self.content.decode()


@pytest.fixture(autouse=True)
def request_get_mocker(monkeypatch: pytest.MonkeyPatch):
    def mock_get(*args, **kwargs):
        return MockResponse(*args, **kwargs)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mocks_path() -> Path:
    path = Path().absolute()
    return path / "tests/websites/mocks"


@pytest.fixture
def content(mocks_path: Path) -> Dict[str, str]:
    return {file.name: file.read_text() for file in mocks_path.iterdir()}

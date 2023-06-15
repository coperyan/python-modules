# from ..file_operations import read_file

from bs4 import BeautifulSoup


def get_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

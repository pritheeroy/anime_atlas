"""
Web scrapping file to get random my anime list users.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import python_ta


def full_scrape(url: str) -> BeautifulSoup:
    """Testing function to obtain full html scripts

    Preconditions:
        - webpage submitted in url is active and scriptable
    """
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def genre_scrap(url: str, lst: list) -> None:
    """Testing function to obtain full html scripts

    Preconditions:
        - webpage submitted in url is active and scriptable
    """
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('a'):
        curr = str(item)
        if curr[:21] == '<a class="link-title"':
            txt = curr[58:-4]

            i = 0
            while txt[i] != '/':
                i += 1

            lst.append(int(txt[:i]))


def scrape(lst: list) -> None:
    """Adds 20 users to user_base list in token.py.

    Preconditions:
        - https://myanimelist.net/users.php is up and running.
    """
    url = "https://myanimelist.net/users.php"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('a'):
        curr = str(item)
        if curr[-4:] == '</a>' and curr[:18] == '<a href="/profile/' and curr[-5] != '>':
            i = len(curr[18:-4]) // 2
            lst.append(curr[18:-4][i + 1:])


# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })

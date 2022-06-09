"""
Scrape the website for texts and prices
"""

import requests
from bs4 import BeautifulSoup as bs


import requests


def get_response_prices() -> requests.models.Response:
    cookies = {
        'session': '.eJwljkFqQzEMBe_idRaSLFtyLvOxLImWQAv_J6uQu9fQ5RsezLzLkWdcX-X-PF9xK8e3l3sBNyNs1lQWc02tAI61CdiyviT7gI2Dx6JpzkBpmGDio_OUFjBCAt2roU9FTPWhNVSrU47W0rJ77K8NmjwneqDC0qCYzFF2yOuK87-GYO91nXk8fx_xs0kXQ25htC1jG4hVQ9xdmHBpkz5xJ9fy-QOG4EAx.YqHlOw.Nxopf6mxCCEPUEeTakSx7rOg-Do',
        'remember_token': '20|40ed4057d976aa0dc1d708f2ea0c076d37e2eb7d1e92fa3b24c6e29cfe205d59a78f88f58611c17d981f8cecfa02fa9895ea22a75d0bae42c9fa72e9ac5d4f5f',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'nl,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://orderbookz.com/bluelagoon/',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'session=.eJwljkFqQzEMBe_idRaSLFtyLvOxLImWQAv_J6uQu9fQ5RsezLzLkWdcX-X-PF9xK8e3l3sBNyNs1lQWc02tAI61CdiyviT7gI2Dx6JpzkBpmGDio_OUFjBCAt2roU9FTPWhNVSrU47W0rJ77K8NmjwneqDC0qCYzFF2yOuK87-GYO91nXk8fx_xs0kXQ25htC1jG4hVQ9xdmHBpkz5xJ9fy-QOG4EAx.YqHlOw.Nxopf6mxCCEPUEeTakSx7rOg-Do; remember_token=20|40ed4057d976aa0dc1d708f2ea0c076d37e2eb7d1e92fa3b24c6e29cfe205d59a78f88f58611c17d981f8cecfa02fa9895ea22a75d0bae42c9fa72e9ac5d4f5f',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    response = requests.get('https://orderbookz.com/company', cookies=cookies, headers=headers)
    return response


def get_response_news() -> requests.models.Response:
    cookies = {
        'session': '.eJwljkFqQzEMBe_idRaSLFtyLvOxLImWQAv_J6uQu9fQ5RsezLzLkWdcX-X-PF9xK8e3l3sBNyNs1lQWc02tAI61CdiyviT7gI2Dx6JpzkBpmGDio_OUFjBCAt2roU9FTPWhNVSrU47W0rJ77K8NmjwneqDC0qCYzFF2yOuK87-GYO91nXk8fx_xs0kXQ25htC1jG4hVQ9xdmHBpkz5xJ9fy-QOG4EAx.YqHlOw.Nxopf6mxCCEPUEeTakSx7rOg-Do',
        'remember_token': '20|40ed4057d976aa0dc1d708f2ea0c076d37e2eb7d1e92fa3b24c6e29cfe205d59a78f88f58611c17d981f8cecfa02fa9895ea22a75d0bae42c9fa72e9ac5d4f5f',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'nl,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://orderbookz.com/company',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'session=.eJwljkFqQzEMBe_idRaSLFtyLvOxLImWQAv_J6uQu9fQ5RsezLzLkWdcX-X-PF9xK8e3l3sBNyNs1lQWc02tAI61CdiyviT7gI2Dx6JpzkBpmGDio_OUFjBCAt2roU9FTPWhNVSrU47W0rJ77K8NmjwneqDC0qCYzFF2yOuK87-GYO91nXk8fx_xs0kXQ25htC1jG4hVQ9xdmHBpkz5xJ9fy-QOG4EAx.YqHlOw.Nxopf6mxCCEPUEeTakSx7rOg-Do; remember_token=20|40ed4057d976aa0dc1d708f2ea0c076d37e2eb7d1e92fa3b24c6e29cfe205d59a78f88f58611c17d981f8cecfa02fa9895ea22a75d0bae42c9fa72e9ac5d4f5f',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    return requests.get('https://orderbookz.com/news', cookies=cookies, headers=headers)

def scrape_prices() -> None:
    """
    Scrape date, time and price.
    :return:
    """
    response = get_response_prices()
    soup = bs(response.text, "lxml")
    try:
        container = soup.find_all("tr")
        print(container)

    except ValueError as e:
        print(e)

    # TODO: clean the data to the format that we want



def scrape_text() -> None:
    """
    Scrapes the news including company name and the text itself.
    :return:
    """
    response = get_response_news()
    soup = bs(response.text, "lxml")
    try:
        container = soup.find_all("div", {"class": "card text-white bg-success"})
        print(container)

    except ValueError as e:
        print(e)
    # TODO: clean data and put it in the correct format


if __name__ == "__main__":
    # scrape_prices()
    scrape_text()


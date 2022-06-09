"""
Scrape the website for texts and prices
"""

from bs4 import BeautifulSoup as bs
import requests

api_key = "QUYCQ"


def get_response_prices() -> requests.models.Response:
    headers = {
        "API-Key": api_key,
    }
    return requests.get('https://orderbookz.com/company', headers=headers)


def get_response_news() -> requests.models.Response:
    headers = {
        "API-Key": api_key,
    }
    return requests.get('https://orderbookz.com/news', headers=headers, verify=False)

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
    # print(":ff")
    scrape_prices()
    # scrape_text()


"""
Scrape the website for texts and prices
"""

from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
from IPython.display import display
api_key = "QUYCQ"


def find_between(s, first, last):
    try:
        regex = rf'{first}(.*?){last}'
        return re.findall(regex, s)
    except ValueError:
        return -1

def get_response_prices() -> requests.models.Response:
    headers = {
        "API-Key": api_key,
    }
    return requests.get('http://orderbookz.com/company', headers=headers)


def get_response_news() -> requests.models.Response:
    headers = {
        "API-Key": api_key,
    }
    return requests.get('http://orderbookz.com/news', headers=headers, verify=False)

def scrape_prices() -> None:
    """
    Scrape date, time and price.
    :return:
    """
    response = get_response_prices()
    soup = bs(response.text, "lxml")
    container = None
    try:
        container = soup.find_all("tr")[1:]
        print(container)
    except ValueError as e:
        print(e)

    l = []
    print("\n\n")
    for th in container:
        row = []
        for line in th:
            line = str(line)
            if len(line) == 0:
                continue
            data= find_between(line, "<td>", "</td>")
            try:
                row.append(data[0])
            except Exception as e:
                print(e)
        l.append(row)

    print(f"the list l {l}")
    print(len(l))
    prices_df = pd.DataFrame(l, columns = ["Date", "Time","Profit over Previous Period"])
    print(prices_df)


    # # add the dataframe
    #
    # labels = ["Date", "Time", "Profit"]

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


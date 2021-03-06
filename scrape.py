"""
Scrape the website for texts and prices
"""
import time

from bs4 import BeautifulSoup as bs
import requests
import re
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd


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


time_until_next_earnings = None


def scrape_prices() -> None:
    """
    Scrape date, time and price.
    :return:
    """
    response = get_response_prices()
    soup = bs(response.text, "html")
    container = None
    try:
        container = soup.find_all("tr")[1:]
    except ValueError as e:
        print(e)


    # Get the time of the next update
    time = "9/6/2022 " + soup.find('p').getText().split(" ")[-1]
    print(time)
    time_untill_update = datetime.strptime(time, "%d/%m/%Y %H:%M:%S")
    current_time = datetime.now() - timedelta(hours=1)
    print(f"time to update {time_untill_update} time now {current_time}")
    diff = time_untill_update - current_time
    print(diff.seconds)

    # # Get the prices
    l = []
    print("\n\n")
    for th in container:
        row = []
        for line in th:
            line = str(line)
            if len(line) == 0:
                continue
            data = find_between(line, "<td>", "</td>")
            try:
                row.append(data[0])
            except Exception as e:
                # print(e)
                pass
        l.append(row)

    # print(f"the list l {l}")
    # print(len(l))
    prices_df = pd.DataFrame(l, columns=["Date", "Time", "Profit over Previous Period"])
    # print(prices_df)
    prices_df.to_csv('earnings.csv')
    # add the dataframe

    return diff.seconds - 5
    # TODO: clean the data to the format that we want


def scrape_text() -> None:
    """
    Scrapes the news including company name and the text itself.
    :return:
    """
    response = get_response_news()
    soup = bs(response.text, "html")
    try:
        container = soup.find_all("div", {"class": "card text-white bg-success"})

    except ValueError as e:
        print(e)

    # card - header
    try:
        container = soup.find_all("div", {"class": "card-header"})
        for i in container:
            company_name = i.get_text().strip()
            l.append([company_name])
            print(company_name)

    except ValueError as e:
        print(e)
   # card-body
    try:
        container = soup.find_all("div", {"class": "card-body"})
        print(type(container[0]))
        print(container)
        for i, text in enumerate(container):
            text = text.get_text().strip()
            l[i].append(text)

    except ValueError as e:
        print(e)

    try:
        container = soup.find_all("div", {"class": "card-footer text-muted"})
        print(container)
        for i, text in enumerate(container):
            text = text.get_text().strip()
            l[i].append(text)

    except ValueError as e:
        print(e)
    print(l)

    prices_df = pd.DataFrame(l, columns=["company", "Message", "Time"])
    print(prices_df)

    # TODO: clean data and put it in the correct format


if __name__ == "__main__":
    # print(":ff")
    while True:
        scrape_prices()
        # time.sleep(1)
    # scrape_text()


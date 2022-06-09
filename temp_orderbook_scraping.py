import requests
import time
import datetime
import pickle
from datetime import datetime

api_key = "QUYCQ"
active_orders = None


def send_req(link):
    headers = {
        "API-Key": api_key,
    }
    params = {
        "page": 1,
        "per_page": 100
    }
    try:
        req = requests.get(r"https://orderbookz.com/bluelagoon/api/"+link,
                   headers=headers, json=params, timeout=1)
    except Exception:
        print("Request timed out, trying again")
        return Exception
    return req.json()

order_book = {}        

# Event trigger based on positive / negative sentiment

i = 0
while True:
    curr_order_book = send_req("orderbook")
    order_book[time.time()] = curr_order_book
    time.sleep(1)
    i += 1
    if i > 60:
        print("Saving")
        current_time = datetime.now().strftime("%H_%M_%S")
        with open(f'./order_books/{current_time}.pickle', 'wb') as f:
            pickle.dump(order_book, f)
        i = 1
        order_book = {}







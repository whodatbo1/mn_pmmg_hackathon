import requests
import time
import datetime

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


def send_order(p, q, d, tif):
    headers = {
        "API-Key": api_key,
    }
    data = {
        "p": p,
        "q": q,
        "d": d,
        "tif": tif
    }
    try:
        req = requests.post(r"https://orderbookz.com/bluelagoon/api/submit",
                   headers=headers, json=data, timeout=1)
    except Exception:
        print("Something went wrong")
    # active_orders[req.json()[]]
    return req.json()


def get_trades():
    return send_req("trades")


def buy(price, quantity, IOC=False):
    return send_order(price, quantity, "buy", "IOC" if IOC else "GTC")


def sell(price, quantity, IOC=False):
    return send_order(price, quantity, "sell", "IOC" if IOC else "GTC")
    

def cancel_order(order_id):
    headers = {
        "API-Key": api_key,
    }
    params = {
        "id": order_id
    }
    try:
        post_req = requests.put(r"https://orderbookz.com/bluelagoon/api/cancel",
                                headers=headers, timeout=1, json=params)
    except Exception:
        print("Request timed out, trying again")
        return Exception
    return post_req.json()


def cancel_all():
    headers = {
        "API-Key": api_key,
    }
    try:
        post_req = requests.put(r"https://orderbookz.com/bluelagoon/api/cancel",
                                headers=headers, timeout=1)
    except Exception:
        print("Request timed out, trying again")
        return Exception
    return post_req.json()

# print(send_req("balance"))
# time.sleep(0.3)
# print(send_req("orderbook"))
# time.sleep(0.3)
# print(send_req("orders/active"))
# time.sleep(0.3)
print(get_trades())
time.sleep(0.3)

# print(cancel_order('BLGX000001166'))

order_book = {}
trades = {}

balance = None
last_traded_value = None
curr_order_book = None

# Event trigger based on positive / negative sentiment

# while True:
#     curr_order_book = send_req("orderbook")
#     order_book[time.time()] = curr_order_book
#     time.sleep(0.2)
#
#     active_orders = send_req("orders/active")
#     time.sleep(0.2)
#
#     balance = send_req("balance")
#     print(curr_order_book, active_orders, balance)

    # if ...some_condition:
    #     do trade

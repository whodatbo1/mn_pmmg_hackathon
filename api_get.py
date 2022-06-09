import requests
import time
import datetime
import pandas as pd

api_key = "QUYCQ"


def send_req(link):
    headers = {
        "API-Key": api_key,
    }
    try:
        req = requests.get(r"https://orderbookz.com/bluelagoon/api/"+link,
                   headers=headers, timeout=2)
    except Exception:
        print("Request timed out, trying again")
        return
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


def get_active_orders():
    return send_req("orders/active")


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
active_orders = None

filled_orders = pd.DataFrame(columns=['buyer', 'direction', 'id', 'price', 'quantity', 'seller', 'timestamp'])

# Event trigger based on positive / negative sentiment

traded_values = []

bid_ask_spread = None

while True:
    curr_order_book = send_req("orderbook")
    order_book[time.time()] = curr_order_book
    time.sleep(0.2)

    active_orders = get_active_orders()
    time.sleep(0.2)
    trades = get_trades()
    time.sleep(0.2)
    # balance = send_req("balance")
    # time.sleep(0.2)
    print(curr_order_book)
    buys = curr_order_book['buy']
    sells = curr_order_book['sell']
    bid_ask_spread = (sells[0] + buys[len(buys) - 1]) / 2
    print('bas', bid_ask_spread)
    # print('active_orders', active_orders)
    # print(balance)
    # print('trades', trades)
    if trades:
        for trade in trades['data']:
            trade_id = trade['id']
            if trade_id not in filled_orders['id'].unique():
                trade_df = pd.DataFrame(trade, index=[len(filled_orders)])
                filled_orders = pd.concat([filled_orders, trade_df], axis=0)

    filled_orders.sort_values(by='timestamp', ignore_index=True, inplace=True, ascending=False)
    last_traded_value = filled_orders.iloc[0]['price']
    print('ltv', last_traded_value)
    traded_values.append(last_traded_value)

# {'buyer': 'Diana Asset Management', 'direction': 'sell', 'id': 'BLGT000000110', 'price': '110.1', 'quantity': 25, 'seller': 'Jupiter Asset Management', 'timestamp': '09 06 2022 15:22:55.928507'
import requests
import time
import datetime
import pandas as pd
import math

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
        return
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
        put_req = requests.put(r"https://orderbookz.com/bluelagoon/api/cancel",
                                headers=headers, timeout=1, json=params)
    except Exception:
        print("Request timed out, trying again")
        return Exception
    return put_req.json()


def cancel_all():
    headers = {
        "API-Key": api_key,
    }
    try:
        put_req = requests.put(r"https://orderbookz.com/bluelagoon/api/cancel/all",
                                headers=headers, timeout=1)
    except Exception:
        print("Request timed out, trying again")
        return Exception
    return put_req.json()

# print(cancel_order('BLGX000001166'))


def load_earnings():
    return pd.read_csv('earnings.csv')


def update_target_price(historical_evidence = -3354.27):
    prices = load_earnings()
    profit = prices["Profit over Previous Period"]
    profits = []
    for j in profit:
        profits.append(float(j))
    profits = profits[::-1]
    number_of_profits = len(profits)
    P = (5 - number_of_profits) * historical_evidence + sum(profits)
    return (100_000 + P) / 1_000

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
# earnings = load_earnings()
highest_buy = 100000000
lowest_sell = 0

is_there_info = False

MAX_STOCK = 30
balance_stock = 0
margin = 0.01
factor = 0.5

target_price_new = 122
target_price_old = 122

prev_earning_release_length = len(load_earnings())

while True:

    has_event_happened = len(load_earnings()) > prev_earning_release_length

    if has_event_happened:
        margin *= factor
        update_target_price()

    # cancel_all()
    curr_order_book = send_req("orderbook")
    order_book[time.time()] = curr_order_book
    # time.sleep(0.2)
    trades = get_trades()
    time.sleep(0.2)
    # print(curr_order_book)

    # active_orders = get_active_orders()

    if curr_order_book:
        buys = curr_order_book['buy']
        sells = curr_order_book['sell']
        highest_buy = float(buys[len(buys) - 1][0])
        lowest_sell = float(sells[0][0])
        # print('highest_buy', highest_buy)
        # print('lowest_sell', lowest_sell)
        # bid_ask_spread = (highest_buy + lowest_sell) / 2
        # print('bid_ass_spread', bid_ask_spread)

    print('balance', balance)
    # if not has_event_happened:
    if highest_buy > target_price_new * (1 + margin):
        cancel_all()
        balance = send_req("balance")
        time.sleep(0.1)
        if balance['stock'] > -30:
            order = sell(target_price_new * (1 + margin), abs(-MAX_STOCK - balance['stock']))
            print('sending', target_price_new * (1 + margin), abs(-MAX_STOCK - balance['stock']))
            print(order)
    if lowest_sell < target_price_new * (1 - margin):
        cancel_all()
        balance = send_req("balance")
        time.sleep(0.1)
        if balance['stock'] < 30:
            order = buy(target_price_new * (1 - margin), MAX_STOCK - balance['stock'])
            print(target_price_new * (1 - margin), MAX_STOCK - balance['stock'])
            print(order)
    # else:
    #     if target_price_new != target_price_old:
    #         cancel_all()
    #         balance = send_req("balance")
    #         if highest_buy > target_price_new and balance['stock'] > -30:
    #             order = sell(target_price_new, math.abs(-MAX_STOCK - balance['stock']))
    #
    #         if lowest_sell < target_price_new and balance['stock'] < 30:
    #             order = buy(target_price_new, MAX_STOCK - balance['stock'])

    time.sleep(0.2)
    active_orders = get_active_orders()
    print('active_orders', active_orders)

    if trades:
        for trade in trades['data']:
            trade_id = trade['id']
            if trade_id not in filled_orders['id'].unique():
                trade_df = pd.DataFrame(trade, index=[len(filled_orders)])
                filled_orders = pd.concat([filled_orders, trade_df], axis=0)

    filled_orders.sort_values(by='timestamp', ignore_index=True, inplace=True, ascending=False)
    if filled_orders.shape[0] >= 0:
        last_traded_value = filled_orders.iloc[0]['price']
    print('ltv', last_traded_value)
    traded_values.append(last_traded_value)
    # print('earnings', earnings)

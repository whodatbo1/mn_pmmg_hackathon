import requests
import time
import datetime

api_key = "QUYCQ"


def send_req(link):
    headers = {
        "API-Key": api_key,
    }
    try:
        req = requests.get(r"https://orderbookz.com/bluelagoon/api/"+link,
                   headers=headers, timeout=1)
    except Exception:
        print("Request timed out, trying again")
        return Exception
    return req.json()


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


print(send_req("balance"))
time.sleep(0.3)
print(send_req("orderbook"))
time.sleep(0.3)
print(send_req("orders/active"))
time.sleep(0.3)
print(send_req("trades"))
time.sleep(0.3)

print(cancel_order('BLGX000001166'))
import requests
import time
import datetime

    
def send_req(link):
    headers = {
        "API-Key": "JGJUR",
    }
    try:
        req = requests.get(r"https://orderbookz.com/bluelagoon/api/"+link,
                   headers=headers, timeout=1)
    except Exception:
        print("Request timed out, trying again")
    return req.json()



print(send_req("balance"))
time.sleep(0.3)
print(send_req("orderbook"))
time.sleep(0.3)
print(send_req("orders/active"))
time.sleep(0.3)
print(send_req("trades"))
time.sleep(0.3)
    
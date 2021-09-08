from binance.client import Client
from binance.enums import *
import config

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)
    try:
        print("Setting order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def avg(arr, num):
    if len(arr == 0):
        return len(arr)
    else:
        return sum(arr[-num:]) / num
import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *
from ta.momentum import RSIIndicator
import pandas as pd

reddit = praw.Reddit(
    client_id = config.REDDIT_ID,
    client_secret = config.REDDIT_SECRET,
    password = config.REDDIT_PASS,
    user_agent = "USERAGENT",
    username = config.REDDIT_USER
)
client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)

sentimentArr = []
prices = []
required = 100
TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = "0"
in_position = False

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("Error: " + e)
        return False
    return True

def Average(arr):
    if len(arr) == 0:
        return arr
    else:
        return sum(arr[-required:])/required

for comment in reddit.subreddit("bitcoinmarkets").stream.comments():
    redditComment = comment.body
    sentAnal = TextBlob(redditComment)
    sent = sentAnal.sentiment
    if sent.polarity != 0.0:
        sentimentArr.append(sent.polarity)
        candle = client.get_historical_klines(TRADE_SYMBOL, Client.KLINE_INTERVAL_5MINUTE, "5 minutes ago UTC")
        val = candle[-1][1]

        if len(prices) == 0:
            prices.append(float(val))

        elif prices[-1] != float(val):
            prices.append(float(val))

        print("Total sentiment is: {0}".format(round(Average(sentimentArr))))
        print("Length of prices list is " + str(len(prices)))
        
        rsi = RSIIndicator(pd.Series(prices))
        dframe = rsi.rsi()
        rsiVal = dframe.iloc[-1]

        if rsiVal < 30 and len(sentimentArr) > required and round(Average(sentimentArr)) > 0.5:
            if in_position:
                print("BUY ORDER BUT IN POSITION")
            else:
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    print("BUY ORDER")
                    in_position = True
        
        elif rsiVal > 70 and len(sentimentArr) > required and round(Average(sentimentArr)) < -0.5:
            if in_position:
                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    print("SELL ORDER")
                    in_position = False
            else:
                print("SELL ORDER BUT NOT IN POSITION")

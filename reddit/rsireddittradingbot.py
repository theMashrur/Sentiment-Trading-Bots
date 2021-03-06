import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *
from ta.momentum import RSIIndicator
import pandas as pd

#initialize interaction with reddit through the PRAW API
reddit = praw.Reddit(
    client_id = config.REDDIT_ID,
    client_secret = config.REDDIT_SECRET,
    password = config.REDDIT_PASS,
    user_agent = "USERAGENT",
    username = config.REDDIT_USER
)
#initialize interaction with binance throught the python binance API
client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)

#initialize variables 
sentimentArr = []
prices = []
required = 100
TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = "0"
in_position = False


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    """
    Executes buy and sell orders on the Binance Exchange.
    """
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("Error: " + e)
        return False
    return True

def avg(arr):
    """
    Calculates the average of the last 'required' items of a list
    """
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
        #retrieve the candles from the last 5 minutes
        candle = client.get_historical_klines(TRADE_SYMBOL, Client.KLINE_INTERVAL_5MINUTE, "5 minutes ago UTC")
        val = candle[-1][1]

        if len(prices) == 0:
            prices.append(float(val))

        elif prices[-1] != float(val):
            prices.append(float(val))

        print("Total sentiment is: {0}".format(round(avg(sentimentArr))))
        print("Length of prices list is " + str(len(prices)))
        
        #get estimated RSI values based on a minimum sample size of 14
        rsi = RSIIndicator(pd.Series(prices))
        dframe = rsi.rsi()
        rsiVal = dframe.iloc[-1]
        #Trading strategy involves RSI as well. A number above 70 indicates that the stock/crypto
        #is overbought (meaning that it would be apt to sell), while 30 indicates that it is oversold (apt to buy)
        if rsiVal < 30 and len(sentimentArr) > required and round(avg(sentimentArr)) > 0.5:
            if in_position:
                print("BUY ORDER BUT IN POSITION")
            else:
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    print("BUY ORDER")
                    in_position = True
        
        elif rsiVal > 70 and len(sentimentArr) > required and round(avg(sentimentArr)) < -0.5:
            if in_position:
                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    print("SELL ORDER")
                    in_position = False
            else:
                print("SELL ORDER BUT NOT IN POSITION")

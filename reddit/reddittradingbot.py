from typing_extensions import Required
import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *

#access reddit through the PRAW API
reddit = praw.Reddit(
    client_id = config.REDDIT_ID,
    client_secret = config.REDDIT_SECRET,
    password = config.REDDIT_PASS,
    user_agent = "USERAGENT",
    username = config.REDDIT_USER
)
#access binance through the binance python API
client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)

#initialize variables
sentimentArr = []
required = 100 #sample taken to calculate sentiment
TRADE_SYMBOL = "BTCUSDT" #stores our exchange symbol. Here its set to BTC/USDT
TRADE_QUANTITY = "0.01"
in_position = False


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    """
    Execute buy and sell orders on the Binance exchange.
    Takes for argument Buy/Sell, quantity, symbol, with a default of market order
    """
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("Error: " + e)
        return False
    return True

def Average(arr):
    """
    Takes the average of the last 'required' items of an array
    """
    if len(arr) == 0:
        return arr
    else:
        return sum(arr[-required:])/required


for comment in reddit.subreddit("bitcoin").stream.comments():
    redditComment = comment.body
    blob = TextBlob(redditComment)
    sent = blob.sentiment
    if sent.polarity != 0.0:
        sentimentArr.append(sent.polarity)
        print("Total sentiment is: {0}".format(round(Average(sentimentArr))))
        if  len(sentimentArr) > required and round(Average(sentimentArr)) > 0.5:
            if in_position:
                print("BUY ORDER BUT IN POSITION")
            else:
                print("BUY ORDER")
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = True
        elif len(sentimentArr) > required and round(Average(sentimentArr)) < -0.5:
            if in_position:
                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = False
            else:
                print("SELL ORDER BUT NOT IN POSITION")

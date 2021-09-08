import requests
import os
import json
import config
import preprocessor as prep
from langdetect import detect
from csv import writer
from order import order, avg
from binance.client import Client
from binance.enums import *


from ernie import SentenceClassifier
import numpy as np
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = config.BEARER_TOKEN
classifier = SentenceClassifier(model_path='./model')

position = False
TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = 0.001
arr = []
num = 100



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    rules = [
        {"value": "bitcoin", "tag": "bitcoin"},
        #{"value": "cat has:images -grumpy", "tag": "cat pictures"},
    ]
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    global position
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response['data']['text']
            tweet = prep.clean(tweet)
            tweet = tweet.replace(':', '')
            try:
                if detect(tweet) == "en":
                    #print(tweet)
                    classes = config.classes
                    probabilities = classifier.predict_one(tweet)
                    pol = classes[np.argmax(probabilities)]
                    arr.append(pol)
                    if len(arr) > num:
                        end = arr[-num:]
                        pos = end.count('positive')
                        neg = end.count('negative')
                        print("Total Positive tweets: {0}".format(pos))
                        print("Total Negative tweets: {0}".format(neg))
                        if pos > 20:
                            if position:
                                print("Buy signalled, but already in position")
                            else:
                                print("Buy Order signalled")
                                #order_executed  = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                                position = True
                                print("Buy order executed")
                        elif neg > 20:
                            if position:
                                print("Sell order signalled")
                                #order_executed = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                                print("Sell order executed")
                                position = False
                            else:
                                print("Sell order signalled, but none in possession")
            except:
                pass


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()
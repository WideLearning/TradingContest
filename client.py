import argparse
import json
from time import time

import requests

parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="unique name for the bot")
name = parser.parse_args().name


def request(command, args, log=True):
    args["command"] = command
    args["account"] = name
    response = requests.post("http://etrade.pythonanywhere.com/", json=args).json()
    if log:
        print(time())
        print(json.dumps(args, indent=2))
        print(json.dumps(response, indent=2))
    return response


if "error" not in request("account", {}):
    overwrite = input("Account already exists. Overwite? ")
    if overwrite.lower() in ["y", "yes"]:
        request("register", {})
else:
    request("register", {})

while True:
    book = request("book", {})
    request("account", {})
    sign, symbol, price, volume = input("> ").split()
    try:
        assert sign in ["buy", "sell"], "unknown sign"
        assert symbol in book, "unknown symbol"
        price = float(price)
        assert price > 0, "negative price"
        volume = float(volume)
        assert volume > 0, "negative volume"
    except Exception as e:
        print(e)
        print("Try again")
        continue
    request(sign, {"symbol": symbol, "price": price, "volume": volume})

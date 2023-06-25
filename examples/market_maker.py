import argparse
import json
from time import time

import requests

parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, required=True, help="unique name for the bot")
name = parser.parse_args().name


def request(command, args, log=True):
    args["command"] = command
    args["account"] = name
    response = requests.post("http://etrade.pythonanywhere.com/", json=request).json()
    if log:
        print(time())
        print(json.dumps(request, indent=2))
        print(json.dumps(response, indent=2))
    return response


if "error" not in request("account", {}):
    overwrite = input("Account already exists. Overwite?")
    if overwrite.lower() in ["y", "yes"]:
        request("register", {})
else:
    request("register", {})

request("book", {})
request("account", {})

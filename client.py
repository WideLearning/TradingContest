import requests


name = "anon"


def post(request):
    request["account"] = name
    return requests.post("http://etrade.pythonanywhere.com/", json=request)


# print(post({"command": "register"}).json())
# print(post({"command": "buy", "symbol": "A", "price": 10.0, "volume": 1.0}).json())
print(post({"command": "book"}).json())
print(post({"command": "account"}).json())

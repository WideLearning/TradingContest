import requests


name = "anon"


def post(request):
    request["account"] = name
    return requests.post("http://etrade.pythonanywhere.com/", json=request)


response = post({"command": "register"})
print(response, response.json())
response = post({"command": "account"})
print(response, response.json())

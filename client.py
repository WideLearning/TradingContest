import requests


name = "anon"


def post(request):
    request["account"] = name
    return requests.post("http://etrade.pythonanywhere.com/", json=request)


_ = post({"command": "register"})
response = post({"command": "account"})

print(response)
print(response.json())

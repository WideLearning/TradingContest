import requests


name = "anon"


def post(request):
    requst["account"] = name
    return requests.post("http://etrade.pythonanywhere.com/", json=request)


post({"command": "register"})
post({"command": "account"})

print(response)
print(response.json())

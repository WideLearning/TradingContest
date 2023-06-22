import requests

order = {
    "command": "order_book"
}

response = requests.post("http://etrade.pythonanywhere.com/", json=order)
print(response)
print(response.json())

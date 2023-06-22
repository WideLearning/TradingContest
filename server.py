from flask import Flask, request, jsonify
from heapq import heappush, heappop
from copy import deepcopy
from lib import BUY, SELL, symbols, Account, Order, OrderBook, OrderBooks, match_price, execute

accounts = {}
books = OrderBooks()


def account_summary():
    return {name: account.to_dict() for name, account in accounts.items()}


def book_summary():
    return books.to_dict()


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_json()
    print(data)
    try:
        command = data["command"]
        account = data["account"]
        response = {}
        if command == "book":
            response = book_summary()
        elif command == "account":
            response = dict(accounts[account])
        elif command == "buy":
            assert account in accounts
            order = Order(symbol=command["symbol"], sign=BUY, price=command["price"], volume=command["volume"], account=account)
            books.put_order(order)
            response = {"status": "ok"}
        elif command == "sell":
            assert account in accounts
            order = Order(symbol=command["symbol"], sign=SELL, price=command["price"], volume=command["volume"], account=account)
            books.put_order(order)
            response = {"status": "ok"}
        elif command == "register":
            accounts[account] = Account()
            response = {"status": "ok"}
        else:
            raise Exception(f"Unknown command {command}")
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route('/', methods=['GET'])
def print_help():
    with open("client.py", encoding="utf-8") as f:
        sample = f.read()
    return f"Example implementation of a client:\n{sample}"


if __name__ == '__main__':
    app.run(debug=True)

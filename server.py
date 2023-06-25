from flask import Flask, jsonify, request

from lib import BUY, SELL, Exchange

exchange = Exchange()

app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_request():
    data = request.get_json()
    print(data)
    try:
        command = data["command"]
        account = data["account"]
        response = {}
        if command == "book":
            response = exchange.books_summary()
        elif command == "account":
            response = exchange.account_summary()
        elif command == "buy" or command == "sell":
            sign = BUY if command == "buy" else SELL
            response = exchange.put_order(
                symbol=data["symbol"],
                sign=sign,
                price=data["price"],
                volume=data["volume"],
                account=account,
            )
        elif command == "cancel":
            response = exchange.cancel_order(id=data["id"])
        elif command == "register":
            response = exchange.register(account=account)
        elif command == "history":
            response = exchange.trade_history
        else:
            raise Exception(f"Unknown command {command}")
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route("/", methods=["GET"])
def print_help():
    with open("client.py", encoding="utf-8") as f:
        sample = f"<pre>{f.read()}</pre>"
    return f"Example implementation of a client:<br><br>{sample}"


if __name__ == "__main__":
    app.run(debug=True)

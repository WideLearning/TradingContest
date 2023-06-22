from heapq import heappush, heappop
from copy import deepcopy

symbols = ["A", "B", "C"]
BUY = +1
SELL = -1


class Account:
    def __init__(self):
        # TODO add some tracking maybe
        self.balance = {symbol: 100 for symbol in symbols}
        self.balance["$"] = 1000

    def change_balance(self, symbol, quantity):
        # TODO do we allow negative balance?
        self.balance[symbol] += quantity

    def __dict__(self):
        return self.balance


class Order:
    def __init__(self, symbol, sign, price, volume, account, time=None):
        assert type(symbol) is str
        assert sign in [BUY, SELL]
        assert type(price) is float and price > 0
        assert type(volume) is float and volume > 0
        assert type(account) is Account
        if time is None:
            time = time()
        else:
            assert type(time) is float and abs((time - time()) / time) < 0.1

        self.sign = sign
        self.price = price
        self.volume = volume
        self.account = account
        self.time = time

    def sorting_key(self):
        return (-self.sign * self.price, self.time)

    def __lt__(self, other):
        return self.sorting_key() < other.sorting_key()

    def fill(self, volume):
        assert volume <= self.volume
        self.account.change_balance(self.symbol, self.sign * volume)
        self.account.change_balance("$", -self.sign * self.price * volume)


def match_price(x: Order, y: Order) -> float | None:
    assert x.symbol == y.symbol
    if x.price > y.price:
        x, y = y, x
    assert x.price <= y.price
    if x.sign == SELL and y.sign == BUY:
        return x.price if x.time < y.time else y.price
    else:
        return None


def execute(x: Order, y: Order) -> tuple[Order, Order]:
    x = deepcopy(x)
    y = deepcopy(y)
    price = match_price(x, y)
    if price is None:
        return (x, y)
    volume = min(x.volume, y.volume)
    x.fill(volume)
    y.fill(volume)
    x = x if x.volume else None
    y = y if y.volume else None
    return (x, y)

# TODO (100, 200) order should be able to match with (99, 100) and (101, 100) together


class OrderBook:
    def __init__(self):
        self.buy = []
        self.sell = []

    def put_order(self, order):
        if order.sign == BUY:
            while self.sell and order is not None:
                price = match_price(order, self.sell[0])
                if price is None:
                    heappush(self.buy, order)
                    return
                counter = heappop(self.sell)
                order, counter = execute(order, counter)
                if counter is not None:
                    heappush(self.sell, counter)
        else:
            while self.buy and order is not None:
                price = match_price(order, self.buy[0])
                if price is None:
                    heappush(self.sell, order)
                    return
                counter = heappop(self.buy)
                order, counter = execute(order, counter)
                if counter is not None:
                    heappush(self.buy, counter)

    def __dict__(self):
        return {"buy": [dict(order) for order in self.buy], "sell": [dict(order) for order in self.sell]}


class OrderBooks:
    def __init__(self):
        self.books = {symbol: OrderBook() for symbol in symbols}

    def put_order(self, order):
        assert order.symbol in self.books
        self.books[order.symbol].put_order(order)

    def __dict__(self):
        return {symbol: dict(book) for symbol, book in self.books.items()}

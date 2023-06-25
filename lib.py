from heapq import heappush, heappop
from copy import deepcopy
from time import time as get_current_time
from uuid import uuid4

BUY = +1
SELL = -1


class Account:
    def __init__(self, symbols):
        # TODO add some tracking maybe
        self.balance = {symbol: 100 for symbol in symbols}
        self.balance["$"] = 1000

    def change_balance(self, symbol, quantity):
        # TODO do we allow negative balance?
        self.balance[symbol] += quantity

    def to_dict(self):
        return self.balance


class Order:
    def __init__(self, symbol, sign, price, volume, account, time=None):
        assert type(symbol) is str, "symbol must be str"
        assert sign in [BUY, SELL], "sign must be BUY or SELL"
        assert type(price) is float and price > 0, "price must be postitive float"
        assert type(volume) is float and volume > 0, "volume must be positive float"
        assert type(account) is Account, "account must be Account"
        if time is None:
            time = get_current_time()
        else:
            assert (
                type(time) is float and abs((time - get_current_time()) / time) < 0.1
            ), "time must be float and close to current time"

        self.symbol = symbol
        self.sign = sign
        self.price = price
        self.volume = volume
        self.account = account
        self.time = time
        self.id = uuid4()

    def sorting_key(self):
        return (-self.sign * self.price, self.time)

    def __lt__(self, other):
        return self.sorting_key() < other.sorting_key()

    def fill(self, volume):
        assert (
            volume <= self.volume
        ), "fill volume must be not greater than order volume"
        print("fill", self.account.balance, self.id, volume)
        self.account.change_balance(self.symbol, self.sign * volume)
        self.account.change_balance("$", -self.sign * self.price * volume)
        print("filled", self.account.balance)
        self.volume -= volume

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "sign": self.sign,
            "price": self.price,
            "volume": self.volume,
            "time": self.time,
        }


def match_price(x: Order, y: Order) -> float | None:
    assert x.symbol == y.symbol, "matched orders must be for the same symbol"
    if x.price > y.price:
        x, y = y, x
    assert x.price <= y.price, "just in case"
    if x.sign == SELL and y.sign == BUY:
        return x.price if x.time < y.time else y.price
    else:
        return None


def execute(x: Order, y: Order, trade_history: dict[str, list[tuple[float, float, float]]]) -> tuple[Order, Order]:
    price = match_price(x, y)
    if price is None:
        return
    volume = min(x.volume, y.volume)
    trade_history[x.symbol].append((get_current_time(), price, volume))
    x.fill(volume)
    y.fill(volume)


# TODO (100, 200) order should be able to match with (99, 100) and (101, 100) together
class OrderBook:
    def __init__(self):
        self.buy = []
        self.sell = []
        self.active_ids = set()

    def pop_active(self, heap):
        while heap:
            top = heappop(heap)
            if top.id not in self.active_ids:
                continue
            else:
                self.active_ids.remove(top.id)
                return top
        return None
    
    def push(self, heap, order):
        heappush(heap, order)
        self.active_ids.add(order.id)

    def put_order(self, order, trade_history):
        same, opposite = (self.buy, self.sell) if order.sign == BUY else (self.sell, self.buy)
        while order.volume:
            counter = self.pop_active(opposite)
            if counter is None:
                break
            price = match_price(order, counter)
            if price is None:
                self.push(opposite, counter)
                break
            execute(order, counter, trade_history)
            if counter.volume:
                self.push(opposite, counter)
        if order.volume:
            self.push(same, order)
            return order.id
        else:
            return None

    def cancel_order(self, id):
        self.active_ids.remove(id)

    def to_dict(self):
        return {
            "buy": [order.to_dict() for order in self.buy if order.id in self.active_ids],
            "sell": [order.to_dict() for order in self.sell if order.id in self.active_ids],
        }


class Exchange:
    def __init__(self):
        self.symbols = ["A", "B", "C"]
        self.trade_history = { symbol : [] for symbol in self.symbols }
        self.books = {symbol: OrderBook() for symbol in self.symbols}
        self.accounts = {}

    def put_order(self, symbol, sign, price, volume, account):
        assert account in self.accounts, "account must be registered"
        assert symbol in self.books, "symbol must be in books"
        order = Order(
            symbol=symbol,
            sign=sign,
            price=price,
            volume=volume,
            account=self.accounts[account],
        )
        return {"id": self.books[order.symbol].put_order(order, self.trade_history)}
    
    def cancel_order(self, id):
        book = next((book for book in self.books.values() if id in book.active_ids), None)
        if book is not None:
            book.cancel_order(id)
            return {}
        else:
            raise Exception("Tried removing non-existing order")
    
    def register(self, account):
        self.accounts[account] = Account(self.symbols)
        return {}

    def books_summary(self):
        return {symbol: book.to_dict() for symbol, book in self.books.items()}
    
    def account_summary(self, account):
        assert account in self.accounts, "account must be registered"
        return self.accounts[account].to_dict()

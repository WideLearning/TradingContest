from lib import *

accounts = {}
books = OrderBooks()


def account_summary():
    return {name: account.to_dict() for name, account in accounts.items()}


def book_summary():
    return books.to_dict()

accounts["a"] = Account()
accounts["b"] = Account()
print(book_summary())
print(accounts["a"].to_dict())
books.put_order(Order("A", BUY, 100.0, 10.0, accounts["a"]))
print(book_summary())
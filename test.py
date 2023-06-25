import unittest

from lib import BUY, SELL, Exchange


class TestStringMethods(unittest.TestCase):
    # def testRegister(self):
    #     e = Exchange()
    #     self.assertEqual(e.register("some"), {})

    # def testTradeOneself(self):
    #     e = Exchange()
    #     e.register("a")
    #     e.put_order("A", BUY, 1.05, 1.0, "a")
    #     e.put_order("A", SELL, 0.95, 1.0, "a")
    #     book = e.books_summary()["A"]
    #     self.assertEqual(book["buy"], [])
    #     self.assertEqual(book["sell"], [])
    #     self.assertEqual(e.trade_history["A"][0][1:], (1.05, 1.0))

    # def testNoTradeOneself(self):
    #     e = Exchange()
    #     e.register("a")
    #     e.put_order("A", BUY, 0.95, 1.0, "a")
    #     e.put_order("A", SELL, 1.05, 1.0, "a")
    #     self.assertEqual(e.trade_history, {"A": [], "B": [], "C": []})
    
    def testTradeTwo(self):
        e = Exchange()
        e.register("a")
        e.register("b")
        e.put_order("A", BUY, 1.05, 1.0, "a")
        e.put_order("A", SELL, 0.95, 1.0, "b")
        book = e.books_summary()["A"]
        account_a = e.account_summary("a")
        account_b = e.account_summary("b")
        self.assertEqual(book["buy"], [])
        self.assertEqual(book["sell"], [])
        self.assertEqual(e.trade_history["A"][0][1:], (1.05, 1.0))
        self.assertEqual(account_a["A"], 101.0)
        self.assertEqual(account_b["A"], 99.0)

if __name__ == "__main__":
    unittest.main()

from collections import defaultdict, deque
from typing import Optional
from engine.order import Order, Side, OrderType  # 🧠 You forgot to import OrderType

class OrderBook:
    def __init__(self):
        # Fix: `self.book` not `self.orders`
        self.book = {
            Side.buy: defaultdict(deque),
            Side.sell: defaultdict(deque),
        }

    def add_order(self, order: Order):
        # ✅ Indentation fixed
        if order.order_type not in [OrderType.limit, OrderType.fok, OrderType.ioc]:
            raise ValueError(f"{order.order_type.value.upper()} orders cannot be added to the order book")

        if order.price is None:
            raise ValueError("Price must be set to add order to book")

        # ✅ Typo fixed: use self.book not self.orders
        self.book[order.side][order.price].append(order)

    def _total_qty(self, side: Side, price: Optional[float]) -> float:
        if price is None or price not in self.book[side]:
            return 0.0
        return sum(order.remaining_qty for order in self.book[side][price])

    def get_bbo(self):
        best_bid = max(self.book[Side.buy].keys(), default=None)
        best_ask = min(self.book[Side.sell].keys(), default=None)

        return {
            "best_bid": {
                "price": best_bid,
                "quantity": self._total_qty(Side.buy, best_bid)
            },
            "best_ask": {
                "price": best_ask,
                "quantity": self._total_qty(Side.sell, best_ask)
            }
        }
 
from engine.order_book import OrderBook
from engine.order import Order, Side, OrderType
from uuid import uuid4
from datetime import datetime
import asyncio
from api.websocket_manager import broadcast_trade
# ✅ Correct import for WebSocket broadcasting
from api.websocket_manager import broadcast_trade

class MatchingEngine:
    def __init__(self):
        self.order_book = OrderBook()
        self.trade_history = []

    def match_order(self, order: Order):
        if order.order_type == OrderType.market:
            trades = self._match_market_order(order)
        else:
            self.order_book.add_order(order)
            trades = []

        self.trade_history.extend(trades)
        return trades

    def _match_market_order(self, order: Order):
        side = Side.sell if order.side == Side.buy else Side.buy
        opposite_book = self.order_book.book[side]
        matched_orders = []

        for price in sorted(opposite_book):
            queue = opposite_book[price]
            while queue and order.remaining_qty > 0:
                top_order = queue[0]
                traded_qty = min(order.remaining_qty, top_order.remaining_qty)
                order.remaining_qty -= traded_qty
                top_order.remaining_qty -= traded_qty

                trade = {
                    "timestamp": datetime.utcnow().isoformat() + 'Z',
                    "symbol": order.symbol,
                    "trade_id": str(uuid4()),
                    "price": price,
                    "quantity": traded_qty,
                    "aggressor_side": order.side.value,
                    "maker_order_id": top_order.id,
                    "taker_order_id": order.id
                }
                matched_orders.append(trade)

                # ✅ WebSocket broadcast (asynchronous)
                asyncio.create_task(broadcast_trade(trade))

                if top_order.remaining_qty == 0:
                    queue.popleft()

                if order.remaining_qty == 0:
                    break
            if order.remaining_qty == 0:
                break

        return matched_orders

    def cancel_order(self, order_id: str) -> bool:
        for side in [Side.buy, Side.sell]:
            for price_level in self.order_book.book[side].values():
                for order in list(price_level):
                    if order.id == order_id:
                        price_level.remove(order)
                        return True
        return False

import time
import uuid
from enum import Enum
from typing import Optional

class OrderType(str, Enum):
    market = "market"
    limit = "limit"
    ioc = "ioc"
    fok = "fok"

class Side(str, Enum):
    buy = "buy"
    sell = "sell"

class Order:
    def __init__(
        self,
        symbol: str,
        order_type: OrderType,
        side: Side,
        quantity: float,
        price: Optional[float] = None
    ):
        if quantity is None:
            raise ValueError("Quantity cannot be None")
        if order_type in [OrderType.limit, OrderType.fok] and price is None:
            raise ValueError(f"{order_type.value.upper()} orders require a price")

        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.symbol = symbol
        self.order_type = order_type
        self.side = side
        self.quantity = quantity
        self.remaining_qty = quantity  # For partial fills
        self.price = price

    def __repr__(self):
        return (
            f"<Order id={self.id}, symbol={self.symbol}, type={self.order_type}, "
            f"side={self.side}, quantity={self.quantity}, price={self.price}, "
            f"timestamp={self.timestamp}>"
        )

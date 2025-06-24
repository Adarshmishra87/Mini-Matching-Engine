from fastapi import APIRouter

router = APIRouter()

@router.get("/orderbook")
def get_order_book():
    return {
        "buy_orders": [{"price": 100, "quantity": 5}],
        "sell_orders": [{"price": 101, "quantity": 3}],
    }

@router.post("/submit")
def submit_order(order: dict):
    return {"status": "Order received", "order": order}

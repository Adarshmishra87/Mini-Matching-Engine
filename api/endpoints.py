
from engine.order import Side, OrderType, Order
from engine.matcher import MatchingEngine
from engine.trade_stream import subscribers, publish_trade
from api.websocket_manager import manager  # Make sure this exists and has `connect`, `disconnect`, `broadcast`

from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import asyncio

router = APIRouter()
engine = MatchingEngine()


class OrderRequest(BaseModel):
    symbol: str
    order_type: OrderType
    side: Side
    quantity: float
    price: Optional[float] = None


@router.post("/order")
def submit_order(request: OrderRequest):
    new_order = Order(
        symbol=request.symbol,
        order_type=request.order_type,
        side=request.side,
        quantity=request.quantity,
        price=request.price
    )
    trades = engine.match_order(new_order)

    for trade in trades:
        asyncio.create_task(manager.broadcast(trade))  # Broadcast to clients

    return {"order_id": new_order.id, "trades": trades}


@router.get("/orderbook")
def get_order_book():
    return {"orders": "example"}


@router.get("/orderbook/full")
def get_orderbook():
    return {
        "buy": {
            price: [o.__dict__ for o in orders]
            for price, orders in engine.order_book.book[Side.buy].items()
        },
        "sell": {
            price: [o.__dict__ for o in orders]
            for price, orders in engine.order_book.book[Side.sell].items()
        }
    }


@router.get("/orderbook/bbo")
def get_bbo():
    return engine.order_book.get_bbo()


@router.delete("/order/{order_id}")
def cancel_order(order_id: str):
    success = engine.cancel_order(order_id)
    if success:
        return {"status": "cancelled"}
    return {"error": "order not found"}


@router.get("/trades")
def get_trade_history():
    return engine.trade_history


@router.websocket("/ws")
async def websocket_keepalive(websocket: WebSocket):
    await websocket.accept()
    subscribers.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscribers.discard(websocket)


@router.websocket("/ws/trades")
async def trades_ws(websocket: WebSocket):
    await websocket.accept()
    subscribers.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            publish_trade(data)  # Re-broadcast
    except WebSocketDisconnect:
        subscribers.discard(websocket)
    except Exception as e:
        subscribers.discard(websocket)
        print(f"WebSocket error: {e}")

# from fastapi import FastAPI
# from api.endpoints import router

# app = FastAPI()
# app.include_router(router)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from api.websocket_manager import manager
from api.endpoints import router

app = FastAPI()
app.include_router(router)

@app.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # We don’t expect input, but it keeps the socket alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

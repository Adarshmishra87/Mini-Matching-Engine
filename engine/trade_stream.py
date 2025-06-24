subscribers = set()

async def broadcast(message):
    for ws in subscribers.copy():
        try:
            await ws.send_json(message)
        except Exception:
            subscribers.remove(ws)

def publish_trade(trade):
    import asyncio
    asyncio.create_task(broadcast(trade))

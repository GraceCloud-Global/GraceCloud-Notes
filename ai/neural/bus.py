import asyncio, websockets, json, datetime

clients = set()

async def handler(ws, path):
    clients.add(ws)
    try:
        async for msg in ws:
            data = json.loads(msg)
            event = {
                'time': datetime.datetime.utcnow().isoformat(),
                'node': data.get('node', 'unknown'),
                'signal': data.get('signal', ''),
            }
            broadcast = json.dumps({'type': 'neural_event', 'data': event})
            await asyncio.gather(*[c.send(broadcast) for c in clients if c != ws])
    finally:
        clients.remove(ws)

async def main():
    async with websockets.serve(handler, '0.0.0.0', 7070):
        print('🧩 Neural Event Bus active @7070')
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())

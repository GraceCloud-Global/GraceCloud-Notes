import asyncio, websockets, json, random, datetime

NODE = 'api-node'

async def connect():
    uri = 'ws://localhost:7070'
    async with websockets.connect(uri) as ws:
        while True:
            signal = random.choice(['load_high', 'stable', 'prediction_event', 'governance_check'])
            msg = json.dumps({'node': NODE, 'signal': signal})
            await ws.send(msg)
            await asyncio.sleep(random.uniform(2, 6))

if __name__ == '__main__':
    asyncio.run(connect())

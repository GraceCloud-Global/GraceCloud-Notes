import asyncio, json, random, datetime
from pathlib import Path

STATE_FILE = Path('ai/orchestrator/state.json')

class Orchestrator:
    def __init__(self):
        self.services = {
            'api': {'status': 'running'},
            'celery': {'status': 'running'},
            'redis': {'status': 'running'},
            'db': {'status': 'running'}
        }

    async def monitor(self):
        while True:
            status = {k: v['status'] for k,v in self.services.items()}
            STATE_FILE.write_text(json.dumps({'time': datetime.datetime.utcnow().isoformat(), 'status': status}, indent=2))
            print('🧠 Orchestrator heartbeat', datetime.datetime.now())
            await asyncio.sleep(10)

    async def anomaly_response(self):
        while True:
            for svc in self.services:
                if random.random() < 0.02:
                    print(f'⚠️ {svc} anomaly detected → restart')
                    self.services[svc]['status'] = 'restarting'
                    await asyncio.sleep(3)
                    self.services[svc]['status'] = 'running'
            await asyncio.sleep(20)

async def main():
    orch = Orchestrator()
    await asyncio.gather(orch.monitor(), orch.anomaly_response())

if __name__ == "__main__":
    asyncio.run(main())

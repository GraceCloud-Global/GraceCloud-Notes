import json, os, datetime, random

MEMORY_DIR = 'ai/memory/nodes'

def store_event(event):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    filename = f'{MEMORY_DIR}/{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json'
    json.dump(event, open(filename, 'w'), indent=2)

def simulate():
    event = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'source': random.choice(['api', 'cognition', 'orchestrator']),
        'signal': random.choice(['info', 'alert', 'update']),
        'value': random.randint(1, 100)
    }
    store_event(event)
    print(f'🧠 Stored distributed memory event from {event["source"]}')

if __name__ == '__main__':
    simulate()

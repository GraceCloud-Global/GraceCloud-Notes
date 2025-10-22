import os, json, datetime

def aggregate():
    base = 'ai/memory/nodes'
    if not os.path.exists(base): return
    events = []
    for f in os.listdir(base):
        path = os.path.join(base, f)
        if f.endswith('.json'):
            events.append(json.load(open(path)))
    merged = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'events': events[-50:],
        'event_count': len(events)
    }
    os.makedirs('ai/memory/global', exist_ok=True)
    json.dump(merged, open('ai/memory/global/state.json', 'w'), indent=2)
    print(f'🪐 Memory grid updated with {len(events)} entries')

if __name__ == '__main__':
    aggregate()

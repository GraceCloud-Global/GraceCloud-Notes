import json, os, datetime, random

REGISTRY = 'ai/federation/registry.json'

def coordinate():
    if not os.path.exists(REGISTRY): return
    data = json.load(open(REGISTRY))
    nodes = data.get('nodes', [])
    active = [n for n in nodes if n['status'] == 'active']
    leader = random.choice(active)['id'] if active else 'none'
    state = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'active_nodes': len(active),
        'leader': leader
    }
    json.dump(state, open('ai/federation/state.json', 'w'), indent=2)
    print(f'🪩 Federation coordination → leader: {leader}')

if __name__ == '__main__':
    coordinate()

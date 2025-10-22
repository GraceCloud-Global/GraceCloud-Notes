import json, datetime, random, os

REGISTRY = 'ai/federation/registry.json'

def register_node():
    os.makedirs('ai/federation', exist_ok=True)
    node = {
        'id': f'node-{random.randint(1000,9999)}',
        'joined': datetime.datetime.utcnow().isoformat(),
        'status': 'active',
        'capabilities': random.sample(['cognition','governance','analytics','insight','predictive'], 3)
    }
    registry = json.load(open(REGISTRY)) if os.path.exists(REGISTRY) else {'nodes': []}
    registry['nodes'].append(node)
    json.dump(registry, open(REGISTRY, 'w'), indent=2)
    print(f'🫧 Node registered → {node["id"]}')

if __name__ == '__main__':
    register_node()

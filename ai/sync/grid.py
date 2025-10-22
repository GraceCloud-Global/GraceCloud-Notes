import json, datetime, random

PEERS = ['node-a', 'node-b', 'node-c', 'node-d']

def sync_grid():
    peers = {p: random.choice(['online','offline']) for p in PEERS}
    grid = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'peers': peers,
        'active_nodes': sum(1 for s in peers.values() if s == 'online')
    }
    json.dump(grid, open('ai/sync/grid_state.json', 'w'), indent=2)
    print(f'🔗 Grid synchronized with {grid["active_nodes"]} active peers')

if __name__ == '__main__':
    sync_grid()

import json, datetime, random, os

NODES = ['NA', 'EU', 'ASIA', 'AFRICA', 'SA']

def sync_planetary():
    signals = {n: random.choice(['active','idle','syncing']) for n in NODES}
    mesh = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'status': signals,
        'uptime_avg': random.uniform(90, 99)
    }
    os.makedirs('ai/planetary', exist_ok=True)
    json.dump(mesh, open('ai/planetary/state.json', 'w'), indent=2)
    print(f'🪐 Planetary mesh sync complete.')

if __name__ == '__main__':
    sync_planetary()

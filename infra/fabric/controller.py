import os, json, datetime, random

STATE = 'infra/fabric/state.json'

def update_fabric():
    clouds = ['Azure', 'AWS', 'Oracle', 'Google']
    nodes = [{ 'cloud': c, 'uptime': random.randint(90, 100), 'load': random.uniform(0.2, 0.8) } for c in clouds]
    status = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'nodes': nodes,
        'average_load': round(sum(n['load'] for n in nodes)/len(nodes), 3)
    }
    os.makedirs('infra/fabric', exist_ok=True)
    json.dump(status, open(STATE, 'w'), indent=2)
    print(f'🌎 Fabric updated: load={status["average_load"]}')

if __name__ == '__main__':
    update_fabric()

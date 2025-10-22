import json, datetime, random, os

STATE = 'ai/collective/state.json'
NODES = ['alpha','beta','gamma','delta','omega']

def collaborate():
    trust_matrix = {a: {b: round(random.uniform(0.4, 1.0),3) for b in NODES if b != a} for a in NODES}
    harmony = sum(sum(v.values()) for v in trust_matrix.values()) / (len(NODES)*(len(NODES)-1))
    data = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'trust_matrix': trust_matrix,
        'harmony_index': round(harmony,3)
    }
    os.makedirs('ai/collective', exist_ok=True)
    json.dump(data, open(STATE, 'w'), indent=2)
    print(f'🌐 Collective harmony={data["harmony_index"]}')

if __name__ == '__main__':
    collaborate()

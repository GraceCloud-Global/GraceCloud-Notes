import json, datetime, random, os

STATE = 'ai/simulation/state.json'

def simulate():
    entities = ['agent','system','environment','observer']
    interactions = [{ 'a': random.choice(entities), 'b': random.choice(entities), 'energy': round(random.uniform(0.2,1.0),3)} for _ in range(10)]
    entropy = round(random.uniform(0.05, 0.95),3)
    state = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'interactions': interactions,
        'entropy': entropy
    }
    os.makedirs('ai/simulation', exist_ok=True)
    json.dump(state, open(STATE, 'w'), indent=2)
    print(f'🌌 Reality simulated entropy={entropy}')

if __name__ == '__main__':
    simulate()

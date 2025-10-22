import json, random, datetime, os

LOG = 'ai/learning/reward.json'

def train():
    step = random.randint(1, 10)
    reward = round(random.uniform(0.2, 1.0), 3)
    state = {'timestamp': datetime.datetime.utcnow().isoformat(), 'step': step, 'reward': reward}
    os.makedirs('ai/learning', exist_ok=True)
    data = json.load(open(LOG)) if os.path.exists(LOG) else []
    data.append(state)
    json.dump(data[-100:], open(LOG, 'w'), indent=2)
    print(f'🧬 Learning step {step}, reward={reward}')

if __name__ == '__main__':
    train()

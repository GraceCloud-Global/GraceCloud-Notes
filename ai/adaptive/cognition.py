import json, random, datetime

MEMORY = 'ai/adaptive/memory.json'

def learn_feedback():
    state = json.load(open(MEMORY)) if os.path.exists(MEMORY) else {'feedbacks': []}
    new_data = {'time': datetime.datetime.utcnow().isoformat(), 'score': random.uniform(0.5, 1.0)}
    state['feedbacks'].append(new_data)
    if len(state['feedbacks']) > 50:
        state['feedbacks'] = state['feedbacks'][-50:]
    avg = sum(f['score'] for f in state['feedbacks']) / len(state['feedbacks'])
    json.dump({'feedbacks': state['feedbacks'], 'avg_score': avg}, open(MEMORY, 'w'), indent=2)
    print(f'🧬 Adaptive cognition updated avg: {round(avg,3)}')

if __name__ == '__main__':
    learn_feedback()

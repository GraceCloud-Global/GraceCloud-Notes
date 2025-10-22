import json, random, datetime, os

def awareness_cycle():
    mem = json.load(open('ai/memory/global/state.json')) if os.path.exists('ai/memory/global/state.json') else {}
    count = mem.get('event_count', 0)
    status = 'alert' if count > 100 else 'stable'
    level = random.uniform(0.1, 0.9)
    state = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'awareness_state': status,
        'sensitivity': round(level, 3),
        'context': random.choice(['governance', 'orchestration', 'finance', 'education'])
    }
    json.dump(state, open('ai/awareness/state.json', 'w'), indent=2)
    print(f'🌐 Awareness {status} @ sensitivity {level}')

if __name__ == '__main__':
    awareness_cycle()

import json, random, datetime

STATE = 'ai/orchestrator/state.json'
LOG = 'ai/selfheal/events.json'

def heal():
    if not os.path.exists(STATE): return
    state = json.load(open(STATE))
    events = []
    for svc, st in state['status'].items():
        if st != 'running' and random.random() < 0.8:
            state['status'][svc] = 'restarted'
            events.append({'time': datetime.datetime.utcnow().isoformat(), 'svc': svc, 'action': 'restarted'})
    json.dump(state, open(STATE, 'w'), indent=2)
    if events:
        old = json.load(open(LOG)) if os.path.exists(LOG) else []
        old.extend(events)
        json.dump(old, open(LOG, 'w'), indent=2)
        print(f'🩺 Self-heal executed for {len(events)} service(s)')

if __name__ == "__main__":
    heal()

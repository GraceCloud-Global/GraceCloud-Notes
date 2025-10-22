import json, random, datetime

NODES = ['alpha', 'beta', 'gamma', 'delta']

def run_consensus():
    votes = {n: random.choice(['yes','no']) for n in NODES}
    yes = sum(1 for v in votes.values() if v == 'yes')
    decision = 'APPROVED' if yes >= len(NODES)//2 + 1 else 'REJECTED'
    state = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'votes': votes,
        'result': decision
    }
    open('ai/consensus/state.json', 'w').write(json.dumps(state, indent=2))
    print(f'🗳️ Consensus result: {decision}')

if __name__ == '__main__':
    run_consensus()

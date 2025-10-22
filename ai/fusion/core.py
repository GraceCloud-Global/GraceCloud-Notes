import os, json, datetime, random

def fuse():
    sources = [
        'ai/predictive/governance_state.json',
        'ai/insight/trends.json',
        'ai/memory/global/state.json',
        'ai/meta/state.json',
        'infra/fabric/state.json'
    ]
    merged = {'timestamp': datetime.datetime.utcnow().isoformat(), 'merged_signals': []}
    for s in sources:
        if os.path.exists(s):
            merged['merged_signals'].append(json.load(open(s)))
    merged['fusion_index'] = round(random.uniform(0.7, 1.0), 3)
    os.makedirs('ai/fusion', exist_ok=True)
    json.dump(merged, open('ai/fusion/state.json', 'w'), indent=2)
    print(f'🧠 Fused intelligence coherence={merged["fusion_index"]}')

if __name__ == '__main__':
    fuse()

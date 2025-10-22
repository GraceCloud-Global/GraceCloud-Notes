import os, json, datetime, random

NODES = ['US-EAST', 'US-WEST', 'EU-CENTRAL', 'ASIA-PAC', 'AFRICA-NORTH']

def aggregate_network():
    metrics = {n: {'uptime': random.uniform(95, 100), 'latency': random.uniform(10, 150)} for n in NODES}
    state = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'nodes': metrics,
        'global_health': round(sum(v['uptime'] for v in metrics.values()) / len(metrics), 2)
    }
    os.makedirs('ai/sentience', exist_ok=True)
    json.dump(state, open('ai/sentience/network.json', 'w'), indent=2)
    print(f'🌍 Sentient network aggregated @ health={state["global_health"]}')

if __name__ == '__main__':
    aggregate_network()

import json, datetime, random, os

LOG = 'infra/autoscaler/log.json'

def auto_scale():
    metric = random.uniform(0.3, 1.0)
    decision = 'scale_up' if metric > 0.8 else 'scale_down' if metric < 0.4 else 'stable'
    log = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'cpu_metric': round(metric, 3),
        'decision': decision
    }
    os.makedirs('infra/autoscaler', exist_ok=True)
    history = json.load(open(LOG)) if os.path.exists(LOG) else []
    history.append(log)
    json.dump(history[-50:], open(LOG, 'w'), indent=2)
    print(f'⚙️ Autoscaler decision: {decision}')

if __name__ == '__main__':
    auto_scale()

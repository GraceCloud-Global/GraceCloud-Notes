import json, datetime, random, math

def analyze():
    trends = []
    for i in range(10):
        value = round(math.sin(i/2) + random.random()*0.5, 3)
        trends.append({'t': i, 'value': value})
    result = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'trend_points': trends,
        'growth_direction': 'up' if trends[-1]['value'] > trends[0]['value'] else 'down'
    }
    json.dump(result, open('ai/insight/trends.json', 'w'), indent=2)
    print(f'📈 Insight generated: {result["growth_direction"]}')

if __name__ == '__main__':
    analyze()

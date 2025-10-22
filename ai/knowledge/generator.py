import json, datetime, random, os

STATE = 'ai/knowledge/state.json'
TOPICS = ['behavior','learning','therapy','systems','ethics','growth','data']

def generate_knowledge():
    insights = [{ 'topic': t, 'confidence': round(random.uniform(0.7,1.0),3) } for t in TOPICS]
    avg = round(sum(i['confidence'] for i in insights)/len(insights),3)
    data = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'insights': insights,
        'knowledge_strength': avg
    }
    os.makedirs('ai/knowledge', exist_ok=True)
    json.dump(data, open(STATE,'w'), indent=2)
    print(f'📘 Knowledge generated avg_strength={avg}')

if __name__ == '__main__':
    generate_knowledge()

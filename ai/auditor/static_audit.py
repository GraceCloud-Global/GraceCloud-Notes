import os, re, json, datetime

def scan_code(base='backend'):
    results = []
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith('.py'):
                content = open(os.path.join(root, f), encoding='utf8').read()
                if 'eval(' in content or 'exec(' in content:
                    results.append({'file': f, 'issue': 'Use of eval/exec'})
                if 'password' in content.lower():
                    results.append({'file': f, 'issue': 'Hardcoded password string'})
    output = {'time': datetime.datetime.utcnow().isoformat(), 'findings': results}
    os.makedirs('ai/auditor/reports', exist_ok=True)
    with open(f'ai/auditor/reports/audit_{datetime.datetime.now().strftime("%H%M")}.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f'✅ Code audit found {len(results)} issues.')

if __name__ == "__main__":
    scan_code()

import yaml, json, datetime

def validate(config_path='datalake/policy.json', rule_path='ai/governance/rules.yaml'):
    with open(rule_path) as f:
        rules = yaml.safe_load(f)
    with open(config_path) as f:
        cfg = json.load(f)
    report = []
    for rule in rules['rules']:
        key_path = rule['condition'].split('==')[0].strip().replace('.', '/')
        parts = key_path.split('/')
        node = cfg
        for p in parts[:-1]:
            node = node.get(p, {})
        key = parts[-1]
        actual = node.get(key)
        expected = rule['condition'].split('==')[1].strip().replace('true', 'True')
        passed = str(actual) == expected
        report.append({'rule': rule['name'], 'passed': passed})
    out = {'timestamp': datetime.datetime.utcnow().isoformat(), 'results': report}
    open('ai/governance/validation_report.json', 'w').write(json.dumps(out, indent=2))
    print('✅ Governance validation done.')

if __name__ == "__main__":
    validate()

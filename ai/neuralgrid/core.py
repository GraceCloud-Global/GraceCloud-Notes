import os, json, datetime, random, math

GRID_FILE = 'ai/neuralgrid/state.json'

def build_grid():
    layers = []
    for i in range(5):
        layer = {
            'layer': i + 1,
            'nodes': [{'id': f'N{i}{j}', 'activation': round(math.sin(j+i) + random.random(), 3)} for j in range(5)]
        }
        layers.append(layer)
    grid = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'layers': layers,
        'entropy': round(random.uniform(0.1, 0.9), 3)
    }
    os.makedirs('ai/neuralgrid', exist_ok=True)
    json.dump(grid, open(GRID_FILE, 'w'), indent=2)
    print(f'🔺 Neural lattice updated entropy={grid["entropy"]}')

if __name__ == '__main__':
    build_grid()

from fastapi import FastAPI
import json, os

app = FastAPI(title='Global Control Tower')

@app.get('/fabric/status')
def get_fabric():
    path = 'infra/fabric/state.json'
    if not os.path.exists(path): return {'error':'no data'}
    return json.load(open(path))

@app.get('/autoscaler/logs')
def get_scaler():
    path = 'infra/autoscaler/log.json'
    if not os.path.exists(path): return {'error':'no data'}
    return json.load(open(path))

@app.post('/fabric/update')
def trigger_update():
    os.system('python infra/fabric/controller.py')
    os.system('python infra/autoscaler/brain.py')
    return {'status': 'triggered'}

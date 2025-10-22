from fastapi import FastAPI
import psutil, datetime

app = FastAPI()

@app.get('/status')
def status():
    return {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'uptime': int(datetime.datetime.now().timestamp() - psutil.boot_time()),
        'services': ['api', 'redis', 'postgres', 'celery', 'gateway']
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8010)

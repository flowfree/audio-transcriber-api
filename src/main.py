from fastapi import FastAPI
from fastapi import HTTPException
from .tasks import celery, long_running_task

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello, World!'}


@app.post('/tasks')
async def create_task(number: int):
    task = long_running_task.delay(number)
    return {
        'task_id': task.id,
        'status': f'http localhost:3000/tasks/{task.id}'
    }


@app.get('/tasks/{task_id}')
async def get_task_result(task_id: str):
    task = celery.AsyncResult(task_id)
    if task.ready():
        return {'result': task.get()}
    elif task.state == 'PENDING':
        print(task.state)
        raise HTTPException(status_code=404, detail='Task not found')
    else:
        return {'status': 'in_progress'}

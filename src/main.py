import pathlib 
import tempfile
import os 

from fastapi import FastAPI, UploadFile

from .tasks import (
    celery, 
    transcribe_from_file
)


app = FastAPI()


@app.get('/ping')
def ping():
    return {'message': 'API is up and running.'}


@app.post('/transcribe')
async def transcribe(audio: UploadFile):
    ext = pathlib.Path(audio.filename).suffix
    _, filepath = tempfile.mkstemp(dir='/tmp', suffix=ext)
    with open(filepath, 'wb') as f:
        f.write(audio.file.read())

    task = transcribe_from_file.delay(filepath)
    return {'taskId': task.id}


@app.get('/transcribe/{task_id}')
async def get_task_result(task_id: str):
    task = celery.AsyncResult(task_id)
    if task.ready():
        return {'status': 'DONE', 'result': task.get()}
    else:
        return {'status': 'IN_PROGRESS'}

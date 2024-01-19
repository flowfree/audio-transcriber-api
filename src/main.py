import pathlib 
import tempfile

from fastapi import FastAPI, UploadFile
from .tasks import celery, long_running_task

app = FastAPI()


@app.post('/transcribe')
async def transcribe(audio: UploadFile):
    ext = pathlib.Path(audio.filename).suffix
    with tempfile.NamedTemporaryFile(suffix=ext) as tmp_file:
        tmp_file.write(audio.file.read())
        # Do something with the tmp_file

    return {'task_id': '12345'}


@app.get('/ping')
def ping():
    return {'message': 'API is up and running.'}


# @app.post('/tasks')
# async def create_task(number: float):
#     task = long_running_task.delay(number)
#     return {'task_id': task.id}
#
# @app.get('/tasks/{task_id}')
# async def get_task_result(task_id: str):
#     task = celery.AsyncResult(task_id)
#     if task.ready():
#         return {'status': 'DONE', 'result': task.get()}
#     else:
#         return {'status': 'IN_PROGRESS'}

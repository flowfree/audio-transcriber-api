import pathlib 
import tempfile

from fastapi import FastAPI, UploadFile, Form
from fastapi import HTTPException

from .tasks import (
    celery, 
    transcribe_from_file,
    transcribe_from_url,
    TaskException
)


app = FastAPI()


@app.post('/transcribe')
async def transcribe(audio: UploadFile = None, url: str = Form(None)):
    if audio and url:
        raise HTTPException(
            status_code=400, 
            detail='Please provide either a file upload or a URL, not both.'
        )

    if audio is None and url is None:
        raise HTTPException(
            status_code=400, 
            detail='Please provide either a file upload or a URL.'
        )
    
    if audio:
        # Save into a temporary file
        ext = pathlib.Path(audio.filename).suffix
        _, filepath = tempfile.mkstemp(dir='/tmp', suffix=ext)
        with open(filepath, 'wb') as f:
            f.write(audio.file.read())

        try:
            # Transcribe from the local file
            # Note that the function is responsible for deleting the file later
            task = transcribe_from_file.delay(filepath)
        except TaskException as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    if url:
        try:
            task = transcribe_from_url.delay(url)
        except TaskException as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {'taskId': task.id}


@app.get('/transcribe/{task_id}')
async def transcribe(task_id: str):
    task = celery.AsyncResult(task_id)
    if task.ready():
        return {'status': 'DONE', 'result': task.get()}
    else:
        return {'status': 'IN_PROGRESS'}


@app.get('/ping')
def ping():
    return {'message': 'API is up and running.'}

import pathlib 
import tempfile

from fastapi import FastAPI, UploadFile, Form
from fastapi import HTTPException
import requests

from .tasks import (
    celery, 
    transcribe_from_file
)


app = FastAPI()


@app.get('/ping')
def ping():
    return {'message': 'API is up and running.'}


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
        # Save the uploaded file
        ext = pathlib.Path(audio.filename).suffix
        _, filepath = tempfile.mkstemp(dir='/tmp', suffix=ext)
        with open(filepath, 'wb') as f:
            f.write(audio.file.read())
    
    if url:
        # Download the file from the URL
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise HTTPException(
                status_code=400, 
                detail='Failed to retrieve file from the provided URL.'
            )

        # Extract the file suffix from the Content-Type header
        try:
            content_type = response.headers.get('Content-Type')
            ext = get_file_extension(content_type)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Save the file to a temporary location
        _, filepath = tempfile.mkstemp(dir='/tmp', suffix=ext)
        with open(filepath, 'wb') as f:
            f.write(response.content)

    task = transcribe_from_file.delay(filepath)
    return {'taskId': task.id}


@app.get('/transcribe/{task_id}')
async def transcribe(task_id: str):
    task = celery.AsyncResult(task_id)
    if task.ready():
        return {'status': 'DONE', 'result': task.get()}
    else:
        return {'status': 'IN_PROGRESS'}


def get_file_extension(content_type): 
    content_types = {
        'audio/flac': 'flac',
        'audio/mpeg': 'mp3',
        'audio/mp4': 'mp4',
        'audio/mpegurl': 'mpeg',
        'audio/mpeg3': 'mpga',
        'audio/x-m4a': 'm4a',
        'audio/ogg': 'ogg',
        'audio/wav': 'wav',
        'audio/webm': 'webm'
    }
    if content_type in content_types:
        return content_types[content_type]
    else:
        raise ValueError(f'Unsupported file format: {content_type}')

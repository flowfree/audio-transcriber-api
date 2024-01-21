import tempfile
import os

from celery import Celery
import requests
import whisper


celery = Celery(
    'tasks', 
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


class TaskException(Exception):
    pass


@celery.task
def transcribe_from_file(filepath: str):
    model = whisper.load_model('base')
    result = model.transcribe(filepath)

    if 'segments' in result:
        for segment in result['segments']:
            required_keys = ['id', 'start', 'end', 'text']
            for key in [k for k in segment.keys() if k not in required_keys]:
                del segment[key]

    try:
        os.remove(filepath)
    except Exception:
        pass

    return result


@celery.task
def transcribe_from_url(url: str):
    try:
        # Download the file from the URL
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise TaskException('Failed to retrieve file from the provided URL.')

    try:
        # Get the suffix extension of the remote file
        content_type = response.headers.get('Content-Type')
        ext = get_file_extension(content_type)
    except ValueError as e:
        raise TaskException(str(e))

    # Save the file to a temporary location
    _, filepath = tempfile.mkstemp(dir='/tmp', suffix=ext)
    with open(filepath, 'wb') as f:
        f.write(response.content)

    return transcribe_from_file(filepath)


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


@celery.task
def square_root(number: float):
    import math
    return round(math.sqrt(number), 4)

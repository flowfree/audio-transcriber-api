import os

from celery import Celery
import whisper


celery = Celery(
    'tasks', 
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


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
def square_root(number: float):
    import math
    return round(math.sqrt(number), 4)

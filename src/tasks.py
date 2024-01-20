# import whisper
# model = whisper.load_model('base')
# result = model.transcribe('samples/alloy.wav')
# print(result)

import time
import math
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
    os.remove(filepath)
    return result


@celery.task
def square_root(number: float):
    return round(math.sqrt(number), 4)

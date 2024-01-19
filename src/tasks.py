# import whisper
# model = whisper.load_model('base')
# result = model.transcribe('samples/alloy.wav')
# print(result)


from celery import Celery
import time
import math

celery = Celery(
    'tasks', 
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery.task
def square_root(number: float):
    return round(math.sqrt(number), 4)


def transcribe_from_file(filepath: str):
    pass

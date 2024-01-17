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
def long_running_task(number: int):
    time.sleep(10) 
    return math.sqrt(number)

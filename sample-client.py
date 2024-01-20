import time
import logging
import sys

import requests

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


filepath = 'samples/echo.wav'
logging.info(f'Audio file = {filepath}')

with open(filepath, 'rb') as f:
    r = requests.post('http://localhost:3000/transcribe_from_file', files={'audio': f})
    if r.status_code != 200:
        logging.error(f'Status code = {r.status_code}')
        sys.exit(1)

task_id = r.json()['taskId']
logging.info(f'Task ID = {task_id}')

while True:
    time.sleep(1)
    r = requests.get(f'http://localhost:3000/status/{task_id}')
    status = r.json()['status']
    if status == 'DONE':
        logging.info(f'Result = {r.json()["result"]}')
        break
    logging.info(f'Status = {status}')

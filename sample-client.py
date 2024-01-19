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

logging.info('hello world')

r = requests.post('http://localhost:3000/tasks?number=9.1')
task_id = r.json()['task_id']
logging.info(f'Task ID = {task_id}')

while True:
    time.sleep(1)
    r = requests.get(f'http://localhost:3000/tasks/{task_id}')
    status = r.json()['status']
    if status == 'DONE':
        logging.info(f'Result = {r.json()["result"]}')
        break
    logging.info(f'Status = {status}')

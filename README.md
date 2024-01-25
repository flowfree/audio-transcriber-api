Audio Transcriber API
=====================
Transcribe audio from URL or upload from local disk.


## Running on develoment machine
Make sure you have Python and Redis installed on your system. After cloning this repo, follow these steps.

1.  Create and activate virtual env:

        python -m venv venv
        . venv/bin/activate

1.  Install the dependencies:

        pip install -r requirements.txt 

1.  Run the development server:

        uvicorn src.main:app --reload

1.  Open another terminal and activate the virtual env as well:

        . venv/bin/activate

1.  Run the celery task:

        celery -A src.tasks --loglevel=info

Once the API is up and running, you can transcribe your audio files e.g:

```python 
import time
import sys
import requests 

with open('/path/to/audio.wav', 'rb') as f:
    r = requests.post('http://localhost:8000/transcribe', files={'audio': f})
    if r.status_code != 200:
        print(f'Error = {r.status_code}, Body = {r.json()}')
        sys.exit(1)

task_id = r.json()['taskId']
while True:
    time.sleep(1)
    r = requests.get(f'http://localhost:8000/transcribe/{task_id}')
    status = r.json()['status']
    if status == 'DONE':
        result = r.json()['result']
        break
    print(f'Status = {status}')

print(f'Result = {result]}')
```


## Run with Docker
If you have Docker installed on your machine, you can run the API using a single command:

    docker compose up

The API will be running and accepting requests on port 8000.


## License
MIT

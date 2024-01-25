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

    It will run on `localhost` and accepting requests on port 8000.

1.  Open another terminal and activate the virtual env as well:

        . venv/bin/activate

1.  Run the celery task:

        celery -A src.tasks --loglevel=info

Once the API is up and running, you can transcribe your audio files e.g:

```python 
import time
import requests 

API_URL = 'http://localhost:8000'

# Upload audio file
with open('/path/to/audio.wav', 'rb') as f:
    r = requests.post(f'{API_URL}/transcribe', files={'audio': f})
    r.raise_for_status()

# Check the status and retrieve the transcriptin
task_id = r.json()['taskId']
while True:
    r = requests.get(f'{API_URL}/transcribe/{task_id}')
    status = r.json()['status']
    print(f'Status = {status}')
    if status == 'DONE':
        break
    time.sleep(1)

print('Result = ', r.json()['result'])
```


## Run with Docker
If you have Docker installed on your machine, you can run the API using a single command:

    docker compose up

The API will be running and accepting requests on port 8000.


## Documentation
FastAPI automatically generate the documentation for the API, you can access the docs at `http://localhost:8000/docs`.


## License
MIT

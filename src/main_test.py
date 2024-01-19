import os
import pytest
from fastapi.testclient import TestClient
from .main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'message': 'API is up and running.'}


# def test_transcribe_endpoint(client):
#     audio_file_path = os.path.join(os.path.dirname(__file__), 'test_audio.wav')
#     with open(audio_file_path, 'rb') as audio_file:
#         response = client.post('/transcribe', files={'audio': audio_file})
#         assert response.status_code == 200
#         assert 'task_id' in response.json()

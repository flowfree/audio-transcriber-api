from unittest.mock import patch, MagicMock
import os

import pytest
from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


def test_ping():
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'message': 'API is up and running.'}


@patch('src.main.transcribe_from_file')
def test_transcribe_by_upload(mock_transcribe_from_file):
    mock_task_id = 'mocked_task_id'
    mock_transcribe_from_file.delay.return_value = MagicMock(id=mock_task_id)

    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, 'samples/alloy.wav')

    with open(file_path, 'rb') as audio_file:
        response = client.post('/transcribe', files={'audio': audio_file})

    assert response.status_code == 200
    assert response.json() == {'taskId': mock_task_id}
    assert mock_transcribe_from_file.delay.call_count == 1


@patch('src.main.transcribe_from_url')
def test_transcribe_by_url(mock_transcribe_from_url):
    mock_task_id = 'mocked_task_id'
    mock_transcribe_from_url.delay.return_value = MagicMock(id=mock_task_id)

    response = client.post('/transcribe', data={'url': 'http://example.com/test.wav'})

    assert response.status_code == 200
    assert response.json() == {'taskId': mock_task_id}
    assert mock_transcribe_from_url.delay.call_count == 1

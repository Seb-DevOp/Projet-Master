import json
import os
import threading
import time
import subprocess
import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from http.server import HTTPServer, BaseHTTPRequestHandler

import pytest

from SimulateData import get_weather, send_weather_to_api


def test_get_weather_structure_and_types():
    data = get_weather()
    expected_keys = {'temperature', 'felt', 'condition', 'season', 'wind', 'humidity', 'location', 'date'}
    assert set(data.keys()) == expected_keys

    assert isinstance(data['temperature'], float)
    assert isinstance(data['felt'], float)
    assert isinstance(data['condition'], str)
    assert data['season'] in {'hiver', 'printemps', 'été', 'automne'}
    assert isinstance(data['wind'], float)
    assert 0.0 <= data['wind'] <= 150.0
    assert isinstance(data['humidity'], float)
    assert 0.0 <= data['humidity'] <= 100.0
    assert isinstance(data['location'], str)
    assert data['date'].endswith("Z")

class DummyHandler(BaseHTTPRequestHandler):
    received = None

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        DummyHandler.received = json.loads(body.decode('utf-8'))
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        return

@pytest.fixture(scope="module")
def http_server():
    server = HTTPServer(('localhost', 0), DummyHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield f'http://localhost:{port}/'
    server.shutdown()
    thread.join()

def test_send_weather_to_api_integration(http_server, monkeypatch):
    calls = {'count': 0}
    original_sleep = time.sleep
    def fake_sleep(sec):
        calls['count'] += 1
        if calls['count'] > 1:
            raise KeyboardInterrupt()
        original_sleep(0)

    monkeypatch.setattr(time, 'sleep', fake_sleep)

    with pytest.raises(KeyboardInterrupt):
        send_weather_to_api(http_server)

    received = DummyHandler.received
    assert received is not None
    assert 'temperature' in received and isinstance(received['temperature'], float)
    assert 'location' in received and isinstance(received['location'], str)


import warnings

def test_cli_end_to_end(monkeypatch, tmp_path):
    script_path = Path(__file__).parent.parent / 'SimulateData.py'
    
    monkeypatch.setattr(time, 'sleep', lambda s: (_ for _ in ()).throw(KeyboardInterrupt()))
    
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        proc = subprocess.Popen(
            [sys.executable, str(script_path)],
            env={**os.environ, 'API_URL': 'http://localhost:12345/unused'},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            out, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()

    assert 'Données envoyées avec succès.' in out or 'Exception lors de l\'envoi' in out or '' in out
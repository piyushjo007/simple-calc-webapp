import pytest
from unittest.mock import patch, MagicMock
mock_func = MagicMock()
import main

main.READY = True
@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        yield client

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"

def test_startup_before_ready(client):
    main.READY = False
    resp = client.get("/startup")
    assert resp.status_code == 503
    assert resp.json["status"] == "starting"

def test_startup_after_ready(client):
    with patch("main.init_app",mock_func): 
        main.READY = True
        resp = client.get("/startup")
        assert resp.status_code == 200
        assert resp.json["status"] == "started"

def test_live_probe(client):
    resp = client.get("/live")
    assert resp.status_code == 200
    assert resp.json["status"] == "alive"

def test_ready_probe(client):
    main.READY = True
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json["status"] == "ready"

def test_not_ready_probe(client):
    main.READY = False
    resp = client.get("/ready")
    assert resp.status_code == 503
    assert resp.json["status"] == "not ready"


def test_user_gists(client):
     resp = client.get("/octocat")
     data=resp.json
     assert resp.status_code == 200
     assert data[0]["owner"]["id"] == 583231
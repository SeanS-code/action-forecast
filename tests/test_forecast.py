from fastapi.testclient import TestClient
from forecast.forecastapi import app

client = TestClient(app)

def test_hello_world():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World!"}

def test_good_bye():
    response = client.get("/bye")
    assert response.status_code == 200
    assert response.json() == {"Good": "Bye"}

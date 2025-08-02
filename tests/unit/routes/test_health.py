from fastapi.testclient import TestClient
from fastapi import FastAPI
from tevye_openai_api.app.routes.health import router
from tevye_openai_api.app.main import app


app.include_router(router)

client = TestClient(app)


def test_live():
    response = client.get("/live")
    assert response.status_code == 200
    assert response.json() == {'message': 'Tevye OpenAI API is live!'}


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {'message': 'Tevye OpenAI API is ready!'}

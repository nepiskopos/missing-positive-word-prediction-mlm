from fastapi.testclient import TestClient
from service.main import app

client = TestClient(app)

def test_predict():
    response = client.post(url="/api/predict_single", content="I wish you have a <blank> day", headers={"accept": "application/json", "Content-Type": "text/plain"})
    assert response.status_code == 200
    assert response.json()['content']

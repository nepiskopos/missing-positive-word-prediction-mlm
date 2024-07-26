import time
from locust import HttpUser, task, between

text = "Ireland is known for its wide expanses of <blank>, green fields."

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def predict(self):
        self.client.post("/predict", data=text, headers={"accept": "application/json", "Content-Type": "text/plain"})

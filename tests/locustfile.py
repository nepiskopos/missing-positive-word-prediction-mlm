from locust import HttpUser, task, between
import time

text = "I wish you have a <blank> day"

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def predict(self):
        self.client.post("/api/predict_single", data=text, headers={"accept": "application/json", "Content-Type": "text/plain"})

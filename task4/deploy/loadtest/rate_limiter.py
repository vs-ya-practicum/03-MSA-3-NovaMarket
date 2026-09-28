from locust import HttpUser, constant, task


class WebUser(HttpUser):
    wait_time = constant(0)

    @task
    def request_api(self):
        self.client.get("/api/", name="/api/web", headers={"Client-Type": "web"})

class MobileUser(HttpUser):
    wait_time = constant(0)

    @task
    def request_api(self):
        self.client.get("/api/", name="/api/mobile", headers={"Client-Type": "mobile"})

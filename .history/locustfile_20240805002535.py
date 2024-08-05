from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_admin(self):
        self.client.get("/admin/")

    # @task
    # def load_about(self):
    #     self.client.get("/about/")

    # @task
    # def load_contact(self):
    #     self.client.get("/contact/")

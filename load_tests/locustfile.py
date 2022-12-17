import os
import random

from locust import HttpUser, task


class TestUser(HttpUser):
    random_files_list = list(os.listdir('random_images'))

    def on_start(self):
        try:
            res = self.client.post("/login", data={"username": "admin", "password": "admin"})
            if res.status_code == 200:
                self._user_login = True
                self.client.headers = {'Authorization': f'Bearer {res.json()["access_token"]}'}

            self.client.get(f"/time")
        except:
            pass

    @task(10)
    def get_prime_number(self):
        self.client.get(f"/prime/{int(round(random.random(), 1) * 922337203685477580) + 1}")

    @task(5)
    def post_img(self):
        with open(f'random_images/{random.choice(self.random_files_list)}', 'rb') as image:
            self.client.post(
                "/picture/invert",
                files={'file': image}
            )


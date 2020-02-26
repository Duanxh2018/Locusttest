# coding=utf-8
import json

import requests
from locust import HttpLocust,TaskSet,task
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Login(TaskSet):
    # 登录请求
    @task(1)
    def Login(self):
        # 定义请求头
        headers = {'Content-Type': 'application/json'}
        data ={
            "unionId": "o37ZAwT-U09TGxf9sxs9CKfVMkTE"
        }
        req = self.client.post("/auth/wx/login", data=json.dumps(data),headers=headers, verify=False)

        if req.status_code == 200 and req.json()["data"]["userInfo"]['uid'] == "2c9195166e7366bc016e7e25a68e0008":

            print("Success")
        else:
            print("Failed")
        # assert req.json()["data"]["userInfo"]['uid'] == "2c91558b6dce40a5016dce7a77fb0003"
        # if req.status_code == 200:
        #     print("success")
        # else:
        #     print("fails")

class websitUser(HttpLocust):
    task_set = Login
    min_wait = 2000  # 单位为毫秒
    max_wait = 5000  # 单位为毫秒

if __name__ == "__main__":
    import os
    os.system("locust -f milinZone-Login.py --host=https://api.milinzone.com")
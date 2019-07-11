import json
# import time

from locust import HttpLocust,TaskSet,task

# f = open('./timegetaccount.txt', 'w')

class UserBehavior(TaskSet):
    @task(1)
    def Getaccount(self):
        # starttime = time.time ()
        url = 'http://192.168.1.13:8089'
        header = {'Content-Type': 'application/json'}
        data = {
            "method": "GetAccount",
            "params": {"chainId": "2", "address": "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23"}
        }
        req = self.client.post(url=url, headers=header, data=json.dumps(data).encode(encoding='UTF8'))
        if req.status_code == 200:
            print("success")
        else:
            print("fails")
        # print(time.time() - starttime, file=f)

class websitUser (HttpLocust):
    task_set = UserBehavior
    host = 'http://192.168.1.13:8089'
    min_wait = 0  # 单位为毫秒
    max_wait = 1  # 单位为毫秒
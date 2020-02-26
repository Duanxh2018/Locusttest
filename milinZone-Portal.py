# coding=utf-8
import json
import queue

import requests
from locust import HttpLocust,TaskSet,task
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Login(TaskSet):
    # 登录请求
    @task(1)
    def portal(self):
        # 获取队列里的数据
        # try:
        # requestId = self.locust.requestId_queue.get()
        # # 取出数据后放于队列尾部，循环使用
        # self.locust.requestId_queue.put_nowait(requestId)
        # print(requestId)
        # 队列取空后，直接退出
        # except queue.Empty:
        #     print('no data exist')
        #     exit(0)
        # 定义请求头
        requestId = range(50)
        headers = {'Content-Type': 'application/json'}
        data ={
            "address": {
            "adCode": "110106",
            "address": "北京市丰台区南苑西路62靠近新宫家园北区",
            "city": "北京市",
            "cityCode": "",
            "code": "010",
            "country": "中国",
            "countryCode": "",
            "createTime": "",
            "details": "#csid:2fe47318187f453989ca11d2e838242b",
            "district": "丰台区",
            "id": "",
            "latitude": "39.814718",
            "longitude": "116.361845",
            "name": "",
            "parentId": "",
            "poiId": "1571289312420",
            "poiName": "新宫家园北区",
            "province": "北京市",
            "provinceCode": "",
            "street": "南苑西路",
            "townCode": "",
            "township": "",
            "typeCode": "5",
            "upTime": ""
                    },
            "pageNum": 1,
            "pageSize": 10,
            "requestId": "requestId"
        }
        req = self.client.post("/feeds/video/portal", data=json.dumps(data),headers=headers, verify=False)
        # print(req.content.decode('utf-8'))
        if req.status_code == 200 and req.json()["message"] =="success":
            print("success")
        else:
            print("fails")

class websitUser(HttpLocust):
    task_set = Login
    min_wait = 2000  # 单位为毫秒
    max_wait = 5000  # 单位为毫秒
    # requestId_queue = queue.Queue()
    # for reqId in range(2000):
    #     requestId = reqId + 1
    #     requestId_queue.put_nowait(requestId)

if __name__ == "__main__":
    import os
    os.system("locust -f milinZone-Portal.py --host=https://api.milinzone.com")
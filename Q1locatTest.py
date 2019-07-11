from locust import HttpLocust, TaskSet, task
# coding:utf-8
from collections import Mapping
import requests
from web3 import Web3, HTTPProvider
from locust import HttpLocust,TaskSet,task
import json
import time
from web3._utils.encoding import (
    remove_0x_prefix, to_bytes, to_hex
)
from eth_utils import keccak as eth_utils_keccak

from eth_keys import (
    keys
)

fromaddress = "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23"

def signTransaction(transaction_dict, private_key):
    FULL_NODE_HOSTS = 'http://192.168.1.13:8089'

    provider = HTTPProvider (FULL_NODE_HOSTS)
    web3 = Web3 (provider)
    if not isinstance(transaction_dict, Mapping):
        raise TypeError("transaction_dict must be dict-like, got %r" % transaction_dict)
    sign_str = transaction_dict["chainId"] + remove_0x_prefix(transaction_dict["from"].lower()) + \
               remove_0x_prefix(transaction_dict["to"].lower()) + transaction_dict["nonce"] + \
               transaction_dict["value"] + remove_0x_prefix(transaction_dict["input"].lower())
    sign_bytes = to_bytes(text=sign_str)
    res = eth_utils_keccak(sign_bytes)
    sign_hash = web3.eth.account.signHash(to_hex(res), private_key=private_key)

    transaction_dict["sig"] = to_hex(sign_hash.signature)
    pk = keys.PrivateKey(private_key)
    transaction_dict["pub"] = "0x04" + pk.public_key.to_hex()[2:]
    return transaction_dict

# 定义用户行为，继承TaskSet类，用于描述用户行为
# (这个类下面放各种请求，请求是基于requests的，每个方法请求和requests差不多，请求参数、方法、响应对象和requests一样的使用，url这里写的是路径)
# client.get===>requests.get
# client.post===>requests.post
class UserBehavior(TaskSet):
    '''用户行为描述'''
    def Getnonceid(self,fromaddress):
        nonceid = 0
        s = requests.session()
        s.keep_alive = False
        url = 'http://192.168.1.13:8089'
        # path = ""
        headers = {'Content-Type': 'application/json'}
        # self.client.headers.update(headers)
        data = {
            "method": "GetAccount",
            "params": {"chainId": "2", "address": fromaddress}
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(data).encode(encoding='UTF8'))
        print(response)
        try:
            resp = json.loads(response.content.decode())
            nonceid = resp["nonce"]
            print(nonceid)
        except:
            print("账户地址nonce获取失败！")
        return nonceid

    @task(1)
    def TestTransfer(self):
        starttime = time.time()
        nonceid = self.Getnonceid(fromaddress)
        s = requests.session()
        s.keep_alive = False
        url = 'http://192.168.1.13:8089'
        headers = {'Content-Type': 'application/json'}
        for i in range(10000):
            con_tx = {
                "chainId": "2",
                "fromChainId": "2",
                "toChainId": "2",
                "from": "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23",
                "nonce": str(nonceid),
                "to": "0x0527e9E86a1C4462eF4ac00F543De8bDBFf06558",
                "input": '',
                "value": "3"
            }
            con_signtx = signTransaction (con_tx,b'\x15\xd1\x158\x1aND]f\xc5\x9fL+\x88Mx\xa3J\xc5K\xcc\xc33\xb4P\x8b\xce\x9c\xac\xf3%9')
            # print (con_signtx)
            data = {"method": "SendTx", "params": con_signtx}
            respTx = self.client.post(url=url, headers=headers,data=json.dumps(data).encode(encoding='UTF8'))
            if respTx.status_code != 200:
                print(u"请求返回状态码:", respTx.status_code)
            elif respTx.status_code == 200:
                if 'TXhash' in json.loads(respTx.content.decode()):
                    print(u'交易请求发送成功！')
                else:
                    print(u'请求结果为空，请确认请求参数是否正确！')
                    # print(respTx.content)
            # 每个账户每次执行请求后，nonce值加1，做循环请求
            nonceid = nonceid + 1
            print(time.time() - starttime)

# 这个类类似设置性能测试，继承HttpLocust
class websitUser (HttpLocust):
    # 指向一个上面定义的用户行为类
    task_set = UserBehavior
    # 执行事物之间用户等待时间的下界，单位毫秒，相当于lr中的think time
    min_wait = 0
    max_wait = 1
# if __name__ == "__main__":
#     import os
#     os.system("locust -f locustfile3.py")
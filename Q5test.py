# coding:utf-8
import queue
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

# maskBit = 0
# listA = [2]

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

def GetfromAddress():
        try:
            file = open("./fromaddress.txt", 'r', encoding='utf-8')
        except IOError:
            error = []
            return error
        fromaddresses = []
        for line in file:
            fromaddresses.append(line.strip ())
        file.close()
        return fromaddresses


class UserBehavior(TaskSet):
    '''用户行为描述'''
    def GettoAddress(self):
        try:
            file = open("./toaddress.txt", 'r', encoding='utf-8')
        except IOError:
            error = []
            return error
        toaddresses = []
        for line in file:
            toaddresses.append(line.strip())
        file.close()
        return toaddresses

    # def GetchainId(self,fromaddress):
    #     addressbyte = bytes.fromhex(fromaddress[2:])
    #     byteSize = (maskBit >> 3) + 1
    #     byteNum = addressbyte[0:byteSize]
    #     idx = ord (byteNum)
    #     mask = maskBit & 0x7
    #     if mask == 0:
    #         return idx
    #     bits = 8 - mask
    #     idx >>= bits
    #     chainId = listA[idx]
    #     return chainId

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
        toaddresses = self.GettoAddress()
        try:
            fromaddress = self.locust.fromaddress_queue.get() # 获取fromaddress队列里的数据，并赋值给fromaddress
        except queue.Empty:  # 队列取空后，直接退出
            print("no data exist")
            exit(0)
        nonceid = self.Getnonceid(fromaddress)
        s = requests.session()
        s.keep_alive = False
        url = 'http://192.168.1.13:8089'
        headers = {'Content-Type': 'application/json'}
        for toaddress in toaddresses:
            con_tx = {
                "chainId": "1",
                "fromChainId": "1",
                "toChainId": "1",
                "from": fromaddress,
                "nonce": str(nonceid),
                "to": toaddress,
                "input": '',
                "value": "3"
            }
            con_signtx = signTransaction (con_tx,b'\x15\xd1\x158\x1aND]f\xc5\x9fL+\x88Mx\xa3J\xc5K\xcc\xc33\xb4P\x8b\xce\x9c\xac\xf3%9')
            # print (con_signtx)
            data = {"method": "SendTx", "params": con_signtx}
            # respTx = self.client.post(path, data=data, verify=False)
            respTx = self.client.post(url=url, headers=headers,data=json.dumps(data).encode(encoding='UTF8'))
            if respTx.status_code != 200:
                print(u"请求返回状态码:", respTx.status_code)
                # print(respTx)
            elif respTx.status_code == 200:
                if 'TXhash' in json.loads(respTx.content.decode()):
                    print(u'交易请求发送成功！')
                else:
                    print(u'请求结果为空，请确认请求参数是否正确！')
            # 每个账户每次执行请求后，nonce值加1，做循环请求
            nonceid = nonceid + 1
            print(time.time() - starttime)


class websitUser(HttpLocust):
    task_set = UserBehavior
    fromaddresses = GetfromAddress ()
    fromaddress_queue = queue.Queue ()
    for fromaddress in fromaddresses:
        fromaddress_queue.put_nowait(fromaddress)
    min_wait = 0  # 单位毫秒
    max_wait = 1  # 单位毫秒

# if __name__ == "__main__":
#     import os
#     os.system("locust -f locustfile3.py")
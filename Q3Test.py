import queue
from collections import Mapping

from web3 import Web3, HTTPProvider
# from locust import HttpLocust,TaskSequence,seq_task
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
import requests

maskBit = 4
# maskBit = 0
# listA = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
listA = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
# listB = [2]

# chainId = "2"

def signTransaction(transaction_dict, private_key):
    FULL_NODE_HOSTS = 'http://192.168.1.126:8089'

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


# def get_privatekey():
#     FULL_NODE_HOSTS = 'http://192.168.1.126:8089'
#
#     provider = HTTPProvider (FULL_NODE_HOSTS)
#     web3 = Web3 (provider)
#     key = '0x15d115381a4e445d66c59f4c2b884d78a34ac54bccc333b4508bce9cacf32539'
#     ret = web3.eth.account.encrypt(key, "123456")
#     # # 打开一个文件
#     keyfile = open("./keystore/key1", "w")
#     keyfile.write(json.dumps(ret))
#     #
#     # # 关闭打开的文件
#     keyfile.close()
#
#     with open("./keystore/key1") as keyfile:
#         encrypted_key = keyfile.read()
#         encrypted_keyobj = json.loads(encrypted_key)
#         private_key = web3.eth.account.decrypt(encrypted_keyobj, '123456')
#     return private_key

def GetfromAddress():
    try:
        file = open("./fromaddress.txt", 'r', encoding='utf-8')
    except IOError:
        error = []
        return error
    fromaddresses = []
    for line in file:
        fromaddresses.append(line.strip())
    file.close()
    return fromaddresses


def GettoAddress():
    try:
        file = open ("./toaddress.txt", 'r', encoding='utf-8')
    except IOError:
        error = []
        return error
    toaddresses = []
    for line in file:
        toaddresses.append (line.strip())
    file.close()
    return toaddresses

def GetchainId(fromaddress):
    addressbyte = bytes.fromhex (fromaddress[2:])
    byteSize = (maskBit >> 3) +1
    byteNum = addressbyte[0:byteSize]
    idx = ord(byteNum)
    mask = maskBit & 0x7
    if mask == 0:
        return idx
    bits = 8 - mask
    idx >>= bits
    chainId = listA[idx]
    return chainId

def GetAccount(chainId,fromaddress):
    url = 'http://172.26.65.237:8088'
    headers = {'Content-Type': 'application/json'}
    data = {
        "method": "GetAccount",
        "params": {"chainId": chainId, "address": fromaddress}
    }
    response = requests.post (url=url, headers=headers, data=json.dumps (data).encode (encoding='UTF8'))
    assert response.status_code
    if 'error' in response:
        return response['error']
    resp = json.loads(response.content.decode())
    nonceid = resp["nonce"]
    return nonceid

class UserBehavior(TaskSet):
    @task(1)
    def TestTransfer(self):
        """转账交易"""
        starttime = time.time()
        for i in range(10000):
            try:
                fromaddress = self.locust.fromaddress_queue.get_nowait() # 获取fromaddress队列里的数据，并赋值给fromaddress
            except queue.Empty:  # 队列取空后，直接退出
                print("no data exist")
                exit(0)
            self.locust.fromaddress_queue.put_nowait(fromaddress)  # 获取fromaddress队列里的数据，并赋值给fromaddress
            chainId = GetchainId(fromaddress)
            nonceid = GetAccount(str(chainId),fromaddress)
            for j in range(10000):
                try:
                    toaddress = self.locust.toaddress_queue.get_nowait()
                except queue.Empty:  # 队列取空后，直接退出
                    print ("no data exist")
                    exit (0)
                self.locust.toaddress_queue.put_nowait(toaddress)
                print(u'当前转出地址：',fromaddress)
                print(u'当前转入地址：',toaddress)
                url = 'http://172.26.65.237:8088'
                headers = {'Content-Type': 'application/json'}
                con_tx = {
                    "chainId": str(chainId),
                    "fromChainId": str(chainId),
                    "toChainId": "2",
                    "from": fromaddress,
                    "nonce": str(nonceid),
                    "to": toaddress,
                    "input": '',
                    "value": "3"
                    }
                con_signtx = signTransaction(con_tx, b'\x15\xd1\x158\x1aND]f\xc5\x9fL+\x88Mx\xa3J\xc5K\xcc\xc33\xb4P\x8b\xce\x9c\xac\xf3%9')
                data = {"method": "SendTx","params":con_signtx}
                with self.client.post(url=url, headers=headers,data=json.dumps (data).encode (encoding='UTF8')) as response:
                    # 设置断言（1、状态码断言；2、返回结果断言）
                    if response.status_code != 200:
                        # print (u"返回异常！")
                        print (u"请求返回状态码:", response.status_code)
                    elif response.status_code == 200:
                        # print (u"返回正常！")
                        if 'TXhash' in json.loads (response.content.decode ()):
                            print (u'交易请求发送成功！')
                        else:
                            print (u'请求结果为空，请确认请求参数是否正确！')
                        # resp = json.loads (response.content.decode ())
                        # # 提取交易请求返回的TXhash值
                        # TXhash = resp["TXhash"]
                        # print(TXhash)
                        # return TXhash
                # 每个账户每次执行请求后，nonce值加1，做循环请求
                nonceid = nonceid + 1
                print(time.time()-starttime)




class websitUser(HttpLocust):
    task_set = UserBehavior
    #从文本中读取fromaddress地址，并加入队列
    fromaddresses = GetfromAddress ()
    fromaddress_queue = queue.Queue()
    for fromaddress in fromaddresses:
        fromaddress_queue.put_nowait(fromaddress)
    toaddresses = GettoAddress ()
    toaddress_queue = queue.Queue ()
    for toaddress in toaddresses:
        toaddress_queue.put_nowait(toaddress)

    min_wait = 10  # 单位毫秒
    max_wait = 2000  # 单位毫秒

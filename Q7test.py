#!/usr/bin/env python
# coding:utf-8
import json

import paramiko
# import urunite_test_py
import unittest
import numpy as np
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import requests
from numpy import datetime64
from itertools import islice
import re,os,time,shutil,logging
import threading
import datetime


# chainId = "0"
# fromaddress = "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23"

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='parallel_test.log',
                filemode='w')

host1={"ip":"192.168.1.13",'port':22,"username":"root","passwd":"chrdwhdhxt"}
host2={"ip":"192.1689.1.14",'port':22,"username":"root","passwd":"chrdwhdhxt"}
#将host添加到HOST中进行监控
HOST=[host1,host2]

data_path=os.path.join(os.getcwd(),"data")
pic_path=os.path.join(os.getcwd(),"picture")


#ssh，返回远程命令的输出结果。
def ssh2(host,cmd):
    result=[]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logging.info("connect to "+host['ip']+",user "+host['username']+",ssh")
        ssh.connect(host['ip'],int(host['port']),host['username'],host['passwd'],timeout=5)
        for m in cmd:
            logging.info(m)
            stdin,stdout,stderr = ssh.exec_command(m)
            out = stdout.readlines()
            #return out
            for o in out:
                logging.info(o)
                result.append(o)
        ssh.close()
    except Exception as e:
        logging.DEBUG(e)
    return out

#sftp,默认从对端home目录获取，放到本地当前目录
def sftpfile(host,getfiles,putfiles):
    try:
        logging.info("connnect to "+host['ip']+",user "+host['username']+",sftp")
        t=paramiko.Transport((host['ip'],int(host['port'])))
        t.connect(username=host['username'],password=host['passwd'])
        sftp =paramiko.SFTPClient.from_transport(t)
        if getfiles != None:
            for file in getfiles:
                logging.info("get "+file)
                file=file.replace("\n", "")
                sftp.get(file,file)
        if putfiles != None:
            for file in putfiles:
                file=file.replace("\n", "")
                logging.info("put "+file)
                sftp.put(file,file)
        t.close()
    except:
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except Exception as e:
            logging.DEBUG(e)

def GetAccount(chainId,fromaddress):
            url = 'http://192.168.1.13:8091'
            headers = {'Content-Type': 'application/json'}
            data = {
                "method": "GetAccount",
                "params": {"chainId": chainId, "address": fromaddress}
            }
            response = requests.post (url=url, headers=headers, data=json.dumps (data).encode (encoding='UTF8'))
            # print(response)
            # time.sleep (5)
            # if 'error' in response:
            #     return response['error']
            # resp = json.loads (response.content.decode ())
            # print(resp)
            # nonceid = resp["nonce"]
            # print(nonceid)
            return response.status_code
            # self.assertEqual(response.status_code,200)



class MyTestCase (unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual (True, False)
    def test_GetAccount(self):
        self.assertEqual(GetAccount("0","0x2c7536e3605d9c16a7a3d7b1898e529396a65c23"),200)
        self.assertEqual(GetAccount ("0", "0x2c7536e3605d9c16a7a3d7b1898e529396"), 200)

if __name__ == '__main__':
    unittest.main ()

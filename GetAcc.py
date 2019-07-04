import json

import requests
fromaddress = "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23"
chainId = "3"
def GetAccount():
        url = 'http://192.168.1.13:8091'
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

GetAccount()
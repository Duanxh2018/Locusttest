import requests
import json

maskBit = 4
# maskBit = 0
# listA = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
listA = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]

def GetfromAddress():
    try:
        file = open ("./fromaddress.txt", 'r', encoding='utf-8')
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


def GetAccount(fromaddresses):
    for fromaddress in fromaddresses:
        chainId = GetchainId(fromaddress)
        url = 'http://192.168.1.13:8093'
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
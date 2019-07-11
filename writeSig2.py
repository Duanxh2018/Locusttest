# !/usr/bin/env python
# -*- coding:utf-8 -*-
#import xlwt #这个专门用于写入excel的库没有用到
import xlrd
from xlutils.copy import copy
#
# maskBit = 1
# listA = [3,4]
#
# def GetchainId(fromaddress):
#     addressbyte = bytes.fromhex(fromaddress[2:])
#     byteSize = (maskBit >> 3) +1
#     byteNum = addressbyte[0:byteSize]
#     idx = ord(byteNum)
#     mask = maskBit & 0x7
#     if mask == 0:
#         return idx
#     bits = 8 - mask
#     idx >>= bits
#     chainId = listA[idx]
#     return chainId

from collections import Mapping
from web3 import Web3, HTTPProvider
from web3._utils.encoding import (
    remove_0x_prefix, to_bytes, to_hex
)
from eth_utils import keccak as eth_utils_keccak
from eth_keys import (
    keys
)

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
    print(transaction_dict)
    return transaction_dict

old_excel = xlrd.open_workbook('data.xlsx')
sheet = old_excel.sheets()[0]
i = 1
new_excel = copy(old_excel)
# for i in range(1,200001):
for row in sheet.get_rows():

    # chainId =sheet.row(i)[0].value
    # fromChainId =sheet.row(i)[1].value
    # toChainId =sheet.row(i)[2].value
    # fromaddress =sheet.row(i)[3].value
    toaddress = sheet.row(i)[4].value
    nonce =sheet.row(i)[5].value
    # value =sheet.row(i)[6].value
    # inputNum =sheet.row(i)[7].value

    con_tx = {
        "chainId": "2",
        "fromChainId": "2",
        "toChainId": "3",
        "from": "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23",
        "nonce": nonce,
        "to": toaddress,
        "input": "",
        "value": "3"
    }
    transaction_dict = signTransaction(con_tx, b'\x15\xd1\x158\x1aND]f\xc5\x9fL+\x88Mx\xa3J\xc5K\xcc\xc33\xb4P\x8b\xce\x9c\xac\xf3%9')
    print(transaction_dict)
    sig =transaction_dict['sig']
    print(sig)
    ws = new_excel.get_sheet(0)
    ws.write(i,8,sig)
    new_excel.save('data.xlsx')
    old_excel = xlrd.open_workbook('data.xlsx')
    new_excel = copy(old_excel)
    i = i+1
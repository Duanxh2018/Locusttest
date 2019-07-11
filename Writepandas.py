#-*- coding:utf-8 -*-
import pandas as pd

from collections import Mapping
from web3 import Web3, HTTPProvider
from web3._utils.encoding import (
    remove_0x_prefix, to_bytes, to_hex
)
from eth_utils import keccak as eth_utils_keccak
from eth_keys import (
    keys
)
maskBit = 1
listA = [3,4]


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

def GetchainId(fromaddress):
    addressbyte = bytes.fromhex(fromaddress[2:])
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


def modsig():
    df = pd.DataFrame(pd.read_excel('./data.xlsx', 1))  # 输入excel路径 和 表的索引
    lenth = len(df)

    for index in range(0,lenth):
        # chainId = df.loc[index,'chainId'])
        # fromchainId = df.loc[index,'fromchainId']
        # tochainId = df.loc[index,'tochainId']
        # fromaddress =df.loc[index, 'fromaddress'])
        toaddress = df.loc[index, 'toaddress']
        nonce = df.loc[index, 'nonce']
        # value = df.loc[index, 'value']
        # inputNum = df.loc[index, 'input'])

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
        transaction_dict = signTransaction(con_tx,b'\x15\xd1\x158\x1aND]f\xc5\x9fL+\x88Mx\xa3J\xc5K\xcc\xc33\xb4P\x8b\xce\x9c\xac\xf3%9')
        print(transaction_dict)
        sig = transaction_dict['sig']
        df.loc[index, 'sig'] = sig

    # dfInter  = df.loc[:,['功能说明', '接口名称']]
    # print(dfInter.head(10))
    df.to_excel('./excel_to_test.xls', sheet_name='result')

if __name__ == '__main__':
    modsig()
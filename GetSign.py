from collections import Mapping

from web3 import Web3, HTTPProvider

from web3._utils.encoding import (
    remove_0x_prefix, to_bytes, to_hex
)
from eth_utils import keccak as eth_utils_keccak

from eth_keys import (
    keys
)

con_tx = {
        "chainId": "2",
    	"fromChainId": "2",
    	"toChainId": "2",
    	"from": "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23",
    	"nonce": "22",
    	"to": "0xbCA7819004C1c02DF6e59c7F42eA49dd70478FE5",
    	"input": "",
    	"value": "3",
}

transaction_dict = con_tx


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

signTransaction(con_tx,b'\x15\xd1\x158\x1aND]f\xc5\x9fL+\x88Mx\xa3J\xc5K\xcc\xc33\xb4P\x8b\xce\x9c\xac\xf3%9')
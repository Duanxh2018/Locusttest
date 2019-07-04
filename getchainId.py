maskBit = 3
# maskBit = 0
listA = [3,4,5,6,7,8,9,10]


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
    print(chainId)
    return chainId

GetchainId("0xD71C785aD93052CF28115F91f84214826D293658")

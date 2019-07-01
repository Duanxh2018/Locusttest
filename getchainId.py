maskBit = 4
# maskBit = 0
listA = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]


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

GetchainId("0x22C73038A2571F02948585b13170A7B84d3b0f6B")

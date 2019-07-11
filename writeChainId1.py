# !/usr/bin/env python
# -*- coding:utf-8 -*-
#import xlwt #这个专门用于写入excel的库没有用到
import xlrd
from xlutils.copy import copy

maskBit = 1
listA = [3,4]

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

old_excel = xlrd.open_workbook('data.xls')
sheet = old_excel.sheets()[0]
i = 14496
new_excel = copy(old_excel)
for row in sheet.get_rows():
    fromaddress = sheet.row(i)[3].value
    print(fromaddress)
    chainId = GetchainId(fromaddress)
    print(chainId)
    fromChainId = chainId
    print(fromChainId)
    #使用json.loads可以把Unicode类型，即json类型转换成dict类型
    ws = new_excel.get_sheet(0)
    ws.write(i,0,chainId)
    ws.write(i,1,fromChainId)
    new_excel.save('data.xls')
    old_excel = xlrd.open_workbook('data.xls')
    new_excel = copy(old_excel)
    i = i+1
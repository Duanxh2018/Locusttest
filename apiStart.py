#-*- coding:utf-8 -*-

import requests
import json
import pandas as pd

host = '192.168.31.92:7002'

url = 'http://'+host+'/im/v1/setting/setting/getBlackList?imtid=1234567890123456&locale=en-US'

token = ''

# get http://{{host}}/im/v1/setting/setting/getBlackList?imtid=1234567890123456&locale=en-US HTTP/1.1
# content-type: application/json
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1YWM0NzljZDYwYjRmODA4MDE3ZDk1NzYiLCJpYXQiOjE1MjI4MjU2NzcsImV4cCI6MTUyNTQxNzY3N30.lpjTeFetMgLTss36HizxueEvfh1A8FloPi9it2XMe6E

# headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbXRpZCI6IkdYQ1pWVCIsImlhdCI6MTUzMDA4MDUzMCwiZXhwIjoxNTMyNjcyNTMwfQ.toJMzGsishYPBPa408pRt9fW6ybBU7qcdJla_p3Xonw'}
# headers["Authorization"] = "Bearer "+ token
# r = requests.request("get", url, headers=headers,data=json.loads("{}"))
# print(r.text)

def login():
    data = '{\
        "telephone": "+8615801556151",\
        "password":"123456"\
    }'
    url = 'http://' + host + '/v1/user/userLogin/login?locale=zh-CN'

    r = requests.request("post", url, data=json.loads(data))
    print(r.text)

    jsonObject = json.loads(r.text)

    token = jsonObject["data"]["token"]
    print(token)

# POST  http://{{host}}/v1/user/userLogin/login?locale=zh-CN  HTTP/1.1
# content-type: application/json
#


#
# url = 'http://'+host+'/im/v1/setting/setting/addBlackList?locale=zh-CN'
#
# print(url)
#
# headers = {'content-type': 'application/json'}

# data = '{\
#     "imtid": "1234567890123456",\
#     "black_name": "hellobc",\
#     "black_img":"http://flimg.fastsalt.com/qingting.png",\
#     "black_id": "f0e02d183d0b2015"\
# }'


# PUT  http://{{host}}/im/v1/setting/setting/addBlackList?locale=zh-CN  HTTP/1.1
# content-type: application/json
#
# {
#     "imtid": "1234567890123456",
#     "black_name": "hellobc",
#     "black_img":"http://flimg.fastsalt.com/qingting.png",
#     "black_id": "f0e02d183d0b2015"
# }

# r = requests.put(url, headers = headers,data=json.loads(data))
#
#
# print(r.text)

#
# PUT  http://{{host}}/im/v1/setting/setting/saveUserInfo?locale=zh-CN  HTTP/1.1
# content-type: application/json
#
# {
#     "imtid": "1234567890123456",
#     "allow_find": true,
#     "sendme": "我关注的人",
#     "showMoney": true
# }

def err_in_str(str):
    ret = False


    if str.find('errCode') > 0 or str.find('errMsg') > 0 :
        print("**** ERROR!")
        ret = True
    try:
        jsonObject = json.loads(str)
    except :
        ret = True
    return ret
def case_test(pwd):
    df = pd.DataFrame(pd.read_excel(pwd + './AppAPI.xls',1)) #输入excel路径 和 表的索引

#请求方法	URL	请求token	输入报文	输出报文

    #dfHead = df.head(2)

    lenth = len(df)

    for index in range (0,lenth):
        print("***",df.loc[index,'接口名称'])
        retStr = ''

        url = 'http://' + host + df.loc[index,'URL']

        data = df.loc[index,'输入报文']

        headers = {'Authorization': ''}

        headers["Authorization"] = "Bearer " + token

        if(df.loc[index,'请求token'] == 'Yes'):

            r = requests.request(df.loc[index, '请求方法'], url,headers=headers, data=json.loads(data))
            print(r.text)
            retStr = r.text
        else:
            r = requests.request(df.loc[index, '请求方法'], url, headers='', data=json.loads(data))
            print(r.text)
            retStr = r.text

        jsonObject = json.loads(retStr)

        df.loc[index, '状态'] = "成功"
        print("***", retStr)

        df.loc[index, '输出报文'] = retStr

        if err_in_str(retStr):
            if df.loc[index, '预期结果'] == "失败":
                df.loc[index, '状态'] = "成功"
            else:
                df.loc[index, '状态'] = "失败"


    # dfInter  = df.loc[:,['功能说明', '接口名称']]
    # print(dfInter.head(10))
    df.to_excel('./excel_to_test.xls', sheet_name='result')

if __name__ == '__main__':

    pwd = ''#cmd_client_return_str('pwd')

    login()

    case_test(pwd)
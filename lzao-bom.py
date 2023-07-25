import json

import redis
import requests

data = ""
answer = ''
code=''

def d():
    url = "http://192.168.5.214/api/mp-oauth-api/oauth/token"

    payload = "<body data here>"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request( "POST", url, headers=headers, data=payload )
    global data
    data = response.json()['data']
    return data


def g():
    url = "http://192.168.5.214/api/mp-oauth-api/oauth/validate-img?token=" + data
    payload = {}
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request( "GET", url, headers=headers, data=payload )
    ip = '192.168.5.214'
    port = '6379'
    password = '1@#4'
    uuid = data

    # 连接redis 取值
    r = redis.StrictRedis( host=ip, port=port, password=password, decode_responses=True )
    validateCode = "mp:validateCode:{}".format( uuid )
    ##print(validateCode)
    global answer
    answer = r.get( validateCode )

    return answer


def lzao():
    url = "http://192.168.5.214/api/mp-oauth-api/oauth/login"

    payload = json.dumps( {
        "token": data,
        "appCode": "lzappwb",
        "loginName": "lzuser",
        "password": "3b612c75a7b5048a435fb6ec81e52ff92d6d795a8b5a9c17070f6a63c97a53b2",
        "validateCode": answer
    } )
    headers = {
        'lang': 'cn',
        'Content-Type': 'application/json'
    }

    response = requests.request( "POST", url, headers=headers, data=payload )
    global code
    code = response.json()['data']['code']
    return code
def  yy():
    url = "http://192.168.5.214/api/mp-oauth-api/oauth/code2token"

    payload = {}
    headers = {
        'code': code,
        'User-Agent': 'application/json'
    }

    response = requests.request( "POST", url, headers=headers, data=payload )
    token = response.json()['data']['token']

    return token


if __name__ == '__main__':
    print( d() )
    print( g() )
    print( lzao() )
    print( yy())

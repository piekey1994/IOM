#/usr/bin/env python
#coding=utf8
import hashlib
from urllib import parse
from urllib import request
import random
import json

def translate(text):
    appKey = '3a5f108e5496c8da'
    secretKey = 'SVgssenwjl6QeVArvpcccKmYUz48O12b'
    
    myurl = 'http://openapi.youdao.com/api'
    q = text
    fromLang = 'EN'
    toLang = 'zh-CHS'
    salt = random.randint(1, 65536)

    sign = appKey+q+str(salt)+secretKey
    sign = hashlib.new('md5', sign.encode('utf-8')).hexdigest()
    myurl = myurl+'?appKey='+appKey+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
 
    req=request.Request(myurl)
    res=request.urlopen(req).read()
    jsonRes=json.loads(str(res,'utf-8'))
    return jsonRes

def translate2(text):
    appKey = '3a5f108e5496c8da'
    secretKey = 'SVgssenwjl6QeVArvpcccKmYUz48O12b'
    
    myurl = 'http://openapi.youdao.com/api'
    q = text
    fromLang = 'EN'
    toLang = 'zh-CHS'
    salt = random.randint(1, 65536)

    sign = appKey+q+str(salt)+secretKey
    sign = hashlib.new('md5', sign.encode('utf-8')).hexdigest()
    myurl = myurl+'?appKey='+appKey+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
 
    req=request.Request(myurl)
    res=request.urlopen(req).read()
    jsonRes=json.loads(str(res,'utf-8'))
    return jsonRes['translation'][0]

from urllib import request
import json
import traceback
import time
import random
from urllib.parse import quote
import socket

timeout = 10
socket.setdefaulttimeout(timeout)


def mitsukuTalk(msg):
    botkey='n0M6dW2XZacnOgCWTp0FRaadjiO5TASZD_5OKHTs9hqAp62JnACkE6BQdHSvL1lL7jiC3vL-JS0~'
    client_name='cw168bddb8200'
    sessionid='403018361'
    channel='6'
    msg=quote(msg, 'utf-8')
    url = 'https://miapi.pandorabots.com/talk?botkey='+botkey+'&input='+msg+'&client_name='+client_name+'&sessionid='+sessionid+'&channel='+channel
    #准备一下头
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept':'*/*',
        'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Length':0,
        'DNT':1,
        'Host':'miapi.pandorabots.com',
        'Origin':'https://www.pandorabots.com',
        'Referer':'https://www.pandorabots.com/mitsuku/'
    }
    #创建一个request,放入我们的地址、数据、头
    print(url)
    req = request.Request(url, None, headers,method='POST')
    #访问
    try:
        res=request.urlopen(req).read().decode('utf-8')
    except:
        while True:
            try:
                res=request.urlopen(req).read().decode('utf-8')
                break
            except:
                pass
    jsonRes=json.loads(res)
    return jsonRes['responses'][0]

with open('en.key','r',encoding='utf-8') as textFile,open('mitsuku.output','w',encoding='utf-8') as resultFile:
    i=0
    for line in textFile:
        key=line.strip()
        value=mitsukuTalk(key).replace('\n',' ')
        resultFile.write(value+'\n')
        print(key+":"+value)
        i += 1
        time.sleep(int(random.random()*10)%4+1)
        
    print('finish:%d' % i)
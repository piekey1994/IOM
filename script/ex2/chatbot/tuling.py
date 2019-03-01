import time
import traceback
import requests
import json

def tulingTalk(key):
    try:
        data={
            "reqType":0,
            "perception": {
                "inputText": {
                    "text": key
                }
            },
            "userInfo": {
                "apiKey": "8375c29532d44c06aecb8fd29cde27d1",
                "userId": "python"
            }
        }
        headers = {'Content-Type': 'application/json'}
        url = 'http://openapi.tuling123.com/openapi/api/v2'
        result=requests.post(url, data=json.dumps(data),headers=headers)
        valueJson=json.loads(result.text)
        for group in valueJson['results']:
            if group['resultType'] == 'text':
                return group['values']['text']
        return ''
    except:
        traceback.print_exc()
        return ''


with open('cn.key','r',encoding='utf-8') as textFile,open('tuling.output','w',encoding='utf-8') as resultFile:
    i=0
    for line in textFile:
        key=line.strip()
        value=tulingTalk(key)
        resultFile.write(value+'\n')
        print(key+":"+value)
        i += 1
    print('finish:%d' % i)

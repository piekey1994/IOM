import json
from model.ltpModel import ltpModel
from model.w2vModel import w2vModel
#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

print('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)

with open('qa_data/weibokb.json','r+',encoding='utf-8') as weiboKbFile:
    kb=json.load(weiboKbFile)
    for i in range(4):
        kbtempFile=open('qa_data/weibokb'+str(i)+'.json','r',encoding='utf-8')
        kbtemp=json.load(kbtempFile)
        for entitytemp in kbtemp:
            flag=False
            for entity in kb:
                if W2vModel.getWordDistance(entity,entitytemp) > 0.9:
                    for k,v in kbtemp[entitytemp].items():
                        kb[entity][k]=v
                    flag=True
                    break
            if flag==False:
                kb[entitytemp]=dict()
                for k,v in kbtemp[entitytemp].items():
                    kb[entitytemp][k]=v
            
    weiboKbFile.seek(0)
    weiboKbFile.truncate()
    weiboKbFile.write(json.dumps(kb,ensure_ascii=False))

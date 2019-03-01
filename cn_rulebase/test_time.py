# -*- coding: utf-8 -*-
import sys
import traceback
from model.ltpModel import ltpModel
from model.qaModel import qaModel
from model.w2vModel import w2vModel
from model.tripleModel import tripleModel
import time

print('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)
TripleModel=tripleModel(LtpModel)
QAModel=qaModel('qa_data\\weibokb.json',LtpModel,TripleModel,W2vModel)    

print('开始读取文件')


with open('weibo.100w.test.key', 'r') as keyFile, open('weibo.100w.test.output', 'r') as valueFile:
    time_start=time.time()
    num=0
    for key,value in zip(keyFile,valueFile):
        
        key=key.strip().replace(' ','')
        value=value.strip().replace(' ','')
        try:
            score,tris=QAModel.getGMScore(key,value)
            num+=1
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        if num == 10000:
            break
    time_end=time.time()    
    print('totally cost',time_end-time_start)
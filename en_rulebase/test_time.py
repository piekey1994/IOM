# -*- coding: utf-8 -*-
import sys
import traceback
from nlpModel import nlpModel
from qaModel import qaModel
from w2vModel import w2vModel
from tripleModel import tripleModel
import time

print('加载模型中...')
NlpModel=nlpModel()
W2vModel=w2vModel()
TripleModel=tripleModel(NlpModel)
QAModel=qaModel('qa_data/kb.json',TripleModel,W2vModel)   


with open('twitter.key','r') as keyFile,open('twitter.value','r') as valueFile:
    time_start=time.time()
    num=0
    for key,value in zip(keyFile,valueFile):
        
        key=key.strip()
        value=value.strip()
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
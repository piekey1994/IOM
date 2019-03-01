# -*- coding: utf-8 -*-
import sys
import traceback
from nlpModel import nlpModel
from qaModel import qaModel
from w2vModel import w2vModel
from tripleModel import tripleModel

modelname='beam1.gm'

print('加载模型中...')
NlpModel=nlpModel()
W2vModel=w2vModel()
TripleModel=tripleModel(NlpModel)
QAModel=qaModel('qa_data/kb.json',TripleModel,W2vModel)   

print('开始读取文件')

with open('weibo.100w.test.key', 'r') as keyFile, open('weibo.100w.test.beam1.gm.output', 'r') as valueFile,\
open('weibo.100w.'+modelname+'.score','w') as out_file:

    triNum=0
    num = 0

    for key,value in zip(keyFile,valueFile):
        
        key=key.strip()
        value=value.strip()
        try:
            if QAModel.checkTriple(key,value):
                triNum+=1
            num+=1
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        if num % 100 == 0:
            print("%d trinum: %d" % (num,triNum))
        
    print(modelname+" finish %d trinum: %d" %(num,triNum))
    out_file.write(modelname+" finish %d trinum: %d" %(num,triNum))
    

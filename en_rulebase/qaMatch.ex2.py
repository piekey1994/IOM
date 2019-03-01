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

scoreNums=[0]*11
scoreSum=0

with open('Twitter.100w.test.key', 'r') as keyFile, open('Twitter.100w.test.beam1.gm.output', 'r') as valueFile,\
open('Twitter.100w.rule.'+modelname+'.score','w') as out_file:

    id = 1

    for key,value in zip(keyFile,valueFile):
        
        key=key.strip()
        value=value.strip()
        try:
            score,tris=QAModel.getGMScore(key,value)
            scoreSum+=score
            
            xh=int(score*10)
            scoreNums[xh]+=1
            id+=1
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        if id % 100 == 0:
            print("%d done %s" % (id,str(scoreNums)) )
        
    print(modelname+" finish %d score:%f" %(id,scoreSum))
    out_file.write("%d done %s\n" % (id,str(scoreNums)))
    out_file.write(modelname+" finish %d score:%f\n" %(id,scoreSum))
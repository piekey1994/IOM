# -*- coding: utf-8 -*-
import sys
import traceback
from model.ltpModel import ltpModel
from model.qaModel import qaModel
from model.w2vModel import w2vModel
from model.tripleModel import tripleModel

modelname='att'

print('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)
TripleModel=tripleModel(LtpModel)
QAModel=qaModel('qa_data\\weibokb.json',LtpModel,TripleModel,W2vModel)    

print('开始读取文件')


scoreNums=[0]*11
scoreSum=0

with open('weibo.100w.test.key', 'r') as keyFile, open('weibo.100w.test.output', 'r') as valueFile,\
open('weibo.100w.rule.'+modelname+'.score','w') as out_file:

    id = 1

    for key,value in zip(keyFile,valueFile):
        
        key=key.strip().replace(' ','')
        value=value.strip().replace(' ','')
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
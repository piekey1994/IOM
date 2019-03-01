# -*- coding: utf-8 -*-
import sys
import traceback
from model.ltpModel import ltpModel
from model.qaModel import qaModel
from model.w2vModel import w2vModel
from model.tripleModel import tripleModel



print('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)
TripleModel=tripleModel(LtpModel)
QAModel=qaModel('qa_data\\weibokb.json',LtpModel,TripleModel,W2vModel)    

print('开始读取文件')

outfilename='weibo.rule.newscore.output.'

with open(r'D:\IOM\dataset\cn_conv\weibo.txt','r',encoding='utf-8') as weiboFile:
    outfile=[]
    for i in range(11):
        of=open(outfilename+str(i),'w',encoding='utf-8')
        outfile.append(of)
    scorehist=[0 for i in range(11)]
    lineNum=0
    for line in weiboFile:
        line=line.strip()
        if line=='' or len(line.split('\t'))!=2:
            continue
        key=line.split('\t')[0].strip()
        value=line.split('\t')[1].strip()
        if key=='' or value=='':
            continue
        try:
            score,reason=QAModel.getGMScore(key,value)
            scorehist[int(score*10)]+=1
            outfile[int(score*10)].write(key+'\t'+value+'\t'+str(score)+'\n')
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        lineNum+=1
        if lineNum % 1000 == 0:
            print("%d done %s" % (lineNum,str(scorehist))) 
    print("分析对话数为：%d\n 分数分布：%s\n" % (lineNum,str(scorehist)))
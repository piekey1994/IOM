# -*- coding: utf-8 -*-
import sys
import traceback
from nlpModel import nlpModel
from qaModel import qaModel
from w2vModel import w2vModel
from tripleModel import tripleModel

print('加载模型中...')
NlpModel=nlpModel()
W2vModel=w2vModel()
TripleModel=tripleModel(NlpModel)
QAModel=qaModel('qa_data/kb.json',TripleModel,W2vModel)   

outfilename='Twitter.rule.newscore.output.'

with open(r'weibo.txt','r',encoding='utf-8') as weiboFile:
    outfile=[]
    for i in range(11):
        of=open(outfilename+str(i),'w',encoding='utf-8')
        outfile.append(of)
    scorehist=[0 for i in range(11)]
    lineNum=0
    for line in weiboFile:
        sents=line.strip().split('\t')
        key=sents[0]
        value=sents[1]
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
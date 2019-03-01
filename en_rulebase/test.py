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
QAModel=qaModel('qa_data\\kb.json',TripleModel,W2vModel)    

with open('test_file/reddit.sql.conv','r',encoding='utf-8') as redditFile,open('test_file/reddit.rule','w',encoding='utf-8') as resultFile:
    for line in redditFile:
        lineList=line.strip().split('\t')

        question=lineList[1]
        answer=lineList[2]
        score,reason=QAModel.getGMScore(question,answer)
        resultFile.write(lineList[0]+'\t'+str(score)+'\n')

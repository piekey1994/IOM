# -*- coding: utf-8 -*-
import sys
import traceback
from model.ltpModel import ltpModel
from model.qaModel import qaModel
from model.w2vModel import w2vModel
from model.tripleModel import tripleModel
import jieba


#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()


modelName='seq'
print('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)
TripleModel=tripleModel(LtpModel)
QAModel=qaModel('qa_data\\weibokb.json',LtpModel,TripleModel,W2vModel)    

print('开始读取文件')
#读取文件


#默认一行记录一问一答，用tab分隔开
with open('eval_file/weibo.test.key', 'r',encoding='utf-8') as keyFile,open('eval_file/weibo.'+modelName+'.test.output', 'r',encoding='utf-8') as valueFile,\
open("test_file/weibo."+modelName+".score.txt", 'w',encoding='utf-8') as scorefile,open("test_file/weibo."+modelName+".hist.txt", 'w',encoding='utf-8') as histfile:
    scoreHist=[0]*10
    scores=[]
    sentence_number=0
    no_tri_num=0
    high_num=0
    word_num=0
    i=0
    for (postLine,responseLine) in zip(keyFile,valueFile):
        try:
            question=postLine[:-1].replace(" ","")
            answer=responseLine[:-1].replace("<unk>","")
            if modelName=='xiaoice' or modelName=='tuling':
                word_num += len(jieba.lcut(answer))
            else:
                word_num += len(answer.split())
            answer=responseLine[:-1].replace(" ","")
            
            if question=="" or answer=="":
                scores.append(0)
                continue
            score,reason=QAModel.getMatchScore(question,answer)
            if score<=0.3:
                no_tri_num+=1
            if score>0.7:
                high_num+=1
            index=int(score*10)
            if index>=10:
                index=9
            scoreHist[index] += 1
            scores.append(score)  
        except:
            scores.append(0)
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            print('%s: done%d %s' %(modelName,sentence_number,str(scoreHist)) )
    print('%s: finish%d  %s' %(modelName,sentence_number,str(scoreHist)) )
    print('score:%f' % sum(scores))
    print('no_tri_num:%d' % no_tri_num)
    print('high_num:%d' % high_num)
    print('avg_word_num:%f' % (word_num/sentence_number))
    histfile.write(str(scoreHist))
    scorefile.write('\n'.join([str(s) for s in scores]))
    # QAModel.saveKB()
        
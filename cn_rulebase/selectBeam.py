# -*- coding: utf-8 -*-
import sys
import traceback


#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()


print('开始读取文件')
#读取文件


#默认一行记录一问一答，用tab分隔开
with open('eval_file/weibo.test.key', 'r',encoding='utf-8') as postFile,open('eval_file/weibo.att.beam10.output', 'r',encoding='utf-8') as responseFile,\
    open('weibo.att.beam2.output', 'w',encoding='utf-8') as beam_file:
    sentence_number = 0
    knowledge_number = 0
    keys=postFile.readlines()
    beamvalues=responseFile.readlines()
    values=[]
    i=0
    for key in keys:
        answerLenList=[]
        # for j in range(10):
        #     answer=beamvalues[i][:-1].replace(" ","")
        #     answer=answer.replace("<unk>","")
        #     i += 1
        #     if question=="" or answer=="":
        #         scores.append(-1)
        #     else:
        #         score,reason=QAModel.getMatchScore(question,answer)
        #         scores.append(score)
        for j in range(10):
            answer=beamvalues[i][:-1].replace(" ","").replace("<unk>","")
            answerLenList.append(len(answer))
            i += 1
        
        index=answerLenList.index(max(answerLenList))
        values.append(beamvalues[i-10+index])
        if i % 100 ==0 :
            print("%d done" % (i))
    beam_file.writelines(values)      

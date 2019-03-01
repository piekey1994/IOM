# -*- coding: utf-8 -*-
import sys
import traceback
from model.ltpModel import ltpModel
from model.qaModel import qaModel
from model.w2vModel import w2vModel
from model.tripleModel import tripleModel

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

print('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)
TripleModel=tripleModel(LtpModel)
QAModel=qaModel('qa_data\\weibokb.json',LtpModel,TripleModel,W2vModel)    

print('开始读取文件')
#读取文件
postFileName = r"D:\知识图谱\关键程序\TieBa-Messenger-Bot-CN\weibo\stc_weibo_train_post"
responseFileName = r"D:\知识图谱\关键程序\TieBa-Messenger-Bot-CN\weibo\stc_weibo_train_response"
out_file_name = "test_file\\weibo.qa.txt"
noqaFileName = "test_file\\weibo.noqa.txt"


#默认一行记录一问一答，用tab分隔开
with open(postFileName, 'r',encoding='utf-8') as postFile,open(responseFileName, 'r',encoding='utf-8') as responseFile,\
    open(out_file_name, 'w',encoding='utf-8') as qa_file,open(noqaFileName, 'w',encoding='utf-8') as noqa_file:
    sentence_number = 0
    knowledge_number = 0
    for (postLine,responseLine) in zip(postFile,responseFile):
        question=postLine[:-1].replace(" ","")
        answer=responseLine[:-1].replace(" ","")
        if question=="" or answer=="":
            continue
        try:
            score,reason=QAModel.getMatchScore(question,answer)
            if score>0.7:
                knowledge_number += 1
                qa_file.write(question+'\t'+answer+'\n') 
            else:
                noqa_file.write(question+'\t'+answer+'\n') 
        except:
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            print("%d done" % (sentence_number))
    QAModel.saveKB()
    print("分析对话数为：%d\n存在知识条目数：%d\n" % (sentence_number,knowledge_number))

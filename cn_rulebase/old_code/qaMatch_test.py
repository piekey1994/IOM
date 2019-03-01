# -*- coding: utf-8 -*-
import sys
import traceback
from ltpModel import ltpModel
from qaModel import qaModel
from w2vModel import w2vModel
from tripleModel import tripleModel
import myLog

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

logger=myLog.getLogging('baiduqalog.txt') #log文件

logger.info('加载模型中...')
LtpModel=ltpModel()
W2vModel=w2vModel(LtpModel)
TripleModel=tripleModel(LtpModel)
QAModel=qaModel('qa_data\\baiduqakb.json',LtpModel,TripleModel,W2vModel)    

logger.info('开始读取文件')
#读取文件
in_file_name = "test_file\\baiduqa.txt"
out_file_name = "test_file\\baiduqa_output.txt"
if len(sys.argv) > 1:
    in_file_name = sys.argv[1]

if len(sys.argv) > 2:
    out_file_name = sys.argv[2]

#默认一行记录一问一答，用tab分隔开
with open(in_file_name, 'r',encoding='utf-8') as in_file,open(out_file_name, 'w',encoding='utf-8') as out_file:
    sentence_number = 0
    knowledge_number = 0
    text_line = in_file.readline()
    while text_line:
        sentence = text_line.strip()#去除空白
        if sentence=="" or len(sentence)>1000 or len(sentence.split('\t'))!=2:
            text_line=in_file.readline()
            continue
        question=sentence.split('\t')[0]
        answer=sentence.split('\t')[1]
        if question=="" or answer=="":
            text_line=in_file.readline()
            continue
        try:
            score,reason=QAModel.getMatchScore(question,answer)
            if score>0.7:
                knowledge_number += 1
                out_file.write(sentence+'\t'+str(score)+'\t'+reason+'\n') 
        except:
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            logger.info("%d done" % (sentence_number))
            QAModel.printKbStatus(logger)
        text_line = in_file.readline()
        if sentence_number==10000:
            break
    QAModel.saveKB()
    print("分析对话数为：%d\n存在知识条目数：%d\n" % (sentence_number,knowledge_number))

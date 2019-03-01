# -*- coding: utf-8 -*-
import sys
import traceback
from nlpModel import nlpModel
from qaModel import qaModel
from w2vModel import w2vModel
from tripleModel import tripleModel
import multiprocessing

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()


def task(param):
    print('加载模型中...')
    NlpModel=nlpModel()
    W2vModel=w2vModel()
    TripleModel=tripleModel(NlpModel)
    QAModel=qaModel('qa_data\\rkb'+str(param['id'])+'.json',TripleModel,W2vModel)  
    
    qaResult=[]
    noqaResult=[]
    lines=param['lines']
    sentence_number=0
    knowledge_number=0
    for line in lines:
        try:
            qaList=line.strip().split('\t')
            if len(qaList)!=2:
                continue
            question=qaList[0]
            answer=qaList[1]
            score,reason=QAModel.getMatchScore(question,answer)
            if score>0.7:
                knowledge_number += 1
                qaResult.append(question+'\t'+answer+'\n') 
            else:
                noqaResult.append(question+'\t'+answer+'\n') 
        except:
            print('process:'+str(param['id'])+' error '+line)
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            print('process:%d done%d qa%d noqa%d' %(param['id'],sentence_number,len(qaResult),len(noqaResult)))
    print('process:%d finish%d qa%d noqa%d' %(param['id'],sentence_number,len(qaResult),len(noqaResult)))
    QAModel.saveKB()
    result={'qaResult':qaResult,'noqaResult':noqaResult,'sentence_number':sentence_number,'knowledge_number':knowledge_number}
    return result

if __name__=='__main__':  
    print('开始读取文件')
    #读取文件
    redditName = "test_file\\redditConv.txt"
    out_file_name = "test_file\\redditConv.qa.txt"
    noqaFileName = "test_file\\redditConv.noqa.txt"
    #默认一行记录一问一答，用tab分隔开
    with open(redditName, 'r',encoding='utf-8') as redditFile,\
        open(out_file_name, 'w',encoding='utf-8') as qa_file,open(noqaFileName, 'w',encoding='utf-8') as noqa_file:
        sentence_number = 0
        knowledge_number = 0
        redditLines=redditFile.readlines()
        allLen=len(redditLines)
        results=[]
        pool = multiprocessing.Pool(processes=4) # 创建4个进程
        for i in range(4):
            begin=allLen//4*i
            end=allLen//4*(i+1)
            if i==3:
                end=allLen
            param={'id':i,'lines':redditLines[begin:end]}
            results.append(pool.apply_async(task, (param,)))
        pool.close() # 关闭进程池，表示不能在往进程池中添加进程
        pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
        print("所有进程已完成.开始写回···")
        for res in results:
            result=res.get()
            sentence_number+=result['sentence_number']
            knowledge_number+=result['knowledge_number']
            qa_file.writelines(result['qaResult'])
            noqa_file.writelines(result['noqaResult'])
        
        print("分析对话数为：%d\n存在知识条目数：%d\n" % (sentence_number,knowledge_number))

# -*- coding: utf-8 -*-
import sys
import traceback
from ltpModel import ltpModel
from qaModel import qaModel
from w2vModel import w2vModel
from tripleModel import tripleModel
import multiprocessing
import emoji

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

dos=20 #difference of sentence's length
minlen=4

def remove_emoji(text):
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

def task(param):
    print('加载模型中...')
    LtpModel=ltpModel()
    W2vModel=w2vModel(LtpModel)
    TripleModel=tripleModel(LtpModel)
    QAModel=qaModel('qa_data\\weibokb'+str(param['id'])+'.json',LtpModel,TripleModel,W2vModel)   
    
    qaResult=[]
    noqaResult=[]
    qlines=param['qlines']
    alines=param['alines']
    sentence_number=0
    knowledge_number=0
    for (postLine,responseLine) in zip(qlines,alines):
        k=remove_emoji(postLine.replace(" ","").replace("\n",""))
        while(len(k)>1):
            if u'\u4e00' <= k[-1] <= u'\u9fff':
                break
            else:
                k=k[:-1]
        while(len(k)>1):
            if u'\u4e00' <= k[0] <= u'\u9fff':
                break
            else:
                k=k[1:]
        if len(k)<minlen:
            continue
        v=remove_emoji(responseLine.replace(" ","").replace("\n",""))
        while(len(v)>1):
            if u'\u4e00' <= v[-1] <= u'\u9fff':
                break
            else:
                v=v[:-1]
        while(len(v)>1):
            if u'\u4e00' <= v[0] <= u'\u9fff':
                break
            else:
                v=v[1:]		
        if len(v)<minlen or abs(len(k)-len(v)) >= dos or k.find('@')!=-1 or v.find('@')!=-1 or k.find('http')!=-1 or v.find('http')!=-1:
            continue
        question=k
        answer=v	
        try:
            score,reason=QAModel.getMatchScore(question,answer)
            if score>0.7:
                knowledge_number += 1
                qaResult.append(question+'\t'+answer+'\n') 
            else:
                noqaResult.append(question+'\t'+answer+'\n') 
        except:
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            try:
                print('process:'+str(param['id'])+' done'+str(sentence_number))
            except:
                traceback.print_exc()
    QAModel.saveKB()
    result={'qaResult':qaResult,'noqaResult':noqaResult,'sentence_number':sentence_number,'knowledge_number':knowledge_number}
    return result

if __name__=='__main__':  
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
        postLines=postFile.readlines()
        responseLines=responseFile.readlines()
        allLen=len(postLines)
        results=[]
        pool = multiprocessing.Pool(processes=4) # 创建4个进程
        for i in range(4):
            begin=allLen//4*i
            end=allLen//4*(i+1)
            if i==3:
                end=allLen
            param={'id':i,'qlines':postLines[begin:end],'alines':responseLines[begin:end]}
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

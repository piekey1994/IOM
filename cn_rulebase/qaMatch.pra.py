# -*- coding: utf-8 -*-
import sys
import traceback
from model.ltpModel import ltpModel
from model.qaModel import qaModel
from model.w2vModel import w2vModel
from model.tripleModel import tripleModel
import multiprocessing
import emoji


process_num=8

def remove_emoji(text):
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

def task(param):
    print('加载模型中...')
    LtpModel=ltpModel()
    W2vModel=w2vModel(LtpModel)
    TripleModel=tripleModel(LtpModel)
    QAModel=qaModel('qa_data\\weibokb'+str(param['id'])+'.json',LtpModel,TripleModel,W2vModel)   
    
    scoreHist=[0]*10
    scores=[]
    lines=param['lines']
    sentence_number=0
    i=0
    for line in lines:
        try:
            qaList=line.strip().split('\t')
            if len(qaList)!=2:
                scores.append(-1)
                continue
            question=qaList[0]
            answer=qaList[1]
            score,reason=QAModel.getMatchScore(question,answer)
            index=int(score*10)
            if index>=10:
                index=9
            scoreHist[index] += 1
            scores.append(score)  
        except:
            scores.append(-1)
            print('process:'+str(param['id'])+' error '+line)
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            print('process:%d done%d %s' %(param['id'],sentence_number,str(scoreHist)) )
    print('process:%d finish%d  %s' %(param['id'],sentence_number,str(scoreHist)) )
    QAModel.saveKB()
    result={'sentence_number':sentence_number,'scoreHist':scoreHist,'scores':scores,'id':param['id']}
    return result

if __name__=='__main__':  
    print('开始读取文件')
    #读取文件
    with open("weibo.txt", 'r',encoding='utf-8') as postFile,\
    open("weibo.score.txt", 'w',encoding='utf-8') as scorefile,open("test_file\\weibo.qa.hist.txt", 'w',encoding='utf-8') as histfile:
        sentence_number = 0
        scoreHist=[0]*10
        scores=[[] for i in range(process_num)]
        postLines=postFile.readlines()
        allLen=len(postLines)
        results=[]
        pool = multiprocessing.Pool(processes=process_num) # 创建4个进程
        for i in range(process_num):
            begin=allLen//process_num*i
            end=allLen//process_num*(i+1)
            if i==process_num-1:
                end=allLen
            param={'id':i,'lines':postLines[begin:end]}
            results.append(pool.apply_async(task, (param,)))
        pool.close() # 关闭进程池，表示不能在往进程池中添加进程
        pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
        print("所有进程已完成.开始写回···")
        for res in results:
            result=res.get()
            sentence_number+=result['sentence_number']
            sh=result['scoreHist']
            id=result['id']
            scores[id]=result['scores']
            for i in range(10):
                scoreHist[i]  += sh[i]
        histfile.write(str(scoreHist))
        for score in scores:
            scorefile.write('\n'.join([str(s) for s in score])+'\n')
        print("分析对话数为：%d\n %s" % (sentence_number,str(scoreHist)))

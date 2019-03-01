#!/usr/bin/env python
# coding: utf-8
from nltk.translate.bleu_score import sentence_bleu
import gensim
from numpy import *

from sklearn.metrics.pairwise import cosine_similarity as cossim
# #win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
# import win_unicode_console
# win_unicode_console.enable()

def cosine_similarity(v1,v2):  
    if v1==[] or v2==[]:
        return 0
    score = cossim(array(v1).reshape(1,-1), array(v2).reshape(1,-1))
    return score[0][0]



# word2VecModel = gensim.models.Word2Vec.load(r"word2vec_data\wiki.zh.text.model")
# dime=200
word2VecModel = gensim.models.KeyedVectors.load_word2vec_format(r"D:\知识图谱\关键程序\KBChatbot\word2vec_data\news12g_bdbk20g_nov90g_dim128\news12g_bdbk20g_nov90g_dim128.bin", binary=True)
dime=64
prefix='weibo1.'
filenames=['test']
for fn in filenames:
    with open(prefix+'3456.'+fn+'.output','r',encoding='utf-8') as resultFile,open(prefix+'3456.test.value','r',encoding='utf-8') as targetFile,open(prefix+fn+'.evelResult.txt','w',encoding='utf-8') as merFile:
        unigrams=dict()
        bigrams=dict()
        wordsNum=0
        sentencesNum=0
        bleuScore=0
        GMScore=0
        EAScore=0
        VEScore=0
        for resultLine,targetLine in zip(resultFile,targetFile):      
            resultWords=resultLine[:-1].split()
            targetWords=targetLine[:-1].split()
            if len(resultWords)==0 or len(targetWords)==0:
                continue
            sentencesNum += 1
            if sentencesNum % 100 == 0:
                print('finish:%d' % (sentencesNum))
            #计算Distinct1和Distinct2
            words=resultWords
            wlen=len(words)
            wordsNum += wlen
            for i in range(wlen):
                word=words[i]
                #统计unigrams
                if word not in unigrams:
                    unigrams[word]=1
                else:
                    unigrams[word]=unigrams[word]+1
                #统计bigrams
                if i<wlen-1:
                    word=words[i]+' '+words[i+1]
                if word not in bigrams:
                    bigrams[word]=1
                else:
                    bigrams[word]=bigrams[word]+1   
            
            #计算BlEU
            reference = [targetWords]
            candidate = resultWords
            score = sentence_bleu(reference, candidate)
            bleuScore += score

            #计算Greedy Matching
            scores=[]
            for w1 in resultWords:
                ss=[]
                for w2 in targetWords:
                    try:
                        ss.append(word2VecModel.similarity(w1,w2))
                    except:
                        if w1==w2:
                            ss.append(1)
                        else:
                            ss.append(0)
                    scores.append(ss)
            max1 = 0
            max2 = 0
            for i in range(len(resultWords)):
                max1 += max(scores[i])
            max1 /= len(resultWords)
            for i in range(len(targetWords)):
                maxnum=0
                for j in range(len(resultWords)):
                    maxnum = scores[j][i] if scores[j][i]>maxnum else maxnum
                max2 += maxnum
            max2 /= len(targetWords)
            GMScore += (max1+max2)/2

            #计算Embedding Average
            resultAvgVec=[0]*dime
            resultLen=0
            targetAvgVec=[0]*dime
            targetLen=0
            for word in resultWords:
                try:
                    resultAvgVec=resultAvgVec+word2VecModel.wv[word]
                    resultLen += 1
                except:
                    pass
            
            for word in targetWords:
                try:
                    targetAvgVec=targetAvgVec+word2VecModel.wv[word]
                    targetLen += 1
                except:
                    pass

            if resultLen!=0 and targetLen!=0:  
                resultAvgVec = resultAvgVec*[1.0/resultLen]
                targetAvgVec = targetAvgVec*[1.0/targetLen]
                #EAScore += getConsim(mat(resultAvgVec),mat(targetAvgVec))
                EAScore += cosine_similarity(resultAvgVec,targetAvgVec)

            #计算Vector Extrema
            resultExtVec=[0]*dime
            targetExtVec=[0]*dime
            resultWordVecList=[[0] for i in range(dime)]
            targetWordVecList=[[0] for i in range(dime)]
            for word in resultWords:
                try:
                    v=word2VecModel.wv[word]
                    for i in range(dime):
                        resultWordVecList[i].append(v[i])
                except:
                    pass
            for word in targetWords:
                try:
                    v=word2VecModel.wv[word]
                    for i in range(dime):
                        targetWordVecList[i].append(v[i])
                except:
                    pass
            for i in range(dime):
                if max(resultWordVecList[i])>abs(min(resultWordVecList[i])):
                    resultExtVec[i]=max(resultWordVecList[i])
                else:
                    resultExtVec[i]=min(resultWordVecList[i])
                if max(targetWordVecList[i])>abs(min(targetWordVecList[i])):
                    targetExtVec[i]=max(targetWordVecList[i])
                else:
                    targetExtVec[i]=min(targetWordVecList[i])
                
            #VEScore += getConsim(mat(resultExtVec),mat(targetExtVec))
            VEScore +=  cosine_similarity(resultExtVec,targetExtVec)

        print("sentencesNum:%d" %(sentencesNum))
        print("wordsNum:%d" %(wordsNum))
        print("unigrams:%f" % (len(unigrams)/wordsNum))
        print("bigrams:%f" % (len(bigrams)/wordsNum))
        print("bleuScore:%f %f" % (bleuScore*100/sentencesNum,bleuScore/sentencesNum))
        print("GMScore:%f %f" % (GMScore*100/sentencesNum,GMScore/sentencesNum))
        print("EAScore:%f %f" % (EAScore*100/sentencesNum,EAScore/sentencesNum))
        print("VEScore:%f %f" % (VEScore*100/sentencesNum,VEScore/sentencesNum))
        merFile.write("sentencesNum:%d\n" %(sentencesNum))
        merFile.write("wordsNum:%d\n" %(wordsNum))
        merFile.write("unigrams:%f\n" % (len(unigrams)/wordsNum))
        merFile.write("bigrams:%f\n" % (len(bigrams)/wordsNum))
        merFile.write("bleuScore:%f %f\n" % (bleuScore*100/sentencesNum,bleuScore/sentencesNum))
        merFile.write("GMScore:%f %f\n" % (GMScore*100/sentencesNum,GMScore/sentencesNum))
        merFile.write("EAScore:%f %f\n" % (EAScore*100/sentencesNum,EAScore/sentencesNum))
        merFile.write("VEScore:%f %f\n" % (VEScore*100/sentencesNum,VEScore/sentencesNum))
#coding=utf-8
import time
from nltk.translate.bleu_score import sentence_bleu
import gensim
from numpy import *
from sklearn.metrics.pairwise import cosine_similarity

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
word2VecModel = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin',binary=True)

def getCosScore(v1,v2):
    if v1==[] or v2==[]:
        return 0
    score = cosine_similarity(np.array(v1).reshape(1,-1), np.array(v2).reshape(1,-1))
    return score[0][0]

def bleu(question,answer):
    resultWords=question.split()
    targetWords=answer.split()
    reference = [targetWords]
    candidate = resultWords
    score = sentence_bleu(reference, candidate)
    return score

#Greedy Matching
def getGMDistance(question,answer):
    A = question.split()
    B = answer.split()
    scores=[]
    for w1 in A:
        ss=[]
        for w2 in B:
            try:
                ss.append(word2VecModel.similarity(w1,w2))
            except:
                if w1==w2:
                    ss.append(1)
                else:
                    ss.append(0)
        scores.append(ss)
    La = 0
    Lb = 0
    for i in range(len(A)):
        La += max(scores[i])
    La /= len(A)
    for i in range(len(B)):
        maxnum=0
        for j in range(len(A)):
            maxnum = scores[j][i] if scores[j][i]>maxnum else maxnum
        Lb += maxnum
    Lb /= len(B)
    return (La+Lb)/2

def getEADistance(question,answer):

    resultWords = question.split()
    targetWords = answer.split()

    resultAvgVec=[0]*300
    resultLen=0
    targetAvgVec=[0]*300
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
        return getCosScore(resultAvgVec,targetAvgVec)
    else:
        return 0

def getVEDistance(word1,word2):
    resultWords = question.split()
    targetWords = answer.split()

    resultExtVec=[0]*300
    targetExtVec=[0]*300
    resultWordVecList=[[0] for i in range(300)]
    targetWordVecList=[[0] for i in range(300)]
    for word in resultWords:
        try:
            v=word2VecModel.wv[word]
            for i in range(300):
                resultWordVecList[i].append(v[i])
        except:
            pass
    for word in targetWords:
        try:
            v=word2VecModel.wv[word]
            for i in range(300):
                targetWordVecList[i].append(v[i])
        except:
            pass
    for i in range(300):
        if max(resultWordVecList[i])>abs(min(resultWordVecList[i])):
            resultExtVec[i]=max(resultWordVecList[i])
        else:
            resultExtVec[i]=min(resultWordVecList[i])
        if max(targetWordVecList[i])>abs(min(targetWordVecList[i])):
            targetExtVec[i]=max(targetWordVecList[i])
        else:
            targetExtVec[i]=min(targetWordVecList[i])
    #VEScore += getConsim(mat(resultExtVec),mat(targetExtVec))
    return  getCosScore(resultExtVec,targetExtVec)

with open('twitter.key','r') as keyFile,open('twitter.value','r') as valueFile:
    time_start=time.time()
    for key,value in zip(keyFile,valueFile):
        question=key.strip()
        answer=value.strip()
        if question=="" or answer=="":
            continue
        bleu(question,answer)
    time_end=time.time()
    print('totally cost:',time_end-time_start)
        
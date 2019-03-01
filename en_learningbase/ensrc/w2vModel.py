# -*- coding: utf-8 -*-
import gensim

class w2vModel:
    def __init__(self):

        print 'loading word2vec...'
        self.word2VecModel = gensim.models.KeyedVectors.load_word2vec_format('../pretrained_word_embeddings/GoogleNews-vectors-negative300.bin',binary=True)
        # self.word2VecModel = gensim.models.KeyedVectors.load_word2vec_format('/data/liupq/supervised-oie/pretrained_word_embeddings/news12g_bdbk20g_nov90g_dim128.bin', binary=True)
        print 'finish loading'

    def cosine_similarity(self,vector1,vector2):  
        dot_product = 0.0  
        normA = 0.0  
        normB = 0.0  
        for a,b in zip(vector1,vector2):  
            dot_product += a*b  
            normA += a**2  
            normB += b**2  
        if normA == 0.0 or normB==0.0:  
            return 0  
        else:  
            return dot_product / ((normA*normB)**0.5) 

    #Greedy Matching
    def getGMDistance(self,word1,word2):
        if word1==None or word2==None or word1=='' or word2=='' or word1==[] or word2==[]:
            return 0
        if type(word1)!=type([]):
            word1=[word1]
        if type(word2)!=type([]):
            word2=[word2]
        A = word1
        B = word2
        scores=[]
        for w1 in A:
            ss=[]
            for w2 in B:
                try:
                    ss.append(self.word2VecModel.similarity(w1,w2))
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

    #Embedding Average
    def getEADistance(self,word1,word2):
        if word1==None or word2==None or word1=='' or word2=='' or word1==[] or word2==[]:
            return 0
        if type(word1)!=type([]):
            word1=[word1]
        if type(word2)!=type([]):
            word2=[word2]
        resultWords = word1
        targetWords = word2

        resultAvgVec=[0]*300
        resultLen=0
        targetAvgVec=[0]*300
        targetLen=0
        for word in resultWords:
            try:
                resultAvgVec=resultAvgVec+self.word2VecModel.wv[word]
                resultLen += 1
            except:
                pass  
        
        for word in targetWords:
            try:
                targetAvgVec=targetAvgVec+self.word2VecModel.wv[word]
                targetLen += 1
            except:
                pass
        if resultLen!=0 and targetLen!=0:  
            resultAvgVec = resultAvgVec*[1.0/resultLen]
            targetAvgVec = targetAvgVec*[1.0/targetLen]
            #EAScore += getConsim(mat(resultAvgVec),mat(targetAvgVec))
            return self.cosine_similarity(resultAvgVec,targetAvgVec)
        else:
            return 0

    #Vector Extrema
    def getVEDistance(self,word1,word2):
        if word1==None or word2==None or word1=='' or word2=='' or word1==[] or word2==[]:
            return 0
        if type(word1)!=type([]):
            word1=[word1]
        if type(word2)!=type([]):
            word2=[word2]
        resultWords = word1
        targetWords = word2

        resultExtVec=[0]*300
        targetExtVec=[0]*300
        resultWordVecList=[[0] for i in range(300)]
        targetWordVecList=[[0] for i in range(300)]
        for word in resultWords:
            try:
                v=self.word2VecModel.wv[word]
                for i in range(300):
                    resultWordVecList[i].append(v[i])
            except:
                pass
        for word in targetWords:
            try:
                v=self.word2VecModel.wv[word]
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
        return  self.cosine_similarity(resultExtVec,targetExtVec)

    
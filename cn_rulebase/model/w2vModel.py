# -*- coding: utf-8 -*-
import gensim


class w2vModel:
    def __init__(self,ltp):
        self.segmentor = ltp.segmentor
        #加载模型word2Vec
        self.word2VecModel = gensim.models.KeyedVectors.load_word2vec_format(r"D:\IOM\word2vec\news12g_bdbk20g_nov90g_dim128.bin", binary=True)
    #计算短文本的距离
    def getWordDistance(self,word1,word2):
        if word1=='' or word2=='':
            return 0
        A = self.segmentor.segment(word1)#分词
        B = self.segmentor.segment(word2)
        if len(A)==0 or len(B)==0:
            return 0
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

    
# -*- coding: utf-8 -*-
import json

class qaModel:
    def __init__(self,kbPath,ltp,triple,w2v):
        #加载LTP模块
        self.segmentor = ltp.segmentor
        self.postagger = ltp.postagger
        self.parser = ltp.parser

        #加载三元组提取模块
        self.TripleModel=triple

        #加载word2Vec模块
        self.W2vModel=w2v

        # self.kb_file=open(kbPath,'r+',encoding='utf-8')
        #self.kb=json.load(self.kb_file)

        # self.lastKbStatus={'NodeSum':0,'EveryNode':{}}

    # def __del__(self):
    #     self.kb_file.seek(0)
    #     self.kb_file.truncate()
    #     self.kb_file.write(json.dumps(self.kb,ensure_ascii=False))

    # def saveKB(self):
    #     #print(self.kb)
    #     self.kb_file.seek(0)
    #     self.kb_file.truncate()
    #     self.kb_file.write(json.dumps(self.kb,ensure_ascii=False))

    # def printKbStatus(self,logger):
    #     nowNodeNum=len(self.kb)
    #     lastNodeNum=self.lastKbStatus['NodeSum']
    #     logger.info('当前节点数为%d，比上一轮增长了%d个节点' %(nowNodeNum,nowNodeNum-lastNodeNum))
    #     self.lastKbStatus['NodeSum']=nowNodeNum
    #     lastNode=self.lastKbStatus['EveryNode']
    #     addNode=[]
    #     for entity in self.kb:
    #         if entity in lastNode:
    #             addNum=len(self.kb[entity])-lastNode[entity] 
    #             if addNum>0:
    #                 logger.info('%s节点增加了%d个属性值' %(entity,addNum))
    #         else:
    #             addNode.append(entity)
    #         self.lastKbStatus['EveryNode'][entity]=len(self.kb[entity])
    #     if len(addNode)>0:
    #         logger.info('其中新增节点如下：')
    #         logger.info(addNode)
        
                



    # #输入三元组返回结果，如果三元组中存在代词，则尝试在知识库中寻找答案
    # def getAnswer(self,tripleResult):
    #     if tripleResult['hasTriple']:
    #         pron=tripleResult['pron']
    #         triple=tripleResult['triple']
    #         if pron[0]:
    #             maxScore=0
    #             answer=""
    #             for entity in self.kb:
    #                 links=self.kb[entity]
    #                 for link in links:
    #                     score=(self.W2vModel.getWordDistance(link,triple[1])+self.W2vModel.getWordDistance(links[link],triple[2]))/2
    #                     if score>maxScore:
    #                         maxScore=score
    #                         answer=entity
    #             return maxScore,0,answer

    #         else:
    #             for entity in self.kb:
    #                 if self.W2vModel.getWordDistance(entity,triple[0]) > 0.6:
    #                     links=self.kb[entity]
    #                     maxScore=0
    #                     answer=""
    #                     for link in links:
    #                         score=self.W2vModel.getWordDistance(link,triple[1])
    #                         if score>maxScore:
    #                             maxScore=score
    #                             answer=links[link]
    #                     return maxScore,2,answer
    #             return 0,2,""#查询不到结果
                        
    #     else:
    #         return 0,-1,""#查询不到结果默认返回值

    # #知识库写入
    # def addKnowledge(self,triple):
    #     for entity in self.kb:
    #         if self.W2vModel.getWordDistance(entity,triple[0]) > 0.9:
    #             self.kb[entity][triple[1]]=triple[2]
    #             return
    #     self.kb[triple[0]]={triple[1]:triple[2]}
        


    #获取问答对价值得分
    def getMatchScore(self,question,answer):
        TripleModel=self.TripleModel
        W2vModel=self.W2vModel
        #知识相似阈值
        knowledgeThreshold=0.7
        #答案相似阈值
        answerThreshold=0.7

        qResult=TripleModel.getTriple(question)
        aResult=TripleModel.getTriple(answer)
        #如果问句存在三元组
        if qResult['hasTriple']:
            pron=qResult['pron']
            triple=qResult['triple']
            #情况1：问句三元组存在代词
            if pron[2] or pron[0]:
                answerScore,answerLoc,realAnswer=self.getAnswer(qResult)
                hasAnswer=False
                if answerScore>answerThreshold:
                    hasAnswer=True
                if aResult['hasTriple']:
                    ap=aResult['pron']
                    at=aResult['triple']
                    if ap[answerLoc]:
                        return 0,str(qResult['triple'])+'\t'+str(aResult['triple'])
                    else:
                        if hasAnswer:
                            return W2vModel.getWordDistance(at[answerLoc],realAnswer),str(qResult['triple'])+'\t'+str(aResult['triple'])
                        else:
                            myScore=0
                            if answerLoc==0:
                                myScore=(W2vModel.getWordDistance(triple[1],at[1])+W2vModel.getWordDistance(triple[2],at[2]))/2
                            else:
                                myScore=(W2vModel.getWordDistance(triple[1],at[1])+W2vModel.getWordDistance(triple[0],at[0]))/2
                            if(myScore>knowledgeThreshold):
                                self.addKnowledge(at)
                                return myScore,str(qResult['triple'])+'\t'+str(aResult['triple'])
                            else:
                                return myScore,str(qResult['triple'])+'\t'+str(aResult['triple'])
                else:
                    if hasAnswer:
                        at=aResult['triple'][0]
                        return W2vModel.getWordDistance(at,realAnswer),str(qResult['triple'])+'\t'+str(aResult['triple'])
                    else:
                        return 0,str(qResult['triple'])+'\t'+str(aResult['triple'])
        #情况2：问句三元组不存在代词或者问句不是三元组
        qanswerScore,qanswerLoc,qrealAnswer=self.getAnswer(qResult)
        aanswerScore,aanswerLoc,arealAnswer=self.getAnswer(aResult)
        if max(qanswerScore,aanswerScore)<0.3 and aResult['hasTriple'] and qResult['hasTriple']:
            qtriple=qResult['triple']
            atriple=aResult['triple']
            myScore1=(W2vModel.getWordDistance(qtriple[0],atriple[0])+W2vModel.getWordDistance(qtriple[1],atriple[1])+W2vModel.getWordDistance(qtriple[2],atriple[2]))/3
            myScore2=(W2vModel.getWordDistance(qtriple[0],atriple[2])+W2vModel.getWordDistance(qtriple[1],atriple[1])+W2vModel.getWordDistance(qtriple[2],atriple[0]))/3
            return max(myScore1,myScore2),str(qResult['triple'])+'\t'+str(aResult['triple'])
        else:
       	    return max(qanswerScore,aanswerScore),'非问答模式，对两句话搜索答案取可能性较大者'


    def checkTriple(self,question,answer):
        TripleModel=self.TripleModel
        W2vModel=self.W2vModel
        qResult=TripleModel.getTriple(question)
        aResult=TripleModel.getTriple(answer)
        if qResult['hasTriple'] and aResult['hasTriple']:
            return True
        else:
            return False

    def getGMScore(self,question,answer):
        TripleModel=self.TripleModel
        W2vModel=self.W2vModel
        M=0.8

        qResult=TripleModel.getTriple(question)
        aResult=TripleModel.getTriple(answer)
        #如果问句存在三元组
        if qResult['hasTriple']:
            pron=qResult['pron']
            triple=qResult['triple']
            #情况1：问句三元组存在代词
            if pron[2] or pron[0]:
                if pron[0]:
                    answerLoc=0
                else:
                    answerLoc=2
                if aResult['hasTriple']:
                    ap=aResult['pron']
                    at=aResult['triple']
                    if ap[answerLoc]:
                        return 0,' \t '
                    else:
                        triple=qResult['triple']
                        myScore=0
                        if answerLoc==0:
                            myScore=(W2vModel.getWordDistance(triple[1],at[1])+W2vModel.getWordDistance(triple[2],at[2]))/2
                        else:
                            myScore=(W2vModel.getWordDistance(triple[1],at[1])+W2vModel.getWordDistance(triple[0],at[0]))/2
                        return myScore,str(qResult['triple'])+'\t'+str(aResult['triple'])
                else:
                    return 0,' \t '
        #情况2：问句三元组不存在代词或者问句不是三元组
        if qResult['hasTriple'] and aResult['hasTriple']:
            tri1=qResult['triple']
            tri2=aResult['triple']
            score1=(W2vModel.getWordDistance(tri1[0],tri2[0])+W2vModel.getWordDistance(tri1[1],tri2[1])+W2vModel.getWordDistance(tri1[2],tri2[2]))/3
            score2=(W2vModel.getWordDistance(tri1[0],tri2[2])+W2vModel.getWordDistance(tri1[1],tri2[1])+W2vModel.getWordDistance(tri1[2],tri2[0]))/3
            maxScore=max(score1,score2)
            #惩罚函数
            if maxScore>M:
                maxScore=M*(1-maxScore)/(1-M)
            return maxScore/M,str(qResult['triple'])+'\t'+str(aResult['triple'])
        else:
            return 0,' \t '
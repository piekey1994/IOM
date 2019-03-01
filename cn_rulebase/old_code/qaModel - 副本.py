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

        self.kb_file=open(kbPath,'r+',encoding='utf-8')
        self.kb=json.load(self.kb_file)

        self.lastKbStatus={'NodeSum':0,'EveryNode':{}}

    # def __del__(self):
    #     self.kb_file.seek(0)
    #     self.kb_file.truncate()
    #     self.kb_file.write(json.dumps(self.kb,ensure_ascii=False))

    def saveKB(self):
        #print(self.kb)
        self.kb_file.seek(0)
        self.kb_file.truncate()
        self.kb_file.write(json.dumps(self.kb,ensure_ascii=False))

    def printKbStatus(self,logger):
        nowNodeNum=len(self.kb)
        lastNodeNum=self.lastKbStatus['NodeSum']
        logger.info('当前节点数为%d，比上一轮增长了%d个节点' %(nowNodeNum,nowNodeNum-lastNodeNum))
        self.lastKbStatus['NodeSum']=nowNodeNum
        lastNode=self.lastKbStatus['EveryNode']
        addNode=[]
        for entity in self.kb:
            if entity in lastNode:
                addNum=len(self.kb[entity])-lastNode[entity] 
                if addNum>0:
                    logger.info('%s节点增加了%d个属性值' %(entity,addNum))
            else:
                addNode.append(entity)
            self.lastKbStatus['EveryNode'][entity]=len(self.kb[entity])
        if len(addNode)>0:
            logger.info('其中新增节点如下：')
            logger.info(addNode)
        
                



    #输入三元组返回结果，如果三元组中存在代词，则尝试在知识库中寻找答案
    def getAnswer(self,tripleResult):
        if tripleResult['hasTriple']:
            pron=tripleResult['pron']
            triple=tripleResult['triple']
            if pron[0]:
                maxScore=0
                answer=""
                for entity in self.kb:
                    links=self.kb[entity]
                    for link in links:
                        score=(self.W2vModel.getWordDistance(link,triple[1])+self.W2vModel.getWordDistance(links[link],triple[2]))/2
                        if score>maxScore:
                            maxScore=score
                            answer=entity
                return maxScore,0,answer

            else:
                for entity in self.kb:
                    if self.W2vModel.getWordDistance(entity,triple[0]) > 0.6:
                        links=self.kb[entity]
                        maxScore=0
                        answer=""
                        for link in links:
                            score=self.W2vModel.getWordDistance(link,triple[1])
                            if score>maxScore:
                                maxScore=score
                                answer=links[link]
                        return maxScore,2,answer
                return 0,2,""#查询不到结果
                        
        else:
            return 0,-1,""#查询不到结果默认返回值

    #知识库写入
    def addKnowledge(self,triple):
        for entity in self.kb:
            if self.W2vModel.getWordDistance(entity,triple[0]) > 0.9:
                self.kb[entity][triple[1]]=triple[2]
                return
        self.kb[triple[0]]={triple[1]:triple[2]}
        


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
                        return 0,'问句和答句代词位置一致，没有匹配的必要'
                    else:
                        if hasAnswer:
                            return W2vModel.getWordDistance(at[answerLoc],realAnswer),'问句存在代词，且知识库有答案，答句存在三元组，与答句的答案进行匹配'
                        else:
                            myScore=0
                            if answerLoc==0:
                                myScore=(W2vModel.getWordDistance(triple[1],at[1])+W2vModel.getWordDistance(triple[2],at[2]))/2
                            else:
                                myScore=(W2vModel.getWordDistance(triple[1],at[1])+W2vModel.getWordDistance(triple[0],at[0]))/2
                            if(myScore>knowledgeThreshold):
                                self.addKnowledge(at)
                                return myScore,'问句存在代词，且找不到答案，答句不存在代词，进行三元组匹配，匹配成功，加入知识库'
                            else:
                                return myScore,'问句存在代词，且找不到答案，答句不存在代词，进行三元组匹配，匹配失败，未加入知识库'
                else:
                    if hasAnswer:
                        at=aResult['triple'][0]
                        return W2vModel.getWordDistance(at,realAnswer),'问句存在代词，且知识库有答案，答句不存在三元组，直接匹配'
                    else:
                        return 0,'问句存在代词，且找不到答案，答句不存在三元组，无法匹配'
        #情况2：问句三元组不存在代词或者问句不是三元组
        qanswerScore,qanswerLoc,qrealAnswer=self.getAnswer(qResult)
        aanswerScore,aanswerLoc,arealAnswer=self.getAnswer(aResult)
        return max(qanswerScore,aanswerScore),'非问答模式，对两句话搜索答案取可能性较大者'


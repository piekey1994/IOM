import numpy as np
import scipy.stats as stats
import pickle
import xlwt

model='cn'

def kappa(testData, k): #testData表示要计算的数据，k表示数据矩阵的是k*k的  
    dataMat = np.mat(testData)  
    P0 = 0.0  
    n = dataMat.sum()
    for i in range(k):  
        P0 += dataMat[i, i]*1.0  
    P0 = P0/n
    xsum = np.sum(dataMat, axis=1)  
    ysum = np.sum(dataMat, axis=0)  
    #xsum是个k行1列的向量，ysum是个1行k列的向量  
    Pe  = float(ysum*xsum)/n**2  
      
    cohens_coefficient = float((P0-Pe)/(1-Pe))  
    return cohens_coefficient

def getKappaScore(list1,list2,num=5):
    kappaMat=[[0]*num for i in range(num)]
    options=[0.1,0.3,0.5,0.7,0.9]
    for num1,num2 in zip(list1,list2):
        hslist=[abs(num1-opscore) for opscore in options]
        op1=hslist.index(min(hslist))
        hslist=[abs(num2-opscore) for opscore in options]
        op2=hslist.index(min(hslist))
        kappaMat[op1][op2] += 1
    return kappa(kappaMat,num)

def getSpearmanScore(list1,list2):
    a= stats.spearmanr(list1,list2)
    return (a.correlation,a.pvalue)

def getPearsonScore(list1,list2):
    return stats.pearsonr(list1,list2)

with open('chatbot'+model+'.dict','rb') as humanScoreFile,open(model+'.score.dict','rb') as origFile:
    scoreDict=pickle.load(humanScoreFile)
    convDict=pickle.load(origFile)
    resultDict=dict()

    scoreTypes=['rulescore','learnscore','bleu','gm','ea','ve']

    idList=[]
    objScoreDict=dict()
    for st in scoreTypes:
        objScoreDict[st]=[]
    i=0
    for key in scoreDict:
        conv=convDict[key]
        if conv['rulekey'].strip()=='':
            i+=1
            if i<80:
                continue
        idList.append(key)
        for st in scoreTypes:
            objScoreDict[st].append(float(conv[st]))
    print(i)
    # for key in scoreDict:
    #     conv=convDict[key]
    #     if conv['rulekey'].strip()!='':
    #         idList.append(key)
    #         for st in scoreTypes:
    #             objScoreDict[st].append(float(conv[st]))
    # for key in scoreDict:
    #     idList.append(key)
    #     conv=convDict[key]
    #     for st in scoreTypes:
    #         objScoreDict[st].append(float(conv[st]))
    #avg
    avgResult=dict()
    avgScoreList=[]
    for id in idList:
        humanScore=[score*0.2-0.1 for score in scoreDict[id]]
        avgScoreList.append(np.mean(humanScore))
    #kappa
    kappaResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        kappaResult[key]=getKappaScore(objScoreList,avgScoreList)
    avgResult['kappa']=kappaResult
    #spearman
    spearmanResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        spearmanResult[key]=getSpearmanScore(objScoreList,avgScoreList)
    avgResult['spearman']=spearmanResult
    #pearson
    pearsonResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        pearsonResult[key]=getPearsonScore(objScoreList,avgScoreList)
    avgResult['pearson']=pearsonResult
    resultDict['avg']=avgResult

    #most votes
    mostResult=dict()
    mostVoteScoreList=[]
    for id in idList:
        humanScores=scoreDict[id]
        scoreSet=list(set(humanScores))
        hslist=[humanScores.count(score) for score in scoreSet]
        mostVoteScoreList.append(scoreSet[hslist.index(max(hslist))]*0.2-0.1)
    #kappa
    kappaResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        kappaResult[key]=getKappaScore(objScoreList,mostVoteScoreList)
    mostResult['kappa']=kappaResult
    #spearman
    spearmanResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        spearmanResult[key]=getSpearmanScore(objScoreList,mostVoteScoreList)
    mostResult['spearman']=spearmanResult
    #pearson
    pearsonResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        pearsonResult[key]=getPearsonScore(objScoreList,mostVoteScoreList)
    mostResult['pearson']=pearsonResult
    resultDict['most']=mostResult
    
    #similar
    similarResult=dict()
    kappaResult=dict()
    spearmanResult=dict()
    pearsonResult=dict()
    for key in objScoreDict:
        objScoreList=objScoreDict[key]
        similarList=[]
        for id in idList:
            humanScores=[score*0.2-0.1 for score in scoreDict[id]]
            conv=convDict[id]
            hslist=[abs(score-float(conv[key])) for score in humanScores]
            similarList.append(humanScores[hslist.index(min(hslist))])
        #kappa
        kappaResult[key]=getKappaScore(objScoreList,similarList)
        #spearman
        spearmanResult[key]=getSpearmanScore(objScoreList,similarList)
        #pearson
        pearsonResult[key]=getPearsonScore(objScoreList,similarList)
    similarResult['kappa']=kappaResult
    similarResult['spearman']=spearmanResult
    similarResult['pearson']=pearsonResult
    resultDict['similar']=similarResult
    
    #写入excel
    workbook = xlwt.Workbook(encoding = 'ascii')
    for scoreName in resultDict:
        worksheet = workbook.add_sheet(scoreName)
        scoreResult=resultDict[scoreName]
        for i,st in enumerate(scoreTypes):
            worksheet.write(i, 0, label = st)
            worksheet.write(i, 1, label = scoreResult['kappa'][st])
            worksheet.write(i, 2, label = scoreResult['spearman'][st][0])
            worksheet.write(i, 3, label = scoreResult['spearman'][st][1])
            worksheet.write(i, 4, label = scoreResult['pearson'][st][0])
            worksheet.write(i, 5, label = scoreResult['pearson'][st][1])
    workbook.save(model+'.xls')
import pickle
import numpy as np
import functools

lang='cn'
model='rule'

def cmpDict(dict1,dict2):
    if dict1['diff']>dict2['diff']:
        return 1
    if dict1['diff']<dict2['diff']:
        return -1
    else:
        return 0

with open('chatbot'+lang+'.dict','rb') as humanFile,open(lang+'.score.dict','rb') as machineFile,\
    open(lang+'.'+model+'.diff','w',encoding='utf-8') as resultFile:
    humanScoreList=pickle.load(humanFile)
    machineScoreList=pickle.load(machineFile)
    convList=[]
    for key in humanScoreList:
        value=humanScoreList[key]
        convDict=dict()
        machineScore=machineScoreList[key]
        convDict['machinescore']=float(machineScore[model+'score'])
        humanScore=[score*0.2-0.1 for score in value]
        convDict['avgscore']=np.mean(humanScore)
        scoreSet=list(set(value))
        hslist=[value.count(score) for score in scoreSet]
        convDict['mostscore']=scoreSet[hslist.index(max(hslist))]*0.2-0.1
        convDict['id']=key
        convDict['diff']=(abs(convDict['machinescore']-convDict['avgscore'])+abs(convDict['machinescore']-convDict['mostscore']))/2
        convList.append(convDict)
    newConvList=sorted(convList,key=functools.cmp_to_key(cmpDict))
    for conv in newConvList:
        machineScore=machineScoreList[conv['id']]
        resultFile.write(machineScore['key']+'\n')
        resultFile.write(machineScore['value']+'\n')
        resultFile.write(machineScore[model+'key']+'\n')
        resultFile.write(machineScore[model+'value']+'\n')
        resultFile.write(str(conv['avgscore'])+'\t'+str(conv['mostscore'])+'\t'+str(conv['machinescore'])+'\n')
        resultFile.write('\n')


    

    
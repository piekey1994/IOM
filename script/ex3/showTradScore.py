import pickle
import numpy as np
import functools

lang='en'

def cmpDict(dict1,dict2):
    if dict1['diff']>dict2['diff']:
        return 1
    if dict1['diff']<dict2['diff']:
        return -1
    else:
        return 0

with open('chatbot'+lang+'.dict','rb') as humanFile,open(lang+'.score.dict','rb') as machineFile,\
    open(r'D:\SCI\结果\weibo.100w.test.value','r',encoding='utf-8') as valueFile,open(lang+'.trad.diff','w',encoding='utf-8') as resultFile:
    humanScoreList=pickle.load(humanFile)
    machineScoreList=pickle.load(machineFile)
    valueList=valueFile.readlines()
    convList=[]
    for key in humanScoreList:
        value=humanScoreList[key]
        ref=valueList[key-1].strip()
        convDict=machineScoreList[key]
        convDict['rulescore']=float(convDict['rulescore'])
        convDict['learnscore']=float(convDict['learnscore'])
        convDict['bleu']=float(convDict['bleu'])
        convDict['gm']=float(convDict['gm'])
        convDict['ea']=float(convDict['ea'])
        convDict['ve']=float(convDict['ve'])
        humanScore=[score*0.2-0.1 for score in value]
        convDict['avgscore']=np.mean(humanScore)
        scoreSet=list(set(value))
        hslist=[value.count(score) for score in scoreSet]
        convDict['mostscore']=scoreSet[hslist.index(max(hslist))]*0.2-0.1
        machineAvg=(convDict['rulescore']+convDict['learnscore'])/2
        tradAvg=(convDict['bleu']+convDict['gm']+convDict['ea']+convDict['ve'])/4
        humanAvg=(convDict['avgscore']+convDict['mostscore'])/2
        convDict['id']=key
        convDict['ref']=ref
        convDict['diff']=abs(machineAvg-tradAvg)-abs(machineAvg-humanAvg)
        convList.append(convDict)
    newConvList=sorted(convList,key=functools.cmp_to_key(cmpDict))
    bleu=0
    gm=0
    ea=0
    ve=0
    for conv in newConvList:
        resultFile.write(conv['key']+'\n')
        resultFile.write(conv['value']+'\n')
        resultFile.write(conv['ref']+'\n')
        resultFile.write('%f\t%f\t%f\t%f\n' %(conv['bleu'],conv['gm'],conv['ea'],conv['ve']))
        bleu+=conv['bleu']
        gm+=conv['gm']
        ea+=conv['ea']
        ve+=conv['ve']
        resultFile.write('rulescore:'+str(conv['rulescore'])+'\n')
        resultFile.write('rulekey:'+conv['rulekey']+'\n')
        resultFile.write('rulevalue:'+conv['rulevalue']+'\n')
        resultFile.write('learnscore:'+str(conv['learnscore'])+'\n')
        resultFile.write('learnkey:'+conv['learnkey']+'\n')
        resultFile.write('learnvalue:'+conv['learnvalue']+'\n')
        resultFile.write(str(conv['avgscore'])+'\t'+str(conv['mostscore'])+'\n')
        resultFile.write('\n')
    print('%s:%f,%f,%f,%f\n'%(lang,bleu/100,gm/100,ea/100,ve/100))
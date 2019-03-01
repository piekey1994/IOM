import pickle

name='weibo.100w.test.nmt'

with open('D:\\SCI\\结果\\weibo.100w\\'+name+'.score','r',encoding='utf-8') as learnFile, open('D:\\SCI\\结果\\rulescore\\'+name+'.score','r',encoding='utf-8') as ruleFile,\
open('D:\\SCI\\结果\\'+name+'.score.txt','r',encoding='utf-8') as otherFile, open(name+'.dict','wb') as scoreFile:
    scoreDict=dict()
    for learnLine,ruleLine,otherLine in zip(learnFile,ruleFile,otherFile):
        learnValues=learnLine.strip().split('\t')
        ruleValues=ruleLine.strip().split('\t')
        otherValues=otherLine.strip().split('\t')
        tempDict={
            'key':learnValues[1],
            'value':learnValues[2],
            'rulekey':ruleValues[3],
            'rulevalue':ruleValues[4],
            'rulescore':ruleValues[5],
            'learnkey':learnValues[3],
            'learnvalue':learnValues[4],
            'learnscore':learnValues[5],
            'bleu':otherValues[1],
            'gm':otherValues[2],
            'ea':otherValues[3],
            've':otherValues[4]
        }
        scoreDict[int(learnValues[0])]=tempDict
    pickle.dump(scoreDict, scoreFile)
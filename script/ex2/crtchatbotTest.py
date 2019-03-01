import pickle
with open(r'D:\IOM\script\ex3\ex3.en.orig.txt','r',encoding='utf-8') as orgFile,\
open(r'D:\IOM\script\ex3\Twitter.100w.test.att.dict','rb') as dictFile,\
open('en.key','w',encoding='utf-8') as inputFile,open('en.value','w',encoding='utf-8') as outputFile:
    scoreDict=pickle.load(dictFile)
    for line in orgFile:
        id=int(line.strip())
        inputFile.write(scoreDict[id]['key']+'\n')
        outputFile.write(scoreDict[id]['value']+'\n')
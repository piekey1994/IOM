import pickle
with open('cn.score.dict','rb') as scoreFile:
    readFiles=[]
    hist=[0]*11
    for i in range(11):
        f=open('cn.read.'+str(i),'w',encoding='utf-8')
        readFiles.append(f)
    scoreDict=pickle.load(scoreFile)
    for id in scoreDict:
        conv=scoreDict[id]
        score=(float(conv['rulescore'])+float(conv['learnscore']))/2
        num=int(score*10)
        hist[num]+=1
        readFiles[num].write(str(id)+'\n')
        readFiles[num].write(conv['key']+'\n')
        readFiles[num].write(conv['value']+'\n')
        readFiles[num].write(conv['rulekey']+'\n')
        readFiles[num].write(conv['rulevalue']+'\n')
        readFiles[num].write(conv['learnkey']+'\n')
        readFiles[num].write(conv['learnvalue']+'\n')
        readFiles[num].write('\n')
    print(hist)
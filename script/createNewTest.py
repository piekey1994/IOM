pre='weibo1.'
with open(pre+'low.test.key','r',encoding='utf-8') as lowkeyFile,open(pre+'low.test.value','r',encoding='utf-8') as lowvalueFile,\
open(pre+'medium.test.key','r',encoding='utf-8') as mediumkeyFile,open(pre+'medium.test.value','r',encoding='utf-8') as mediumvalueFile,\
open(pre+'high.test.key','r',encoding='utf-8') as highkeyFile,open(pre+'low.test.value','r',encoding='utf-8') as highvalueFile,\
open(pre+'syn.test.key','w',encoding='utf-8') as synkeyFile,open(pre+'syn.test.value','w',encoding='utf-8') as synvalueFile:

    i=0
    for (lowkeyLine,lowvalueLine,mediumkeyLine,mediumvalueLine,highkeyLine,highvalueLine) in zip(lowkeyFile,lowvalueFile,\
    mediumkeyFile,mediumvalueFile,highkeyFile,highvalueFile):
        if i>=500:
            break
        synkeyFile.write(lowkeyLine)
        synkeyFile.write(mediumkeyLine)
        synkeyFile.write(highkeyLine)
        synvalueFile.write(lowvalueLine)
        synvalueFile.write(mediumvalueLine)
        synvalueFile.write(highvalueLine)
        i += 1
    

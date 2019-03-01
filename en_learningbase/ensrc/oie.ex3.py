from oie_cn import OIEModel
import traceback
import sys

reload(sys)
sys.setdefaultencoding('utf8')
modelname='nmt'
                

oieModel=OIEModel('../models/27_07_2018_09_55/',False)
scoreFiles=[]
scoreNums=[0]*11

for i in range(0,11):
    f=open('Twitter.100w.test.'+modelname+'.score'+str(i),'w')
    scoreFiles.append(f)

scoreSum=0

with open('Twitter.100w.test.key', 'r') as keyFile, open('Twitter.100w.test.'+modelname+'.output', 'r') as valueFile,\
open('Twitter.100w.test.'+modelname+'.score','w') as out_file:


    id = 1

    for key,value in zip(keyFile,valueFile):
        
        question=key.strip()
        answer=value.strip()
        try:
            score,tri1,tri2=oieModel.getGMScoreAndTri(question,answer)
            scoreSum+=score
            out_file.write(str(id)+'\t'+question+'\t'+answer+'\t'+tri1+'\t'+tri2+'\t'+str(score)+'\n')
            xh=int(score*10)
            scoreFiles[xh].write(str(id)+'\t'+question+'\t'+answer+'\t'+tri1+'\t'+tri2+'\t'+str(score)+'\n')
            scoreNums[xh]+=1
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        id+=1
        if id % 100 == 0:
            print "%d done %s" % (id,str(scoreNums)) 
        
    print modelname+" finish %d score:%f" %(id,scoreSum)
    

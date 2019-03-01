from oie import OIEModel
import traceback
import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "7"

reload(sys)
sys.setdefaultencoding('utf8')
modelname='fairseq'
                

oieModel=OIEModel('../models/27_07_2018_09_55/',False)
scoreNums=[0]*11

scoreSum=0

with open('Twitter.100w.test.key', 'r') as keyFile, open('twitter.100w.out.sys', 'r') as valueFile,\
open('Twitter.100w.learn.'+modelname+'.score','w') as out_file:


    id = 1

    for key,value in zip(keyFile,valueFile):
        
        question=key.strip()
        answer=value.strip()
        try:
            score=oieModel.getGMScore(question,answer)
            scoreSum+=score
            
            xh=int(score*10)
            scoreNums[xh]+=1
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        id+=1
        if id % 100 == 0:
            print "%d done %s" % (id,str(scoreNums)) 
        
    print modelname+" finish %d score:%f" %(id,scoreSum)
    out_file.write("%d done %s\n" % (id,str(scoreNums)))
    out_file.write(modelname+" finish %d score:%f\n" %(id,scoreSum))
    

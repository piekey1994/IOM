from oie_cn import OIEModel
import traceback
import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "5"

reload(sys)
sys.setdefaultencoding('utf8')

oieModel=OIEModel('../models/13_12_2018_21_27/',False)
modelname='fairseq'
scoreNums=[0]*11
scoreSum=0



with open('weibo.100w.test.key', 'r') as keyFile, open('weibo.100w.sys', 'r') as valueFile,\
open('weibo.100w.'+modelname+'.score','w') as out_file:


    id = 1

    for key,value in zip(keyFile,valueFile):
        
        question=key.strip().replace(' ','')
        answer=value.strip().replace(' ','')
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

    

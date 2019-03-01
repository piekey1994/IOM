from oie_cn import OIEModel
import traceback
import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

reload(sys)
sys.setdefaultencoding('utf8')
modelname='cn.old.learn'
                

oieModel=OIEModel('../models/13_12_2018_21_27/',False)

with open('weibo.100w.test.key', 'r') as keyFile, open('weibo.100w.test.beam1.gm.output', 'r') as valueFile,\
open('weibo.100w.'+modelname+'.score','w') as out_file:

    triNum=0
    num = 0

    for key,value in zip(keyFile,valueFile):
        
        question=key.strip().replace(' ','')
        answer=value.strip().replace(' ','')
        try:
            if oieModel.checkTriple(question,answer):
                triNum+=1
            num+=1
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        if num % 100 == 0:
            print "%d trinum: %d" % (num,triNum) 
        
    print modelname+" finish %d trinum: %d" %(num,triNum)
    out_file.write(modelname+" finish %d trinum: %d" %(num,triNum))
    

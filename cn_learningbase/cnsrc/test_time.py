from oie_cn import OIEModel
import traceback
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

oieModel=OIEModel('../models/13_12_2018_21_27/',False)



with open('weibo.100w.test.key', 'r') as keyFile, open('weibo.100w.test.nmt.output', 'r') as valueFile:
    id = 0
    time_start=time.time()
    for key,value in zip(keyFile,valueFile):
        
        question=key.strip().replace(' ','')
        answer=value.strip().replace(' ','')
        try:
            score=oieModel.getGMScore(question,answer)
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        id+=1
        if id == 10000:
            break
    time_end=time.time()        
    print 'totally cost',time_end-time_start

    

import xiaoiceapi 
import time
import traceback
xb = xiaoiceapi.xiaoiceApi()

with open('cn.key','r',encoding='utf-8') as textFile,open('xiaobing.output','w',encoding='utf-8') as resultFile:
    i=0
    for line in textFile:
        try:
            key=line.strip()
            result=xb.chat(key)
            time.sleep(1)
            if result['type']=='text':
                resultFile.write(result['text']+'\n')
            else:
                for j in range(3):
                    result=xb.chat(key)
                    time.sleep(1)
                    if result['type']=='text':
                        resultFile.write(result['text']+'\n')
                        break
                    elif j==2:
                        resultFile.write(result['text']+'\n')
                        break
            i += 1
            print(key+":"+str(result['text']))
        except:
            traceback.print_exc()
    print('finish:%d' % i)

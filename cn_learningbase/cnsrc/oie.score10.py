from oie_cn import OIEModel
import traceback
import sys

reload(sys)
sys.setdefaultencoding('utf8')

oieModel=OIEModel('../models/13_12_2018_21_27/',False)
outfilename='weibo.bert.output.'
with open('weibo.txt', 'r') as in_file:
    outfile=[]
    for i in range(11):
        of=open(outfilename+str(i), 'w')
        outfile.append(of)
    scorehist=[0 for i in range(11)]
    sentence_number = 0
    text_line = in_file.readline()
    while text_line:
        sentence = text_line.strip()#去除空白
        if sentence=="" or len(sentence.split('\t'))!=2:
            text_line=in_file.readline()
            continue
        question=sentence.split('\t')[0]
        answer=sentence.split('\t')[1]
        if question=="" or answer=="":
            text_line=in_file.readline()
            continue
        try:
            score=oieModel.getGMScore(question,answer)
            scorehist[int(score*10)]+=1
            outfile[int(score*10)].write(question+'\t'+answer+'\t'+str(score)+'\n')
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            print "%d done %s" % (sentence_number,str(scorehist)) 
        text_line = in_file.readline()
        
    print "分析对话数为：%d\n 分数分布：%s\n" % (sentence_number,str(scorehist))
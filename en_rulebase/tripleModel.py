# coding: utf-8 

class tripleModel:
    def __init__(self,nlp):
        self.nlp=nlp.nlp

    def linkWordByChildren(self,wordList,i):
        begin=i
        end=i
        while(True):
            flag=0
            if len(wordList[begin]['children'])!=0 and wordList[begin]['children'][0]<begin:
                begin=wordList[begin]['children'][0]
                flag += 1
            if len(wordList[end]['children'])!=0 and wordList[end]['children'][-1]>end:
                end=wordList[end]['children'][-1]
                flag += 1
            if flag==0:
                break
        return self.linkWord(wordList,begin,end)

    def linkWordByHead(self,wordList,head,i):
        if head < i :
            return self.linkWord(wordList,head,i)
        else:
            return self.linkWord(wordList,i,head)
    

    def findHead(self,wordList,i,begin):
        head=i
        while(True):
            if wordList[head]['dep']!='ROOT' and wordList[head]['head']>begin:
                head=wordList[head]['head']
            else:
                break
        return head

    def linkWord(self,wordList,begin,end):
        result=''
        for i in range(begin,end+1):
            result = result+' '+wordList[i]['text']
        return result[1:]
    
    def getOwnership(self,wordList,i):
        fullWords=self.linkWordByChildren(wordList,i)
        if fullWords.find('the')!=-1 and fullWords.find('of')!=-1:
            B=fullWords[fullWords.find('the')+4:fullWords.find('of')]
            A=fullWords[fullWords.find('of')+3:]
            return (A,B)
        if fullWords.find("'s")!=-1:
            A=fullWords[:fullWords.find("'s")]
            B=fullWords[fullWords.find("'s")+3:]
            return (A,B)
        return ('','')

    #提取三元组函数
    def getTriple(self,sentence):
        sentence=sentence.lower()
        doc=self.nlp(sentence)
        #存储句法依存关系
        wordList=[]   
        for token in doc:
            wordList.append(
                {
                    'text':token.text,
                    'i':token.i,
                    'pos':token.pos_,
                    'dep':token.dep_,
                    'head':token.head.i,
                    'children':[child.i for child in token.children]
                }
            )
        result=dict()  
        result['hasTriple']=False
        result['triple']=[sentence]
        result['pron']=[False]   
        #寻找疑问词
        interrogativeList=['what','where','who','which']
        beList=['are','am','is','was','were']
        interrogative=-1
        for word in wordList:
            if word['text'] in interrogativeList:
                interrogative=word['i']
                break
        if interrogative != -1:
            #找出疑问词关联的动词
            itgHead=wordList[interrogative]['head']
            #不是修饰从句
            if wordList[itgHead]['head'] >= interrogative:
                if wordList[interrogative]['dep'] == 'det':
                    Cindex=wordList[interrogative]['head']
                    C=self.linkWord(wordList,interrogative,Cindex)
                else:
                    Cindex=interrogative
                    C=wordList[interrogative]['text']
                #存在do（缺宾语）Who did he hit / what movie do you like
                if wordList[Cindex]['dep'].endswith('obj') or wordList[Cindex]['dep'].endswith('advmod') :
                    #找到动词谓语的起源
                    Bindex=self.findHead(wordList,wordList[Cindex]['head'],Cindex)
                    B=self.linkWordByHead(wordList,Bindex,wordList[Cindex]['head'])
                    #寻找主语
                    if wordList[Bindex]['dep']=='prep':
                        Bindex=wordList[Bindex]['head']
                    BChildren=wordList[Bindex]['children']
                    for child in BChildren:
                        if wordList[child]['dep'].endswith('ubj') and wordList[child]['head']==Bindex:
                            Aindex=child
                            A=self.linkWordByChildren(wordList,Aindex)
                            result['hasTriple']=True
                            result['triple']=[A,B,C]
                            result['pron']=[False,False,True]  
                #缺表语
                if wordList[Cindex]['dep'].endswith('attr') or wordList[Cindex]['dep'].endswith('advmod') :
                    bev=wordList[wordList[Cindex]['head']]
                    if bev['text'] in beList and len(bev['children'])>1:
                        ubj=wordList[bev['children'][1]]
                        (A,B)=self.getOwnership(wordList,ubj['i'])
                        if A=='' and B=='':
                            A=self.linkWordByChildren(wordList,ubj['i'])
                            B= bev['text']
                        result['hasTriple']=True
                        result['triple']=[A,B,C]
                        result['pron']=[False,False,True]  

                #缺主语（主动）
                if wordList[Cindex]['dep'].endswith('ubj'):
                    Bindex=wordList[Cindex]['head']
                    if len(wordList[Bindex]['children'])>1:
                        B=wordList[Bindex]['text']
                        A=C
                        Cindex=wordList[Bindex]['children'][1]
                        C=self.linkWordByChildren(wordList,Cindex)
                        result['hasTriple']=True
                        result['triple']=[A,B,C]
                        result['pron']=[True,False,False] 
                #缺主语（被动）
                if wordList[Cindex]['dep'].endswith('ubjpass'):
                    A=C
                    Bindex = wordList[Cindex]['head']
                    for child in wordList[Bindex]['children']:
                        if wordList[child]['dep']=='auxpass':
                            begin=child
                            if Bindex<wordList[Bindex]['children'][-1]:
                                end=wordList[Bindex]['children'][-1]
                                B=self.linkWord(wordList,begin,end)
                                if len(wordList[end]['children'])>0:
                                    for c in wordList[end]['children']:
                                        if wordList[c]['dep']=='pobj':
                                            C=self.linkWordByChildren(wordList,c)
                                            result['hasTriple']=True
                                            result['triple']=[A,B,C]
                                            result['pron']=[True,False,False] 
        else:        
            #其他情况：
            for word in wordList:
                if word['dep']=='ROOT':
                    A=''
                    B=word['text']
                    C=''
                    for child in word['children']:
                        if wordList[child]['dep'].endswith('ubj') or wordList[child]['dep'].endswith('ubjpass'):
                            Aindex=child
                            A=self.linkWordByChildren(wordList,Aindex)
                            break
                    for child in word['children']:
                        if wordList[child]['dep'].endswith('obj') or wordList[child]['dep'].endswith('attr') :
                            Cindex=child
                            C=self.linkWordByChildren(wordList,Cindex)
                            break
                        elif wordList[child]['dep'].endswith('prep'):
                            newword=wordList[child]
                            for newchild in newword['children']:
                                if wordList[newchild]['dep'].endswith('obj') or wordList[newchild]['dep'].endswith('attr') :
                                    Cindex=newchild
                                    C=self.linkWordByChildren(wordList,Cindex)
                                    break
                    if A!='' and C!='':
                        result['hasTriple']=True
                        result['triple']=[A,B,C]
                        result['pron']=[False,False,False] 
                        if A in interrogativeList:
                            result['pron'][0]=True
                        if C in interrogativeList:
                            result['pron'][2]=True
        
        return result

                
                


                        
                            







        





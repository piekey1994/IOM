# -*- coding: utf-8 -*-

class tripleModel:
    def __init__(self,ltp):
        self.segmentor = ltp.segmentor
        self.postagger = ltp.postagger
        self.parser = ltp.parser
    def findSpWord(self,sentence):
        spWords=['怎样','啥','哪','什么','谁']
        for word in spWords:
            if sentence.find(word)!=-1:
                return True

        return False

    #提取三元组函数
    def getTriple(self,sentence):
        #print(sentence)
        segmentor=self.segmentor
        postagger=self.postagger
        parser=self.parser

        result=dict()#存储结果
        result['hasTriple']=False
        result['triple']=[sentence]
        result['pron']=[False]
        words = segmentor.segment(sentence)#分词
        postags = postagger.postag(words)#词性标注
        arcs = parser.parse(words, postags)#句法分析
        #为句子中的每个词语维护一个保存句法依存儿子节点的字典
        child_dict_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index].head == index + 1:
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)
        
        #模板1：先找动词‘是’作为分析依据
        #默认一句话第一个‘是’连接的主谓宾为所需的三元组
        for index in range(len(postags)):
            A=''
            B=''
            C=''
            if postags[index] == 'v' and words[index]=='是':
                child_dict=child_dict_list[index]
                #如果‘是’前后存在主语和宾语,则B和C可以找到
                if 'SBV' in child_dict and 'VOB' in child_dict:
                    CTempIndex=child_dict['VOB'][0]
                    CTempChild_dict=child_dict_list[CTempIndex]
                    #1. 中国的电脑是美国产的
                    if postags[CTempIndex] == 'v'  and 'SBV' in CTempChild_dict:
                        Bindex=CTempIndex
                        B=words[Bindex]
                        Aindex=child_dict['SBV'][0]
                        A=self.complete_e(words, postags, child_dict_list, Aindex)
                        Cindex=CTempChild_dict['SBV'][0]
                        C = self.complete_e(words, postags, child_dict_list, Cindex)
                    else:
                        Cindex=child_dict['VOB'][0]
                        C=self.complete_e(words, postags, child_dict_list, Cindex)
                        BTempIndex=child_dict['SBV'][0]
                        BTempChild_dict=child_dict_list[BTempIndex]
                        if 'ATT' in BTempChild_dict:
                            ATempIndex=BTempChild_dict['ATT'][0]
                            #3. 长城的长度是一米八
                            if postags[ATempIndex] == 'n':
                                Aindex=ATempIndex
                                A=self.complete_e(words, postags, child_dict_list, Aindex)
                                Bindex=BTempIndex
                                B=words[Bindex]
                            #4. 美丽的小红是女神
                            else:
                                Aindex=BTempIndex
                                A=self.complete_e(words, postags, child_dict_list, Aindex)
                                Bindex=index
                                B=words[Bindex]
                        else:
                            Aindex=BTempIndex
                            A=self.complete_e(words, postags, child_dict_list, Aindex)
                            Bindex=index
                            B=words[Bindex]
                    result['hasTriple']=True
                    result['triple']=[A,B,C]
                    result['pron']=[False,False,False]
                    #out_file.write("%s\t(%s, %s, %s)" % (sentence,A, B, C))
                    #如果主语是代词的话
                    if A=='' or self.findSpWord(A):
                        result['pron'][0]=True
                        #out_file.write('\twarning:主语为代词，该三元组缺失主语')
                    if C=='' or self.findSpWord(C):
                        result['pron'][2]=True
                        #out_file.write('\twarning:属性值为代词，该三元组缺失属性值')
                    #out_file.write('\n')
                    if result['pron'][0] and result['pron'][2]:
                        result['hasTriple']=False
                    return result
                            
        #模板2：不存在是，则尝试寻找其他动词作为连接依据
        for index in range(len(postags)):
            if postags[index] == 'v':
                child_dict=child_dict_list[index]
                if 'SBV' in child_dict:
                    if 'VOB' in child_dict:
                        Aindex=child_dict['SBV'][0]
                        Cindex=child_dict['VOB'][0]
                        A = self.complete_e(words, postags, child_dict_list, Aindex)
                        B = words[index]
                        C = self.complete_e(words, postags, child_dict_list, Cindex)
                        result['hasTriple']=True
                        result['triple']=[A,B,C]
                        result['pron']=[False,False,False]
                        #out_file.write("%s\t(%s, %s, %s)" % (sentence,A, B, C))
                        #如果主语是代词的话
                        if self.findSpWord(A):
                            result['pron'][0]=True
                            #out_file.write('\twarning:主语为代词，该三元组缺失主语')
                        if self.findSpWord(C):
                            result['pron'][2]=True
                            #out_file.write('\twarning:属性值为代词，该三元组缺失属性值')
                        #out_file.write('\n')
                        if result['pron'][0] and result['pron'][2]:
                            result['hasTriple']=False
                        return result
                    #介宾关系
                    elif 'CMP' in child_dict:
                        tempchild_dict = child_dict_list[child_dict['CMP'][0]]
                        if 'POB' in tempchild_dict:
                            Aindex=child_dict['SBV'][0]
                            Cindex=tempchild_dict['POB'][0]
                            A = self.complete_e(words, postags, child_dict_list, Aindex)
                            B = words[index]
                            C = self.complete_e(words, postags, child_dict_list, Cindex)
                            #out_file.write("%s\t(%s, %s, %s)" % (sentence,A, B, C))
                            result['hasTriple']=True
                            result['triple']=[A,B,C]
                            result['pron']=[False,False,False]
                            #如果主语是代词的话
                            if self.findSpWord(A):
                                result['pron'][0]=True
                                #out_file.write('\twarning:主语为代词，该三元组缺失主语')
                            if self.findSpWord(C):
                                result['pron'][2]=True
                                #out_file.write('\twarning:属性值为代词，该三元组缺失属性值')
                            #out_file.write('\n')
                            if result['pron'][0] and result['pron'][2]:
                                result['hasTriple']=False
                            return result
        #模板3：该句子可能为一个单独的答案
        for index in range(len(postags)):
            #找出句子核心
            if arcs[index].relation=='HED':
                A = self.complete_e(words, postags, child_dict_list, index)
                result['hasTriple']=False
                result['triple']=[A]
                result['pron']=[False]
                #out_file.write("%s\t(%s)\twarning:该句子没有三元组，可能为一个单独的答案\n" % (sentence,A))
                break
        return result


    #将与实体存在ATT关系的词汇串联起来
    def complete_e(self,words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix
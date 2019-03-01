# -*- coding: utf-8 -*-
""" Usage:
trained_oie_extractor [--model=MODEL_DIR] --in=INPUT_FILE --out=OUTPUT_FILE [--tokenize] [--conll]

Run a trined OIE model on raw sentences.

MODEL_DIR - Pretrained RNN model folder (containing model.json and pretrained weights).
INPUT FILE - File where each row is a tokenized sentence to be parsed with OIE.
OUTPUT_FILE - File where the OIE tuples will be output.
tokenize - indicates that the input sentences are NOT tokenized.
conll - Print a CoNLL represenation with probabilities

Format of OUTPUT_FILE:
    Sent, prob, pred, arg1, arg2, ...
"""

from rnn.model_old import load_pretrained_rnn
from docopt import docopt
import logging
import nltk
import re
import numpy as np
from collections import defaultdict
from w2vModel import w2vModel

import jieba.posseg as pseg

logging.basicConfig(level = logging.DEBUG)

class Trained_oie:
    """
    Compose OIE extractions given a pretrained RNN OIE model predicting classes per word
    """
    def __init__(self, model, tokenize):
        """
        model - pretrained supervised model
        tokenize - instance-wide indication whether all of the functions should
                   tokenize their input
        """
        self.model = model
        self.tokenize = tokenize

    def split_words(self, sent):
        """
        Apply tokenization if needed, else just split by space
        sent - string
        """
        return [word for word,flag in pseg.cut(sent)]


    def get_extractions(self, sent):
        """
        Returns a list of OIE extractions for a given sentence
        sent - a list of tokens
        """
        ret = []

        for ((pred_ind, pred_word), labels) in self.model.predict_sentence(sent):
            cur_args = []
            cur_arg = []
            probs = []

            # collect args
            for (label, prob), word in zip(labels, sent):
                if label.startswith("A"):
                    cur_arg.append(word)
                    probs.append(prob)

                elif cur_arg:
                    cur_args.append(cur_arg)
                    cur_arg = []

            # Create extraction
            if cur_args:
                ret.append(Extraction(sent,
                                      pred_word,
                                      cur_args,
                                      probs
                                  ))
        return ret

    def conll_with_prob(self, sent):
        """
        Returns a conll representation of sentence
        Format:
        word index, word, pred_index, label, probability
        """
        #logging.debug("Parsing: {}".format(sent))
        sent = self.split_words(sent)
        ret = ""
        for ((pred_ind, pred_word), labels) in self.model.predict_sentence(sent):
            for (word_ind, ((label, prob), word)) in enumerate(zip(labels, sent)):
                ret+= "\t".join(map(str,
                                         [word_ind, word, pred_ind, label, prob]
                                     )) + '\n'
            ret += '\n'
        return ret

    def parse_sent(self, sent):
        """
        Returns a list of extractions for the given sentence
        sent - a tokenized sentence
        tokenize - boolean indicating whether the sentences should be tokenized first
        """
        #logging.debug("Parsing: {}".format(sent))
        return self.get_extractions(self.split_words(sent))

    def parse_sents(self, sents):
        """
        Returns a list of extractions per sent in sents.
        sents - list of tokenized sentences
        tokenize - boolean indicating whether the sentences should be tokenized first
        """
        return [self.parse_sent(sent)
                for sent in sents]

class Extraction:
    """
    Store and print an OIE extraction
    """
    def __init__(self, sent, pred, args, probs,
                 calc_prob = lambda probs: 1.0 / (reduce(lambda x, y: x * y, probs) + 0.001)):
        """
        sent - Tokenized sentence - list of strings
        pred - Predicate word
        args - List of arguments (each a string)
        probs - list of float in [0,1] indicating the probability
               of each of the items in the extraction
        calc_prob - function which takes a list of probabilities for each of the
                    items and computes a single probability for the joint occurence of this extraction.
        """
        self.sent = sent
        self.calc_prob = calc_prob
        self.probs = probs
        self.prob = self.calc_prob(self.probs)
        self.pred = pred
        self.args = args
        #logging.debug(self)

    def __str__(self):
        """
        Format (tab separated):
        Sent, prob, pred, arg1, arg2, ...
        """
        return '\t'.join(map(str,
                             [' '.join(self.sent),
                              self.prob,
                              self.pred,
                              '\t'.join([' '.join(arg)
                                         for arg in self.args])]))
class Mock_model:
    """
    Load a conll file annotated with labels And probabilities
    and present an external interface of a trained rnn model (through predict_sentence).
    This can be used to alliveate running the trained model.
    """
    def __init__(self, conll_file):
        """
        conll_file - file from which to load the annotations
        """
        self.conll_file = conll_file
        self.dic, self.sents = self.load_annots(self.conll_file)

    def load_annots(self, conll_file):
        """
        Updates internal state according to file
        for ((pred_ind, pred_word), labels) in self.model.predict_sentence(sent):
                    for (label, prob), word in zip(labels, sent):
        """
        cur_ex = []
        cur_sent = []
        pred_word = ''
        ret = defaultdict(lambda: {})
        sents = []

        # Iterate over lines and populate return dictionary
        for line_ind, line in enumerate(conll_file.split('\n')):
            if not (line_ind % pow(10,5)):
                pass
                #logging.debug(line_ind)
            line = line.strip()
            if not line:
                if cur_ex:
                    assert(pred_word != '') # sanity check
                    cur_sent = " ".join(cur_sent)

                    # This is because of the dups bug --
                    # doesn't suppose to happen any more
                    ret[cur_sent][pred_word] = (((pred_ind, pred_word), cur_ex),)

                    sents.append(cur_sent)
                    cur_ex = []
                    pred_ind = -1
                    cur_sent = []
            else:
                word_ind, word, pred_ind, label, prob = line.split('\t')
                prob = float(prob)
                word_ind = int(word_ind)
                pred_ind = int(pred_ind)
                cur_sent.append(word)
                if word_ind == pred_ind:
                    pred_word = word
                cur_ex.append((label, prob))
        return (self.flatten_ret_dic(ret, 1),
                list(set(sents)))

    def flatten_ret_dic(self, dic, num_of_dups):
        """
        Given a dictionary of dictionaries, flatten it
        to a dictionary of lists
        """
        ret = defaultdict(lambda: [])
        for sent, preds_dic in dic.iteritems():
            for pred, exs in preds_dic.iteritems():
                ret[sent].extend(exs * num_of_dups)
        return ret

    def predict_sentence(self, sent):
        """
        Return a pre-predicted answer
        """
        return self.dic["".join(sent).encode('utf-8')]

example_sent = "The Economist is an English language weekly magazine format newspaper owned by the Economist Group\
    and edited at offices in London."


class OIEModel:
    def __init__(self,model_dir,tokenize):
        self.model = load_pretrained_rnn(model_dir)
        self.oie = Trained_oie(self.model,tokenize = tokenize)
        self.w2v = w2vModel(self.model.emb.word2VecModel)

    def getTriple(self,str1):
        bio1=self.oie.conll_with_prob(str1.strip())
        bio='\n\n'.join([bio1])
        try:
            mock = Mock_model(bio)
        except:
            return []
        sents = mock.sents
        oie = Trained_oie(mock,tokenize = False)
        for sent in sents:
            return oie.parse_sent(sent.strip())

    def checkTriple(self,str1,str2):
        tri1=self.getTriple(str1)
        tri2=self.getTriple(str2)
        if tri1 == None or tri2==None or tri1==[] or tri2==[]:
            return False
        else:
            return True

    def getGMScore(self,str1,str2):
        M=0.8

        tri1=self.getTriple(str1)
        tri2=self.getTriple(str2)
        if tri1 == None or tri2==None or tri1==[] or tri2==[]:
            return 0
        maxScore=0
        maxTri1=tri1[0]
        maxTri2=tri2[0]
        for t1 in tri1:
            if t1!=None:
                for t2 in tri2:
                    if t2 != None:
                        predScore=self.w2v.getGMDistance(t1.pred,t2.pred)
                        argScore=0
                        for arg1 in t1.args:
                            tempscore=0
                            for arg2 in t2.args:
                                tempscore+=self.w2v.getGMDistance(arg1,arg2)
                            tempscore/=len(t2.args)
                            argScore+=tempscore
                        argScore/=len(t1.args)
                        sumScore=(predScore+argScore)/2
                        if sumScore>maxScore:
                            maxScore=sumScore
                            maxTri1=t1
                            maxTri2=t2
        #惩罚函数
        if maxScore>M:
            maxScore=M*(1-maxScore)/(1-M)
        return maxScore/M
    
    def getGMScoreAndTri(self,str1,str2):
        M=0.8

        tri1=self.getTriple(str1)
        tri2=self.getTriple(str2)
        if tri1 == None or tri2==None or tri1==[] or tri2==[]:
            return 0,'',''
        maxScore=0
        maxTri1=tri1[0]
        maxTri2=tri2[0]
        for t1 in tri1:
            if t1!=None:
                for t2 in tri2:
                    if t2 != None:
                        predScore=self.w2v.getGMDistance(t1.pred,t2.pred)
                        argScore=0
                        for arg1 in t1.args:
                            tempscore=0
                            for arg2 in t2.args:
                                tempscore+=self.w2v.getGMDistance(arg1,arg2)
                            tempscore/=len(t2.args)
                            argScore+=tempscore
                        argScore/=len(t1.args)
                        sumScore=(predScore+argScore)/2
                        if sumScore>maxScore:
                            maxScore=sumScore
                            maxTri1=t1
                            maxTri2=t2
        tri1Str='(pred:'+maxTri1.pred+' | args:'+str(maxTri1.args)+')'.replace('\t',',')
        tri2Str='(pred:'+maxTri2.pred+' | args:'+str(maxTri2.args)+')'.replace('\t',',')
        
        #惩罚函数
        if maxScore>M:
            maxScore=M*(1-maxScore)/(1-M)
        return maxScore/M,tri1Str,tri2Str

    def getEAScore(self,str1,str2):
        tri1=self.getTriple(str1)
        tri2=self.getTriple(str2)
        if tri1 == None or tri2==None:
            return 0
        maxScore=0
        for t1 in tri1:
            if t1!=None:
                for t2 in tri2:
                    if t2 != None:
                        predScore=self.w2v.getEADistance(t1.pred,t2.pred)
                        argScore=0
                        for arg1 in t1.args:
                            tempscore=0
                            for arg2 in t2.args:
                                tempscore+=self.w2v.getEADistance(arg1,arg2)
                            tempscore/=len(t2.args)
                            argScore+=tempscore
                        argScore/=len(t1.args)
                        sumScore=(predScore+argScore)/2
                        if sumScore>maxScore:
                            maxScore=sumScore
        return maxScore
    def getVEScore(self,str1,str2):
        tri1=self.getTriple(str1)
        tri2=self.getTriple(str2)
        if tri1 == None or tri2==None:
            return 0
        maxScore=0
        for t1 in tri1:
            if t1!=None:
                for t2 in tri2:
                    if t2 != None:
                        predScore=self.w2v.getVEDistance(t1.pred,t2.pred)
                        argScore=0
                        for arg1 in t1.args:
                            tempscore=0
                            for arg2 in t2.args:
                                tempscore+=self.w2v.getVEDistance(arg1,arg2)
                            tempscore/=len(t2.args)
                            argScore+=tempscore
                        argScore/=len(t1.args)
                        sumScore=(predScore+argScore)/2
                        if sumScore>maxScore:
                            maxScore=sumScore
        return maxScore

                




if __name__ == "__main__":
    oieModel=OIEModel('../models/27_07_2018_09_55/',False)
    with open('reddit.sql.conv','r') as redditFile,open('reddit.sql.oldTri','w') as resultFile:
        for line in redditFile:
            lineList=line.strip().split('\t')
            id=lineList[0]
            question=lineList[1]
            answer=lineList[2]
            score,tri1,tri2=oieModel.getGMScore(question,answer)
            resultFile.write(id+'\t'+str(score)+'\t'+str(tri1)+'\t'+str(tri2)+'\n')
    

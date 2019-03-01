# -*- coding: utf-8 -*-
import sys
import traceback
from nlpModel import nlpModel
from tripleModel import tripleModel

#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

print('加载模型中...')
NlpModel = nlpModel()
TripleModel=tripleModel(NlpModel)

print('开始读取文件')
#读取文件
in_file_name = "test_file\\train.oie.sent"
out_file_name = "test_file\\train.oie.sent.output.txt"

if len(sys.argv) > 1:
    in_file_name = sys.argv[1]

if len(sys.argv) > 2:
    out_file_name = sys.argv[2]

#默认一行只允许存在一句话
with open(in_file_name, 'r',encoding='utf-8') as in_file,open(out_file_name, 'w',encoding='utf-8') as out_file:
    sentence_number = 0
    triple_number = 0
    text_line = in_file.readline()
    while text_line:
        sentence = text_line.strip()#去除空白
        if sentence=="" or len(sentence)>1000:
            text_line=in_file.readline()
            continue
        # print(sentence)
        # triple_result = TripleModel.getTriple(sentence)#开始提取三元组    
        try:
            #print(sentence)
            triple_result = TripleModel.getTriple(sentence)#开始提取三元组
            if triple_result['hasTriple']:
                triple_number += 1
                pron=triple_result['pron']
                triple=triple_result['triple']
                out_file.write("%s\t(%s, %s, %s)" % (sentence,triple[0], triple[1], triple[2]))
                if pron[0]:
                    out_file.write('\twarning:主语为代词，该三元组缺失主语')
                elif pron[2]:
                    out_file.write('\twarning:属性值为代词，该三元组缺失属性值')
                out_file.write('\n')
            else:
                out_file.write("%s\t(%s)\twarning:该句子没有三元组，可能为一个单独的答案\n" % (sentence,triple_result['triple'][0]))
            out_file.flush()
        except:
            traceback.print_exc()
        sentence_number += 1
        if sentence_number % 100 == 0:
            print("%d done" % (sentence_number))
        text_line = in_file.readline()

print("分析句子数为：%d\n提取三元组数为：%d\n" % (sentence_number,triple_number))

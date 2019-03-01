# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor,Postagger,Parser



class ltpModel:
    def __init__(self):
        #加载模型pyltp
        
        LTP_DATA_DIR = 'ltp_data'  # ltp模型目录的路径
        cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
        par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

        self.segmentor = Segmentor()  # 初始化分词实例
        self.segmentor.load(cws_model_path) 
        self.postagger = Postagger() # 初始化词性标注实例
        self.postagger.load(pos_model_path)  
        self.parser = Parser() # 初始化句法分析实例
        self.parser.load(par_model_path)  
    def __del__(self):
        # 释放模型
        self.segmentor.release()  
        self.postagger.release()  
        self.parser.release() 
    





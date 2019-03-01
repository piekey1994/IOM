# Information-oriented Metric (IOM)

这个项目提供一个基于信息三元组的自动化对话系统评估方法，它有基于规则和基于神经网络两种实现，并且支持中英文。该项目还包含了做对话系统评估常用的工具和数据集。

## Reference

如果你使用IOM评估你的聊天机器人，请引用下面的文章：

Liu P, Zhong S, Ming Z, et al. Information-Oriented Evaluation Metric for Dialogue Response Generation Systems[C]//2018 IEEE 30th International Conference on Tools with Artificial Intelligence (ICTAI). IEEE, 2018: 780-785.

```
@inproceedings{liu2018information,
  title={Information-Oriented Evaluation Metric for Dialogue Response Generation Systems},
  author={Liu, Peiqi and Zhong, Sheng-hua and Ming, Zhong and Liu, Yan},
  booktitle={2018 IEEE 30th International Conference on Tools with Artificial Intelligence (ICTAI)},
  pages={780--785},
  year={2018},
  organization={IEEE}
}
```

## Rule-base Method

### 中文

环境：python3

安装流程：

- 下载ltp模型文件放到ltp_data目录，参考https://github.com/HIT-SCIR/pyltp
- pip install -r requirements.txt

评估流程：

参考qaMatch.ex2.py文件

### 英文

环境：python3

安装流程：

- pip install -r requirements.txt
- python -m spacy download en

评估流程：

参考qaMatch.ex2.py文件

## Learning-base Mthod

该方法由[RNN-OIE](https://github.com/gabrielStanovsky/supervised-oie)改进而来，增加了类似beam search的机制提高提取率，并且增加了中文的版本

### 中文

环境：python2

安装流程：
- pip install -r requirements.txt
- 安装[recurrentshop](https://github.com/farizrahman4u/recurrentshop)库
```
git clone https://www.github.com/datalogai/recurrentshop.git
cd recurrentshop
python setup.py install
```
- 安装[seq2seq](https://github.com/farizrahman4u/seq2seq.git)库
```
pip install git+https://github.com/farizrahman4u/seq2seq.git
```
- 下载预训练embedding模型

    将hyperparams\confidence.json中的"emb_filename"参数改成任意一个你下载好的中文预训练word2vec文件，可参考本项目后面的Tools。如果使用的是非二进制的文本模式的预训练模型，则需要将cnsrc\rnn\load_pretrained_word_embeddings.py第40行换成binary=False模式

训练流程：
```
cd ./cnsrc/
./train.sh
```
评估流程：

参考oie.ex2.py，需要将OIEModel的参数改成你训练好的文件

预训练模型：

成熟的中文预训练模型还未完成，暂缺

### 英文

环境：python2

安装流程：

- pip install -r requirements.txt
- 安装[recurrentshop](https://github.com/farizrahman4u/recurrentshop)库
```
git clone https://www.github.com/datalogai/recurrentshop.git
cd recurrentshop
python setup.py install
```
- 安装[seq2seq](https://github.com/farizrahman4u/seq2seq.git)库
```
pip install git+https://github.com/farizrahman4u/seq2seq.git
```
- 下载预训练embedding模型
```
cd ./pretrained_word_embeddings/
./download_external.sh
```

训练流程：

下载训练数据，解压到data目录：链接：https://pan.baidu.com/s/1_lQ9DOd-fnzbgDRmtu5bpA 提取码：qv1e 
```
cd ./ensrc/
./train.sh
```
评估流程：

参考oie.ex2.py，需要将OIEModel的参数改成你训练好的文件

预训练模型：

链接：https://pan.baidu.com/s/1kE_QoEUanjLTJY33Qx0kig 提取码：ith2 

下载后解压到models目录

## Dialogue Generation Models

[Chatbot](https://github.com/piekey1994/IOM/tree/master/chatbot)目录里存放了三个常用的Seq2seq模型（GNMT，Fairseq，Transformer），已经写好了一些运行脚本在里面方便直接训练。这里同时也列出了一些收集到的开源聊天机器人：

- [GNMT](https://github.com/tensorflow/nmt) :基于LSTM的seq2seq模型，支持attention和beam search。按照我脚本里的参数训练可以训练出能用的聊天机器人，默认参数对话生成质量很差，会出现大量重复内容（在10w和100w的语料库上做过测试）
- [Fairseq](https://github.com/pytorch/fairseq) :基于CNN的seq2seq模型，直接用默认参数训练对话语料结果会出现大量重复的短语，原因未知。
- [Transformer](https://github.com/tensorflow/tensor2tensor/) :只基于attention的seq2seq模型，他需要自己建立脚本，已经写好在chatbot目录里了（在10w级的语料训练效果比GNMT好，100w训练结果会出现大量重复短语，原因未知）
- [AMM](https://github.com/lancopku/AMM) :2018年EMNLP的一篇对话系统的改进，在100w语料库训练时会显存耗尽（Tesla V100）
- [jiweil's NDG](https://github.com/jiweil/Neural-Dialogue-Generation) :李jiwei的各种对话系统的代码集合，里面我只尝试了NAACL2016提出的模型，但是在运行10w以上稍大的语料库会报显存耗尽（Tesla V100）
- [TA-Seq2Seq](https://github.com/LynetteXing1991/TA-Seq2Seq) :AAAI2017提出的利用主题词优化的Seq2seq模型，没跑过不知效果如何。

## Tools

这里收集了一些常用工具，尽量追求有SOTA水平的版本

### Word2Vec

- 英文预训练模型：[word2vec-GoogleNews-vectors](https://github.com/mmihaltz/word2vec-GoogleNews-vectors)

  备份地址（链接：https://pan.baidu.com/s/1ISv2EUuV5pOFwtC7kubmUw 
提取码：n6ld）

    python代码：
```python
import gensim
word2VecModel = gensim.models.KeyedVectors.load_word2vec_format(r"GoogleNews-vectors-negative300.bin", binary=True)
}
```
- 中文预训练模型：[Chinese Word Vectors](https://github.com/Embedding/Chinese-Word-Vectors)

    python代码：
```python
import gensim
word2VecModel = gensim.models.KeyedVectors.load_word2vec_format(r"merge_sgns_bigram_char300.txt", binary=False)
}
```

### 传统的对话系统评估方法

- BLEU

    参考链接：https://cloud.tencent.com/developer/article/1042161

    python代码
```python
from nltk.translate.bleu_score import sentence_bleu
def bleu(question,answer):
    resultWords=question.split()
    targetWords=answer.split()
    reference = [targetWords]
    candidate = resultWords
    score = sentence_bleu(reference, candidate) #默认是BLEU-4
    # score = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)) #BLEU-1
    return score
}
```
- Embedding-based method

    基于词向量的对话评估方法，与BLEU一样依赖参考答案。具体实现细节参考文章：https://arxiv.org/abs/1603.08023

    python代码参考[script](https://github.com/piekey1994/IOM/tree/master/script)目录的calc_time.py

- Distinct-N

    计算生成句子中的Unigram和Bigram，具体实现参考文章：https://arxiv.org/pdf/1510.03055.pdf

    python代码参考[script](https://github.com/piekey1994/IOM/tree/master/script)目录的evalResult.py

### 中文分词与词性分析

- [pkuseg](https://github.com/lancopku/PKUSeg-python)：北大19年发布的中文分词工具包，达到了SOTA水平，远胜于较为常用的[jieba](https://github.com/fxsjy/jieba)
- [jieba](https://github.com/fxsjy/jieba)：可以分词也可以做词性分析

- [pynlpir](https://github.com/tsroten/pynlpir)：中科院的中文NLP工具箱，用它做分词和词性分析会有坑。它运行大规模的句子分词时，会不断调整内部结构，导致你跑同一个句子，只要上下文不一样，就会出现分词结果不一样的问题。
- [常用中文词性标注对照表](https://gist.github.com/guodong000/54c74ed55575fa2305b6afd0cf46ba7c)：适用于jieba和nlpir

### 依存语法分析

- [spacy](https://spacy.io/)：英文依存语法分析工具
- [pyltp](https://github.com/HIT-SCIR/pyltp)：中文依存语法分析工具，哈工大出品

### Sentence2Vec

- [bert](https://github.com/google-research/bert)：谷歌出品的杰作

    python接口：https://github.com/hanxiao/bert-as-service

### 主观对话评估平台

基于amaze-UI和CI框架编写的用于人类评估对话的打分系统，代码在[web](https://github.com/piekey1994/IOM/tree/master/web)目录

![主界面](https://github.com/piekey1994/IOM/blob/master/web/1551430284(1).png)


### 语料爬虫工具

自己编写的百度贴吧爬虫，有时候会假死，有待更新：https://github.com/piekey1994/TieBa-Messenger-Bot-CN

### 商用聊天机器人自动对话工具

在[script\ex2\chatbot](https://github.com/piekey1994/IOM/tree/master/script/ex2/chatbot)目录中，有一个[tuling](http://www.turingapi.com/)机器人的api，还有一个[小冰](https://github.com/yanwii/msxiaoiceapi)的api，还有一个我自己编写的英文聊天机器人[mitsuku](https://www.pandorabots.com/mitsuku/)的api。**请不要滥用这些api！！！**

## Datasets

这里主要存放一些聊天机器人训练用的语料库。
+ 英文
    + [cornell_movie_dialogs_corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) ：10,292对电影角色之间的220,579次会话，质量未知。
    + [Ubuntu Dialogue Corpus](https://www.kaggle.com/rtatman/ubuntu-dialogue-corpus) ：100w级的对话，没训练过，质量未知。
    + [twitter_en big](https://github.com/Marsan-Ma-zz/chat_corpus) ：Twitter 100w级的语料库，但里面有很多特朗普选举时期的对话，质量一般。
    + [Reddit](https://archive.org/details/2015_reddit_comments_corpus) ：Reddit亿级以上的语料库，我自己处理了其中500w组保存成方便的格式，质量略差于Twitter。我处理的版本下载地址（https://pan.baidu.com/s/1dsQ0IJBpyJx5M_mCvWSBPw 提取码：xb2g ）
+ 中文
    + [Douban Conversation Corpus](https://github.com/MarkWuNLP/MultiTurnResponseSelection)：微软和北航出品的豆瓣语料库，100w级，质量未知
    + [小黄鸡](https://github.com/fate233/dgk_lost_conv/tree/master/results) ：小黄鸡聊天机器人产生的对话语料，50w级别，质量一般。
    + Weibo ：华为诺亚实验室2015年整理的微博语料库，质量上乘，原地址已经找不到了，不过我已经下载清理完，地址如下（https://pan.baidu.com/s/1aI10LRVriuztm1TjqVD7gg 提取码：mssd ）

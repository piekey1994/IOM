import jieba.posseg as pseg

def nlpir_parser(text):
    """
    Parse sentence with static instance.
    """
    tags = pseg.cut(text)
    result=[]
    i=0
    for word,flag in tags:
        res={
            'i':i,
            'tag':flag,
            'word':word
        }
        result.append(res)
        i+=1
    return result


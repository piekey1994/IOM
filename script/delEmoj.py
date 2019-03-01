import emoji

def remove_emoji(text):
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

with open('cleaned_corpus_en.txt','r',encoding='utf-8',errors='ignore') as chatFile,open('Twitter.big.txt','w',encoding='utf-8') as resultFile:
    lines=chatFile.readlines()
    i=0
    conv=''
    while(True):
        line1=remove_emoji(lines[i]).strip()
        line2=remove_emoji(lines[i+1]).strip()
        i+=2
        if len(line1)>0 and len(line2)>0:
            resultFile.write(line1+'\t'+line2+'\n')
        if i>=len(lines):
            break
        

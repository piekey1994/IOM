pre='Twitter.100w.'
names=['train','test']
results=['dialogues_text.txt','test_samples.txt']
for name,result in zip(names,results):
    with open(pre+name+'.key','r',encoding='utf-8') as keyFile,open(pre+name+'.value','r',encoding='utf-8') as valueFile,open(result,'w',encoding='utf-8') as resultFile:
        for keyLine,valueLine in zip(keyFile,valueFile):
            key=keyLine.strip()
            value=valueLine.strip()
            resultFile.write(key+' __eou__ '+value+' __eou__ '+'\n')
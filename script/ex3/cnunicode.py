name=r'D:\SCI\结果\weibo.100w\weibo.100w.test.nmt.score'

# for i in range(11):
#     with open(name+str(i),'r',encoding='utf-8') as uniFile,open(name+str(i)+'.utf8','w',encoding='utf-8') as utf8File:
#         for line in uniFile:
#             values=line.strip().split('\t')
#             utf8File.write(values[0]+'\t'+values[1]+'\t'+values[2]+'\t')
#             value3=''
#             if values[3].strip()!='':
#                 tri=values[3].split('|')
#                 args=tri[1].replace("u'","'").encode('utf-8').decode('unicode_escape')
#                 value3=tri[0]+args
#             value4=''
#             if values[4].strip()!='':
#                 tri=values[4].split('|')
#                 args=tri[1].replace("u'","'").encode('utf-8').decode('unicode_escape')
#                 value4=tri[0]+args
#             utf8File.write(value3+'\t'+value4+'\t'+values[5]+'\n')

with open(name,'r',encoding='utf-8') as uniFile,open(name+'.utf8','w',encoding='utf-8') as utf8File:
    for line in uniFile:
        values=line.strip().split('\t')
        utf8File.write(values[0]+'\t'+values[1]+'\t'+values[2]+'\t')
        value3=''
        if values[3].strip()!='':
            tri=values[3].split('|')
            args=tri[1].replace("u'","'").encode('utf-8').decode('unicode_escape')
            value3=tri[0]+args
        value4=''
        if values[4].strip()!='':
            tri=values[4].split('|')
            args=tri[1].replace("u'","'").encode('utf-8').decode('unicode_escape')
            value4=tri[0]+args
        utf8File.write(value3+'\t'+value4+'\t'+values[5]+'\n')

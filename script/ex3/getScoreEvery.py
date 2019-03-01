import pymysql
import pickle

databaseName='chatboten'
# ul=[2,3,5,7,9,11,12,13,14,15]
# ul=[2,3,5,6,7,8,9,10,11,12,13] cn2
ul=[9,10,12,13,16,17,18,19,20,22] #en
# userlist=[9,10,12,13,16,17,18,19,20,22]

for u in ul:
    userlist=[u]
    resultDict=dict()
    with open(databaseName+str(u)+'.dict','wb') as resultFile:
        db = pymysql.connect("localhost","root","112119110",databaseName,use_unicode=True, charset="utf8" )
        cursor = db.cursor()
        sql='SELECT id FROM conversation WHERE 1'
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            resultDict[row[0]]=[]
        for user in userlist:
            sql='select cid,score from relscore where uid='+str(user)
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                resultDict[row[0]].append(row[1])
        pickle.dump(resultDict, resultFile)
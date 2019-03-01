import pymysql
import pickle

databaseName='chatboten'
userlist=[9,10,12,16,17,18,19,20,22]
# userlist=[2,3,5,7,9,11,12,14,15]
# userlist=[9,10,12,19,22]
# userlist=[2,5,11,12,14]
resultDict=dict()

with open(databaseName+'.dict','wb') as resultFile:
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
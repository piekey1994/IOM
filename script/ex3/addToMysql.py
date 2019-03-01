import pymysql
import pickle
 
# 打开数据库连接
db = pymysql.connect("localhost","root","112119110","chatbotcn",use_unicode=True, charset="utf8" )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

with open('weibo.100w.test.nmt.dict','rb') as scoreFile,open('ex3.cn.orig.txt','r',encoding='utf-8') as origFile:
    scoreDict=pickle.load(scoreFile)
    for line in origFile:
        id=int(line.strip())
        allScore=scoreDict[id]
        sql = """INSERT INTO conversation(id,question,
                answer)
                VALUES (%d, '%s', '%s')""" % (id,allScore['key'].replace("'",''),allScore['value'].replace("'",''))
        print(sql)
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
 
# 关闭数据库连接
db.close()

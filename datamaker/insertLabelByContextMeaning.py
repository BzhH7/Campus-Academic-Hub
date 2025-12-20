#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cmath import nan
import MySQLdb

db = MySQLdb.connect("localhost", "root", "248433", "nsm")
cursor = db.cursor()
keyword = input("请输入关键词语： ")

sql = "SELECT cno FROM course WHERE cname LIKE"+" '%"+str(keyword)+"%';"
result_cno = []
try:
    cursor.execute(sql)
    result_cno = list(cursor.fetchall())
    print(len(result_cno))
    print(result_cno[0][0])
    while(True):
        label = input("请输入标签名： ")
        flag = input("确认为"+str(len(result_cno))+"门课程打上"+str(label)+"作为标签吗（Y/N）：")
        if flag == 'Y':
            for i in range(len(result_cno)):
                sql = "INSERT INTO clabel VALUES('"+str(result_cno[i][0])+"','"+str(label)+"');"
                cursor.execute(sql)
            go = input("是否继续？（Y/N）")
            if go == 'Y':
                continue
            else:
                break
        else:
            print("bye")
            break;
except :
    print('1')

db.commit()
db.close()
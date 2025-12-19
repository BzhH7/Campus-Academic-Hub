#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
from cmath import nan
import MySQLdb

db = MySQLdb.connect("localhost", "root", "2001929yyh", "nsm")
cursor = db.cursor()
keywordA = input("请输入关键词语A： ")
sqlA = "SELECT cno FROM course WHERE cname LIKE"+" '%"+str(keywordA)+"%';"
keywordB = input("请输入关键词语B： ")
sqlB = "SELECT cno FROM course WHERE cname LIKE"+" '%"+str(keywordB)+"%';"
result_cnoA = []
result_cnoB = []

cursor.execute(sqlA)
result_cnoA = list(cursor.fetchall())
cursor.execute(sqlB)
result_cnoB = list(cursor.fetchall())

for i in range(len(result_cnoA)):
    for j in range(len(result_cnoB)):
        value = random.randint(0,8)
        sql = "INSERT INTO crelation VALUES('"+str(result_cnoA[i][0])+"','"+str(result_cnoB[j][0])+"','"+str(value)+"');"
        cursor.execute(sql)


db.commit()
db.close()
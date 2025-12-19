#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cmath import nan

import MySQLdb
import pandas as pd

df = pd.read_excel("../data/course_data2.xlsx")
data = df.values

keys = df.keys().values
keys = keys
print(keys)
print(data[0][0])

db = MySQLdb.connect("localhost", "root", "2001929yyh", "nsm")

cursor = db.cursor()
'''
CREATE TABLE `nsm`.`course` (
  `cno` VARCHAR(20) NOT NULL,
  `cname` VARCHAR(20) NOT NULL,
  `tname` INT NOT NULL,
  `dname` INT NOT NULL,
  `cclf` VARCHAR(20) NULL,
  `credit` INT NOT NULL,
  `csche` VARCHAR(50) NULL,
  `exam` INT NULL,
  `length` INT NULL,
  `slimit` INT NULL,
  `campus` INT NULL,
  `description` VARCHAR(300) NULL,
  PRIMARY KEY (`cno`));
  ['课程代码0' '课程名称1' '学分2' '教学班代码3' '教学班名称4' '课程类别5' '任务类型6' '开课部门7' '授课教师8' '日期时间地点人员9'
 '考核方式10' '授课校区11' '授课语言12' '总学时13' '重修人数14' '选课人数上限15' '是否必修16']
'''
cnt = 0
for i in range(len(data)):
    cnt = cnt +1
    print(cnt)
    # print("fuck")
    if type(data[i][8]) is float:
        tname = "none"
    else:
        tname = str(data[i][8].split(";")[0])

    sql = "INSERT INTO course VALUES('" + str(data[i][3]) + "','" + str(data[i][1]) + "','" + tname + "','" + str(data[i][7]) + "','" + str(data[i][5]) + "','" + str(data[i][2]) + "','" + str(data[i][9]) + "','" + str(data[i][10]) + "','" + str(data[i][13]) + "','" + str(data[i][15]) + "','" + str(data[i][11]) + "'," + "'nothing');"
    # print(sql)
    try:
        cursor.execute(sql)
    except:
        print("fuck")

db.commit()
db.close()


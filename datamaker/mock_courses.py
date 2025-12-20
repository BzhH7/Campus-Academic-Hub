import MySQLdb
from faker import Faker
import random

# 配置数据库连接 (请修改你的密码!)
# 注意：host, user, password, database
db = MySQLdb.connect("localhost", "root", "248433", "nsm", charset='utf8')
cursor = db.cursor()
fake = Faker("zh_CN")  # 使用中文生成器

# 预设一些数据让它看起来更像计算机学院的课
prefixes = ['高级', '基础', '应用', '现代', '工程']
subjects = ['数据库', '操作系统', '计算机网络', '算法分析', '机器学习', '深度学习', '编译原理', '软件工程', '前端开发', '云计算', '网络安全']
suffixes = ['原理', '实践', '导论', '设计', '系统']
depts = ['计算机学院', '软件学院', '网络空间安全学院', '人工智能学院']

print("开始生成虚假课程数据...")

for i in range(100):  # 生成100门课
    # 1. 构造数据
    cno = f"CS{2025000 + i}"  # 课程号: CS2025000...
    
    # 随机组合课程名
    cname = random.choice(prefixes) + random.choice(subjects) + random.choice(suffixes)
    # 去重稍微处理一下(简单粗暴)
    if random.random() > 0.8: cname += "(双语)"
    
    tname = fake.name()  # 随机老师名字
    dname = random.choice(depts)  # 学院
    cclf = random.choice(['必修', '选修', '通识课'])
    credit = random.randint(1, 5)  # 学分
    
    # 上课时间地点 (伪造: 1-16周 周一 1-2节)
    csche = f"1-{random.randint(12,18)}周 周{random.choice(['一','二','三','四','五'])} {random.randint(1,4)*2-1}-{random.randint(1,4)*2}节"
    
    exam = random.choice(['考试', '考查', '大作业'])
    length = credit * 16
    slimit = random.randint(30, 150)
    campus = random.choice(['长安校区', '友谊校区'])
    description = fake.text(max_nb_chars=50) # 随机生成一段介绍

    # 2. 插入数据库
    sql = "INSERT INTO course VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (cno, cname, tname, dname, cclf, credit, csche, exam, length, slimit, campus, description)
    
    try:
        cursor.execute(sql, val)
    except Exception as e:
        print(f"插入失败: {e}")

db.commit()
db.close()
print("成功生成 100 门课程数据！")
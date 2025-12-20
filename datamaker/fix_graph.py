import MySQLdb
import random

# 配置数据库连接 (记得改密码!)
db = MySQLdb.connect("localhost", "root", "248433", "nsm", charset='utf8')
cursor = db.cursor()

# 1. 前端 dashboard.vue 里写死的三个标签
target_labels = ['计算机视觉', '机器人', '数学基础']

print("正在获取现有课程列表...")
cursor.execute("SELECT cno, cname FROM course")
all_courses = list(cursor.fetchall())

if len(all_courses) < 10:
    print("错误：数据库里课程太少！请先运行之前的 mock_courses.py 生成课程数据。")
    exit()

print("开始注入特定标签数据...")

# 清理旧的测试标签（可选，防止重复报错）
try:
    cursor.execute("DELETE FROM clabel")
    cursor.execute("DELETE FROM crelation")
    db.commit()
except:
    pass

selected_courses = []

# 2. 为每个标签随机分配 5-8 门课程
for label in target_labels:
    # 随机抽 5 到 8 门课
    courses_to_label = random.sample(all_courses, random.randint(5, 8))
    
    for course in courses_to_label:
        cno = course[0]
        cname = course[1]
        selected_courses.append(cno)
        
        # 插入标签表 (clabel)
        sql_label = "INSERT INTO clabel (cno, label) VALUES (%s, %s)"
        try:
            cursor.execute(sql_label, (cno, label))
            print(f"  [标签] 课程 {cname} -> 打上 '{label}' 标签")
        except Exception as e:
            pass # 忽略重复主键

# 3. 建立这些课程之间的“连线”关系 (crelation)
# 如果课程之间没有关系，图就是一个个孤立的点，也不好看
print("开始构建课程关系网...")
for i in range(len(selected_courses)):
    for j in range(len(selected_courses)):
        if i != j and random.random() > 0.7: # 30%的概率建立连线
            cno1 = selected_courses[i]
            cno2 = selected_courses[j]
            weight = random.randint(1, 10)
            
            sql_relation = "INSERT INTO crelation (fcno, scno, value) VALUES (%s, %s, %s)"
            try:
                cursor.execute(sql_relation, (cno1, cno2, weight))
            except:
                pass

db.commit()
db.close()
print("\n✅ 修复完成！")
print("现在去刷新网页，你的'课程关系图'应该会非常漂亮了！")
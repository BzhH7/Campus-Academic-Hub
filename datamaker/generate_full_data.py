import MySQLdb
from faker import Faker
import random

# ================= 配置区域 =================
# TODO: 请务必修改这里的密码！
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "248433" 
DB_NAME = "nsm"
# ===========================================

db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME, charset='utf8')
cursor = db.cursor()
fake = Faker("zh_CN")

# 定义丰富的标签库 (这些都会成为图谱上的分类)
TAGS = [
    "人工智能", "深度学习", "计算机视觉", "Web开发", "后端架构", 
    "大数据", "网络安全", "嵌入式", "游戏开发", "区块链", 
    "云计算", "数学基础", "通识教育"
]

# 课程命名前缀和后缀
PREFIXES = ['高级', '应用', '现代', '工程', '基础', '核心', '分布式']
SUFFIXES = ['原理', '实践', '导论', '设计', '系统', '分析', '算法']

def clear_data():
    print("🧹 正在清空旧数据...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE clabel")
    cursor.execute("TRUNCATE TABLE crelation")
    cursor.execute("TRUNCATE TABLE course")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.commit()

def generate_courses(num=120):
    print(f"📚 正在生成 {num} 门课程...")
    courses = []
    
    for i in range(num):
        # 1. 生成课程基本信息
        cno = f"CS{2025000 + i}"
        # 随机分配一个标签，作为课程名的主题
        tag = random.choice(TAGS)
        cname = f"{tag}-{random.choice(PREFIXES)}{random.choice(SUFFIXES)}"
        
        tname = fake.name()
        dname = f"计算机学院-{random.randint(1,5)}系"
        cclf = "必修" if random.random() > 0.3 else "选修"
        credit = random.randint(1, 6)
        csche = f"1-16周 {fake.day_of_week()} {random.randint(1,4)*2-1}-{random.randint(1,4)*2}节"
        exam = random.choice(['闭卷', '开卷', '大作业'])
        length = credit * 16
        slimit = random.randint(30, 200)
        campus = random.choice(['长安校区', '友谊校区'])
        desc = fake.paragraph(nb_sentences=3)

        sql = """
            INSERT INTO course 
            (cno, cname, tname, dname, cclf, credit, csche, exam, length, slimit, campus, description) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (cno, cname, tname, dname, cclf, credit, csche, exam, length, slimit, campus, desc))
            # 存下来备用
            courses.append({'cno': cno, 'tag': tag})
        except Exception as e:
            print(f"插入课程失败: {e}")
    
    db.commit()
    return courses

def assign_labels_and_relations(courses):
    print("🏷️ 正在给每门课打标签并建立关系...")
    
    relation_count = 0
    
    for course in courses:
        cno = course['cno']
        tag = course['tag']
        
        # 1. 必做：插入标签 (直接用刚才生成课程时分配的主题)
        # 也可以随机多加一个标签，让它属于多个分类
        try:
            cursor.execute("INSERT INTO clabel (cno, label) VALUES (%s, %s)", (cno, tag))
            if random.random() > 0.8: # 20%的概率拥有双标签
                extra_tag = random.choice(TAGS)
                if extra_tag != tag:
                    cursor.execute("INSERT INTO clabel (cno, label) VALUES (%s, %s)", (cno, extra_tag))
        except:
            pass

        # 2. 建立关系 (让同标签的课更容易连在一起)
        # 随机找 1-3 个“前置课程”
        targets = random.sample(courses, random.randint(1, 3))
        for target in targets:
            if target['cno'] != cno:
                # 如果标签相同，权重高；否则权重低
                weight = random.randint(5, 10) if target['tag'] == tag else random.randint(1, 3)
                try:
                    cursor.execute(
                        "INSERT INTO crelation (fcno, scno, value) VALUES (%s, %s, %s)",
                        (cno, target['cno'], weight)
                    )
                    relation_count += 1
                except:
                    pass

    db.commit()
    print(f"🕸️ 成功建立 {relation_count} 条课程关系！")

if __name__ == "__main__":
    try:
        clear_data()
        all_courses = generate_courses(100) # 生成100门课
        assign_labels_and_relations(all_courses)
        print("\n✅ 所有数据生成完毕！")
        print("请刷新前端页面，你将看到一个色彩斑斓的动态知识图谱！")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("请检查数据库密码是否正确，以及数据库服务是否开启。")
    finally:
        db.close()
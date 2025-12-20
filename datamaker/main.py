from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import bs4
from bs4 import BeautifulSoup
import json
from browsermobproxy import Server



opt = webdriver.ChromeOptions()  # 创建Chrome参数对象
opt.headless = False
s = Service(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')

driver = webdriver.Chrome(service=s, options=opt)

driver.get('https://uis.nwpu.edu.cn/cas/login?service=https%3A%2F%2Fjwxt.nwpu.edu.cn%2Fstudent%2Fsso-login')

id = input("输入学号：")
password = input("输入密码： ")
driver.find_element(By.XPATH, '//*[@id="vue_main"]/div[2]/div[3]/div/div[2]/div[3]/div/div/div[1]/ul/li[3]').click()
driver.find_element(By.XPATH, '//*[@id="username"]').clear()
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(id)
driver.find_element(By.XPATH, '//*[@id="password"]').clear()
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="fm1"]/div[4]/div/input[6]').click()

cookie = {}
cookies = ''
print("登陆中，请稍后...")
time.sleep(5)
html = ''
if driver.current_url != 'https://jwxt.nwpu.edu.cn/student/home':

    check_btn = driver.find_element(By.XPATH, '//*[@id="vue_main"]/div[2]/div[4]/div/div/div[2]/div[3]/div[2]/button')
    if (check_btn.is_displayed()):
        print('需要验证')
        check_btn.click()
        code = input('请输入验证码： ')
        code_input = driver.find_element(By.XPATH,
                                         '//*[@id="vue_main"]/div[2]/div[4]/div/div/div[2]/div[3]/div[2]/div[1]/input')
        code_input.send_keys(code)
        confirm_btn = driver.find_element(By.XPATH, '//*[@id="vue_main"]/div[2]/div[4]/div/div/div[3]/span/button')
        while (True):
            if confirm_btn.is_enabled():
                break
        print("登陆中")
        confirm_btn.click()
        time.sleep(5)
        if driver.current_url != 'https://jwxt.nwpu.edu.cn/student/home':
            print("登录失败")
            driver.close()
            exit()
        else:
            print("登录成功1")
            cookies = driver.get_cookies()
            for i in cookies:
                name = i['name']
                value = i['value']
                cookie[name] = value
            driver.get('https://jwxt.nwpu.edu.cn/student/for-std/grade/sheet/semester-index/267291')
            time.sleep(5)

            html = driver.page_source

    else:
        print("登录失败")
        driver.close()
        exit()
    '验证码文本框： //*[@id="vue_main"]/div[2]/div[4]/div/div/div[2]/div[3]/div[2]/div[1]/input'
    '验证码按钮： //*[@id="vue_main"]/div[2]/div[4]/div/div/div[2]/div[3]/div[2]/button'
    '验证码确认按钮： //*[@id="vue_main"]/div[2]/div[4]/div/div/div[3]/span/button'
    '验证失败文本： //*[@id="vue_main"]/div[2]/div[4]/div/div/div[2]/div[3]/div[2]/div[2]'
    time.sleep(1)


else:
    print("登录成功2")
    cookies = driver.get_cookies()
    for i in cookies:
        name = i['name']
        value = i['value']
        cookie[name] = value

    search_box = driver.find_element(By.XPATH, '//*[@id="menu-search"]/a/div/input')
    search_box.send_keys('成绩信息')
    search_box.click()
    driver.find_element(By.XPATH, '// *[ @ id = "menu-search"] / div / ul / li[1] / span').click()

    driver.get('https://jwxt.nwpu.edu.cn/student/for-std/grade/sheet/semester-index/267291')
    time.sleep(5)
    html = driver.page_source

driver.close()

# driver.get
soup = BeautifulSoup(html, 'html.parser')
# 获取 Class 对应的标签
score_table = soup.findAll('table', 'student-grade-table table')
score_board = {}
for i in range(len(score_table)):
    for tr in score_table[i].tbody.find_all('tr'):
        td = tr.find_all('td')
        name = str(td[0].text).split('U')[0]
        GPA = str(td[2].text)
        score = str(td[3].text)
        # print(name+' GPA: '+GPA+' 总成绩: '+score)
        score_board[name] = [GPA, score]
'2020302998'
'wal18339443895,'
print("成绩已加载")
name = input("请输入需要查找的课程名称：")
if name in score_board:
    print(score_board[name])
exit()

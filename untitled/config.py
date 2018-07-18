# config for this test and some function
from requests import post
from requests import put, get
from requests.exceptions import RequestException
# from requests_oauthlib import oauth2_auth

import jsonpath
import smtplib, HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from data import region_id_name, place_name_id, AREAS
from data import login_url, login_json, search_url

# 登录，并获取当前用户token
def login_test(url,json):
    send = post(url=url, json=json)
    state = send.status_code
    login_result = send.json()
    auth_token = login_result['auth_token']

    if (state == 200) and (login_result['name'] == '姚思文'):
        print("        登录成功")
        return (auth_token)
    else :
        e = RequestException
        print(e)

Authorization = login_test(login_url,login_json)
headers = {'Authorization': Authorization}

# 检查入/出境城市，若相同则返回1，不同则返回0
# 单一入/出境城市
def check_start_place(place, path):
    start_place = path.split('-')
    return (place == start_place[0])

def check_finish_place(place, path):
    finish_place = path.split('-')
    return (place == finish_place[len(finish_place)-1])

def check_immigration(start_place, finish_place, path):
    result1 = check_start_place(start_place, path=path)
    result2 = check_finish_place(finish_place, path=path)
    result = int(result1 and result2)
    return (result)

# 检查出入境城市
def check_immigrations(start_place, finish_place, json):
    y = 1
    for i in range(0, len(json['plans'])):
        x = check_immigration(start_place=start_place, finish_place=finish_place, path=json['plans'][i]['path'])
        y = x and y
    return (y)

# 检查搜索结果中所有方案的出行天数，是否在设置的区间内，若在则返回1，不在则返回0
def check_days(min_day, max_day, json):
    y = 1
    for i in range(0, len(json['plans'])):
        x = (json['plans'][i]['days'] in range(min_day, max_day + 1))
        y = x and y
    return (y)

# 检查搜索结果中所有方案的place，是否在选中的区域，若在则返回1，不在则返回0
#
# def check_area(area_name, place_name):
#     for i in range(0, len()):
#         x
#         return 0
#
#     if  place_name_id[place_name] in AREAS[area_name]:
#         return 0
#
# def check_areas(area_name, place_name):

# 检查搜索的POI是否在结果项目中
def check_pois(testcase, result):
    testcase['country_ids'][0]



# 发送邮件
def send_eamil(email_from, email_password, email_to):
    msg = MIMEMultipart()
    msg['from'] = email_from
    msg['to'] = email_to
    msg['subject'] = u'测试报告'

    txt = MIMEText(u"自动化测试报告-HTML", "plain", "utf-8")
    msg.attach(txt)

    # 构造附件
    att = MIMEText(open(u"/Users/Desktop/TestReport/TestReport.html", "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment; filename=TestResult.html"
    msg.attach(att)

    try:
        smtpObj = smtplib.SMTP()
        #smtpObj.connect("hwsmtp.exmail.qq.com","465")
        smtpObj.connect("smtp.163.com","25")
        state = smtpObj.login(email_from,email_password)
        if state[0] == 235:
            smtpObj.sendmail(msg["from"],msg["to"],msg.as_string())
            print(u"邮件发送成功")
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(str(e))

# 生成HTML报告
def creat_report(self):
    print('')

from selenium import webdriver
driver = webdriver.Chrome()
driver.find_element(by='id', value='').click()
# data
import os
from requests import post
from requests.exceptions import RequestException

login_url = ''
login_json = {"email":"","password":""}

search_checker_url = ''

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

# 检查返回结果，是否被命中提醒
# def search_checker(testcase, json):
#     if json['data']['status'] == 'warning':
#         print('测试通过')
#         print(json['data']['title'] + json['data']['reason'])
#         return 1
#
#     else :
#         print('测试失败')
#         print(testcase)
#         return 0

# 检查后端返回的提示信息是否正确
# def check_response(,)

# 发送邮件

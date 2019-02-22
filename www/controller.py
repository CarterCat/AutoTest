import time
from requests import post, get, put
from hashlib import sha1
from unittest import SkipTest
# from creat_plan import unicrm_login_url
unicrm_login_url = ''
# unicrm_login_url = ''

# 通过账号和密码，登录unicrm系统
# 获取用户token，构造请求头
def login_unicrm(email, password):
    json = {'email': email,'password': password}
    Authorization = post(url=unicrm_login_url, json=json).json()['authentication_token']
    headers = {'Authorization': Authorization}
    return headers

# 通过手机号，检查是否创建对应交易
# 通过手机号获取交易列表，
def check_unicrm(email, password, tel):
    url = '' + tel + ''
    time.sleep(5)
    unicrm_result = get(url=url, headers=login_unicrm(email=email, password=password)).json()
    print(unicrm_result['deals'])
    if len(unicrm_result['deals']) :
        creat_time = unicrm_result['deals'][0]['created_at']
        if creat_time in time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):
            return unicrm_result['deals'][0]['callcenter_ticket_id']
        else :
            return 0
    else :
        return 0

# 通过账号和密码，登录udesk系统
# 获取open_api_auth_token，用于鉴权
def login_callcenter( email, password):
    url = ''
    headers = {'content-type': 'application/json'}
    json = {'email': email,'password': password}
    token = post(url=url, json=json, headers=headers).json()
    if token['code'] == 1000:
        return token['open_api_auth_token']
    else:
        print(token['code'])

# 取消udesk工单
# 通过工单ID，设置取消原因"自己人测试"，关闭工单
def cancel_ticket(email, password, ticket_id):
    headers = {'content-type': 'application/json'}
    timestamp = str(int(time.time()))
    open_api_token = login_callcenter(email=email, password=password)
    sign_str = email + '&' + open_api_token + '&' + timestamp
    sign = sha1(sign_str.encode('utf-8')).hexdigest()
    url = '' + ticket_id + '?email=' + email + '&timestamp=' + timestamp + '&sign=' + sign
    cancel_json = {"ticket": {"custom_fields": {"SelectField_7983": "12"}}}
    return (put(url=url, json=cancel_json, headers=headers).json())

# 检查填单成功窗口是否弹出
def check_played(result):
    if result.is_displayed():
        print(result.text)
    else:
        print('提交失败！')
        print(result.text)

# 检查窗口是否打开，如打开，则关闭，用来处理自动弹窗
def close_bookmodal_window(book_modal, close):
    if book_modal.is_displayed():
        close.click()
    else:
        print('~~~~~~~~~测试用例3~~~~~~~~~')
        print('【自动填单窗口，刷新界面后未弹出！】')

# 输出信息，并按照选择的类型，进行输入

class put_info():
    def __init__(self, num):
        self.num = num
    # 检查窗口是否打开
    def output(self, book_modal_win):
        if book_modal_win:
            print('~~~~~~~~~测试用例' + str(self.num) + '~~~~~~~~~')
            print('【自动填单窗口已弹出，进行自动化填单测试！】')
            return 1
        else:
            print('~~~~~~~~~测试用例' + str(self.num) + '~~~~~~~~~')
            print('【自动填单窗口，未弹出！】')

    # 按照类型，输入手机号或微信号
    def data(self, type):
        if type == 'tel':
            print('请输入测试用例' + str(self.num) + '的手机号：（注意不能重复）')
            tel = input('tel' + str(self.num) + ' = ')
            return tel
        elif type == 'wechat':
            print('请输入测试用例' + str(self.num) + '的微信号：（注意不能重复）')
            wechat = input('wechat' + str(self.num) + ' = ')
            return wechat
        else:
            print('类型有误，请确认后重新输入！')

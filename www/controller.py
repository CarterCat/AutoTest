import time
from requests import post, get, put
from hashlib import sha1

# from creat_plan import unicrm_login_url
unicrm_login_url = ''


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
    cancel_json = {"": {"": {"": ""}}}
    return (put(url=url, json=cancel_json, headers=headers).json())

# 检查填单成功窗口是否弹出
def check_played(result):
    if result.is_displayed():
        print('填单成功！')
    else:
        print('填单失败！')
        print(result.text)
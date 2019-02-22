from json import loads, dumps
from random import randint
# testcase

case1 = loads('')
# case2 = loads('')

# url
def return_url():
    print('=====选择测试脚本的运行环境！======')
    environment = input('线上还是测试？')
    if environment == '线上':
        url = 'com'
    else:
        url = 'cc'
    return url

url = return_url()

login_url = '.' + url + ''
search_url = '' + url + ''
audits_url = '' + url + ''
unified_plans_url = '' + url + ''
basic_url = '' + url + ''

# eamil and password

login_json = {"":"","":""}

# data

PATH_ID = {

}


dumps()


def generate_testcase():
    n = randint(1,5)

    while n == 1:
        return True

    while n == 2:
        return True

    while n == 3:
        return True

    while n == 4:
        return True

    while n == 5:
        return True

    else:
        return True

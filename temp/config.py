from requests import post
from requests.exceptions import RequestException
import attr
login_url = ''
login_json = {"email":"","password":""}
search_url = ''

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

class my_post():

    def result(url, json, headers):
        a = post(url=url, json=json, headers=headers).json()
        return (a)

class check():

    def check_days(source, test):
        if source in range(test['days'][0], test['days'][1] + 1):
            return 1
        else:
            return 0

    def check_path(self, start_place, finish_place, source):
        path = source.split('-')
        if (path[0] == start_place) and (path[len(path) - 1] == finish_place):
            return 1
        else:
            return 0

    def search_plans(category, source, test):


    def search_checker(self):


    def is_least(self, type):
        if type == 'LEAST':
            return 1
        else:



def cycle_check(self, json, case, type):

    y = 1
    if type == 'days':
        for i in range(0, len(json['plans'])):
            x = check.check_days(json['plans'][i]['days'], test=case['days'])
            y = x and y
            if json['plans'][i]['step'] == 'LEAST':
                return 1
        return (y)

    if type == 'path':
        for i in range(0, len(json['plans'])):
            x = check.check_path(json['plans'][i]['path'], case['start_place_ids'], case['finish_place_ids'])
            y = x and y
            if json['plans'][i]['step'] == 'LEAST':
                return 1
        return (y)

    if type == 'checker':
        check.search_checker()

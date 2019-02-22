from requests import post, get
from requests import RequestException

from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
from search.data import *

from splinter import browser
b = browser.Browser('chrome',headless=True)

class login():
    def __init__(self):
        self.url = login_url
        self.json = login_json
        self.send = post(url= self.url, json= self.json)
        self.state = self.send.status_code
        self.login_result = self.send.json()

    # def auth_token(self):

    def headers(self):
        if (self.state == 200) and (self.login_result['name'] == ''):
            Authorization = self.login_result['auth_token']
            headers = {'Authorization': Authorization}
            return headers

        else:
            e = RequestException
            print(e)
            raise Exception('当前登录状态：' + str(self.state))


class normal():

    # def __init__(self):

    def is_in_testcase(self, condition, testcase):
        key = testcase.keys()
        print(key)
        if condition in key:
            return True
        else:
            return False

    def is_modify(self, result):
        if result['modify'] != {}:
            raise Exception('妥协搜索结果：' + str(result['unified_plan_id']) + '，此方案的妥协原因为：' + str(result['modify']))
        else:
            return True

    def return_json(self, dict):
        json = str(dict)
        return json.replace('\'',"\"")

    def get_unified_plan_ids(self, plans):
        unified_plan_id = []
        for i in range(0, len(plans)):
            unified_plan_id.append(plans[i]['unified_plan_id'])
        return unified_plan_id

    def get_plan_schedules(self, unified_plan_id):
        url = unified_plans_url + str(unified_plan_id) + '/schedules'
        schedules = get(url= url, headers= login().headers()).json()
        return schedules

    def get_start_place_name(self, plans):
        start_place_name = plans['path'].split('-')[0]
        return start_place_name

    def get_finish_place_name(self, plans):
        finish_place_name = plans['path'].split('-')[len(plans['path'].split('-')) - 1]
        return finish_place_name

    # 超级恶心的for循环们
    def get_unified_plans_pois_is_car_rental(self, unified_plan_ids, testcase):

        categories = []
        y = True
        for i in range(0, len(unified_plan_ids)):
            # 初始化dist方案
            get(url=unified_plans_url + str(unified_plan_ids[i]) + '/basic', headers= login().headers())
            sleep(1)
            unified_plan_schedules = get(url=unified_plans_url + str(unified_plan_ids[i]) + '/schedules', headers= login().headers()).json()

            for n in range(0, len(unified_plan_schedules['schedules'])):
                for m in range(0, len(unified_plan_schedules['schedules'][n]['places'])):
                    for p in range(0, len(unified_plan_schedules['schedules'][n]['places'][m])):
                        for q in range(0, len(unified_plan_schedules['schedules'][n]['places'][m]['pois'])):
                            categories.append(
                                unified_plan_schedules['schedules'][n]['places'][m]['pois'][q]['category'])

            if 'car_rental' in categories:
                continue
            else:
                y = ('car_rental' in categories) and y
                print('不符合条件的方案是：' + str(unified_plan_ids[i]) + '，此方案的自驾情况为：False，当前测试用例的自驾情况为：' + str(testcase['self_drive']))

        return y



class get_result():

    def __init__(self, testcase):
        self.case = testcase
        self.url = search_url
        self.send = post(url= self.url, json= self.case, headers= login().headers())
        self.state = self.send.status_code
        self.json = self.send.json()

    def result(self):
        return self.json

    def plans(self):
        if (self.state == 200) and (self.json['plans'] != []):
            return self.json['plans']
        else:
            print('当前接口返回值：' + str(self.state) + '，搜索出了' + str(len(self.json['plans'])) + '条方案')
            print('当前搜索log为：' + str(self.json['gen_plan_search_log_id']))
            print('当前搜索条件为：' + str(self.case))
            raise Exception('\033[1;31;47m报错了，手动检查下呀！\033[0m')

    def gen_plan_search_log_id(self):
        if self.state == 200:
            return self.json['gen_plan_search_log_id']
        else:
            print('当前接口返回值：' + str(self.state) + '，没有生成log')




class get_schedules():

    def __init__(self, unified_plans_id):
        self.id = unified_plans_id
        self.url = unified_plans_url + str(unified_plans_id) + '/schedules'
        self.audits_url = audits_url + str(unified_plans_id)
        self.basic_url = basic_url + str(unified_plans_id) + '/basic?utm_campaign=2414'

    def places_ids(self):

        get(url = self.basic_url, headers = login().headers())
        sleep(1)
        schedules = get(url = self.url, headers = login().headers()).json()
        schedules = schedules['schedules']
        places_ids = []

        for i in range(0, len(schedules)):
            for n in range(0, len(schedules[i]['places'])):
                places_ids.append(schedules[i]['places'][n]['regionId'])

        places_ids = list(set(places_ids))
        return places_ids

    def pois_ids(self):

        get(url=self.basic_url, headers=login().headers())
        sleep(1)
        schedules = get(url=self.url, headers=login().headers()).json()
        schedules = schedules['schedules']
        pois_ids = []

        for i in range(0, len(schedules)):
            for n in range(0, len(schedules[i]['places'])):
                for m in range(0, len(schedules[i]['places'][n])):
                    for p in range(0, len(schedules[i]['places'][n]['pois'])):
                        pois_ids.append(schedules[i]['places'][n]['pois'][p]['id'])

        pois_ids = list(set(pois_ids))
        return pois_ids



class check_result():

    def __init__(self, testcase, result):
        self.case = testcase
        self.result = result

    # 检查出行天数
    def check_days(self):

        y = True

        for i in range(0, len(self.result)):
            if normal().is_modify(result=self.result[i]):
                x = (self.result[i]['days'] in range(self.case['days'][0], self.case['days'][1] + 1))
                if x == True:
                    y = x and y
                elif x == False:
                    print('不符合条件的方案是：' + str(self.result[i]['unified_plan_id']) + '，此方案的出行时间为：' + str(self.result[i]['days']))
                    y = x and y
                else:
                    print("检查失效，请手动确认结果！")
                    y = x and y
        # return y
        if y:
            print('搜索结果的出行天数与测试用例相同！')
        else:
            raise Exception('\033[1;31;47m搜索结果的出行天数与测试用例不符！\033[0m')

    # 检查入境城市
    def check_start_places(self):

        if len(self.case['start_place_ids']) == 0:
            print('测试用例中不包含入境城市！')
            return True

        else:
            y = True

            for i in range(0, len(self.result)):

                start_place_names = []

                for n in range(0, len(self.case['start_place_ids'])):
                    for m in range(0, len(self.case['country_ids'])):
                        start_place_names.append(PATH_ID['[' + str(self.case['country_ids'][m]) + ']']['[' + str(self.case['start_place_ids'][n]) + ']'])

                start_place = normal().get_start_place_name(plans=self.result[i])

                result = (start_place in start_place_names)
                y = result and y

                if result:
                    continue
                else:
                    print('搜索结果的入境城市与测试用例不符！')
                    print('不符合条件的方案是：' + str(self.result['plans'][i]['unified_plan_id']) + ',当前搜索结果的入境城市为：' + start_place + '，当前测试用例的入境城市为：' + str(start_place_names))
            if y:
                print('搜索结果的入境城市与测试用例相同！')
            else:
                raise Exception('\033[1;31;47m搜索结果的入境城市与测试用例不符！\033[0m')

    # 检查出境城市
    def check_finish_places(self):

        if len(self.case['finish_place_ids']) == 0:
            print('测试用例中不包含出境城市！')
            return True

        else:
            y = True

            for i in range(0, len(self.result)):

                finish_place_names = []

                for n in range(0, len(self.case['finish_place_ids'])):
                    for m in range(0, len(self.case['country_ids'])):
                        finish_place_names.append(PATH_ID['[' + str(self.case['country_ids'][m]) + ']']['[' + str(self.case['finish_place_ids'][n]) + ']'])

                finish_place = normal().get_finish_place_name(plans=self.result[i])

                result = (finish_place in finish_place_names)
                y = result and y

                if result:
                    continue
                else:
                    print('搜索结果的出境城市与测试用例不符！')
                    print('不符合条件的方案是：' + str(self.result['plans'][i]['unified_plan_id']) + ',当前搜索结果的出境城市为：' + finish_place + '，当前测试用例的出境城市为：' + str(finish_place_names))
            if y:
                print('搜索结果的出境城市与测试用例相同！')
            else:
                raise Exception('\033[1;31;47m搜索结果的出境城市与测试用例不符！\033[0m')


    # 未完成，因为region和place关系未搞定，暂时没有更好的解决方案
    # 检查旅行城市，覆盖了"只去该城市"和"按顺序搜索"这两个条件
    def check_include_places(self):

        # 只去+按顺序
        if (self.case['is_region_only'] and self.case['is_in_order']):
            print('1')
            result = True
            order = []
            for i in range(0,len(self.case['order'])):
                order.append(self.case['order'][i]['id'])

            unified_plans_ids = normal().get_unified_plan_ids(plans= self.result)

            for n in range(0, len(unified_plans_ids)):
                places_ids = get_schedules(unified_plans_id= unified_plans_ids[n]).places_ids()
                if order == places_ids:
                    result = True

                else:
                    print('搜索结果的旅行城市或者城市顺序与测试用例不符！')
                    print('不符合条件的方案是：' + str(unified_plans_ids[n]) + ',当前搜索结果的只去的城市和城市的顺序为：' + str(places_ids))
                    result = False

            if result:
                print('搜索结果的旅行城市的顺序和测试用例相同，并且没有包含其他城市！')
            else:
                raise Exception('\033[1;31;47m搜索结果的旅行城市或者城市顺序与测试用例不符！\033[0m')

        # 只去+不按顺序
        elif self.case['is_region_only']:
            print('2')
            result = True
            order = []
            for i in range(0,len(self.case['order'])):
                order.append(self.case['order'][i]['id'])
            unified_plans_ids = normal().get_unified_plan_ids(plans= self.result)
            for n in range(0, len(unified_plans_ids)):
                places_ids = get_schedules(unified_plans_id= unified_plans_ids[n]).places_ids()
                if set(order) >= set(places_ids):
                    result = True

                else:
                    print('搜索结果的旅行城市或者城市顺序与测试用例不符！')
                    print('不符合条件的方案是：' + str(unified_plans_ids[n]) + ',当前搜索结果的只去的城市和城市的顺序为：' + str(places_ids))
                    result = False
            print('result is ' + str(result))
            if result:
                print('搜索结果的旅行城市的顺序和测试用例相同，并且没有包含其他城市！')
            else:
                raise Exception('\033[1;31;47m搜索结果的旅行城市或者城市顺序与测试用例不符！\033[0m')

        # 按顺序+非只去
        elif self.case['is_in_order']:
            print('3')
            result = True
            order = []
            for i in range(0,len(self.case['order'])):
                order.append(self.case['order'][i]['id'])

            unified_plans_ids = normal().get_unified_plan_ids(plans= self.result)

            for n in range(0, len(unified_plans_ids)):
                places_ids = get_schedules(unified_plans_id= unified_plans_ids[n]).places_ids()
                all_include = set(order).intersection(set(places_ids))

                if list(set(order) - all_include) == places_ids:
                    result = True

                else:
                    print('搜索结果的旅行城市或者城市顺序与测试用例不符！')
                    print('不符合条件的方案是：' + str(unified_plans_ids[n]) + ',当前搜索结果的只去的城市和城市的顺序为：' + str(places_ids))
                    result = False

            if result:
                print('搜索结果的旅行城市的顺序和测试用例相同，并且没有包含其他城市！')
            else:
                raise Exception('\033[1;31;47m搜索结果的旅行城市或者城市顺序与测试用例不符！\033[0m')

        # 非只去+不按顺序
        else:
            print('4')
            result = True
            order = []
            for i in range(0,len(self.case['order'])):
                order.append(self.case['order'][i]['id'])

            unified_plans_ids = normal().get_unified_plan_ids(plans= self.result)

            for n in range(0, len(unified_plans_ids)):
                places_ids = get_schedules(unified_plans_id= unified_plans_ids[n]).places_ids()
                if list(set(order).intersection(set(places_ids))):
                    result = True

                else:
                    print('搜索结果的旅行城市或者城市顺序与测试用例不符！')
                    print('不符合条件的方案是：' + str(unified_plans_ids[n]) + ',当前搜索结果的只去的城市和城市的顺序为：' + str(places_ids))
                    result = False

            if result:
                print('搜索结果的旅行城市的顺序和测试用例相同，并且没有包含其他城市！')
            else:
                raise Exception('\033[1;31;47m搜索结果的旅行城市或者城市顺序与测试用例不符！\033[0m')

    # 检查不去的旅行城市
    def check_disable_places(self):
        return 1

    # 检查想要去的POI
    def check_include_pois(self):

        if (self.case['poi_ids'] != []):
            poi_ids = self.case['poi_ids']
            result = True
            unified_plans_ids = normal().get_unified_plan_ids(plans=self.result)
            for i in range(0, len(unified_plans_ids)):
                pois_ids = get_schedules(unified_plans_id= unified_plans_ids[i]).pois_ids()
                if set(pois_ids) >= set(poi_ids):
                    result = True

                else:
                    print('搜索结果包含的POI与测试用例不符！')
                    print('不符合条件的方案是：' + str(unified_plans_ids[i]) + ',当前搜索结果的POI_ID为：' + str(pois_ids))
                    result = False

            if result:
                print('搜索结果包含的POI和测试用例相同！')
            else:
                raise Exception('\033[1;31;47m搜索结果的POI与测试用例不符！\033[0m')

        else:
            print('测试用例中不包含想去的POI！')
            return True

    # 检查不想去的POI
    def check_disable_pois(self):

        if (self.case['disable_poi_ids'] != []):
            poi_ids = self.case['disable_poi_ids']
            result = True
            unified_plans_ids = normal().get_unified_plan_ids(plans=self.result)
            for i in range(0, len(unified_plans_ids)):
                pois_ids = get_schedules(unified_plans_id= unified_plans_ids[i]).pois_ids()
                all_include = set(poi_ids).intersection(set(pois_ids))
                if all_include == []:
                    result = True

                else:
                    print('搜索结果不去的POI与测试用例不符！')
                    print('不符合条件的方案是：' + str(unified_plans_ids[i]) + ',当前搜索结果的POI_ID为：' + str(pois_ids))
                    result = False

            if result:
                print('搜索结果不去的POI和测试用例相同！')
            else:
                raise Exception('\033[1;31;47m搜索结果的POI与测试用例不符！\033[0m')

        else:
            print('测试用例中不包含不去的POI！')
            return True

    # 检查是否自驾
    def check_self_drive(self):
        # unified_plan_ids = normal().get_unified_plan_ids(plans= self.result['plans'])
        unified_plan_ids = normal().get_unified_plan_ids(plans= self.result)

        if ('self_drive' in self.case.keys()):

            if self.case['self_drive'] == True:

                if normal().get_unified_plans_pois_is_car_rental(unified_plan_ids= unified_plan_ids,testcase= self.case):
                    print('搜索结果的自驾情况与测试用例相同！')
                else:
                    raise Exception('\033[1;31;47m搜索结果的自驾情况与测试用例不符！\033[0m')

            else:
                if normal().get_unified_plans_pois_is_car_rental(unified_plan_ids= unified_plan_ids,testcase= self.case):
                    raise Exception('\033[1;31;47m搜索结果的自驾情况与测试用例不符！\033[0m')
                else:
                    print('搜索结果的自驾情况与测试用例相同！')

        else:
            print('测试用例中不包含是否自驾！')


class check():

    def __init__(self, testcase, result):
        self.case = testcase
        self.result = result

    def run(self):

        try:
            check_result(testcase=self.case, result=self.result).check_days()
            check_result(testcase=self.case, result=self.result).check_start_places()
            check_result(testcase=self.case, result=self.result).check_finish_places()
            check_result(testcase=self.case, result=self.result).check_self_drive()
            # check_result(testcase=self.case, result=self.result).check_include_places()
            # check_result(testcase=self.case, result=self.result).check_disable_places()
            check_result(testcase=self.case, result=self.result).check_include_pois()
            check_result(testcase=self.case, result=self.result).check_disable_pois()


        except Exception as e:
            print(e)






# class send_result():
#
#     def __init__(self, email, password, recipient):
#         self.eamil = email
#         self.password = password
#         self.recipient = recipient
#
#     def send_eamil(self):
#         msg = MIMEMultipart()
#         msg['from'] = self.eamil
#         msg['to'] = self.recipient
#         msg['subject'] = u'测试报告'
#
#         txt = MIMEText(u"自动化测试报告-HTML", "plain", "utf-8")
#         msg.attach(txt)
#
#         # 构造附件
#         att = MIMEText(open(u"", "rb").read(), "base64", "utf-8")
#         att["Content-Type"] = "application/octet-stream"
#         att["Content-Disposition"] = "attachment; filename=TestResult.html"
#         msg.attach(att)
#
#         try:
#             smtpObj = SMTP()
#             # smtpObj.connect("","")
#             smtpObj.connect("", "")
#             state = smtpObj.login(self.eamil, self.password)
#             if state[0] == 235:
#                 smtpObj.sendmail(msg["from"], msg["to"], msg.as_string())
#                 print(u"邮件发送成功")
#             smtpObj.quit()
#         except SMTPException as e:
#             print(str(e))

# run testcase, creat report and send email to myself
import unittest
from requests import post
from testcase import *
from config import headers
# from config import creat_report, send_eamil
from config import check_days, check_immigrations
from data import search_url

class run_test(unittest.TestCase):

    # def setUp(self):


    def test1(self):
        # search days is right or wrong
        test1 = post(url=search_url, json=case1, headers=headers)
        test1_days = test1.json()

        # 检查搜索结果中所有方案的出行天数，是否在设置的区间内，若在则返回1，不在则返回0
        if check_days(4,14,test1_days):
            print('出行天数在4-14区间之内，测试通过')
        else:
            print('出行天数在4-14区间之内，测试失败！')

    def test2(self):
        test2 = post(url=search_url, json=case2, headers=headers)
        test2_days = test2.json()

        if check_days(1,15,test2_days):
            print('出行天数在1-15区间之内，测试通过')
        else:
            print('出行天数在1-15区间之内，测试失败！')

    def test3(self):
        test3 = post(url=search_url, json=case3, headers=headers)
        test3_days = test3.json()

        if check_days(3,30,test3_days):
            print('出行天数在3-30区间之内，测试通过')
        else:
            print('出行天数在3-30区间之内，测试失败！')

    def test4(self):
        test4 = post(url=search_url,json=case4, headers=headers)
        test4_days = test4.json()

        if check_days(4,4,test4_days):
            print('出行天数4天，测试通过')
        else:
            print('出行天数4天，测试失败！')

    def test5(self):
        test5 = post(url=search_url, json=case5, headers=headers)
        json = test5.json()

        if check_immigrations(start_place='大阪', finish_place='大阪', json=json):
            print('出入境城市相符，测试通过')
        else:
            print('出入境城市不符，测试失败！')

    def test6(self):
        test6 = post(url=search_url, json=case6, headers=headers)
        json = test6.json()

        if check_immigrations(start_place='东京', finish_place='大阪', json=json):
            print('出入境城市相符，测试通过')
        else:
            print('出入境城市不符，测试失败！')

    # def test7(self):
    #     post(url=search_url,json=, headers=headers)
    #
    # def test8(self):
    #     post(url=search_url,json=, headers=headers)
    #
    # def test9(self):
    #     post(url=search_url,json=, headers=headers)
    #
    # def test10(self):
    #     post(url=search_url,json=, headers=headers)
    #
    # def test11(self):
    #     post(url=search_url,json=, headers=headers)
    #
    # def test12(self):
    #     post(url=search_url,json=, headers=headers)
    #
    # def test13(self):
    #     post(url=search_url,json=, headers=headers)

    # def tearDown(self):

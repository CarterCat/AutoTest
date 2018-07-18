import unittest
from requests import post
from data import headers, search_checker_url, search_checker
from testcase import *

class run_test(unittest.TestCase):

    # def setUp(self):
    #

    def test1(self):
        test1 = post(url=search_checker_url, json=case1, headers=headers).json()
        search_checker(case1, test1)

    def test2(self):
        test2 = post(url=search_checker_url, json=case2, headers=headers).json()
        search_checker(case2, test2)

    def test3(self):
        test3 = post(url=search_checker_url, json=case3, headers=headers).json()
        search_checker(case3, test3)

    def test4(self):
        test4 = post(url=search_checker_url, json=case4, headers=headers).json()
        search_checker(case4, test4)

    def test5(self):
        test5 = post(url=search_checker_url, json=case5, headers=headers).json()
        search_checker(case5, test5)

    def test6(self):
        test6 = post(url=search_checker_url, json=case6, headers=headers).json()
        search_checker(case6, test6)

    def test7(self):
        test7 = post(url=search_checker_url, json=case7, headers=headers).json()
        search_checker(case7, test7)

    # def tearDown(self):
    #

if __name__ == "__main__":
    print("=====AutoTest Start======")

    suite = unittest.makeSuite(run_test)
    runner = unittest.TextTestRunner()
    runner.run(suite)

    print("=====AutoTest Over======")
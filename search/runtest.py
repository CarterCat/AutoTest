from unittest import TestCase, TextTestRunner, makeSuite
from search.data import case1, search_url
from search.controller import check_result, check, generate_testcase, get_result
from time import sleep

from search.controller import login
from requests import post

class run_test(TestCase):

    # def setUp(self):

    def test1(self):

        # case1 = generate_testcase()
        result = get_result(testcase= case1).plans()
        check(testcase=case1, result=result).run()

    # def test2(self):
    #     case2 = generate_testcase()
    #     result = get_result(testcase= case2).plans()
    #     check(testcase=case2, result=result).run()

    # def tearDown(self):






if __name__ == "__main__":
    print("=====AutoTest Start======")
    times = input('请输入要执行的次数：')
    for i in range(0, int(times)):
        print('第' + str(i + 1) + '次测试开始：')
        suite = makeSuite(run_test)
        # unittest.main()
        # creat_report(suite)
        # send from, password, send to
        # send_eamil('', '', '')
        runner = TextTestRunner()
        # times = input('请输入要执行的次数：')
        # for i in range(0, int(times)):
        runner.run(suite)
        sleep(3)

    print("=====AutoTest Over======")

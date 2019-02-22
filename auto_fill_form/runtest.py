from unittest import TestCase, makeSuite, TextTestRunner, TestSuite
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from auto_fill_form.controller import check_played,check_result
from auto_fill_form.pageobject import *
from random import randint

environment = input('请输入要测试的环境（线上/测试）：')
type = input('请输入需要测试的类型（电脑端/移动端）：')
start_num = int(input('请输入需要测试的手机号：'))

global envir

if environment == '线上':
    envir = ''
elif environment == '测试':
    envir = ''
else:
    print('输入的环境不对，请重新输入！')

class run_test(TestCase):

    def setUp(self):
        if type == '电脑端':
            self.driver = webdriver.Chrome()
        elif type == '移动端':
            mobileEmulation = {'deviceName': 'iPhone 6/7/8 Plus'}
            options = webdriver.ChromeOptions()
            options.add_experimental_option('mobileEmulation', mobileEmulation)
            self.driver = webdriver.Chrome(chrome_options = options)
        else:
            print('输入的类型不对，请重新输入！')
        self.num = int(start_num)

    # 测试右上角填单按钮
    def test1(self):
        n = randint(0, 17)
        num = self.num
        driver = self.driver
        driver.get(envir + web_url_up[n])
        print('当前测试的地址为：' + envir + web_url_up[n])
        sleep(20)
        book_modal_content = driver.find_element_by_class_name('book_modal_content')
        close = driver.find_element_by_class_name('close')
        if check_played(book_modal_content):
            close.click()
            sleep(1)
            button = driver.find_element_by_class_name('close')
            button.click()
            sleep(1)
            alertDestination = driver.find_element_by_id('alertDestination')
            alertDestination.send_keys('测试目的地')
            sleep(1)
            phone = driver.find_element_by_id('alertPhone')
            phone.send_keys(str(num))
            sleep(1)
            receive = driver.find_element_by_class_name('receive')
            receive.click()
            sleep(1)
            result = driver.find_element_by_id('book_success_close_btn')
            check_result(str(num),result)

        else:
            print('自动填单窗口20s未弹出！')
            sleep(1)
            button = driver.find_element_by_class_name('book-now-btn')
            button.click()
            sleep(1)
            alertDestination = driver.find_element_by_id('alertDestination')
            alertDestination.send_keys('测试目的地')
            sleep(1)
            phone = driver.find_element_by_id('alertPhone')
            phone.send_keys(str(num))
            sleep(1)
            result = driver.find_element_by_id('book_success_close_btn')
            receive = driver.find_element_by_class_name('receive')
            receive.click()
            check_result(str(num), result)

    # 测试最下方填单界面
    def test2(self):
        num = self.num + 1
        m = randint(0, 14)
        driver = self.driver
        driver.get(envir + web_url_down[m])
        print('当前测试的地址为：' + envir + web_url_up[n])
        sleep(20)
        book_modal_content = driver.find_element_by_class_name('book_modal_content')
        close = driver.find_element_by_class_name('close')
        if check_played(book_modal_content):
            close.click()
            sleep(1)

            name = driver.find_element_by_id('name')
            name.send_keys('测试姓名')
            sleep(1)

            old_destination = driver.find_element_by_id('old_destination')
            old_destination.send_keys('测试目的地')

            sleep(1)
            travel_days = driver.find_element_by_id('travel_days')
            travel_days.send_keys('15')

            sleep(1)
            phone = driver.find_element_by_id('phone')
            phone.send_keys(str(num))

            sleep(1)
            comment = driver.find_element_by_id('comment')
            comment.send_keys('测试备注内容')

            sleep(1)
            submit = driver.find_element_by_css_selector('#bottomPlanForm > div.row.submit > button')
            submit.click()

            sleep(1)
            result = driver.find_element_by_id('book_success_close_btn')
            check_result(num,result)

        else:
            print('自动填单窗口20s未弹出！')

    # 测试自动弹窗填单
    # def test3(self):
    #     num = self.num + 2
    #     i = randint(0, 16)
    #     driver = self.driver
    #     driver.get(envir + web_url_auto[i])
    #     print('当前测试的地址为：' + envir + web_url_up[n])
    #     sleep(20)
    #     book_modal_content = driver.find_element_by_class_name('book_modal_content')
    #     if check_played(book_modal_content):
    #         alertDestination = driver.find_element_by_id('alertDestination')
    #         alertDestination.send_keys('测试目的地')
    #         sleep(1)
    #         phone = driver.find_element_by_id('alertPhone')
    #         phone.send_keys(str(num))
    #         sleep(1)
    #         result = driver.find_element_by_id('book_success_close_btn')
    #         check_result(str(num),result)
    #     else:
    #         print('自动填单窗口20s未弹出！')

    # def test4(self):
    #     num3 = self.num + 3
    #     print(4)
    #
    # def test5(self):
    #     num3 = self.num + 4
    #     print(4)
    #
    # def test6(self):
    #     num3 = self.num + 5
    #     print(4)
    #
    # def test7(self):
    #     num3 = self.num + 6
    #     print(4)
    #
    # def test8(self):
    #     num3 = self.num + 7
    #     print(4)
    #
    # def test9(self):
    #     num3 = self.num + 8
    #     print(4)
    #
    # def test10(self):
    #     num3 = self.num + 9
    #     print(4)
    #
    # def test11(self):
    #     num3 = self.num + 10
    #     print(4)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    print("=====AutoTest Start======")

    suite = TestSuite()

    if type == '电脑端':
        test = [run_test('test1')]
        suite.addTests(test)
        runner = TextTestRunner()
        runner.run(suite)
        n = len(test) - 1
        end_num = str(start_num + n)
        print('此次测试用到的号码段为：' + '\033[1;35m ' + str(start_num) + '\033[0m' + '-' + '\033[1;35m' + end_num + '\033[0m')

    elif type == '移动端':
        test = [run_test('test1')]
        suite.addTests(test)
        runner = TextTestRunner()
        runner.run(suite)
        n = len(test)
        end_num = str(start_num + n)
        print('此次测试用到的号码段为：' + '\033[1;35m ' + str(start_num) + '\033[0m' + '-' + '\033[1;35m' + end_num + '\033[0m')

    else:
        print('输入的类型不对，请重新输入！')

    # suite = makeSuite(run_test)
    sleep(1)
    print("=====AutoTest Over======")
from unittest import SkipTest, TestCase, makeSuite, TextTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class put_info():
    def __init__(self, num):
        self.num = num
    # 检查窗口是否打开
    def output(self, book_modal_win):
        if book_modal_win:
            print('~~~~~~~~~测试用例' + str(self.num) + '~~~~~~~~~')
            print('【自动填单窗口已弹出，进行自动化填单测试！】')
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

driver = webdriver.Chrome()

class run_test(TestCase):
    def test1(self):
        driver.get('')
        sleep(20)
        close = driver.find_element(By.CLASS_NAME, 'close')
        close.click()
        sleep(3)
        book_modal = driver.find_element(By.ID, 'book_modal')
        win = book_modal.is_displayed()
        if win:
            put_info(num=9999).output(book_modal_win=win)
        else:
            put_info(num=9999).output(book_modal_win=win)

    def test2(self):
        print('这是第二个测试')


if __name__ == '__main__':
        print("=====AutoTest Start======")
        suite = makeSuite(run_test)
        runner = TextTestRunner()
        runner.run(suite)
        driver.quit()
        print("=====AutoTest Over======")

class a(TestCase):
    def test1(self,a,b):
        self.a = a
        self.b = b
        self.assertEqual(self.a, self.b, msg='')

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep
import unittest
from controller import check_unicrm, cancel_ticket, check_played

# global tel1

# 设置Chrome启动，headless模式
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()

# 首页官网
url = ''
driver.get(url)

# 打开网页，第一次弹窗提示填单
sleep(20)

# 检查是否提交成功，并对udesk工单进行处理
def check_result(tel, result):
    if result.is_displayed() :
        if result.text == '提交成功！':
            sleep(2)
            ticket_id = check_unicrm(email='', password='', tel=tel)
            cancel_result = cancel_ticket('', '', ticket_id)
            if cancel_result:
                print('***测试工单和交易，已取消。工单ID：' + ticket_id + '***')
                return 1
            else:
                print('****测试工单和交易，取消失败。工单ID：' + ticket_id + '***')
                return 1
        else:
            print(result.text)
            return 0
    else:
        print(result.text)
        return 0

# 运行测试脚本
class run_test(unittest.TestCase):

# 用于测试自动弹窗，进行填单
    def test1(self):

        sleep(10)

        book_modal = driver.find_element(By.ID, 'book_modal')
        if book_modal.is_displayed():
            print('~~~~~~~~~测试用例1~~~~~~~~~')
            print('【自动填单窗口已弹出，进行自动化填单测试！】')
            print('请输入测试用例1的手机号：（注意不能重复）')
            tel1 = input('tel1 = ')
            print('请输入测试用例1的微信号：（注意不能重复）')
            wechat1 = input('wechat1 = ')
            # 获取所需要的元素
            # 第一部分，目的地、人数、出发城市和出行日期
            dest = driver.find_element(By.ID, 'dest')
            # person = driver.find_element(By.ID, 'person')
            city = driver.find_element(By.ID, 'city')
            # mydate = driver.find_element(By.ID, 'mydate')
            # 下一步按钮
            # consult_next = driver.find_element(By.CLASS_NAME, 'consult next')
            consult_next = driver.find_element(By.CSS_SELECTOR, 'p.consult.next')
            # 第二部分，其他需求、姓名、手机号、微信号
            comment = driver.find_elements(By.ID, 'comment')[1]
            name = driver.find_elements(By.ID, 'name')[1]
            phone = driver.find_elements(By.ID, 'phone')[1]
            weixin = driver.find_element(By.ID, 'weixin')
            # 免费咨询按钮
            submit = driver.find_elements(By.ID, 'submit')[1]

            sleep(10)

            # 提交测试数据
            dest.send_keys('日本')
            sleep(1)
            # person.send_keys('3')
            city.send_keys('北京')
            sleep(1)
            # mydate.send_keys('')
            consult_next.click()
            sleep(3)
            comment.send_keys('测试方案，用完即删')
            sleep(1)
            name.send_keys('测试')
            sleep(1)
            phone.send_keys(tel1)
            sleep(1)
            weixin.send_keys(wechat1)
            sleep(1)
            submit.click()
            sleep(2)

            # 获取提交结果，并取消工单
            result = driver.find_element(By.CLASS_NAME, 'submit_title')

            check_played(result)
            check_result(tel=tel1, result=result)
        else:
            print('~~~~~~~~~测试用例1~~~~~~~~~')
            print('【自动填单窗口，未弹出！' + '\n窗口：' + str(book_modal.is_displayed()) + '】')

# 用于测试页面最底端填单，进行填单
    def test2(self):

        driver.refresh()
        # 关闭自动弹出的窗口
        sleep(20)
        book_modal = driver.find_element(By.ID, 'book_modal')
        if book_modal.is_displayed():
            sleep(1)
            close = driver.find_element(By.CLASS_NAME, 'close')
            close.click()
            sleep(1)

            print('~~~~~~~~~测试用例2~~~~~~~~~')
            print('【关闭自动填单窗口，填写页面最下方信息，进行自动化填单测试！】')
            print('请输入测试用例2的手机号：（注意不能重复）')
            tel2 = input('tel2 = ')
            # print('请输入测试用例2的微信号：（注意不能重复）')
            # wechat2 = input('wechat2 = ')
            # 获取页面数据
            old_name = driver.find_elements(By.ID, 'name')[0]
            old_destination = driver.find_element(By.ID, 'old_destination')
            old_days = driver.find_element(By.ID, 'travel_days')
            old_comment = driver.find_elements(By.ID, 'comment')[0]
            old_phone = driver.find_elements(By.ID, 'phone')[0]
            old_submit = driver.find_elements(By.ID, 'submit')[0]

            sleep(10)

            # 提交测试数据
            old_name.send_keys('测试')
            sleep(1)
            old_destination.send_keys('日本')
            sleep(1)
            old_days.send_keys('5')
            sleep(1)
            old_phone.send_keys(tel2)
            sleep(1)
            old_comment.send_keys('测试方案，用完即删')
            sleep(1)

            # 提交表单
            old_submit.click()
            sleep(2)

            # 获取提交结果，并取消工单
            old_result = driver.find_element(By.CLASS_NAME, 'submit_title')

            check_played(old_result)
            check_result(tel=tel2, result=old_result)

        else:
            print('~~~~~~~~~测试用例2~~~~~~~~~')
            print('【自动填单窗口，刷新界面后未弹出！' + '\n窗口：' + str(book_modal.is_displayed()) + '】')

# 用于测试主动点击"免费咨询"按钮，进行填单
    def test3(self):

        driver.refresh()
        # 关闭自动弹出的窗口
        sleep(20)
        book_modal = driver.find_element(By.ID, 'book_modal')
        if book_modal.is_displayed():
            close = driver.find_element(By.CLASS_NAME, 'close')
            close.click()
        else:
            print('~~~~~~~~~测试用例3~~~~~~~~~')
            print('【自动填单窗口，刷新界面后未弹出！' + '\n窗口：' + str(book_modal.is_displayed()) + '】')

        # 获取页面数据

        sleep(5)

        button = driver.find_element(By.CSS_SELECTOR, 'a.book-now-btn.show_book_modal.ga_event')
        button.click()
        sleep(2)

        # 判断窗口是否打开
        book_modal = driver.find_element(By.ID, 'book_modal')
        if book_modal.is_displayed():
            print('~~~~~~~~~测试用例3~~~~~~~~~')
            print('【弹窗窗口已弹出，进行自动化填单测试！】')
            print('请输入测试用例3的手机号：（注意不能重复）')
            tel3 = input('tel3 = ')
            print('请输入测试用例3的微信号：（注意不能重复）')
            wechat3 = input('wechat3 = ')

            # 获取页面数据
            # 第一部分，目的地、人数、出发城市和出行日期
            new_dest = driver.find_element(By.ID, 'dest')
            # person = driver.find_element(By.ID, 'person')
            new_city = driver.find_element(By.ID, 'city')
            # mydate = driver.find_element(By.ID, 'mydate')
            # 下一步按钮
            # consult_next = driver.find_element(By.CLASS_NAME, 'consult next')
            new_consult_next = driver.find_element(By.CSS_SELECTOR, 'p.consult.next')
            # 第二部分，其他需求、姓名、手机号、微信号
            new_comment = driver.find_elements(By.ID, 'comment')[1]
            new_name = driver.find_elements(By.ID, 'name')[1]
            new_phone = driver.find_elements(By.ID, 'phone')[1]
            new_weixin = driver.find_element(By.ID, 'weixin')
            # 免费咨询按钮
            new_submit = driver.find_elements(By.ID, 'submit')[1]

            sleep(10)

            # 提交测试数据
            new_dest.send_keys('日本')
            sleep(1)
            # person.send_keys('3')
            # sleep(1)
            new_city.send_keys('北京')
            sleep(1)
            # mydate.send_keys('')
            new_consult_next.click()
            sleep(3)
            new_comment.send_keys('测试方案，用完即删')
            sleep(1)
            new_name.send_keys('测试')
            sleep(1)
            new_phone.send_keys(tel3)
            sleep(1)
            new_weixin.send_keys(wechat3)
            sleep(1)
            new_submit.click()
            sleep(2)

            # 获取提交结果，并取消工单
            new_result = driver.find_element(By.CLASS_NAME, 'submit_title')

            check_played(new_result)
            check_result(tel=tel3, result=new_result)

        else:
            print('~~~~~~~~~测试用例3~~~~~~~~~')
            print('【填单窗口未弹出！' + '\n窗口：' + str(book_modal.is_displayed()) + '】')

if __name__ == '__main__':
        print("=====AutoTest Start======")
        suite = unittest.makeSuite(run_test)
        # unittest.main()
        # creat_report(suite)
        # send from, password, send to
        # send_eamil('', '', '')
        runner = unittest.TextTestRunner()
        runner.run(suite)
        driver.quit()
        print("=====AutoTest Over======")

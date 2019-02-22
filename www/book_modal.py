from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep
import unittest
from controller import check_unicrm, cancel_ticket, check_played, close_bookmodal_window, put_info

# global tel1

# 设置Chrome启动，headless模式
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()

# 首页官网
# url = ''
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
        # 等待时间
        sleep(10)
        # 检查是否打开弹窗窗口
        book_modal = driver.find_element(By.ID, 'book_modal')
        win = book_modal.is_displayed()
        # 自动弹窗后，进行测试
        if win:
            put_info(num=1).output(book_modal_win=win)
            tel1 = put_info(num=1).data(type='tel')
            wechat1 = put_info(num=1).data(type='wechat')
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
            # 检查填单成功窗口是否显示
            check_played(result=result)
            # 尝试取消工单
            check_result(tel=tel1, result=result)
        else:
            put_info(num=1).output(book_modal_win=win)
            self.skipTest(reason='【自动填单窗口，未弹出！】')

# 用于测试页面最底端填单，进行填单
    def test2(self):

        driver.refresh()
        # 关闭自动弹出的窗口
        sleep(20)
        book_modal = driver.find_element(By.ID, 'book_modal')
        win = book_modal.is_displayed()
        if win:
            put_info(num=2).output(book_modal_win=win)
            sleep(1)
            close = driver.find_element(By.CLASS_NAME, 'close')
            close_bookmodal_window(book_modal=book_modal, close=close)
            sleep(1)

            tel2 = put_info(num=2).data(type='tel')
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

            check_played(result=old_result)
            check_result(tel=tel2, result=old_result)

        else:
            put_info(num=2).output(book_modal_win=win)
            self.skipTest('【自动填单窗口，未弹出！】')

# 用于测试主动点击"免费咨询"按钮，进行填单
    def test3(self):

        driver.refresh()
        # 关闭自动弹出的窗口
        sleep(20)
        book_modal = driver.find_element(By.ID, 'book_modal')
        close = driver.find_element(By.CLASS_NAME, 'close')
        close_bookmodal_window(book_modal=book_modal, close=close)

        # 获取页面数据

        sleep(5)

        button = driver.find_element(By.CSS_SELECTOR, 'a.book-now-btn.show_book_modal.ga_event')
        button.click()
        sleep(2)

        # 判断窗口是否打开
        book_modal = driver.find_element(By.ID, 'book_modal')
        win = book_modal.is_displayed()
        if win:
            put_info(num=3).output(book_modal_win=win)
            tel3 = put_info(num=3).data(type='tel')
            wechat3 = put_info(num=3).data(type='wechat')

            # 获取页面数据
            # 第一部分，目的地、人数、出发城市和出行日期
            new_dest = driver.find_element(By.ID, 'dest')
            # person = driver.find_element(By.ID, 'person')
            new_city = driver.find_element(By.ID, 'city')
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

            check_played(result=new_result)
            check_result(tel=tel3, result=new_result)

        else:
            put_info(num=3).output(book_modal_win=win)
            self.skipTest('【自动填单窗口，未弹出！】')

# 用于测试进入攻略界面，点击"免费咨询"按钮进行填单
    def test4(self):

        # driver.refresh()
        driver.get('')
        # driver.get('')

        # 关闭自动弹出的窗口
        sleep(20)
        book_modal = driver.find_element(By.ID, 'book_modal')
        close = driver.find_element(By.CLASS_NAME, 'close')
        close_bookmodal_window(book_modal=book_modal, close=close)

        # 点击界面上的"免费咨询"
        button4 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/div/div[2]/a')
        button4.click()
        sleep(1)

        # 判断窗口是否打开
        book_modal = driver.find_element(By.ID, 'book_modal')
        win = book_modal.is_displayed()
        if win:
            put_info(num=4).output(book_modal_win=win)
            tel4 = put_info(num=4).data(type='tel')
            wechat4 = put_info(num=4).data(type='wechat')

            # 获取页面数据
            # 第一部分，目的地、人数、出发城市和出行日期
            dest4 = driver.find_element(By.ID, 'dest')
            # person = driver.find_element(By.ID, 'person')
            city4 = driver.find_element(By.ID, 'city')
            # 下一步按钮
            consult_next4 = driver.find_element(By.CSS_SELECTOR, 'p.consult.next')
            # 第二部分，其他需求、姓名、手机号、微信号
            comment4 = driver.find_elements(By.ID, 'comment')[1]
            name4 = driver.find_elements(By.ID, 'name')[1]
            phone4 = driver.find_elements(By.ID, 'phone')[1]
            weixin4 = driver.find_element(By.ID, 'weixin')
            # 免费咨询按钮
            submit4 = driver.find_elements(By.ID, 'submit')[1]

            sleep(10)

            # 提交测试数据
            dest4.send_keys('日本')
            sleep(1)
            # person.send_keys('3')
            # sleep(1)
            city4.send_keys('北京')
            sleep(1)
            # mydate.send_keys('')
            consult_next4.click()
            sleep(3)
            comment4.send_keys('测试方案，用完即删')
            sleep(1)
            name4.send_keys('测试')
            sleep(1)
            phone4.send_keys(tel4)
            sleep(1)
            weixin4.send_keys(wechat4)
            sleep(1)
            submit4.click()
            sleep(2)

            # 获取提交结果，并取消工单
            result4 = driver.find_element(By.CLASS_NAME, 'submit_title')

            check_played(result4)
            check_result(tel=tel4, result=result4)

        else:
            put_info(num=4).output(book_modal_win=win)
            self.skipTest('【自动填单窗口，未弹出！】')

# 用来测试进入攻略界面，点击"免费咨询"按钮进行填单，继承于test4
    def test5(self):
        driver.refresh()
        # 关闭自动弹出的窗口
        sleep(20)
        book_modal = driver.find_element(By.ID, 'book_modal')
        close = driver.find_element(By.CLASS_NAME, 'close')
        close_bookmodal_window(book_modal=book_modal, close=close)

        # 点击界面上的"免费咨询"
        button5 = driver.find_element(By.CSS_SELECTOR, 'span.book_now.show_book_modal.ga_event')
        button5.click()
        sleep(1)

        # 判断窗口是否打开
        book_modal = driver.find_element(By.ID, 'book_modal')
        win = book_modal.is_displayed()
        if win:
            put_info(num=5).output(book_modal_win=win)
            tel5 = put_info(num=5).data(type='tel')
            wechat5 = put_info(num=5).data(type='wechat')

            # 获取页面数据
            # 第一部分，目的地、人数、出发城市和出行日期
            dest5 = driver.find_element(By.ID, 'dest')
            # person = driver.find_element(By.ID, 'person')
            city5 = driver.find_element(By.ID, 'city')
            # 下一步按钮
            consult_next5 = driver.find_element(By.CSS_SELECTOR, 'p.consult.next')
            # 第二部分，其他需求、姓名、手机号、微信号
            comment5 = driver.find_elements(By.ID, 'comment')[1]
            name5 = driver.find_elements(By.ID, 'name')[1]
            phone5 = driver.find_elements(By.ID, 'phone')[1]
            weixin5 = driver.find_element(By.ID, 'weixin')
            # 免费咨询按钮
            submit5 = driver.find_elements(By.ID, 'submit')[1]

            sleep(10)

            # 提交测试数据
            dest5.send_keys('日本')
            sleep(1)
            # person.send_keys('3')
            # sleep(1)
            city5.send_keys('北京')
            sleep(1)
            # mydate.send_keys('')
            consult_next5.click()
            sleep(3)
            comment5.send_keys('测试方案，用完即删')
            sleep(1)
            name5.send_keys('测试')
            sleep(1)
            phone5.send_keys(tel5)
            sleep(1)
            weixin5.send_keys(wechat5)
            sleep(1)
            submit5.click()
            sleep(2)

            # 获取提交结果，并取消工单
            result5 = driver.find_element(By.CLASS_NAME, 'submit_title')

            check_played(result=result5)
            check_result(tel=tel5, result=result5)

        else:
            put_info(num=5).output(book_modal_win=win)
            self.skipTest('【自动填单窗口，未弹出！】')


if __name__ == '__main__':
        print("=====AutoTest Start======")
        suite = unittest.makeSuite(run_test)
        runner = unittest.TextTestRunner()
        runner.run(suite)
        driver.quit()
        print("=====AutoTest Over======")

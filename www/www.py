from selenium import webdriver
from unittest import TestCase, makeSuite, TextTestRunner
from time import sleep

# 设置Chrome启动，headless模式
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome()
# 需要测试的地址链接
url = ['', '']

# 检查是否包含特殊字符
def check_text(text):
    return ('<' in text )and('&lt;' in text )and('&gt;' in text )

# 检查所选链接界面内，所有文章标题和摘要，是否包含"<"
def check_articles(num, titles, boxes):
    for i in range(0, len(titles)):
        title = titles[i].text
        box = boxes[i].text
        if (check_text(title) or check_text(box)):
            print('链接：'+ url[num])
            print(title + box+ '显示错误')
        elif i < (len(titles)-1):
            continue
        else:
            print('链接：'+ url[num])
            print('所有文章标题和摘要，显示正常')

# 运行测试，启用headless模式Chrome
def result(num):
    driver.get(url[num])
    sleep(5)
    item_title = driver.find_elements_by_class_name('item_title')
    item_content_box = driver.find_elements_by_class_name('item_content_box')
    # print("=====AutoTest Start======")
    check_articles(num, item_title, item_content_box)
    # print("=====AutoTest Over======")

# 执行测试集
class run_test(TestCase):

    def test1(self):
        result(0)

    def test2(self):
        result(1)

if __name__ == "__main__":
    print("=====AutoTest Start======")
    # creat_report(suite)
    # send from, password, send to
    # send_eamil('', '', '')
    suite = makeSuite(run_test)
    runner = TextTestRunner()
    runner.run(suite)
    driver.quit()
    print("=====AutoTest Over======")

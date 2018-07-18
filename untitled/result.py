# run this py and get the result
import unittest
from test import run_test
# from config import send_eamil, creat_report

if __name__ == "__main__":
    print("=====AutoTest Start======")

    suite = unittest.makeSuite(run_test)
    # unittest.main()
    # creat_report(suite)
    # send from, password, send to
    # send_eamil('', '', '')
    runner = unittest.TextTestRunner()

    runner.run(suite)

    print("=====AutoTest Over======")

from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

driver.find_element_by_name('1').click()
driver.quit()
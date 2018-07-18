import json
from selenium import webdriver
driver = webdriver.Chrome()
driver.switch_to_frame('')
from selenium.webdriver.support.ui import Select
driver.find_element_by_tag_name()
# test travle days
# 目的地：日本，出行天数：4-14天
case1 = json.loads('{}')

# 目的地：日本，出行天数：1-15天
case2 = json.loads('{}')

# 目的地：日本，出行天数：3-30天
case3 = json.loads('{}')

# 目的地：日本，出行天数：4-4天
case4 = json.loads('{}')

# test finish and start places, single
# 目的地：日本，出行天数：4-14天，出境城市：大阪，入境城市：大阪
case5 = json.loads('{}')

# 目的地：日本，出行天数：4-14天，出境城市：东京，入境城市：大阪
case6 = json.loads('{}')
# 目的地：日本，出行天数：4-14天，旅行区域：只去该区域+关东
case7 = json.loads('{}')
#
# case = {}
#
# case8 = {}
#
# case9 = {}
#
# case10 = {}
#
# case11 = {}
#
# case12 = {}
#
# case13 = {}

from appium import webdriver
driver = webdriver.Remote()
driver.find_element_by_ios('')

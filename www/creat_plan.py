# from django.utils.http import urlquote, unquote
from requests import post
from controller import check_unicrm, cancel_ticket
import time, unittest
from urllib.parse import quote

# 测试官网填单的手机号，修改此处后，运行脚本即可
# tel = '18966666665'
tel = input('请输入测试用手机号：')
# unicrm
global null, false
# unicrm_login_url = ''
# null = 'NULL'
# false = 'False'

# udesk
callcenter_url = ''
secrect = ''

# www
creat_plan_url = ''
# creat_plan_url = ''

headers = {'content-type':'application/x-www-form-urlencoded; charset=UTF-8'}

utm_term = 'utm_term=desktop'
utm_medium = 'utm_medium=' + quote('测试')
utm_campaign = 'utm_campaign=' + quote('测试')
utm_source = 'utm_source=' + quote('测试')
name = 'name=' + quote('测试')
phone = 'phone=' + tel
destination = 'destination=' + quote('欧洲')
days = 'days=' + '10'
comment = 'comment=' + quote('测试方案，用完即删')
unicrm = 'unicrm=1'

# 创建方案，
data = utm_term + '&' + utm_medium + '&' + utm_campaign + '&' + utm_source + '&' + name + '&' + phone + '&' + destination + '&' + days + '&' + comment + '&' + unicrm
result = post(url=creat_plan_url, headers=headers, data=data).json()
time.sleep(5)

# 获取已经创建的交易对应的工单号
ticket_id = check_unicrm(email='', password='', tel=tel)

# 判断是否成功创建方案
if result['err'] == 0:
    if ticket_id:
        print('创建成功')
        # 创建成功后，取消对应udesk工单
        time.sleep(5)
        cancel_result = cancel_ticket('', '', ticket_id)
        if cancel_result['ticket']['status'] == '已关闭' :
             print('工单已取消')
        else :
             print('工单取消失败，请手动取消')
    else:
        print('创建失败')
else:
    print(result['msg'])

# if __name__ == "__main__":
#     print("=====AutoTest Start======")
#     suite = unittest.makeSuite(run_test)
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
#     print("=====AutoTest Over======")
from requests import get, put, post
from time import sleep
from urllib.parse import quote
from requests import exceptions
import pdb

# data
unicrm_login_url = ''
create_deal_url = ''

email = ''
password = ''
deal_source = {""}

# 各阶段及状态对应值
{
    'status':
        {
            '已签单': '',
            '已取消': '',
            '处理中': ''
        },
    'stage':
        {
            'current_stage':
            {
                '呼叫跟进': '',
                '销售联系': '',
                '需求沟通': '',
                '方案准备': '',
                '方案讨论': '',
                '价格讨论': ''
            }
        }

}

# 检查接口是否正常使用
def check_status(result):
    if result.status_code == 200:
        return True
    elif result.status_code == 500:
        print('请求超时，请稍后再试。。。')
    else:
        print(result.status_code)
        # print(result.json())
        return False

# 登录unicrm，获取auth
def login_unicrm(email, password):
    login_json = {"email": email, "password": password}
    result = post(url=unicrm_login_url, json=login_json)
    if check_status(result=result):
        return result.json()['authentication_token']

# 构造headers

Dist_email = ""
Dist_password = ""

Dist_id = input('请输入需要绑定的Dist方案ID：')

Authorization = login_unicrm(email=email, password=password)
headers = {'Authorization': Authorization}

# 创建交易，返回交易ID
def create_deal():
    try:
        result = post(url = create_deal_url, json = deal_source, headers = headers)
        if check_status(result=result):
            return result.json()['deal']['id']
    except exceptions.Timeout as e:
        print('请求超时：' + str(e))
    except exceptions.HTTPError as e:
        print('请求错误：' + str(e))

# 通过交易ID，获取交易信息，返回的json
def deal_info(deal_id, type):
    try:
        result = get(url ='' + str(deal_id), headers = headers)

        if check_status(result=result):
            if isinstance(type, str):
                return result.json()['deal'][type]
            else:
                return result.json()['deal'][str(type)]
        else:
            print('获取交易信息失败！ 接口信息：' + str(result.status_code))
    except exceptions.Timeout as e:
        print('请求超时：' + str(e))
    except exceptions.HTTPError as e:
        print('请求错误：' + str(e))

# 检查是否从上个阶段，跳转至下一阶段/状态
def check_jump_states(deal_id, from_stage):
    try:
        status = deal_info(deal_id = deal_id, type = 'status')
        result = deal_info(deal_id = deal_id, type = 'stage')

        from_stage = str(from_stage)
        if (status == 'won') or (status == 'lost'):
            print('当前交易已签单或已取消')

        else:
            # 呼叫跟进，忽略状态跳转
            if from_stage == 'callcenter_followup':
                if 'contact_customer' == result['current_stage']:
                    return True
                else:
                    return False

            # 从销售联系，跳转到需求沟通
            elif from_stage == 'contact_customer':
                if 'discover_needs' == result['current_stage']:
                    return True
                else:
                    return False

            # 从需求沟通，跳转到方案准备
            elif from_stage == 'discover_needs':
                if result['current_stage'] == 'prepare_proposal':
                    return True
                else:
                    return False

            # 从方案准备，跳转到方案讨论
            elif from_stage == 'prepare_proposal':
                if result['current_stage'] == 'discuss_proposal':
                    return True
                else:
                    return False

            # 从方案讨论，跳转到价格讨论
            elif from_stage == 'discuss_proposal':
                if result['current_stage'] == 'discuss_price':
                    return True
                else:
                    return False

            # discuss_price
            # 从价格讨论，跳转到已签单
            # elif from_stage == 'discuss_price':
            #     print('6')
            #     status = deal_info(deal_id=deal_id, type='status')
            #     if ('discuss_price' == result['current_stage']) and (status == 'won'):
            #         return True
            #     else:
            #         return False

            else:
                print('状态错误！')

    except exceptions.Timeout as e:
        print('请求超时：' + str(e))
    except exceptions.HTTPError as e:
        print('请求错误：' + str(e))

# 登录dist，返回登录auth
def login_dist(email, password):
    dist_login_url = ''
    result = post(url = dist_login_url, json = {"email": email, "password": password})
    if check_status(result=result):
        return result.json()['auth_token']
    else:
        print(result.json())

# 核价表单，创建出行人员
def creat_user(deal_id, adult, child):
    travelers_url = '' + str(deal_id) + ''
    result = post(url = travelers_url, json = {"adult": adult, "child": child}, headers = headers).json()
    # traveler_id = result['travelers'][0]['id']
    traveler_info = result['travelers']
    return traveler_info

# 核价表单，创建房间
def creat_room(deal_id, number):
    rooms_url = '' + str(deal_id) + ''
    result = post(url=rooms_url, json={"number":int(number)}, headers = headers).json()
    # room_id = result['rooms'][0]['id']
    room_info = result['rooms']
    return room_info

# 将创建的出行人员，添加到房间中，并修改房型信息
def add_user_to_room(deal_id):
    try:
        traveler_info = creat_user(deal_id = deal_id, adult = 4, child = 2)
        room_info = creat_room(deal_id = deal_id, number = 3)

        # 房间1，设置2个成人，1个儿童
        url1 = '' + str(deal_id) + '' + str(room_info[0]['id'])
        sleep(1)
        put(url = url1, json = {"adult_ids": [traveler_info[0]['id'],traveler_info[1]['id']]}, headers = headers)
        put(url=url1, json={"child_ids": [traveler_info[4]['id']]}, headers=headers)

        # 房间2，设置1个成人，1个儿童
        url2 = '' + str(deal_id) + '' + str(room_info[1]['id'])
        sleep(1)
        put(url=url2, json={"adult_ids": [traveler_info[2]['id']]}, headers=headers)
        sleep(1)
        put(url=url2, json={"child_ids": [traveler_info[5]['id']]}, headers=headers)

        # 房间3，设置1个成人，0个儿童
        url3 = '' + str(deal_id) + '' + str(room_info[2]['id'])
        sleep(1)
        put(url=url3, json={"adult_ids": [traveler_info[3]['id']]}, headers=headers)

        # 大床、双床/多人床、其他（默认）
        # 第1间房，默认为大床房，不需要修改
        # 第2间房，修改成双床/多人床
        put(url=url2, json={"bed_type":"multi"}, headers=headers)
        # 第3间房，修改成其他，并设置备注信息
        put(url=url3, json={"bed_type":"other"}, headers=headers)
        put(url=url3, json={"remark":"测试其他房型备注信息"}, headers=headers)

    except exceptions.Timeout as e:
        print('请求超时：' + str(e))
    except exceptions.HTTPError as e:
        print('请求错误：' + str(e))

    else:
        print('将出行人员添加至房间中失败！请手动检查交易核价表单中的信息是否正确！')

# 确认核价表单
def confirm_price_check(deal_id):
    plan_id = deal_info(deal_id = deal_id, type = 'plan_id')

    result = post(url='' + str(plan_id) + '', json = {"status":"processing"})

    if result.json()['data']['status'] == 'processing':
        print('核价表单，确认成功！')
    else:
        print('核价表单，确认失败！')

# 完成核价
def finish_price_check(deal_id):
    plan_id = deal_info(deal_id=deal_id, type='plan_id')

    result = post(url='' + str(plan_id) + '', json={"status": "finished"})

    if result.json()['data']['status'] == 'finished':
        print('核价表单，核价成功！')
    else:
        print('核价表单，核价失败！')

# 获取方案的成本价
def get_prime_price(deal_id):
    url = '' + str(deal_id) + ''
    result = get(url = url, headers = headers)
    if check_status(result = result):
        prime_price = result.json()['unified_plan']['prime_price']
        return int(float(prime_price))

# 设置方案的最终报价
def set_final_price(deal_id, final_price):
    url = '' + str(deal_id) + ''
    json = {"final_price":final_price}
    result = put(url = url, json = json, headers = headers)
    if check_status(result = result):
        print('最终报价设置成功！')

# 获取交易签约表单的信息
def get_sign_form_info(deal_id):
    url = '' + str(deal_id) + ''
    result = get(url = url, headers = headers)
    return result.json()

#
def a():
    return 1

#
def b():
    return 2

# 阶段跳转，从本阶段，跳转至下个阶段或状态
def jump_next_states(deal_id):
    result = deal_info(deal_id=deal_id, type='stage')
    current_stage = result['current_stage']

    # 销售联系->需求沟通
    if current_stage == 'contact_customer':
        put(url = '' + str(deal_id), json = {""}, headers = headers)
        check_jump_states(deal_id = deal_id, from_stage = current_stage)

    # 需求沟通->方案准备
    elif current_stage == 'discover_needs':
        put(url = '' + str(deal_id), json = {""}, headers = headers)
        check_jump_states(deal_id = deal_id, from_stage = current_stage)

    # 方案准备->方案讨论
    elif current_stage == 'prepare_proposal':

        Dist_Authorization = login_dist(email = Dist_email, password = Dist_password)
        dist_headers = {'Authorization': Dist_Authorization}
        # print(dist_headers)
        post(url = '' + Dist_id + '', json = {""}, headers = dist_headers)
        check_jump_states(deal_id=deal_id, from_stage=current_stage)

    # 方案讨论->价格讨论
    elif current_stage == 'discuss_proposal':

        # 填写核价表单
        add_user_to_room(deal_id = deal_id)
        url = '' + str(deal_id) + ''
        json = {""}
        result = post(url = url, json = json, headers = headers)

        # 确认核价表单、完成核价
        confirm_price_check(deal_id = deal_id)
        sleep(1)
        finish_price_check(deal_id = deal_id)

        sleep(2)

        if check_jump_states(deal_id = deal_id, from_stage = current_stage):
            return True
        else:
            return False

    # 价格讨论->已签单
    elif current_stage == 'discuss_price':

        # 设置最终报价
        prime_price = get_prime_price(deal_id = deal_id)
        final_price = prime_price + 1
        set_final_price(deal_id = deal_id, final_price = final_price)
        # 录入收入，确认收入
        # 收入这里有点麻烦，但是这里卡住了签约表单的保存，因为付款时的合同，是签约表单中的必填项


        # 填写签约表单
        # 填写姓名和拼音
        # 默认6个出行人员，4个成人和2个儿童
        result = get_sign_form_info(deal_id = deal_id)

        traveler_id0 = result['sign_form']['travelers_attributes'][0]['id']
        url0 = '' + str(deal_id) + '' + str(traveler_id0)
        json0 = {"name": "张三", "pinyin": "ZHANG/SAN", "age": 30, "gender": "male"}
        put(url = url0, json = json0, headers = headers)

        traveler_id1 = result['sign_form']['travelers_attributes'][1]['id']
        url1 = '' + str(deal_id) + '' + str(traveler_id1)
        json1 = {"name": "李四", "pinyin": "LI/SI", "age": 31, "gender": "male"}
        put(url = url1, json = json1, headers = headers)

        traveler_id2 = result['sign_form']['travelers_attributes'][2]['id']
        url2 = '' + str(deal_id) + '' + str(traveler_id2)
        json2 = {"name": "王五", "pinyin": "WANG/WU", "age": 32, "gender": "female"}
        put(url = url2, json = json2, headers = headers)

        traveler_id3 = result['sign_form']['travelers_attributes'][3]['id']
        url3 = '' + str(deal_id) + '' + str(traveler_id3)
        json3 = {"name": "赵六", "pinyin": "ZHAO/LIU", "age": 33, "gender": "female"}
        put(url = url3, json = json3, headers = headers)

        traveler_id4 = result['sign_form']['travelers_attributes'][4]['id']
        url4 = '' + str(deal_id) + '' + str(traveler_id4)
        json4 = {"name": "儿童", "pinyin": "ER/TONG", "age": 10, "gender": "male"}
        put(url = url4, json = json4, headers = headers)

        traveler_id5 = result['sign_form']['travelers_attributes'][5]['id']
        url5 = '' + str(deal_id) + '' + str(traveler_id5)
        json5 = {"name": "小孩", "pinyin": "XIAO/HAI", "age": 11, "gender": "male"}
        put(url=url5, json=json5, headers=headers)

        # 保存签约表单
        # sign_form_url = {}
        # sign_form_json = {}


        # 确认全款

        # check_jump_states(deal_id=deal_id, from_stage=current_stage)

    else:
        print('请检查交易的状态，是否正确!')

# # 检查对应方案所有预定的状态
# def check_booking_status(plan_id):
#     return 1
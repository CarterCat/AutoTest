from auto_order.controller import create_deal, jump_next_states,deal_info
from time import sleep

deal_id = create_deal()
plan_id = deal_info(deal_id = deal_id, type = 'plan_id')

print('当前交易ID：' + str(deal_id))
print('当前方案ID：' + str(plan_id))

# 跳转至"需求沟通"
sleep(2)
jump_next_states(deal_id= deal_id)

# 跳转至"方案准备"
sleep(2)
jump_next_states(deal_id= deal_id)

# 跳转至"方案讨论"
sleep(2)
jump_next_states(deal_id= deal_id)

result = deal_info(deal_id= deal_id, type= 'stage')
print('当前交易所处阶段：' + result['current_stage'])

# 跳转至"价格讨论"
# sleep(2)
# print('=========方案进入核价阶段=========')
# print('核价表单，选择最终核改！默认添加3个成人，2个儿童，3间房！')
# if jump_next_states(deal_id= deal_id):
#     print('=========方案已核价，进入"价格讨论"阶段=========')
# else:
#     result = deal_info(deal_id=deal_id, type='stage')
#     print('当前交易所处阶段：' + result['current_stage'])
#     print('=========方案核价或阶段跳转失败=========')

# 跳转至"已签单"
# sleep(2)
# jump_next_states(deal_id= deal_id)

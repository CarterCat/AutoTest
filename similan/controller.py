from requests import put, post, get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import json, time

def submit_order(self):
    return 1

def check_order(self):
    return 1

def cancel_order(self):
    return 1

def check_status(self):
    return 1

def get_order_info(order_id, type):
    url = ''
    headers = ''
    order_info = json.loads('{'+ order_id +'}')
    order_json = post(url=url, json=order_info, headers=headers).json()

    if type == '':
        result = order_json['']
        return result

    if type == '':
        result = order_json['']
        return result

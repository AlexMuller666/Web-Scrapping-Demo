import time
import requests
import os.path

import vk.vk_token

token = vk.vk_token.token

path = '../vk/result'


def get_vk_data(url, params):
    repeat = True
    while repeat:
        resp = requests.get(url, params=params)
        data = resp.json()

        if 'error' in data and 'error_code' in data['error'] and data['error']['error_code'] == 6:
            time.sleep(1)
        else:
            repeat = False

    return data['response']


def try_except(elem, target):
    if elem in target:
        try:
            target_item = target[elem]

        except:
            target_item = 'Empty'
    else:
        target_item = 'None'

    if target_item == '':
        target_item = 'None'

    return target_item


def path_set(path):
    if os.path.exists(path) is False:
        os.mkdir(path)
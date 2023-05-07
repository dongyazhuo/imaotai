import datetime
import json
import time
from email.mime.text import MIMEText

import config
from encrypt import Encrypt
import requests
import hashlib
import smtplib
import logging

AES_KEY = 'qbhajinldepmucsonaaaccgypwuvcjaa'
AES_IV = '2018534749963515'
SALT = '2af72f100c356273d46284f6fd1dfc08'

CURRENT_TIME = str(int(time.time() * 1000))
headers = {}

header_context = f'''
Host: app.moutai519.com.cn
MT-User-Tag: 0
Accept: */*
MT-Network-Type: WIFI
MT-Token: 1
MT-Team-ID: 
MT-Info: 028e7f96f6369cafe1d105579c5b9377
MT-Device-ID: 2F2075D0-B66C-4287-A903-DBFF6358342A
MT-Bundle-ID: com.moutai.mall
Accept-Language: en-CN;q=1, zh-Hans-CN;q=0.9
MT-Request-ID: 167560018873318465
MT-APP-Version: 1.3.7
User-Agent: iOS;16.3;Apple;?unrecognized?
MT-R: clips_OlU6TmFRag5rCXwbNAQ/Tz1SKlN8THcecBp/HGhHdw==
Content-Length: 93
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: application/json
userId: 2
'''


def init_headers(user_id: str = '1', token: str = '2'):
    for k in header_context.rstrip().lstrip().split("\n"):
        temp_l = k.split(': ')
        dict.update(headers, {temp_l[0]: temp_l[1]})
    dict.update(headers, {"userId": user_id})
    dict.update(headers, {"MT-Token": token})


def signature(data: dict):
    keys = sorted(data.keys())
    temp_v = ''
    for item in keys:
        temp_v += data[item]
    text = SALT + temp_v + CURRENT_TIME
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf8'))
    md5 = hl.hexdigest()
    return md5


print()


def get_vcode(mobile: str):
    params = {'mobile': mobile}
    md5 = signature(params)
    dict.update(params, {'md5': md5, "timestamp": CURRENT_TIME})
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/user/register/vcode", json=params,
                              headers=headers)
    if responses.status_code != 200:
        logging.info(
            f'get v_code : params : {params}, response code : {responses.status_code}, response body : {responses.json()}')


def login(mobile: str, v_code: str):
    params = {'mobile': mobile, 'vCode': v_code, 'ydToken': '', 'ydLogId': ''}
    md5 = signature(params)
    dict.update(params, {'md5': md5, "timestamp": CURRENT_TIME})
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/user/register/login", json=params,
                              headers=headers)
    if responses.status_code != 200:
        logging.info(
            f'login : params : {params}, response code : {responses.status_code}, response body : {responses.json()}')
    dict.update(headers, {'MT-Token': responses.json()['data']['token']})
    dict.update(headers, {'userId': responses.json()['data']['userId']})
    return responses.json()['data']['token'], responses.json()['data']['userId']


def get_current_session_id():
    day_time = int(time.mktime(datetime.date.today().timetuple())) * 1000
    responses = requests.get(f"https://static.moutai519.com.cn/mt-backend/xhr/front/mall/index/session/get/{day_time}")
    if responses.status_code != 200:
        logging.warning(
            f'get_current_session_id : params : {day_time}, response code : {responses.status_code}, response body : {responses.json()}')
    current_session_id = responses.json()['data']['sessionId']
    dict.update(headers, {'current_session_id': str(current_session_id)})


def get_location_count(city: str, item_code: str):
    day_time = int(time.mktime(datetime.date.today().timetuple())) * 1000
    session_id = headers['current_session_id']
    responses = requests.get(
        f"https://static.moutai519.com.cn/mt-backend/xhr/front/mall/shop/list/slim/v3/{session_id}/{city}/{item_code}/{day_time}")
    if responses.status_code != 200:
        logging.warning(
            f'get_location_count : params : {day_time}, response code : {responses.status_code}, response body : {responses.json()}')
    shops = responses.json()['data']['shops']
    max_count = 0
    max_shop_id = 0
    for shop in shops:
        shopId = shop['shopId']
        items = shop['items']
        for item in items:
            if item['itemId'] != str(item_code):
                continue
            if item['inventory'] > max_count:
                max_count = item['inventory']
                max_shop_id = shopId

    logging.debug(f'item code {item_code}, max shop id : {max_shop_id}, max count : {max_count}')
    return max_shop_id


encrypt = Encrypt(key=AES_KEY, iv=AES_IV)


def act_params(shop_id: str, item_id: str):
    # {
    #     "actParam": "a/v0XjWK/a/a+ZyaSlKKZViJHuh8tLw==",
    #     "itemInfoList": [
    #         {
    #             "count": 1,
    #             "itemId": "2478"
    #         }
    #     ],
    #     "shopId": "151510100019",
    #     "sessionId": 508
    # }
    session_id = headers['current_session_id']
    userId = headers['userId']
    params = {"itemInfoList": [{"count": 1, "itemId": item_id}],
              "sessionId": int(session_id),
              "userId": userId,
              "shopId": shop_id
              }
    s = json.dumps(params)
    act = encrypt.aes_encrypt(s)
    params.update({"actParam": act})
    return params


def send_email(msg: str):
    if config.EMAIL_SENDER_USERNAME is None or config.EMAIL_SENDER_USERNAME == '':
        return
    smtp = smtplib.SMTP()
    smtp.connect(config.SMTP_SERVER, config.SMTP_PORT)
    smtp.login(config.EMAIL_SENDER_USERNAME, config.EMAIL_SENDER_PASSWORD)

    message = MIMEText(msg, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '[i茅台登录失效]'
    # 发送方信息
    message['From'] = config.EMAIL_SENDER_USERNAME
    # 接受方信息
    message['To'] = config.EMAIL_RECEIVER

    smtp.sendmail(config.EMAIL_SENDER_USERNAME, config.EMAIL_RECEIVER, message.as_string())
    smtp.quit()


def reservation(params: dict, mobile: str):
    params.pop('userId')
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/mall/reservation/add", json=params,
                              headers=headers)
    if responses.text.__contains__('bad token'):
        send_email(f'[{mobile}],登录token失效，需要重新登录')
        raise RuntimeError
    logging.info(
        f'预约 : mobile:{mobile} : params : {params}, response code : {responses.status_code}, response body : {responses.json()}')

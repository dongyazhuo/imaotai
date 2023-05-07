import configparser
import json
import os

import process

config = configparser.ConfigParser()  # 类实例化
# 定义文件路径
home_path = os.getenv("HOME")
path = home_path + '/.imaotai/credentials'
try:
    os.mkdir(home_path + '/.imaotai/')
except OSError:
    pass
config.read(path)
sections = config.sections()
providers = {
    "1": "河北省",
    "2": "山西省",
    "3": "吉林省",
    "4": "辽宁省",
    "5": "黑龙江省",
    "6": "陕西省",
    "7": "甘肃省",
    "8": "青海省",
    "9": "山东省",
    "10": "福建省",
    "11": "浙江省",
    "12": "河南省",
    "13": "湖北省",
    "14": "湖南省",
    "15": "江西省",
    "16": "江苏省",
    "17": "安徽省",
    "18": "广东省",
    "19": "海南省",
    "20": "四川省",
    "21": "贵州省",
    "22": "云南省",
    "23": "北京市",
    "24": "上海市",
    "25": "天津市",
    "26": "重庆市",
    "27": "内蒙古自治区",
    "28": "新疆维吾尔自治区",
    "29": "宁夏回族自治区",
    "30": "广西壮族自治区",
    "31": "西藏自治区"
}

if __name__ == '__main__':

    while True:
        process.init_headers()
        print(json.dumps(providers, indent=5, ensure_ascii=False))
        city = input("选择序号[23]:").lstrip().rstrip()
        if city == '':
            city = '23'
        city = providers.get(city)
        keyword = input("输入门店关键字[廊坊]:").lstrip().rstrip()
        if keyword == '':
            keyword = city
        mobile = input("输入手机号[13812341234]:").lstrip().rstrip()
        process.get_vcode(mobile)
        code = input(f"输入 [{mobile}] 验证码[1234]:").lstrip().rstrip()
        token, userId = process.login(mobile, code)
        if mobile not in sections:
            config.add_section(mobile)  # 首先添加一个新的section
        config.set(mobile, 'city', str(city))
        config.set(mobile, 'token', str(token))
        config.set(mobile, 'userId', str(userId))
        config.set(mobile, 'keyword', str(keyword))
        config.write(open(path, 'w+'))  # 保存数据
        condition = input(f"是否继续输入[Y/N]:").lstrip().rstrip()
        condition = condition.lower()
        if condition == 'n':
            break

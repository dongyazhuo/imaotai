import configparser
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

if __name__ == '__main__':

    while True:
        process.init_headers()
        city = input("Enter city name[北京市]:").lstrip().rstrip()
        if city == '':
            city = '北京市'
        if not city.endswith("市"):
            city += "市"
        mobile = input("Enter mobile No[13812341234]:").lstrip().rstrip()
        process.get_vcode(mobile)
        code = input(f"Enter [{mobile}] verify code[1234]:").lstrip().rstrip()
        token, userId = process.login(mobile, code)
        if mobile not in sections:
            config.add_section(mobile)  # 首先添加一个新的section
        config.set(mobile, 'city', str(city))
        config.set(mobile, 'token', str(token))
        config.set(mobile, 'userId', str(userId))

        condition = input(f"是否继续输入[Y/N]:").lstrip().rstrip()
        condition = condition.lower()
        if condition == 'n':
            break

    # if not os.path.exists(path):
    #     os.mknod(path)
    config.write(open(path, 'w+'))  # 保存数据


# i茅台预约脚本
## 原理：
### 1、登录获取验证码
### 2、输入验证码获取TOKEN
### 3、获取当日SESSION ID
### 4、根据配置文件预约CONFIG文件中，所在城市的i茅台商品（仅预约兔茅）

## 使用：
### 0、rename config.py.example config.py
```shell
mv config.py.example config.py
```
### 1、安装依赖
```shell
pip3 install -r requirements.txt
```
### 2、修改config.py Email相关的配置.如果出现token失效等预约失败,会进行邮件通知。不需要的话请设置 EMAIL_SENDER_USERNAME 为空
```shell
EMAIL_SENDER_USERNAME = "sender@126.com"
EMAIL_SENDER_PASSWORD = "XXXGKIB"
EMAIL_RECEIVER = EMAIL_SENDER_USERNAME
```
### 3、按提示输入 预约城市、手机号、验证码 等，生成的token等 配置文件会保存在 $HOME/.imaotai/credentials, 很长时间不再需要登录。支持多账号
```shell
mobian@mobian:~/app/imaotai$ python3 login.py
{
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
选择预约省份序号[23]:23
输入门店关键字[西直门店]:西直门
输入手机号[13812341234]:186116*****
输入 [186116****] 验证码[1234]:3268
是否继续添加账号[Y/N]:n
```
```shell
mobian@mobian:~/app/imaotai$ cat ~/.imaotai/credentials 
[1850006****]
city = 西安市
token = zF3viZiQyUeYb5i4dxAhcBWguXS5VFYUPS5Di7BdsLs
userid = 106944****

[1863637****]
city = 北京市
token = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
userid = 1102514****

[1861164****]
city = 北京市
token = 6INvrtyGOTdpsvFmiw0I4FoFNDyG-ekt2WFsQsU9nBU
userid = 10677****
```
### 4、python3 main.py ,执行预约操作
```shell
python3 main.py
```

## 注意:
### 1、手机登录以后，脚本token可能会失效。
### 2、可以配置一个定时任务，执行每日自动预约。 
```shell
# imaotai
10 9 * * * root python3 /home/mobian/app/imaotai/main.py >> /var/log/imaotai.log
```
### 3、


##### 感谢提供的文档：https://blog.csdn.net/weixin_47481826/article/details/128893239

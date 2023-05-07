
# i茅台预约脚本
## 原理：
### 1、登录获取验证码
### 2、输入验证码获取TOKEN
### 3、获取当日SESSION ID
### 4、根据配置文件预约CONFIG文件中，所在城市的i茅台商品（仅预约兔茅）

## 使用：
### rename config.py.example config.py
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
Enter city name[北京市]:
Enter mobile No[13812341234]:1861164****
Enter [1861164****] verify code[1234]:1433
是否继续输入[Y/N]:n
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
10 9 * * * root python3 /home/mobian/app/imaotai/main.py >> /tmp/logs/imaotai.log
```
### 3、


##### 感谢提供的文档：https://blog.csdn.net/weixin_47481826/article/details/128893239

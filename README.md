
# i茅台预约脚本
## 原理：
### 1、登录获取验证码
### 2、输入验证码获取TOKEN
### 3、获取当日SESSION ID
### 4、根据配置文件预约CONFIG文件中，所在城市的i茅台商品（仅预约兔茅）

## 使用：
### 1、修改config.py Email相关的配置.如果出现token失效等预约失败,会进行邮件通知。不需要的话请设置 EMAIL_SENDER_USERNAME 为空
### 2、python3 login.py ,按提示输入 预约城市、手机号、验证码 等，配置文件会保存在 $HOME/.imaotai/credentials,支持多账号
### 3、python3 main.py ,执行预约操作

## 注意:
### 1、手机登录以后，脚本token会失效。
### 2、可以配置一个定时任务，执行每日自动预约。 [cron 10 9 * * * python3 main.py]
### 3、


#### 感谢提供的文档：https://blog.csdn.net/weixin_47481826/article/details/128893239

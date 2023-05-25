ITEM_MAP = {
    "10213": "53%vol 500ml贵州茅台酒（癸卯兔年）",
    "10214": "53%vol 375ml×2贵州茅台酒（癸卯兔年）",
    "10056": "53%vol 500ml茅台1935",
    "2478": "53%vol 500ml贵州茅台酒（珍品）"
}

# 需要预约的商品(默认只预约2个兔茅)
########################
ITEM_CODES = ['10213', '10214']

# 预约失败的邮件通知，默认不发送，发送需要配置发件人信息（一般为登录过期，token失效）
########################
# 发件人邮箱 ： hello@hi.com
EMAIL_SENDER_USERNAME = "@"
# 发件人密码：123456
EMAIL_SENDER_PASSWORD = "x"
# 发件人邮箱服务器
SMTP_SERVER = "smtp." + EMAIL_SENDER_USERNAME.split("@")[1]
# 发件人邮箱服务器端口
SMTP_PORT = 25
# 收件人邮箱
EMAIL_RECEIVER = EMAIL_SENDER_USERNAME
########################

# 预约规则配置
########################
# 预约本市出货量最大的门店
MAX_ENABLED = True
# 预约你的位置附近门店
DISTANCE_ENABLED = False
########################

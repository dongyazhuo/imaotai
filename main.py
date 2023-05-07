import config
import login
import process

# 获取当日session id
process.get_current_session_id()

configs = login.config
for section in configs.sections():
    mobile = section
    city = configs.get(section, 'city')
    token = configs.get(section, 'token')
    userId = configs.get(section, 'userid')

    process.UserId = userId
    process.TOKEN = token
    process.init_headers(user_id=userId, token=token)
    # 根据配置中，要预约的商品ID，城市 进行自动预约
    for item in config.ITEM_CODES:
        max_shop_id = process.get_location_count(city=city, item_code=item)
        reservation_params = process.act_params(max_shop_id, item)
        process.reservation(reservation_params)

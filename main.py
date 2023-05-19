import logging
import sys

import config
import login
import process

DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
                    stream=sys.stdout,
                    datefmt=DATE_FORMAT)

# 获取当日session id
process.get_current_session_id()

configs = login.config
for section in configs.sections():
    mobile = section
    city = configs.get(section, 'city')
    token = configs.get(section, 'token')
    userId = configs.get(section, 'userid')
    keyword = configs.get(section, 'keyword')

    process.UserId = userId
    process.TOKEN = token
    process.init_headers(user_id=userId, token=token)
    # 根据配置中，要预约的商品ID，城市 进行自动预约
    try:
        for item in config.ITEM_CODES:
            max_shop_id = process.get_location_count(city=city, item_code=item, keyword=keyword)
            if int(max_shop_id) == 0:
                continue
            reservation_params = process.act_params(max_shop_id, item)
            process.reservation(reservation_params, mobile)
    except BaseException as e:
        logging.error(e)

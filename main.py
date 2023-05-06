import config
import process

# 获取当日session id
process.get_current_session_id()

# 根据配置中，要预约的商品ID，城市 进行自动预约
for item in config.ITEM_CODES:
    max_shop_id = process.get_location_count(city=config.CITY, item_code=item)
    reservation_params = process.act_params(max_shop_id, item)
    process.reservation(reservation_params)

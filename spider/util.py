import csv
import hashlib
from urllib.parse import urlencode


def get_xiapi_match(params):
    data = urlencode(params)
    str_request = f"55b03{hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()}55b03"
    if_none_match = f"55b03-{hashlib.md5(str_request.encode(encoding='UTF-8')).hexdigest()}"
    return {
        'if-none-match-': if_none_match
    }

def create_folder(folder_path):
    try:
        folder_path.mkdir(parents=True)
    except:
        pass

def create_csv(path):
    with open(path, 'w', encoding='utf-8_sig', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows([['itemid-shopid-catid', 'similar-flag', 'name', 'price', 'price_before_discount', 'discount', 'rating_star', 'historical_sold', 'comment_count']])
        f.flush()

def get_info(item):
    item_shop_carId = '-'.join(map(str, [item.get('itemid'), item.get('shopid'), item.get('catid')]))
    name = item.get('name')
    discount = item.get('discount') if item.get('discount') else '10'
    price_min, price_max = item.get('price_min') // 100000, item.get('price_max') // 100000
    price = f'{price_min}-{price_max}' if price_min != price_max else price_min
    if discount == '10':
        price_before_discount = price
    else:
        price_min_before_discount, price_max_before_discount = item.get('price_min_before_discount') // 100000, item.get('price_max_before_discount') // 100000
        price_before_discount = f'{price_min_before_discount}-{price_max_before_discount}' if price_min_before_discount != price_max_before_discount else price_min_before_discount
    rating_star = item.get('item_rating', {}).get('rating_star')
    rating_star = round(rating_star, 1) if rating_star else rating_star
    historical_sold, cmt_count = item.get('historical_sold'), item.get('cmt_count')
    name = name.strip()
    info = [item_shop_carId, 0, name, price, price_before_discount, discount, rating_star, historical_sold, cmt_count]
    # info = list(map(lambda x: x.encode('utf-8').decode('utf-8') if type(x) == type(str) else x, info))
    return info
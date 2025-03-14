import json
from typing import List, Dict
from base import JsonSerializable, NON_STATED
from raw_data_handlers import PoizonProductRaw

#todo не уверен в верности проверки
def any_in_stock(raw_data: PoizonProductRaw) -> bool:
    if 'price' not in raw_data.skus[0]:
        return False
    for sku in raw_data.skus:
        if 'price' in sku:
            if sku['price']['quantity'] != '0':
                return True
        else: return False
    return False

def is_in_stock(sku_id: int, raw_data: PoizonProductRaw) -> bool:
    if 'price' not in raw_data.skus[0]:
        return False

    for sku in raw_data.skus:
            if sku['skuId'] == sku_id and sku['price']['quantity'] != 0:
                return True
    return False

class ParseSizes(JsonSerializable):
    """
    class that parses all info about sizes: current_sizes, size_ids, size_table
    """
    def __init__(self,
                 current_sizes: List[int] | NON_STATED,
                 size_ids: List[int] | NON_STATED,
                 size_table: Dict[str, str] | NON_STATED,):
        self.current_sizes = current_sizes
        self.size_ids = size_ids
        self.size_table = size_table

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        if not any_in_stock(raw_data):
            return cls(current_sizes=NON_STATED, size_ids=NON_STATED, size_table=NON_STATED)

        current_sizes = []
        size_ids = []
        size_table = {}
        for i in raw_data.skus:
            if is_in_stock(sku_id=i['skuId'], raw_data=raw_data):
                for j in i["properties"]:
                    if 'saleProperty' in j:
                        if j["saleProperty"]["name"] == "尺码":
                            current_sizes.append(j["saleProperty"]["value"])
                            size_ids.append(j["saleProperty"]["propertyValueId"])

        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]

        if not current_sizes: current_sizes = NON_STATED
        if not size_ids: size_ids = NON_STATED
        if not size_table: size_table = NON_STATED

        return cls(current_sizes, size_ids, size_table)

class ParseColors(JsonSerializable):
    def __init__(self,
                 current_colors: List[str] | NON_STATED,
                 color_ids: List[int] | NON_STATED):
        self.current_colors = current_colors
        self.color_ids = color_ids
    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        if not any_in_stock(raw_data):
            return cls(color_ids=NON_STATED, current_colors=NON_STATED)

        current_colors = []
        color_ids = []
        for i in raw_data.skus:
            if is_in_stock(sku_id=i['skuId'], raw_data=raw_data):
                for j in i["properties"]:
                    if 'saleProperty' in j:
                        if j["saleProperty"]["name"] == "颜色":
                            current_colors.append(j["saleProperty"]["value"])
                            color_ids.append(j["saleProperty"]["propertyValueId"])

        if not current_colors: current_colors = NON_STATED
        if not color_ids: color_ids = NON_STATED

        return cls(current_colors, color_ids)

class ParseProductIds(JsonSerializable):
    def __init__(self,
                 sku_ids: List[int] | NON_STATED,
                 spu_id: int,
                 article: str):
        self.sku_ids = sku_ids
        self.spu_id = spu_id
        self.article = article

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        sku_ids = []
        for i in raw_data.skus:
            if is_in_stock(sku_id=i['skuId'], raw_data=raw_data):
                sku_ids.append(i['skuId'])

        if not sku_ids: sku_ids = NON_STATED

        return cls(sku_ids=sku_ids,
                   spu_id=raw_data.detail["spuId"],
                   article=raw_data.detail['articleNumber'])

class ParseProductProperties(JsonSerializable):
    def __init__(self,
                 product_addictive_params: Dict[str, str] | NON_STATED,
                 category: str,
                 category_id: int,
                 title: str,
                 desc: str | NON_STATED
                 ):
        self.product_addictive_params = product_addictive_params
        self.category = category
        self.category_id = category_id
        self.title = title
        self.desc = desc

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        product_addictive_params = {}
        for i in raw_data.basicParam['basicList']:
            product_addictive_params[i["key"]] = i["value"]

        return cls(product_addictive_params=product_addictive_params,
                   category=raw_data.detail.get("categoryName", NON_STATED),
                   category_id=raw_data.detail["categoryId"],
                   title=raw_data.detail["title"],
                   desc=raw_data.detail["desc"] if raw_data.detail["desc"] else NON_STATED)

class ParseBrandInfo(JsonSerializable):
    def __init__(self,
                 brand: str,
                 brand_id: int,
                 brand_logo: str):
        self.brand = brand
        self.brand_id = brand_id
        self.brand_logo = brand_logo

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        return cls(brand=raw_data.brandRootInfo["brandItemList"][0]["brandName"],
                   brand_id=raw_data.detail["brandId"],
                   brand_logo=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"])

class ParsePriceInfo(JsonSerializable):
    def __init__(self,
                 recommended_prices: List[int] | NON_STATED, #TODO не очень вариант тк флор прайс иногда бывает на евро доставку
                 types_of_prices: Dict[int, Dict[int, int]] | NON_STATED,
                 floor_price: int | NON_STATED,
                 max_price: int | NON_STATED,):
        self.recommended_prices = recommended_prices
        self.types_of_prices = types_of_prices
        self.floor_price = floor_price
        self.max_price = max_price
    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        if not any_in_stock(raw_data): # проверка есть ли хоть один товар в продаже, если нет - возвращаем NON_STATED
            return cls(recommended_prices=NON_STATED, types_of_prices=NON_STATED, floor_price=NON_STATED, max_price=NON_STATED)
        recommended_prices = []
        for item in raw_data.skus:
            recommended_prices.append(item['authPrice'])

        types_of_prices = {}
        for item in raw_data.skus:
            sku_id = item['skuId']
            prices = {}
            if is_in_stock(sku_id=sku_id, raw_data=raw_data):
                for price in item['price']['prices']:
                    prices[price['tradeType']] = price['price']
                types_of_prices[sku_id] = prices
        floor_price = raw_data.price['item']['floorPrice']
        max_price = raw_data.price['item']['maxPrice']

        return cls(recommended_prices=recommended_prices,
                   types_of_prices=types_of_prices,
                   floor_price=floor_price,
                   max_price=max_price)



class ParseImages(JsonSerializable):
    def __init__(self,
                 current_images: Dict[int, List[str]],
                 images_ids: List[str], #TODO сделать дикт skuId: ValueId
                 general_logo_image: str):
        self.current_images = current_images # colorId:img_url
        self.images_ids = images_ids #imgIds
        self.general_logo_image = general_logo_image

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        current_images = {}
        images_ids = []
        if not any_in_stock(raw_data):
            return cls(current_images=NON_STATED, images_ids=NON_STATED, general_logo_image=raw_data.detail['logoUrl'])

        # sku_to_color_id = {}
        # for i in raw_data.image['spuImage']['arSkuIdRelation']:
        #     sku_to_color_id[i['propertyValueId']] = i['skuId']

        for i in raw_data.image['spuImage']['arSkuIdRelation']:
            if is_in_stock(sku_id=i['skuId'], raw_data=raw_data): # TODO переделать логику чтобы искала по ску айди
                images_ids.append(i['propertyValueId'])

        for id in images_ids:
            tmp_imgs = []
            for img in raw_data.image['spuImage']['images']:
                if id == img['propertyValueId']:
                    tmp_imgs.append(img['url'])
            current_images[id] = tmp_imgs

        if not current_images: current_images = NON_STATED
        if not images_ids: images_ids = NON_STATED

        return cls(current_images=current_images,
                   images_ids=images_ids,
                   general_logo_image=raw_data.detail['logoUrl'])



# with open('../cologne.json', 'r') as f:
#     dictData = json.load(f)
#
# raw_data = PoizonProductRaw.from_json(json_data=dictData)
#
# priceInfo = ParsePriceInfo.from_json(raw_data=raw_data)
#
# print(f'types_of_prices = {priceInfo.types_of_prices}')
# print(f'floor_price = {priceInfo.floor_price}')
# print(f'max_price = {priceInfo.max_price}')
# print(f'recommended_prices = {priceInfo.recommended_prices}')
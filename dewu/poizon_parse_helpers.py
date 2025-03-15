import json
from typing import List, Dict
from base import JsonSerializable, NON_STATED
from raw_data_handlers import PoizonProductRaw

#todo не уверен в верности проверки
def any_in_stock(raw_data: PoizonProductRaw) -> bool:
    if raw_data.price:
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

class PoizonCategoryParser(JsonSerializable):
    """
    class for getting/updating categories list api: GET /getCategories
    """

    def __init__(self, categories: Dict[str, str]):
        self.categories = categories

    @classmethod
    def from_json(cls, json_data):
        categories = {}
        for i in json_data:
            categories[i["id"]] = i["name"]
        return cls(categories=categories)

class ParseSizes(JsonSerializable):
    """
    class that parses info about sizes: current_sizes, size_table
    """
    def __init__(self,
                 current_sizes: List[int] | NON_STATED,
                 size_table: Dict[str, str] | NON_STATED,):
        self.current_sizes = current_sizes
        self.size_table = size_table

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        if not any_in_stock(raw_data):
            return cls(current_sizes=NON_STATED, size_table=NON_STATED)

        current_sizes = {}
        size_table = {}
        for item in raw_data.skus:
            sku_id = item['skuId']
            if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
                for prop in item["properties"]:
                    if 'saleProperty' in prop:
                        if prop["saleProperty"]["name"] == "尺码":
                            current_sizes[sku_id] = prop["saleProperty"]["value"]

        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]

        if not current_sizes: current_sizes = NON_STATED
        if not size_table: size_table = NON_STATED

        return cls(current_sizes, size_table)

class ParseColors(JsonSerializable):
    def __init__(self,
                 sku_to_color: Dict[int, str] | NON_STATED):
        self.sku_to_color = sku_to_color
    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        if not any_in_stock(raw_data):
            return cls(sku_to_color=NON_STATED)

        sku_to_color = {}
        for item in raw_data.skus:
            sku_id = item['skuId']
            if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
                for prop in item["properties"]:
                    if 'saleProperty' in prop:
                        if prop["saleProperty"]["name"] == "颜色":
                            sku_to_color[sku_id] = prop["saleProperty"]["value"]

        if not sku_to_color: sku_to_color = NON_STATED

        return cls(sku_to_color)

class ParseProductIds(JsonSerializable):
    def __init__(self,
                 color_ids: Dict[int, int] | NON_STATED,
                 sku_ids: List[int] | NON_STATED,
                 spu_id: int,
                 article_number: str,
                 category_id: int,
                 brand_id: str,
                 size_ids: Dict[int, int]):
        self.color_ids = color_ids
        self.sku_ids = sku_ids
        self.spu_id = spu_id
        self.article_number = article_number
        self.category_id = category_id
        self.brand_id = brand_id
        self.size_ids = size_ids

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        sku_ids = []
        for i in raw_data.skus:
            if is_in_stock(sku_id=i['skuId'], raw_data=raw_data):
                sku_ids.append(i['skuId'])

        color_ids = {}
        for item in raw_data.skus:
            sku_id = item['skuId']
            if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
                for prop in item["properties"]:
                    if 'saleProperty' in prop:
                        if prop["saleProperty"]["name"] == "颜色":
                            color_ids[sku_id] = prop["saleProperty"]["value"]
        size_ids = {}
        for item in raw_data.skus:
            sku_id = item['skuId']
            if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
                for prop in item["properties"]:
                    if 'saleProperty' in prop:
                        if prop["saleProperty"]["name"] == "尺码":
                            size_ids[sku_id] = prop["saleProperty"]["value"]

        return cls(color_ids=color_ids,
                   sku_ids=sku_ids,
                   spu_id=raw_data.detail["spuId"],
                   article_number=raw_data.detail['articleNumber'],
                   category_id=raw_data.detail["categoryId"],
                   brand_id=raw_data.detail["brandId"],
                   size_ids=size_ids)

class ParseProductProperties(JsonSerializable):
    def __init__(self,
                 product_addictive_params: Dict[str, str] | NON_STATED,
                 category: str,
                 title: str,
                 desc: str | NON_STATED
                 ):
        self.product_addictive_params = product_addictive_params
        self.category = category
        self.title = title
        self.desc = desc

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        product_addictive_params = {}
        for i in raw_data.basicParam['basicList']:
            product_addictive_params[i["key"]] = i["value"]

        return cls(product_addictive_params=product_addictive_params,
                   category=raw_data.detail.get("categoryName", NON_STATED),
                   title=raw_data.detail["title"],
                   desc=raw_data.detail["desc"] if raw_data.detail["desc"] else NON_STATED)

class ParseBrandInfo(JsonSerializable):
    def __init__(self,
                 brand_name: str,
                 brand_logo: str):
        self.brand_name = brand_name
        self.brand_logo = brand_logo

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        return cls(brand_name=raw_data.brandRootInfo["brandItemList"][0]["brandName"],
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
            if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
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
    def __init__(self, general_logo_image, current_images):
        self.general_logo_image = general_logo_image
        self.current_images = current_images

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        if not any_in_stock(raw_data):
            return cls(general_logo_image=NON_STATED, current_images=NON_STATED)
        general_logo_image = raw_data.detail['logoUrl']
        sku_to_image_id = {} #skuID:propertyValueId of color
        image_id_to_sku = {}
        for item in raw_data.image['spuImage']['arSkuIdRelation']:
                if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
                    image_id_to_sku[item['propertyValueId']] = item['skuId']
                    sku_to_image_id[item['skuId']] = item['propertyValueId']
        current_images = {}
        for sku in sku_to_image_id.keys():
            imgs = []
            for item in raw_data.image['spuImage']['images']:
                if item['propertyValueId'] == sku_to_image_id[sku]:
                    imgs.append(item['url'])
            current_images[sku] = imgs

        return cls(general_logo_image=general_logo_image,
                   current_images=current_images)


if __name__ == '__main__':
    with open('../controlles_all.json', 'r') as f:
        dictData = json.load(f)

    raw_data = PoizonProductRaw.from_json(json_data=dictData)
    priceInfo = ParsePriceInfo.from_json(raw_data=raw_data)
    images = ParseImages.from_json(raw_data=raw_data)
    ids = ParseProductIds.from_json(raw_data=raw_data)

    print(ids.color_ids)
    print(ids.sku_ids)
    print(ids.category_id)
    print(ids.article_number)
    print(ids.spu_id)

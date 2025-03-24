from typing import List, Dict
from dewu.base import JsonSerializable, NON_STATED
from dewu.raw_data_handlers import PoizonProductRaw

#todo не уверен в верности проверки
def any_in_stock(raw_data: PoizonProductRaw) -> bool:
    nothing_in_stock = True
    if raw_data.price:
        if 'price' not in raw_data.skus[0]:
            return False
    for sku in raw_data.skus:
        if 'price' in sku:
            if int(sku['price']['quantity']) != 0:
                nothing_in_stock = False
    if nothing_in_stock:
        return False
    return True
def is_in_stock(sku_id: int, raw_data: PoizonProductRaw) -> bool:
    if 'price' not in raw_data.skus[0]:
        return False

    for sku in raw_data.skus:
            if sku['skuId'] == sku_id and sku['price']['quantity'] != 0:
                return True
    return False

# new
class ProductCore(JsonSerializable):
    def __init__(self, additional_params: Dict[str, str],
                 category: str,
                 category_id: int,
                 title: str,
                 description: str,
                 article_number: int,
                 spu_id: int):
        self.additional_params = additional_params
        self.category = category
        self.category_id = category_id
        self.title = title
        self.description = description
        self.article_number = article_number
        self.spu_id = spu_id

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        product_addictive_params = {}
        for i in raw_data.basicParam['basicList']:
            product_addictive_params[i["key"]] = i["value"]
        return cls(additional_params=product_addictive_params,
                   category = raw_data.detail["categoryName"],
                   category_id = raw_data.detail["categoryId"],
                   title = raw_data.detail["title"],
                   description = raw_data.detail["desc"] if raw_data.detail["desc"] else NON_STATED,
                   article_number=raw_data.detail['articleNumber'],
                   spu_id = raw_data.detail["spuId"])

class ProductStock(JsonSerializable):
    def __init__(self,
                 recommended_prices: Dict[int, int] | NON_STATED,
                 types_of_prices: Dict[int, Dict[int, int]] | NON_STATED,
                 types_of_prices_desc: str,
                 floor_price: int | NON_STATED,
                 max_price: int | NON_STATED,
                 stock: Dict[int, int] | NON_STATED,
                 sku_ids: List[int] | NON_STATED,
                 variants: Dict[int, Dict[str, str]]):
        self.recommended_prices = recommended_prices
        self.types_of_prices = types_of_prices
        self.types_of_prices_desc = types_of_prices_desc
        self.floor_price = floor_price
        self.max_price = max_price
        self.stock = stock
        self.sku_ids = sku_ids
        self.variants = variants

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        recommended_prices = {}
        for item in raw_data.skus: recommended_prices[item['skuId']] = item['authPrice']

        types_of_prices = {}
        for item in raw_data.skus:
            sku_id = item['skuId']
            prices = {}
            for price in item['price']['prices']:
                prices[price['tradeType']] = price['price']
                types_of_prices[sku_id] = prices

        if 'item' in raw_data.price:
            floor_price = raw_data.price['item']['floorPrice']
            max_price = raw_data.price['item']['maxPrice']
        else:
            floor_price = NON_STATED
            max_price = NON_STATED

        stock = {}
        for item in raw_data.skus:
            stock[item['skuId']] = item['price']['quantity']

        sku_ids = []
        for i in raw_data.skus:
            sku_ids.append(i['skuId'])
        variants = {}
        for item in raw_data.skus:
            dict_of_props = {}
            for prop in item['properties']:
                dict_of_props[prop['saleProperty']['name']] = prop['saleProperty']['value']
            variants[item['skuId']] = dict_of_props



        return cls(recommended_prices=recommended_prices,
                   types_of_prices=types_of_prices,
                   types_of_prices_desc=NON_STATED,
                   floor_price=floor_price,
                   max_price=max_price,
                   stock=stock,
                   sku_ids=sku_ids,
                   variants=variants
                   )

class ProductSizeTable(JsonSerializable):
    def __init__(self, size_table: List[int] | NON_STATED):
        self.size_table = size_table

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        size_table = {}

        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]

        return cls(size_table=size_table)

class ProductImages(JsonSerializable):
    def __init__(self,
                 general_logo_url: str,
                 sku_to_image_url: Dict,
                 all_images: List[str]):
        self.general_logo_url = general_logo_url
        self.sku_to_image_url = sku_to_image_url
        self.all_images = all_images

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        general_logo_url = raw_data.detail['logoUrl']
        sku_to_image_id = {}  # skuID:propertyValueId of color
        image_id_to_sku = {}
        for item in raw_data.image['spuImage']['arSkuIdRelation']:
            image_id_to_sku[item['propertyValueId']] = item['skuId']
            sku_to_image_id[item['skuId']] = item['propertyValueId']
        sku_to_image_url = {}
        for sku in sku_to_image_id.keys():
            imgs = []
            for item in raw_data.image['spuImage']['images']:
                if item['propertyValueId'] == sku_to_image_id[sku]:
                    imgs.append(item['url'])
            sku_to_image_url[sku] = imgs
        all_images = []
        for item in raw_data.image['spuImage']['images']:
            all_images.append(item['url'])


        return cls(general_logo_url=general_logo_url,
                   sku_to_image_url=sku_to_image_url,
                   all_images=all_images)

class ProductBrand(JsonSerializable):
    def __init__(self,
                 brand_name: str,
                 brand_logo_url: str,
                 brand_id: int):
        self.brand_name = brand_name
        self.brand_logo_url = brand_logo_url
        self.brand_id = brand_id

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        return cls(brand_name=raw_data.brandRootInfo["brandItemList"][0]["brandName"],
                   brand_logo_url=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"],
                   brand_id=raw_data.detail["brandId"])


# if (__name__ == "__main__"):
#     with open('../double_trans_shoes.json', 'r') as f:
#         dictData = json.load(f)
#
# a = ParseStock.from_json(raw_data=PoizonProductRaw.from_json(dictData))
#
# print(a.types_of_prices)
# print(a.types_of_prices_desc)
# print(a.recommended_prices)
# print(a.floor_price)
# print('max_price=', a.max_price)
# print('sku_ids=', a.sku_ids)
# print('stock=', a.stock)
#
# b = ParseProductCore.from_json(raw_data=PoizonProductRaw.from_json(dictData))
# print(b.additional_params)
# print(b.category)
# print(b.category_id)
# print(b.title)
# print('desc=', b.description)
# print(b.article_number)
# print(b.spu_id)
#
# s = ParseSizeTable.from_json(raw_data=PoizonProductRaw.from_json(dictData))
# print('size_table=', s.size_table)
#
# i = Images.from_json(raw_data=PoizonProductRaw.from_json(dictData))
# print('general_logo_url=', i.general_logo_url)
# print('sku_to_image_url=', i.sku_to_image_url)

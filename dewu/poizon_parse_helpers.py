from typing import List, Dict
from .base import JsonSerializable, NON_STATED
from .raw_data_handlers import PoizonProductRaw

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

# class PoizonCategoryParser(JsonSerializable):
#     """
#     class for getting/updating categories list api: GET /getCategories
#     """
#
#     def __init__(self, categories: Dict[str, str]):
#         self.categories = categories
#
#     @classmethod
#     def from_json(cls, json_data):
#         categories = {}
#         for i in json_data:
#             categories[i["id"]] = i["name"]
#         return cls(categories=categories)
# #todo убрать цвет и размер добавить вместо этого список вариаций
# class ParseSizes(JsonSerializable):
#     """
#     class that parses info about sizes: current_sizes, size_table
#     """
#     def __init__(self,
#                  current_sizes: List[int] | NON_STATED,
#                  size_table: Dict[str, str] | NON_STATED,):
#         self.current_sizes = current_sizes
#         self.size_table = size_table
#
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         if not any_in_stock(raw_data):
#             return cls(current_sizes=NON_STATED, size_table=NON_STATED)
#
#         current_sizes = {}
#         size_table = {}
#         for item in raw_data.skus:
#             sku_id = item['skuId']
#             if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
#                 for prop in item["properties"]:
#                     if 'saleProperty' in prop:
#                         if prop["saleProperty"]["name"] == "尺码":
#                             current_sizes[sku_id] = prop["saleProperty"]["value"]
#
#         if "sizeInfo" in raw_data.sizeDto:
#             for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
#                 size_table[f"{i["sizeKey"]}"] = i["sizeValue"]
#
#         if not current_sizes: current_sizes = NON_STATED
#         if not size_table: size_table = NON_STATED
#
#         return cls(current_sizes, size_table)
# #todo
# class ParseColors(JsonSerializable):
#     def __init__(self,
#                  sku_to_color: Dict[int, str] | NON_STATED):
#         self.sku_to_color = sku_to_color
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         if not any_in_stock(raw_data):
#             return cls(sku_to_color=NON_STATED)
#
#         sku_to_color = {}
#         for item in raw_data.skus:
#             sku_id = item['skuId']
#             if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
#                 for prop in item["properties"]:
#                     if 'saleProperty' in prop:
#                         if prop["saleProperty"]["name"] == "颜色":
#                             sku_to_color[sku_id] = prop["saleProperty"]["value"]
#
#         if not sku_to_color: sku_to_color = NON_STATED
#
#         return cls(sku_to_color)
#
# class ParseProductIds(JsonSerializable):
#     def __init__(self,
#                  color_ids: Dict[int, int] | NON_STATED,
#                  sku_ids: List[int] | NON_STATED,
#                  spu_id: int,
#                  article_number: str,
#                  category_id: int,
#                  brand_id: str,
#                  size_ids: Dict[int, int]):
#         self.color_ids = color_ids
#         self.sku_ids = sku_ids
#         self.spu_id = spu_id
#         self.article_number = article_number
#         self.category_id = category_id
#         self.brand_id = brand_id
#         self.size_ids = size_ids
#
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         sku_ids = []
#         for i in raw_data.skus:
#             if is_in_stock(sku_id=i['skuId'], raw_data=raw_data):
#                 sku_ids.append(i['skuId'])
#
#         color_ids = {}
#         for item in raw_data.skus:
#             sku_id = item['skuId']
#             if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
#                 for prop in item["properties"]:
#                     if 'saleProperty' in prop:
#                         if prop["saleProperty"]["name"] == "颜色":
#                             color_ids[sku_id] = prop["saleProperty"]["value"]
#         size_ids = {}
#         for item in raw_data.skus:
#             sku_id = item['skuId']
#             if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
#                 for prop in item["properties"]:
#                     if 'saleProperty' in prop:
#                         if prop["saleProperty"]["name"] == "尺码":
#                             size_ids[sku_id] = prop["saleProperty"]["value"]
#
#         return cls(color_ids=color_ids,
#                    sku_ids=sku_ids,
#                    spu_id=raw_data.detail["spuId"],
#                    article_number=raw_data.detail['articleNumber'],
#                    category_id=raw_data.detail["categoryId"],
#                    brand_id=raw_data.detail["brandId"],
#                    size_ids=size_ids)
#
# class ParseProductProperties(JsonSerializable):
#     def __init__(self,
#                  product_addictive_params: Dict[str, str] | NON_STATED,
#                  category: str,
#                  title: str,
#                  desc: str | NON_STATED
#                  ):
#         self.product_addictive_params = product_addictive_params
#         self.category = category
#         self.title = title
#         self.desc = desc
#
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         product_addictive_params = {}
#         for i in raw_data.basicParam['basicList']:
#             product_addictive_params[i["key"]] = i["value"]
#
#         return cls(product_addictive_params=product_addictive_params,
#                    category=raw_data.detail.get("categoryName", NON_STATED),
#                    title=raw_data.detail["title"],
#                    desc=raw_data.detail["desc"] if raw_data.detail["desc"] else NON_STATED)
#
# class ParseBrandInfo(JsonSerializable):
#     def __init__(self,
#                  brand_name: str,
#                  brand_logo: str):
#         self.brand_name = brand_name
#         self.brand_logo = brand_logo
#
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         return cls(brand_name=raw_data.brandRootInfo["brandItemList"][0]["brandName"],
#                    brand_logo=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"])
#
# class ParsePriceInfo(JsonSerializable):
#     def __init__(self,
#                  recommended_prices: List[int] | NON_STATED, #TODO не очень вариант тк флор прайс иногда бывает на евро доставку
#                  types_of_prices: Dict[int, Dict[int, int]] | NON_STATED,
#                  floor_price: int | NON_STATED,
#                  max_price: int | NON_STATED,):
#         self.recommended_prices = recommended_prices
#         self.types_of_prices = types_of_prices
#         self.floor_price = floor_price
#         self.max_price = max_price
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         if not any_in_stock(raw_data): # проверка есть ли хоть один товар в продаже, если нет - возвращаем NON_STATED
#             return cls(recommended_prices=NON_STATED, types_of_prices=NON_STATED, floor_price=NON_STATED, max_price=NON_STATED)
#         recommended_prices = []
#         for item in raw_data.skus:
#             if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
#                 recommended_prices.append(item['authPrice'])
#
#         types_of_prices = {}
#         for item in raw_data.skus:
#             sku_id = item['skuId']
#             prices = {}
#             # if is_in_stock(sku_id=sku_id, raw_data=raw_data):
#             for price in item['price']['prices']:
#                 prices[price['tradeType']] = price['price']
#                 types_of_prices[sku_id] = prices
#
#         if 'item' in raw_data.price:
#             floor_price = raw_data.price['item']['floorPrice']
#             max_price = raw_data.price['item']['maxPrice']
#         else:
#             floor_price = NON_STATED
#             max_price = NON_STATED
#         return cls(recommended_prices=recommended_prices,
#                    types_of_prices=types_of_prices,
#                    floor_price=floor_price,
#                    max_price=max_price)
#
# class ParseImages(JsonSerializable):
#     def __init__(self, general_logo_image, current_images):
#         self.general_logo_image = general_logo_image
#         self.current_images = current_images
#
#     @classmethod
#     def from_json(cls, raw_data: PoizonProductRaw):
#         if not any_in_stock(raw_data):
#             return cls(general_logo_image=NON_STATED, current_images=NON_STATED)
#         general_logo_image = raw_data.detail['logoUrl']
#         sku_to_image_id = {} #skuID:propertyValueId of color
#         image_id_to_sku = {}
#         for item in raw_data.image['spuImage']['arSkuIdRelation']:
#                 if is_in_stock(sku_id=item['skuId'], raw_data=raw_data):
#                     image_id_to_sku[item['propertyValueId']] = item['skuId']
#                     sku_to_image_id[item['skuId']] = item['propertyValueId']
#         current_images = {}
#         for sku in sku_to_image_id.keys():
#             imgs = []
#             for item in raw_data.image['spuImage']['images']:
#                 if item['propertyValueId'] == sku_to_image_id[sku]:
#                     imgs.append(item['url'])
#             current_images[sku] = imgs
#
#         return cls(general_logo_image=general_logo_image,
#                    current_images=current_images)



# new
class ParseProductCore(JsonSerializable):
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

class ParseStock(JsonSerializable):
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

class ParseSizeTable(JsonSerializable):
    def __init__(self, size_table: List[int] | NON_STATED):
        self.size_table = size_table

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        size_table = {}

        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]

        return cls(size_table=size_table)

class Images(JsonSerializable):
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

class ParseBrand(JsonSerializable):
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

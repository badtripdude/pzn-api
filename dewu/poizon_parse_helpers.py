from typing import List, Dict
from base import JsonSerializable, NON_STATED
from raw_data_handler import PoizonProductRaw


class ParseSizes(JsonSerializable):
    """
    class that parses all info about sizes: current_sizes, size_ids, size_table
    """
    def __init__(self, current_sizes, size_ids, size_table):
        self.current_sizes = current_sizes
        self.size_ids = size_ids
        self.size_table = size_table

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        current_sizes = []
        size_ids = []
        size_table = {}
        for i in raw_data.skus:
            for j in i["properties"]:
                if 'saleProperty' in j:
                    if j["saleProperty"]["name"] == "尺码":
                        current_sizes.append(j["saleProperty"]["value"])
                        size_ids.append(j["saleProperty"]["propertyValueId"])
        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]
        return cls(current_sizes, size_ids, size_table)

class ParseColors(JsonSerializable):
    def __init__(self,current_colors, color_ids):
        self.current_colors = current_colors
        self.color_ids = color_ids
    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        current_colors = []
        color_ids = []
        for i in raw_data.skus:
            for j in i["properties"]:
                if 'saleProperty' in j:
                    if j["saleProperty"]["name"] == "颜色":
                        current_colors.append(j["saleProperty"]["value"])
                        color_ids.append(j["saleProperty"]["propertyValueId"])
        return cls(current_colors, color_ids)

class ParseProductIds(JsonSerializable):
    def __init__(self, sku_ids, spu_id, article):
        self.sku_ids = sku_ids
        self.spu_id = spu_id
        self.article = article

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        sku_ids = []
        for i in raw_data.skus:
            sku_ids.append(i['skuId'])

        return cls(sku_ids=sku_ids, spu_id=raw_data.detail["spuId"], article=raw_data.detail['articleNumber'])

class ParseProductProperties(JsonSerializable):
    def __init__(self,
                 product_addictive_params: Dict[str, str],
                 category: str,
                 category_id: int,
                 title: str,
                 desc: str
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
    def __init__(self, brand, brand_id, brand_logo):
        self.brand = brand
        self.brand_id = brand_id
        self.brand_logo = brand_logo

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        return cls(brand=raw_data.brandRootInfo["brandItemList"][0]["brandName"], brand_id=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"], brand_logo=raw_data.detail["brandId"])

class ParsePriceInfo(JsonSerializable):
    def __init__(self, floor_price, prices):
        self.floor_price = floor_price
        self.prices = prices

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        prices = []
        for i in raw_data.skus:
            if 'price' in i:
                prices.append(i["price"]["prices"][0]["price"] if i["price"]["prices"] else NON_STATED)


        return cls(
            floor_price=raw_data.price["item"]["floorPrice"] if raw_data.price else NON_STATED,
            prices=prices
        )


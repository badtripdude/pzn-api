from typing import List, Dict
from base import JsonSerializable, NON_STATED
from raw_data_handlers import PoizonProductRaw

def is_in_stock(sku: Dict) -> bool:
    if 'price' in sku:
        if sku['price']['quantity'] != 0:
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
        current_sizes = []
        size_ids = []
        size_table = {}
        for i in raw_data.skus:
            if is_in_stock(i):
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
        current_colors = []
        color_ids = []
        for i in raw_data.skus:
            if is_in_stock(i):
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
                   brand_id=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"],
                   brand_logo=raw_data.detail["brandId"])

class ParsePriceInfo(JsonSerializable):
    def __init__(self,
                 floor_price: int | NON_STATED,
                 prices: List[int] | NON_STATED):
        self.floor_price = floor_price
        self.prices = prices

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        prices = []
        for i in raw_data.skus:
            if is_in_stock(i):
                prices.append(i["price"]["prices"][0]["price"] if i["price"]["prices"] else NON_STATED)

        if not prices: prices = NON_STATED

        return cls(
            floor_price=raw_data.price["item"]["floorPrice"] if raw_data.price else NON_STATED,
            prices=prices
        )

class ParseImages(JsonSerializable):
    def __init__(self,
                 current_images: Dict[int, List[str]],
                 images_ids: List[str],
                 general_logo_image: str):
        self.current_images = current_images
        self.images_ids = images_ids
        self.general_logo_image = general_logo_image

    @classmethod
    def from_json(cls, raw_data: PoizonProductRaw):
        current_images = {}
        images_ids = []
        for i in raw_data.image['spuImage']['arSkuIdRelation']:
            images_ids.append(i['propertyValueId'])

        for id in images_ids:
            tmp_imgs = []
            for img in raw_data.image['spuImage']['images']:
                if id == img['propertyValueId']:
                    tmp_imgs.append(img['url'])
            current_images[id] = tmp_imgs

        return cls(current_images=current_images,
                   images_ids=images_ids,
                   general_logo_image=raw_data.detail['logoUrl'])



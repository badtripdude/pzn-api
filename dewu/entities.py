import json
from typing import Optional, List, Dict
from base import JsonSerializable
from poizon_parse_helpers import ParseSizes, ParseColors, ParseProductIds, ParseProductProperties, ParseBrandInfo, ParsePriceInfo
from raw_data_handlers import PoizonProductRaw
from base import NON_STATED
# class Product:
#     id: int
#     title: str
#     desc: str
#     images: list
#     category: str

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



class PoizonProduct(JsonSerializable):
    """
        class for parsing and keeping data from PoizonProductRaw
    """

    def __init__(self,
                 all_images: List[str],
                 current_images: List[str],
                 product_addictive_params: Dict[str, str] | NON_STATED,
                 article: str,
                 category: str | NON_STATED,
                 category_id: int,
                 current_colors: List[str] | NON_STATED,
                 current_sizes: List[int] | NON_STATED,
                 size_ids: List[int] | NON_STATED,
                 size_table: Dict[str, str] | NON_STATED,
                 color_ids: List[int] | NON_STATED,
                 prices: List[int] | NON_STATED,
                 sku_ids: List[int] | NON_STATED,
                 spu_id: int,
                 floor_price: int | NON_STATED,
                 brand: str,
                 brand_logo: str,
                 brand_id: str,
                 title: str,
                 desc: str | NON_STATED
                 ):
        self.all_images = all_images
        self.current_images = current_images
        self.product_addictive_params = product_addictive_params
        self.article = article
        self.category= category
        self.category_id = category_id
        self.current_colors = current_colors
        self.current_sizes = current_sizes
        self.size_ids = size_ids
        self.size_table = size_table
        self.color_ids = color_ids
        self.prices = prices
        self.sku_ids = sku_ids  # уникальный
        self.spu_id = spu_id  # общий
        self.floor_price = floor_price
        self.brand = brand
        self.brand_logo = brand_logo
        self.brand_id = brand_id
        self.title = title
        self.desc = desc

    # картинки соотносятся по цветам не по размерам
    @classmethod
    def from_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)
        # TODO товары с доставкой через европу убрать из списка, картинки
        #sizes
        size_info = ParseSizes.from_json(raw_data=raw_data)
        current_sizes = size_info.current_sizes
        size_ids = size_info.size_ids
        size_table = size_info.size_table
        #colors
        color_info = ParseColors.from_json(raw_data=raw_data)
        current_colors = color_info.current_colors
        color_ids = color_info.color_ids
        #product ids
        product_ids = ParseProductIds.from_json(raw_data=raw_data)
        sku_ids = product_ids.sku_ids
        spu_id = product_ids.spu_id
        article = product_ids.article
        #product properties
        product_properties = ParseProductProperties.from_json(raw_data=raw_data)
        product_addictive_params = product_properties.product_addictive_params
        category = product_properties.category
        category_id = product_properties.category_id
        title = product_properties.title
        desc = product_properties.desc
        #brand info
        brand_info = ParseBrandInfo.from_json(raw_data=raw_data)
        brand = brand_info.brand
        brand_id = brand_info.brand_id
        brand_logo = brand_info.brand_logo
        #price info
        price_info = ParsePriceInfo.from_json(raw_data=raw_data)
        floor_price = price_info.floor_price
        prices = price_info.prices

        return cls(
            all_images=[],
            current_images=[],
            product_addictive_params=product_addictive_params,
            article=article,
            category=category,
            category_id=category_id,
            current_sizes=current_sizes,
            current_colors=current_colors,
            size_ids=size_ids,
            color_ids=color_ids,
            prices=prices,
            sku_ids=sku_ids,
            spu_id=spu_id,
            floor_price=floor_price,
            brand=brand,
            brand_logo=brand_logo,
            brand_id=brand_id,
            title=title,
            size_table=size_table,
            desc=desc
        )



if (__name__ == "__main__"):
    with open('../controlles_all.json', 'r') as f:
        dictData = json.load(f)

    a = PoizonProduct.from_json(json_data=dictData)
    print(f"sizeIDs = {a.size_ids}")
    print(f"colorIds = {a.color_ids}")
    print(f"skuIds = {a.sku_ids}")
    print(f"current_sizes = {a.current_sizes}")
    print(f"current_colors = {a.current_colors}")
    print(f"prices = {a.prices}\n")
    print(f"brand = {a.brand}")
    print(f"brand_logo = {a.brand_logo}")

    print(f"brand_id = {a.brand_id}")
    print(f"spu_id = {a.spu_id}")
    print(f"floor_price = {a.floor_price}")
    print(f"title = {a.title}")
    print(f"desc = {a.desc}")
    print(f"current_images = {a.current_images}")
    print(f"category = {a.category}")
    print(f"category_id = {a.category_id}")
    print(f"size_table = {a.size_table}")
    print(f"product_addictive_params = {a.product_addictive_params}")
    print(f"article = {a.article}")

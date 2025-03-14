import json
from typing import List, Dict
from base import JsonSerializable
from poizon_parse_helpers import ParseSizes, ParseColors, ParseProductIds, ParseProductProperties, ParseBrandInfo, ParsePriceInfo, ParseImages
from raw_data_handlers import PoizonProductRaw
from base import NON_STATED
# class Product:
#     id: int
#     title: str
#     desc: str
#     images: list
#     category: str

class PoizonProductPrice: #todo есть еще описание каждого вида цены но хз надо ли
    def __init__(self, recommended_prices, types_of_prices, floor_price, max_price):
        self.recommended_prices = recommended_prices
        self.types_of_prices = types_of_prices
        self.floor_price = floor_price
        self.max_price = max_price

    def get_recommended_prices(self):
        return self.recommended_prices

    def get_types_of_prices(self):
        return self.types_of_prices

    def get_floor_price(self):
        return self.floor_price

    def get_max_price(self):
        return self.max_price

class PoizonProductSize:
    def __init__(self, current_sizes, size_ids, size_table):
        self.current_sizes = current_sizes
        self.size_ids = size_ids
        self.size_table = size_table

    def get_current_sizes(self):
        return self.current_sizes

    def get_size_ids(self):
        return self.size_ids

    def get_size_table(self):
        return self.size_table




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
                 sizes: PoizonProductSize,

                 current_colors: List[str] | NON_STATED,
                 color_ids: List[int] | NON_STATED,

                 sku_ids: List[int] | NON_STATED,
                 spu_id: int,
                 article: str,

                 product_addictive_params: Dict[str, str] | NON_STATED,
                 category: str | NON_STATED,
                 category_id: int,
                 title: str,
                 desc: str | NON_STATED,

                 brand: str,
                 brand_id: str,
                 brand_logo: str,

                 prices: PoizonProductPrice | NON_STATED,

                 images_ids: List[str],
                 current_images: List[str],
                 general_logo_image: str,
                 ):
        self.general_logo_image = general_logo_image
        self.current_images = current_images
        self.images_ids = images_ids
        self.product_addictive_params = product_addictive_params
        self.article = article
        self.category= category
        self.category_id = category_id
        self.current_colors = current_colors
        # self.current_sizes = current_sizes
        # self.size_ids = size_ids
        # self.size_table = size_table
        self.sizes = sizes
        self.color_ids = color_ids
        self.sku_ids = sku_ids  # уникальный
        self.spu_id = spu_id  # общий
        self.brand = brand
        self.brand_logo = brand_logo
        self.prices = prices
        self.brand_id = brand_id
        self.title = title
        self.desc = desc

    # картинки соотносятся по цветам не по размерам
    @classmethod
    def from_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)
        #sizes
        size_info = ParseSizes.from_json(raw_data=raw_data)
        sizes = PoizonProductSize(current_sizes=size_info.current_sizes,
                                  size_ids=size_info.size_ids,
                                  size_table=size_info.size_table)
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
        prices = PoizonProductPrice(recommended_prices=price_info.recommended_prices,
                           types_of_prices=price_info.types_of_prices,
                           floor_price=price_info.floor_price, max_price=price_info.max_price)
        #imgs 3 positions
        images_info = ParseImages.from_json(raw_data=raw_data)
        images_ids = images_info.images_ids
        current_images = images_info.current_images
        general_logo_image = images_info.general_logo_image
        return cls(
            sizes=sizes,
            current_colors=current_colors,
            color_ids=color_ids,
            sku_ids=sku_ids,
            spu_id=spu_id,
            article=article,
            product_addictive_params=product_addictive_params,
            category=category,
            category_id=category_id,
            title=title,
            desc=desc,
            brand=brand,
            brand_id=brand_id,
            brand_logo=brand_logo,
            prices=prices,
            images_ids=images_ids,
            current_images=current_images,
            general_logo_image=general_logo_image
        )



if (__name__ == "__main__"):
    with open('../jacket.json', 'r') as f:
        dictData = json.load(f)

    a = PoizonProduct.from_json(json_data=dictData)
    print(f"colorIds = {a.color_ids}")
    print(f"skuIds = {a.sku_ids}")
    print(f'images_ids = {a.images_ids}')
    print(f"current_colors = {a.current_colors}")
    print(f"brand = {a.brand}")
    print(f"brand_logo = {a.brand_logo}")

    print(f"brand_id = {a.brand_id}")
    print(f"spu_id = {a.spu_id}")
    print(f"title = {a.title}")
    print(f"desc = {a.desc}")
    print(f"category = {a.category}")
    print(f"category_id = {a.category_id}")
    print(f"product_addictive_params = {a.product_addictive_params}")
    print(f"article = {a.article}")
    print(f'current_images = {a.current_images}')
    print(f"general_logo_image = {a.general_logo_image}")

    print("\n### PRICES ###")
    print(f"types_of_prices = {a.prices.types_of_prices}")
    print(f'recommended_prices = {a.prices.recommended_prices}')
    print(f'floor_price = {a.prices.floor_price}')
    print(f'max_price = {a.prices.max_price}')

    print(f'current_sizes = {a.sizes.current_sizes}')
    print(f'size_ids = {a.sizes.size_ids}')
    print(f'size_table = {a.sizes.size_table}')
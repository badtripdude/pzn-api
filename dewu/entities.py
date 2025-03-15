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

    class PoizonProductPrice:  # todo есть еще описание каждого вида цены но хз надо ли
        def __init__(self, recommended_prices, types_of_prices, floor_price, max_price):
            self.recommended_prices = recommended_prices
            self.types_of_prices = types_of_prices
            self.floor_price = floor_price
            self.max_price = max_price

    class PoizonProductSize:
        def __init__(self, current_sizes, size_table):
            self.current_sizes = current_sizes
            self.size_table = size_table

    class PoizonProductImages:
        def __init__(self, general_logo_image, current_images):
            self.general_logo_image = general_logo_image
            self.current_images = current_images

    class PoizonProductDescription:
        def __init__(self, product_addictive_params, category, title, desc):
            self.product_addictive_params = product_addictive_params
            self.category = category
            self.title = title
            self.desc = desc

    class PoizonProductIds:
        def __init__(self, color_ids, sku_ids, spu_id, article_number, category_id, brand_id, size_ids):
            self.color_ids = color_ids
            self.sku_ids = sku_ids
            self.spu_id = spu_id
            self.article_number = article_number
            self.category_id = category_id
            self.brand_id = brand_id
            self.size_ids = size_ids


    def __init__(self,
                 sizes: PoizonProductSize,
                 descriptions: PoizonProductDescription,
                 prices: PoizonProductPrice | NON_STATED,
                 images: PoizonProductImages | NON_STATED,
                 product_ids: PoizonProductIds,

                 current_colors: List[str] | NON_STATED,

                 brand: str,
                 brand_logo: str


                 ):
        self.images = images
        self.product_ids = product_ids
        self.descriptions = descriptions
        self.prices = prices
        self.current_colors = current_colors
        self.sizes = sizes
        self.brand = brand
        self.brand_logo = brand_logo

    # картинки соотносятся по цветам не по размерам
    @classmethod
    def from_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)
        #sizes
        size_info = ParseSizes.from_json(raw_data=raw_data)
        sizes = PoizonProduct.PoizonProductSize(current_sizes=size_info.current_sizes,
                                  size_table=size_info.size_table)
        #colors
        color_info = ParseColors.from_json(raw_data=raw_data)
        current_colors = color_info.current_colors
        #product ids
        product_ids_info = ParseProductIds.from_json(raw_data=raw_data)
        product_ids = PoizonProduct.PoizonProductIds(color_ids=product_ids_info.color_ids,
                                                   sku_ids=product_ids_info.sku_ids,
                                                   spu_id=product_ids_info.spu_id,
                                                   article_number=product_ids_info.article_number,
                                                   category_id=product_ids_info.category_id,
                                                   brand_id=product_ids_info.brand_id,
                                                   size_ids=product_ids_info.size_ids)
        #desc_info
        desc_info = ParseProductProperties.from_json(raw_data=raw_data)
        descriptions = PoizonProduct.PoizonProductDescription(product_addictive_params=desc_info.product_addictive_params,
                                                              category=desc_info.category,
                                                              title=desc_info.title,
                                                              desc=desc_info.desc)

        #brand info
        brand_info = ParseBrandInfo.from_json(raw_data=raw_data)
        brand = brand_info.brand
        brand_logo = brand_info.brand_logo
        #price info
        price_info = ParsePriceInfo.from_json(raw_data=raw_data)
        prices = PoizonProduct.PoizonProductPrice(recommended_prices=price_info.recommended_prices,
                           types_of_prices=price_info.types_of_prices,
                           floor_price=price_info.floor_price, max_price=price_info.max_price)
        #imgs 3 positions
        images_info = ParseImages.from_json(raw_data=raw_data)
        images = PoizonProduct.PoizonProductImages(general_logo_image=images_info.general_logo_image,
                                     current_images=images_info.current_images)
        return cls(
            sizes=sizes,
            product_ids=product_ids,
            descriptions=descriptions,
            current_colors=current_colors,
            brand=brand,
            brand_logo=brand_logo,
            prices=prices,
            images=images
        )



if (__name__ == "__main__"):
    with open('../jacket.json', 'r') as f:
        dictData = json.load(f)

    a = PoizonProduct.from_json(json_data=dictData)
    print(f"current_colors = {a.current_colors}")
    print(f"brand = {a.brand}")
    print(f"brand_logo = {a.brand_logo}")


    print("\n### PRICES ###")
    print(f"types_of_prices = {a.prices.types_of_prices}")
    print(f'recommended_prices = {a.prices.recommended_prices}')
    print(f'floor_price = {a.prices.floor_price}')
    print(f'max_price = {a.prices.max_price}')

    print(f'current_sizes = {a.sizes.current_sizes}')
    print(f'size_table = {a.sizes.size_table}')

    print(f'current_images = {a.images.current_images}')
    print(f'general_logo_image = {a.images.general_logo_image}')

    print(f'product_addictive_params = {a.descriptions.product_addictive_params}')
    print(f'category = {a.descriptions.category}')
    print(f'desc = {a.descriptions.desc}')
    print(f'title = {a.descriptions.title}')

    print(f'color_ids = {a.product_ids.color_ids}')
    print(f'sku_ids = {a.product_ids.sku_ids}')
    print(f'spu_id = {a.product_ids.spu_id}')
    print(f'article_number = {a.product_ids.article_number}')
    print(f'category_id = {a.product_ids.category_id}')
    print(f'brand_id = {a.product_ids.brand_id}')
    print(f'size_ids = {a.product_ids.size_ids}')

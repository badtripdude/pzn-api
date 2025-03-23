import dataclasses
from typing import List, Dict

from .base import JsonSerializable
from .base import NON_STATED
from .poizon_parse_helpers import ParseBrand, ParseSizeTable, ParseStock, ParseProductCore, Images
from .raw_data_handlers import PoizonProductRaw


# class Product:
#     id: int
#     title: str
#     desc: str
#     images: list
#     category: str


class ProductSearchCard(JsonSerializable):
    def __init__(self, title: str = None, spu_id: int = None,
                 logo_url: str = None, images: list[str] = None, article_number: str = None,
                 price: int = None, min_sale_price: int = None, max_sale_price: int = None,
                 spu_min_sale_price: int = None, sku_id: int = None, level1_category_id: int = None,
                 category_id: int = None, brand_id: int = None, brand_name: str = None,
                 brand_logo_url: str = None):
        self.level1_category_id = level1_category_id
        self.max_sale_price = max_sale_price
        self.brand_name = brand_name
        self.min_sale_price = min_sale_price
        self.sku_id = sku_id
        self.spu_min_sale_price = spu_min_sale_price
        self.brand_id = brand_id
        self.brand_logo_url = brand_logo_url
        self.category_id = category_id
        self.price = price
        self.article_number = article_number
        self.images = images
        self.spu_id = spu_id
        self.logo_url = logo_url
        self.title = title

    @classmethod
    def from_json(cls, json_data):
        return cls(
            # almost always passed
            title=json_data.get('title'),
            spu_id=json_data.get('spuId'),
            logo_url=json_data.get('logoUrl'),
            images=json_data.get('images'),
            article_number=json_data.get('articleNumber'),
            # :(
            price=json_data.get('price'),
            min_sale_price=json_data.get('minSalePrice'),
            max_sale_price=json_data.get('maxSalePrice'),
            sku_id=json_data.get('skuId'),
            level1_category_id=json_data.get('level1CategoryId'),
            category_id=json_data.get('categoryId'),
            brand_id=json_data.get('brandId'),
            brand_name=json_data.get('brandName'),
            brand_logo_url=json_data.get('brandLogoUrl'),
        )


class ProductSearchResult(JsonSerializable):
    def __init__(self,
                 total: int, page: int, last_id: str = None,
                 product_list: list[ProductSearchCard] = None,
                 ):
        self.product_list = product_list
        self.last_id = last_id
        self.page = page
        self.total = total

    @classmethod
    def from_json(cls, json_data):
        return cls(
            total=json_data['total'],
            page=json_data['page'],
            last_id=json_data.get('lastId', None),
            product_list=[ProductSearchCard.from_json(data) for data in json_data.get('productList', [])]
        )


class PoizonProduct(JsonSerializable):
    """
            class for parsing and keeping data from PoizonProductRaw
    """

    # # TODO: dataclasses оставить ~
    # @dataclasses.dataclass()
    # class PoizonProductPrice:  # todo есть еще описание(не всегда) каждого вида цены но хз надо ли
    #     recommended_prices: List[int]
    #     types_of_prices: Dict[int, Dict[int, int]] | NON_STATED
    #     floor_price: int | NON_STATED
    #     max_price: int
    #

    # #todo delivery duration
    # class PoizonProductDelivery:
    # # 3 -eu
    # # 2 - ch
    # # 95 - 95
    # # 2 - ch
    # # 0 - ch

    @dataclasses.dataclass
    class PoizonProductCore:
        additional_params: Dict[str, str]
        category: str
        category_id: int
        title: str
        description: str
        article_number: int
        spu_id: str

    @dataclasses.dataclass()
    class PoizonProductStock:
        recommended_prices: List[int]
        types_of_prices: Dict[int, Dict[int, int]] | NON_STATED
        types_of_prices_desc: str
        floor_price: int | NON_STATED
        max_price: int
        stock: int
        sku_ids: List[int]

    @dataclasses.dataclass()
    class PoizonProductSizeTable:
        size_table: List[int] | NON_STATED

    @dataclasses.dataclass()
    class PoizonProductImages:
        general_logo_url: str
        sku_to_image_url: Dict[int, List[str]]
        all_images: List[str]

    @dataclasses.dataclass()
    class PoizonProductBrand:
        brand_name: str
        brand_logo_url: str
        brand_id: int

    def __init__(self,

                 core: PoizonProductCore,
                 stock: PoizonProductStock,
                 size_table: PoizonProductSizeTable,
                 images: PoizonProductImages,
                 brand: PoizonProductBrand
                 ):
        self.core = core
        self.stock = stock
        self.size_table = size_table
        self.images = images
        self.brand = brand

    # картинки соотносятся по цветам не по размерам
    @classmethod
    def from_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)

        parsed_core = ParseProductCore.from_json(raw_data=raw_data)
        core = cls.PoizonProductCore(additional_params=parsed_core.additional_params,
                                     category=parsed_core.category,
                                     category_id=parsed_core.category_id,
                                     title=parsed_core.title,
                                     description=parsed_core.description,
                                     article_number=parsed_core.article_number,
                                     spu_id=parsed_core.spu_id)

        parsed_stock = ParseStock.from_json(raw_data=raw_data)
        stock = cls.PoizonProductStock(recommended_prices=parsed_stock.recommended_prices,
                                       types_of_prices=parsed_stock.types_of_prices,
                                       types_of_prices_desc=parsed_stock.types_of_prices_desc,
                                       floor_price=parsed_stock.floor_price,
                                       max_price=parsed_stock.max_price,
                                       stock=parsed_stock.stock,
                                       sku_ids=parsed_stock.sku_ids)

        parsed_size_table = ParseSizeTable.from_json(raw_data=raw_data)
        size_table = cls.PoizonProductSizeTable(size_table=parsed_size_table.size_table)

        parsed_images = Images.from_json(raw_data=raw_data)
        images = cls.PoizonProductImages(general_logo_url=parsed_images.general_logo_url,
                                         sku_to_image_url=parsed_images.sku_to_image_url,
                                         all_images=parsed_images.all_images)

        parsed_brand = ParseBrand.from_json(raw_data=raw_data)
        brand = cls.PoizonProductBrand(brand_name=parsed_brand.brand_name,
                                       brand_logo_url=parsed_brand.brand_logo_url,
                                       brand_id=parsed_brand.brand_id)

        return cls(
            core=core,
            stock=stock,
            size_table=size_table,
            images=images,
            brand=brand
        )

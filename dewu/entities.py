from typing import List, Dict
from base import JsonSerializable
from poizon_parse_helpers import ParseBrand, ParseSizeTable, ParseStock, ParseProductCore, PoizonProductRaw, Images
from raw_data_handlers import PoizonProductRaw
from base import NON_STATED
import dataclasses

# class Product:
#     id: int
#     title: str
#     desc: str
#     images: list
#     category: str



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
    # @dataclasses.dataclass()
    # class PoizonProductSize:
    #     current_sizes: Dict[int, str]
    #     size_table: Dict[str, str]
    #
    # @dataclasses.dataclass()
    # class PoizonProductImages:
    #     general_logo_image: str
    #     current_images: Dict[int, List[str]]
    #
    # @dataclasses.dataclass()
    # class PoizonProductDescription:
    #     product_addictive_params: Dict[str, str]
    #     category: str
    #     title: str
    #     desc: str | NON_STATED
    #
    # @dataclasses.dataclass()
    # class PoizonProductIdentifiers:
    #     color_ids: Dict[int, int]
    #     sku_ids: List[int]
    #     spu_id: int
    #     article_number: int
    #     category_id: int
    #     brand_id: int
    #     size_ids: Dict[int, str]
    #
    # @dataclasses.dataclass()
    # class PoizonProductColors:
    #     sku_to_color: Dict[int, str]
    #
    # @dataclasses.dataclass()
    # class PoizonProductBrandInfo:
    #     brand_name: str
    #     brand_logo: str
    #
    # #todo delivery duration
    # @dataclasses.dataclass()
    # class PoizonProductDelivery:
    #     ...
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
                                         sku_to_image_url=parsed_images.sku_to_image_url)

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
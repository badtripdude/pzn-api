from dewu.utils.parse_helpers import ProductBrand, ProductSizeTable, ProductStock, ProductCore, ProductImages
from .base import JsonSerializable
from .raw_data_handlers import ProductRaw


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
    """
    class represents search results data
    """
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

    def __init__(self,
                 core: ProductCore,
                 stock: ProductStock,
                 size_table: ProductSizeTable,
                 images: ProductImages,
                 brand: ProductBrand
                 ):
        self.core = core
        self.stock = stock
        self.size_table = size_table
        self.images = images
        self.brand = brand

    @classmethod
    def from_json(cls, json_data):
        raw_data = ProductRaw.from_json(json_data=json_data)

        return cls(
            core=ProductCore.from_json(raw_data=raw_data),
            stock=ProductStock.from_json(raw_data=raw_data),
            size_table=ProductSizeTable.from_json(raw_data=raw_data),
            images=ProductImages.from_json(raw_data=raw_data),
            brand=ProductBrand.from_json(raw_data=raw_data)
        )

from typing import List, Dict

from dewu.base import JsonSerializable, NON_STATED
from dewu.raw_data_handlers import ProductRaw


class ProductCore(JsonSerializable):
    """
    contains product core info

Attributes:
    category: name of the product category
    category_id: identifier of category
    title: title of product
    description: description of product
    article_number: article number of product
    spu_id: Standard Product Unit identifier
    """

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
    def from_json(cls, raw_data: ProductRaw):
        product_addictive_params = {}
        for i in raw_data.basicParam['basicList']:
            product_addictive_params[i["key"]] = i["value"]

        return cls(additional_params=product_addictive_params,
                   category=raw_data.detail["categoryName"],
                   category_id=raw_data.detail["categoryId"],
                   title=raw_data.detail["title"],
                   description=raw_data.detail["desc"] if raw_data.detail["desc"] else NON_STATED,
                   article_number=raw_data.detail['articleNumber'],
                   spu_id=raw_data.detail["spuId"])


class ProductStock(JsonSerializable):
    """
    keeps information about stock parameters of product.

Attributes:
    recommended_prices: relation between product sku_id and price that is recommended for it by Poizon
    types_of_prices: dict{sku_id: {type of trade: price}} relation between product sku_id and dict of its prices (that depends on trade type)
    types_of_prices_desc:  str description of types_of_prices param (optional)
    min_price: lowest price of all the products in the product card
    max_price: highest price of all the products in the product card
    stock: dict{sku_id: stock quantity}, relation between product sku_id and stock quantity
    sku_ids: list of all Stock Keeping Unit identifiers (every single product identifiers in product card)
    sku_to_variant: dict{sku_id: dict{variant_name: variant_value}} relation between sku_id and its price that depends on variant_value
    """

    def __init__(self,
                 recommended_prices: Dict[int, int] | NON_STATED,
                 types_of_prices: Dict[int, Dict[int, int]] | NON_STATED,
                 types_of_prices_desc: str,
                 min_price: int | NON_STATED,
                 max_price: int | NON_STATED,
                 stock: Dict[int, int] | NON_STATED,
                 sku_ids: List[int] | NON_STATED,
                 sku_to_variant: Dict[int, Dict[str, str]]):
        self.recommended_prices = recommended_prices
        self.types_of_prices = types_of_prices
        self.types_of_prices_desc = types_of_prices_desc
        self.min_price = min_price
        self.max_price = max_price
        self.stock = stock
        self.sku_ids = sku_ids
        self.sku_to_variant = sku_to_variant

    @classmethod
    def from_json(cls, raw_data: ProductRaw):
        recommended_prices = {}
        for item in raw_data.skus: recommended_prices[item['skuId']] = item['authPrice']

        if 'price' in raw_data.skus[0]:
            types_of_prices = {}
            for item in raw_data.skus:
                sku_id = item['skuId']
                prices = {}
                for price in item['price']['prices']:
                    prices[price['tradeType']] = price['price']
                    types_of_prices[sku_id] = prices
        else:
            types_of_prices = NON_STATED

        if 'item' in raw_data.price:
            min_price = raw_data.price['item']['floorPrice']
            max_price = raw_data.price['item']['maxPrice']
        else:
            min_price = NON_STATED
            max_price = NON_STATED

        stock = {}
        if 'price' in raw_data.skus[0]:
            for item in raw_data.skus:
                stock[item['skuId']] = item['price']['quantity']
        else:
            stock = NON_STATED

        sku_ids = []
        for i in raw_data.skus:
            sku_ids.append(i['skuId'])

        if 'price' in raw_data.skus[0]:
            sku_to_variant = {}
            for item in raw_data.skus:
                dict_of_props = {}
                for prop in item['properties']:
                    dict_of_props[prop['saleProperty']['name']] = prop['saleProperty']['value']
                sku_to_variant[item['skuId']] = dict_of_props
        else:
            sku_to_variant = NON_STATED

        return cls(recommended_prices=recommended_prices,
                   types_of_prices=types_of_prices,
                   types_of_prices_desc=NON_STATED,
                   min_price=min_price,
                   max_price=max_price,
                   stock=stock,
                   sku_ids=sku_ids,
                   sku_to_variant=sku_to_variant
                   )


class ProductSizeTable(JsonSerializable):
    """
    keeps only the size table of a product

Attributes:
    size_table: list of different size tables, for ex. eu, uk, us size tables etc.
    """

    def __init__(self, size_table: List[int] | NON_STATED):
        self.size_table = size_table

    @classmethod
    def from_json(cls, raw_data: ProductRaw):
        size_table = {}

        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]

        return cls(size_table=size_table)


class ProductImages(JsonSerializable):
    """
    keeps information about product images

Attributes:
    general_logo_url: url of the general image of the product card
    sku_to_image_url: dict, relation between sku_id and pictures of product with that sku_id
    all_images: all images of the product card not bounded to anything
    """

    def __init__(self,
                 general_logo_url: str,
                 sku_to_image_url: Dict,
                 all_images: List[str]):
        self.general_logo_url = general_logo_url
        self.sku_to_image_url = sku_to_image_url
        self.all_images = all_images

    @classmethod
    def from_json(cls, raw_data: ProductRaw):
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
    """
    keeps information about the brand of the product

Attributes:
    brand_name: the string name of the brand
    brand_logo_url: url of the brand logo
    brand_id: id of the brand
    """

    def __init__(self,
                 brand_name: str,
                 brand_logo_url: str,
                 brand_id: int):
        self.brand_name = brand_name
        self.brand_logo_url = brand_logo_url
        self.brand_id = brand_id

    @classmethod
    def from_json(cls, raw_data: ProductRaw):
        if raw_data.brandRootInfo:
            return cls(brand_name=raw_data.brandRootInfo["brandItemList"][0]["brandName"] if raw_data.brandRootInfo else NON_STATED,
                    brand_logo_url=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"]  if raw_data.brandRootInfo else NON_STATED,
                    brand_id=raw_data.detail["brandId"]  if raw_data.brandRootInfo else NON_STATED)
        return cls(brand_name=NON_STATED, brand_logo_url=NON_STATED, brand_id=NON_STATED)